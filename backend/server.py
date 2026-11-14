#!/usr/bin/env python3
"""Threaded HTTP API Server for AI Trading Intelligence.

Provides the clean server-side API wrapping:
- `integrations/python/trading_intel` (V1-V3 calculation & Quick Signal engine)
- `knowledge/` & `markets/` Markdown loaders
- Authentication, sessions, password reset, user profile, settings
- Asynchronous/tracked analysis job execution with real stage updates
- Immutable analysis history, watchlists, news & market-data adapter status

Zero third-party Python dependencies required. Binds to 0.0.0.0:8000 by default.
"""

from __future__ import annotations

import base64
import http.cookies
import json
import os
import secrets
import sys
import threading
import traceback
import urllib.parse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from backend.analysis_service import AnalysisOrchestrator, SAMPLE_CHART_PRESETS  # noqa: E402
from backend.database import Database  # noqa: E402
from backend.knowledge_service import KnowledgeLoader  # noqa: E402
from backend.providers_service import (  # noqa: E402
    MarketDataAdapter,
    NewsResearchAdapter,
    VisionProviderAdapter,
)
from backend.screenshot_service import ImageValidationError, ScreenshotService  # noqa: E402


SESSION_COOKIE = "ti_session"


def _make_sample_png_base64() -> str:
    """Create a valid minimal 480x280 dark navy PNG image for explicit sample demos."""
    import struct
    import zlib

    width, height = 480, 280
    # RGB background #111C2D (17, 28, 45) with a simple horizontal support/resistance line
    rows = []
    for y in range(height):
        row = bytearray([0])  # filter type 0
        for x in range(width):
            if y == 90 and 40 <= x <= 440:
                # Resistance line (#F16F83)
                row.extend((241, 111, 131))
            elif y == 195 and 40 <= x <= 440:
                # Support line (#16B995)
                row.extend((22, 185, 149))
            elif (x % 22 in (8, 9, 10, 11, 12)) and (110 + (x % 35) <= y <= 175 + (x % 25)):
                # Stylized candle body (#667AFF or #16B995)
                if (x // 22) % 2 == 0:
                    row.extend((22, 185, 149))
                else:
                    row.extend((241, 111, 131))
            else:
                row.extend((17, 28, 45))
        rows.append(bytes(row))
    raw_data = b"".join(rows)

    def chunk(tag: bytes, payload: bytes) -> bytes:
        return (
            struct.pack(">I", len(payload))
            + tag
            + payload
            + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF)
        )

    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw_data, 6))
        + chunk(b"IEND", b"")
    )
    return "data:image/png;base64," + base64.b64encode(png).decode("ascii")


SAMPLE_PNG_DATA_URL = _make_sample_png_base64()


class JobManager:
    """Tracks real in-flight and completed analysis jobs in memory + DB."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._jobs: Dict[str, Dict[str, Any]] = {}

    def create_job(self, job_id: str, user_id: str) -> Dict[str, Any]:
        job = {
            "job_id": job_id,
            "user_id": user_id,
            "status": "running",
            "current_stage_index": 0,
            "current_stage": "read_screenshot",
            "stages": [],
            "analysis_id": None,
            "error": None,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        with self._lock:
            self._jobs[job_id] = job
        return dict(job)

    def update_stage(
        self, job_id: str, idx: int, stage_id: str, stages: List[Dict[str, Any]]
    ) -> None:
        with self._lock:
            if job_id in self._jobs:
                self._jobs[job_id]["current_stage_index"] = idx
                self._jobs[job_id]["current_stage"] = stage_id
                self._jobs[job_id]["stages"] = [dict(s) for s in stages]

    def complete_job(
        self, job_id: str, analysis_id: str, result: Dict[str, Any]
    ) -> None:
        with self._lock:
            if job_id in self._jobs:
                self._jobs[job_id]["status"] = "completed"
                self._jobs[job_id]["analysis_id"] = analysis_id
                self._jobs[job_id]["stages"] = result.get("stages", [])
                self._jobs[job_id]["result"] = result

    def fail_job(self, job_id: str, error_msg: str) -> None:
        with self._lock:
            if job_id in self._jobs:
                self._jobs[job_id]["status"] = "failed"
                self._jobs[job_id]["error"] = error_msg

    def get_job(self, job_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            j = self._jobs.get(job_id)
            if not j or j["user_id"] != user_id:
                return None
            return dict(j)


class ApplicationContainer:
    def __init__(self, db_path: Optional[str] = None, upload_dir: Optional[str] = None) -> None:
        self.db = Database(db_path=db_path)
        self.screenshots = ScreenshotService(upload_dir=upload_dir)
        self.knowledge = KnowledgeLoader()
        self.vision = VisionProviderAdapter()
        self.market_data = MarketDataAdapter()
        self.news = NewsResearchAdapter()
        self.orchestrator = AnalysisOrchestrator(
            knowledge_loader=self.knowledge,
            vision_adapter=self.vision,
            market_adapter=self.market_data,
            news_adapter=self.news,
        )
        self.jobs = JobManager()


def create_handler(app: ApplicationContainer):
    class APIHandler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, fmt: str, *args: Any) -> None:
            if os.environ.get("TI_QUIET_LOGS") == "1":
                return
            sys.stderr.write(f"[api] {self.command} {self.path} - {fmt % args}\n")

        # --------------------------------------------------------------
        # HTTP helpers
        # --------------------------------------------------------------
        def _send_json(
            self,
            status_code: int,
            payload: Dict[str, Any],
            extra_headers: Optional[List[Tuple[str, str]]] = None,
        ) -> None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self._send_cors_headers()
            for k, v in extra_headers or []:
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(body)

        def _send_binary(
            self, status_code: int, data: bytes, content_type: str
        ) -> None:
            self.send_response(status_code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "private, max-age=3600")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(data)

        def _send_cors_headers(self) -> None:
            origin = self.headers.get("Origin")
            if origin:
                self.send_header("Access-Control-Allow-Origin", origin)
                self.send_header("Access-Control-Allow-Credentials", "true")
            else:
                self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header(
                "Access-Control-Allow-Headers",
                "Content-Type, Authorization, X-Requested-With",
            )
            self.send_header(
                "Access-Control-Allow-Methods",
                "GET, POST, PUT, PATCH, DELETE, OPTIONS",
            )

        def _read_json_body(self, max_bytes: int = 18 * 1024 * 1024) -> Dict[str, Any]:
            length_str = self.headers.get("Content-Length", "0")
            try:
                length = int(length_str)
            except ValueError:
                length = 0
            if length <= 0:
                return {}
            if length > max_bytes:
                raise ImageValidationError(
                    f"Request payload ({length // (1024 * 1024)} MB) exceeds maximum allowed upload limit."
                )
            raw = self.rfile.read(length)
            try:
                data = json.loads(raw.decode("utf-8"))
                return data if isinstance(data, dict) else {}
            except json.JSONDecodeError as exc:
                raise ValueError("Invalid JSON request body.") from exc

        def _extract_token(self) -> Optional[str]:
            auth_hdr = self.headers.get("Authorization", "")
            if auth_hdr.lower().startswith("bearer "):
                return auth_hdr[7:].strip()
            cookie_hdr = self.headers.get("Cookie", "")
            if cookie_hdr:
                jar = http.cookies.SimpleCookie()
                try:
                    jar.load(cookie_hdr)
                    if SESSION_COOKIE in jar:
                        return jar[SESSION_COOKIE].value
                except http.cookies.CookieError:
                    pass
            # Also check query param `token` for authenticated image tags
            parsed = urllib.parse.urlparse(self.path)
            qs = urllib.parse.parse_qs(parsed.query)
            if "token" in qs and qs["token"]:
                return qs["token"][0]
            return None

        def _current_user(self) -> Optional[Dict[str, Any]]:
            token = self._extract_token()
            return app.db.get_user_by_session(token)

        def _require_user(self) -> Optional[Dict[str, Any]]:
            user = self._current_user()
            if not user:
                self._send_json(
                    401,
                    {"ok": False, "error": "Authentication required. Please sign in to continue."},
                )
                return None
            return user

        @staticmethod
        def _session_cookie_header(token: str, clear: bool = False) -> Tuple[str, str]:
            if clear:
                return (
                    "Set-Cookie",
                    f"{SESSION_COOKIE}=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax",
                )
            max_age = 14 * 24 * 3600
            return (
                "Set-Cookie",
                f"{SESSION_COOKIE}={token}; Path=/; Max-Age={max_age}; HttpOnly; SameSite=Lax",
            )

        # --------------------------------------------------------------
        # Routing
        # --------------------------------------------------------------
        def do_OPTIONS(self) -> None:
            self.send_response(204)
            self._send_cors_headers()
            self.send_header("Content-Length", "0")
            self.end_headers()

        def do_GET(self) -> None:
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path.rstrip("/") or "/"
            qs = urllib.parse.parse_qs(parsed.query)

            try:
                if path == "/api/health":
                    self._send_json(
                        200,
                        {
                            "ok": True,
                            "service": "ai-trading-intelligence-api",
                            "version": "1.1.0",
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "capabilities": {
                                "vision": app.vision.status(),
                                "market_data": app.market_data.status(),
                                "news": app.news.status(),
                                "max_upload_mb": app.screenshots.max_upload_mb,
                                "supported_formats": ["PNG", "JPG", "JPEG", "WEBP"],
                            },
                        },
                    )
                    return

                if path == "/api/auth/me":
                    user = self._current_user()
                    if not user:
                        self._send_json(200, {"ok": True, "authenticated": False, "user": None})
                        return
                    settings = app.db.get_settings(user["id"])
                    self._send_json(
                        200,
                        {
                            "ok": True,
                            "authenticated": True,
                            "user": user,
                            "settings": settings,
                        },
                    )
                    return

                if path == "/api/presets":
                    presets = [
                        {
                            "id": pid,
                            "label": p["label"],
                            "instrument": p["instrument"],
                            "exchange": p["exchange"],
                            "market": p["market"],
                            "timeframe": p["timeframe"],
                            "is_fictional_demo": True,
                        }
                        for pid, p in SAMPLE_CHART_PRESETS.items()
                    ]
                    self._send_json(200, {"ok": True, "presets": presets, "sample_image": SAMPLE_PNG_DATA_URL})
                    return

                if path == "/api/markets":
                    markets = app.knowledge.get_markets_overview()
                    mkt_status = app.market_data.status()
                    quotes: Dict[str, Any] = {}
                    sym_query = (qs.get("symbol") or [""])[0].strip().upper()
                    if sym_query and mkt_status["configured"]:
                        quotes[sym_query] = app.market_data.fetch_quote_if_configured(sym_query)
                    self._send_json(
                        200,
                        {
                            "ok": True,
                            "provider_status": mkt_status,
                            "markets": markets,
                            "quotes": quotes,
                        },
                    )
                    return

                if path == "/api/news":
                    q = (qs.get("q") or [""])[0]
                    market = (qs.get("market") or ["all"])[0]
                    instrument = (qs.get("instrument") or [""])[0]
                    res = app.news.fetch_news(query=q, market=market, instrument=instrument)
                    self._send_json(200, {"ok": True, **res})
                    return

                if path == "/api/education":
                    domain = (qs.get("domain") or [""])[0]
                    slug = (qs.get("slug") or [""])[0]
                    if domain:
                        article = app.knowledge.get_article(domain, slug)
                        if not article:
                            self._send_json(404, {"ok": False, "error": "Knowledge module not found."})
                            return
                        self._send_json(200, {"ok": True, "article": article})
                        return
                    self._send_json(200, {"ok": True, "catalog": app.knowledge.list_catalog()})
                    return

                if path == "/api/analyses":
                    user = self._require_user()
                    if not user:
                        return
                    limit = min(100, int((qs.get("limit") or ["50"])[0]))
                    instrument = (qs.get("instrument") or [""])[0].strip() or None
                    items = app.db.list_analyses(user["id"], limit=limit, instrument=instrument)
                    self._send_json(200, {"ok": True, "analyses": items})
                    return

                if path.startswith("/api/analyses/") and path.endswith("/image"):
                    user = self._require_user()
                    if not user:
                        return
                    parts = path.split("/")
                    analysis_id = parts[3]
                    rec = app.db.get_analysis(user["id"], analysis_id)
                    if not rec or not rec.get("screenshot_ref"):
                        self._send_json(404, {"ok": False, "error": "Screenshot not found."})
                        return
                    img_tuple = app.screenshots.read_image_bytes(rec["screenshot_ref"])
                    if not img_tuple:
                        self._send_json(404, {"ok": False, "error": "Screenshot binary missing."})
                        return
                    self._send_binary(200, img_tuple[0], img_tuple[1])
                    return

                if path.startswith("/api/analyses/"):
                    user = self._require_user()
                    if not user:
                        return
                    analysis_id = path.split("/")[3]
                    rec = app.db.get_analysis(user["id"], analysis_id)
                    if not rec:
                        self._send_json(404, {"ok": False, "error": "Analysis report not found."})
                        return
                    self._send_json(200, {"ok": True, "analysis": rec})
                    return

                if path.startswith("/api/jobs/"):
                    user = self._require_user()
                    if not user:
                        return
                    job_id = path.split("/")[3]
                    job = app.jobs.get_job(job_id, user["id"])
                    if not job:
                        self._send_json(404, {"ok": False, "error": "Analysis job not found."})
                        return
                    self._send_json(200, {"ok": True, "job": job})
                    return

                if path == "/api/watchlist":
                    user = self._require_user()
                    if not user:
                        return
                    items = app.db.list_watchlist(user["id"])
                    mkt_status = app.market_data.status()
                    # Attach live quote ONLY when authorized market data provider is configured
                    if mkt_status["configured"]:
                        for it in items:
                            q_res = app.market_data.fetch_quote_if_configured(it["symbol"])
                            if q_res.get("available"):
                                it["live_quote"] = q_res
                    self._send_json(
                        200,
                        {
                            "ok": True,
                            "watchlist": items,
                            "market_data_status": mkt_status,
                        },
                    )
                    return

                if path == "/api/settings":
                    user = self._require_user()
                    if not user:
                        return
                    self._send_json(200, {"ok": True, "settings": app.db.get_settings(user["id"])})
                    return

                if path == "/api/admin/diagnostics":
                    user = self._require_user()
                    if not user:
                        return
                    diag = app.db.get_system_diagnostics(user)
                    diag["capabilities"] = {
                        "vision": app.vision.status(),
                        "market_data": app.market_data.status(),
                        "news": app.news.status(),
                    }
                    self._send_json(200, {"ok": True, "diagnostics": diag})
                    return

                self._send_json(404, {"ok": False, "error": f"Unknown endpoint: {path}"})
            except Exception as exc:
                traceback.print_exc()
                self._send_json(500, {"ok": False, "error": str(exc)})

        def do_POST(self) -> None:
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path.rstrip("/") or "/"

            try:
                if path == "/api/auth/signup":
                    body = self._read_json_body()
                    user = app.db.create_user(
                        email=str(body.get("email") or ""),
                        password=str(body.get("password") or ""),
                        name=str(body.get("name") or ""),
                    )
                    token = app.db.create_session(
                        user["id"], user_agent=self.headers.get("User-Agent", "")
                    )
                    settings = app.db.get_settings(user["id"])
                    self._send_json(
                        201,
                        {
                            "ok": True,
                            "user": user,
                            "token": token,
                            "settings": settings,
                        },
                        extra_headers=[self._session_cookie_header(token)],
                    )
                    return

                if path == "/api/auth/signin":
                    body = self._read_json_body()
                    user = app.db.authenticate_user(
                        email=str(body.get("email") or ""),
                        password=str(body.get("password") or ""),
                    )
                    if not user:
                        self._send_json(
                            401,
                            {"ok": False, "error": "Invalid email or password."},
                        )
                        return
                    token = app.db.create_session(
                        user["id"], user_agent=self.headers.get("User-Agent", "")
                    )
                    settings = app.db.get_settings(user["id"])
                    self._send_json(
                        200,
                        {
                            "ok": True,
                            "user": user,
                            "token": token,
                            "settings": settings,
                        },
                        extra_headers=[self._session_cookie_header(token)],
                    )
                    return

                if path == "/api/auth/signout":
                    token = self._extract_token()
                    app.db.delete_session(token)
                    self._send_json(
                        200,
                        {"ok": True, "message": "Signed out."},
                        extra_headers=[self._session_cookie_header("", clear=True)],
                    )
                    return

                if path == "/api/auth/reset-request":
                    body = self._read_json_body()
                    email = str(body.get("email") or "").strip().lower()
                    if not email or "@" not in email:
                        self._send_json(400, {"ok": False, "error": "Please enter a valid email address."})
                        return
                    code = app.db.create_password_reset_token(email)
                    # Since no SMTP server is configured in local/offline sandbox, return a clear
                    # verification code banner in local mode when account exists, while documenting SMTP in .env.example
                    resp_payload: Dict[str, Any] = {
                        "ok": True,
                        "message": "If an account exists for this email, a 6-digit password reset code has been generated (valid for 30 minutes).",
                    }
                    if code and not os.environ.get("SMTP_HOST"):
                        resp_payload["local_verification_code"] = code
                        resp_payload["delivery_mode"] = "LOCAL_SANDBOX_CODE (SMTP_HOST not configured)"
                    self._send_json(200, resp_payload)
                    return

                if path == "/api/auth/reset-confirm":
                    body = self._read_json_body()
                    ok = app.db.reset_password_with_token(
                        email=str(body.get("email") or ""),
                        reset_code=str(body.get("code") or ""),
                        new_password=str(body.get("new_password") or ""),
                    )
                    if not ok:
                        self._send_json(
                            400,
                            {"ok": False, "error": "Invalid or expired reset code."},
                        )
                        return
                    self._send_json(200, {"ok": True, "message": "Password has been reset. You can now sign in."})
                    return

                if path == "/api/analyze":
                    user = self._require_user()
                    if not user:
                        return
                    body = self._read_json_body()
                    sample_preset_id = body.get("sample_preset_id")
                    img_b64 = str(body.get("image_base64") or "")
                    filename = str(body.get("filename") or "chart.png")
                    if not img_b64 and sample_preset_id in SAMPLE_CHART_PRESETS:
                        img_b64 = SAMPLE_PNG_DATA_URL
                        filename = f"{sample_preset_id}.png"

                    screenshot = app.screenshots.decode_and_save(img_b64, filename=filename)
                    preferences = body.get("preferences") if isinstance(body.get("preferences"), dict) else {}
                    transcription = body.get("transcription") if isinstance(body.get("transcription"), dict) else {}
                    async_mode = bool(body.get("async_job", False))

                    job_id = f"job_{secrets.token_hex(8)}"
                    app.jobs.create_job(job_id, user["id"])

                    def run_pipeline() -> Dict[str, Any]:
                        result = app.orchestrator.execute_analysis(
                            screenshot=screenshot,
                            preferences=preferences,
                            transcription=transcription,
                            sample_preset_id=sample_preset_id,
                            progress_callback=lambda idx, sid, stg: app.jobs.update_stage(job_id, idx, sid, stg),
                        )
                        saved = app.db.save_analysis(user["id"], result)
                        app.jobs.complete_job(job_id, saved["id"], saved)
                        return saved

                    if async_mode:
                        t = threading.Thread(target=self._safe_bg_job, args=(job_id, run_pipeline), daemon=True)
                        t.start()
                        self._send_json(
                            202,
                            {
                                "ok": True,
                                "job_id": job_id,
                                "status": "running",
                            },
                        )
                        return

                    saved = run_pipeline()
                    self._send_json(
                        201,
                        {
                            "ok": True,
                            "job_id": job_id,
                            "analysis": saved,
                        },
                    )
                    return

                if path == "/api/watchlist":
                    user = self._require_user()
                    if not user:
                        return
                    body = self._read_json_body()
                    item = app.db.add_watchlist_item(
                        user_id=user["id"],
                        symbol=str(body.get("symbol") or ""),
                        exchange=str(body.get("exchange") or ""),
                        market=str(body.get("market") or "auto"),
                        notes=str(body.get("notes") or ""),
                    )
                    self._send_json(201, {"ok": True, "item": item})
                    return

                self._send_json(404, {"ok": False, "error": f"Unknown endpoint: {path}"})
            except ImageValidationError as exc:
                self._send_json(400, {"ok": False, "error": str(exc), "code": "IMAGE_VALIDATION_ERROR"})
            except ValueError as exc:
                self._send_json(400, {"ok": False, "error": str(exc), "code": "VALIDATION_ERROR"})
            except Exception as exc:
                traceback.print_exc()
                self._send_json(500, {"ok": False, "error": f"Server error: {exc}"})

        def do_PUT(self) -> None:
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path.rstrip("/") or "/"
            try:
                if path == "/api/settings":
                    user = self._require_user()
                    if not user:
                        return
                    body = self._read_json_body()
                    updated = app.db.update_settings(user["id"], body)
                    self._send_json(200, {"ok": True, "settings": updated})
                    return

                if path == "/api/auth/profile":
                    user = self._require_user()
                    if not user:
                        return
                    body = self._read_json_body()
                    if body.get("new_password"):
                        app.db.update_password(
                            user["id"],
                            current_password=str(body.get("current_password") or ""),
                            new_password=str(body.get("new_password") or ""),
                        )
                    updated_user = app.db.update_profile(
                        user["id"],
                        name=body.get("name"),
                        bio=body.get("bio"),
                    )
                    self._send_json(200, {"ok": True, "user": updated_user})
                    return

                self._send_json(404, {"ok": False, "error": f"Unknown endpoint: {path}"})
            except ValueError as exc:
                self._send_json(400, {"ok": False, "error": str(exc)})
            except Exception as exc:
                traceback.print_exc()
                self._send_json(500, {"ok": False, "error": str(exc)})

        def do_DELETE(self) -> None:
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path.rstrip("/") or "/"
            try:
                if path == "/api/analyses":
                    user = self._require_user()
                    if not user:
                        return
                    deleted_count = app.db.clear_all_analyses(user["id"])
                    self._send_json(200, {"ok": True, "deleted": deleted_count})
                    return

                if path.startswith("/api/analyses/"):
                    user = self._require_user()
                    if not user:
                        return
                    analysis_id = path.split("/")[3]
                    img_ref = app.db.delete_analysis(user["id"], analysis_id)
                    if img_ref is None:
                        self._send_json(404, {"ok": False, "error": "Analysis not found."})
                        return
                    if img_ref:
                        app.screenshots.delete_image(img_ref)
                    self._send_json(200, {"ok": True, "deleted_id": analysis_id})
                    return

                if path.startswith("/api/watchlist/"):
                    user = self._require_user()
                    if not user:
                        return
                    item_id = path.split("/")[3]
                    ok = app.db.remove_watchlist_item(user["id"], item_id)
                    if not ok:
                        self._send_json(404, {"ok": False, "error": "Watchlist item not found."})
                        return
                    self._send_json(200, {"ok": True, "deleted_id": item_id})
                    return

                self._send_json(404, {"ok": False, "error": f"Unknown endpoint: {path}"})
            except Exception as exc:
                traceback.print_exc()
                self._send_json(500, {"ok": False, "error": str(exc)})

        @staticmethod
        def _safe_bg_job(job_id: str, fn: Any) -> None:
            try:
                fn()
            except Exception as exc:
                app.jobs.fail_job(job_id, str(exc))

    return APIHandler


def run_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    app = ApplicationContainer()
    handler = create_handler(app)
    server = ThreadingHTTPServer((host, port), handler)
    print(f"AI Trading Intelligence API listening on http://{host}:{port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    bind_host = os.environ.get("TI_API_HOST", "0.0.0.0")
    bind_port = int(os.environ.get("TI_API_PORT", "8000"))
    run_server(host=bind_host, port=bind_port)
