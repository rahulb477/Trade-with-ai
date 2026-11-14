"""Comprehensive backend unit + HTTP end-to-end tests for AI Trading Intelligence Web App."""

from __future__ import annotations

import base64
import json
import os
import struct
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
import zlib
from http.server import ThreadingHTTPServer

from backend.database import Database
from backend.knowledge_service import KnowledgeLoader
from backend.providers_service import (
    MarketDataAdapter,
    NewsResearchAdapter,
    VisionProviderAdapter,
)
from backend.screenshot_service import (
    ImageValidationError,
    ScreenshotService,
    detect_image_format_and_dimensions,
    infer_metadata_from_filename,
)
from backend.server import ApplicationContainer, SAMPLE_PNG_DATA_URL, create_handler


def make_test_jpeg_bytes(width: int = 320, height: int = 200) -> bytes:
    # Minimal valid SOI + APP0 JFIF + SOF0 + EOI JPEG binary header for dimension parsing
    app0 = b"\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
    sof0_payload = struct.pack(">BHHB", 8, height, width, 3) + b"\x01\x11\x00\x02\x11\x00\x03\x11\x00"
    sof0_seg = b"\xff\xc0" + struct.pack(">H", len(sof0_payload) + 2) + sof0_payload
    return b"\xff\xd8" + app0 + sof0_seg + b"\xff\xd9"


def make_test_webp_bytes(width: int = 400, height: int = 300) -> bytes:
    w_minus_1 = (width - 1).to_bytes(3, "little")
    h_minus_1 = (height - 1).to_bytes(3, "little")
    vp8x = b"VP8X" + struct.pack("<I", 10) + b"\x00\x00\x00\x00" + w_minus_1 + h_minus_1
    riff_size = 4 + len(vp8x)
    return b"RIFF" + struct.pack("<I", riff_size) + b"WEBP" + vp8x


class TestScreenshotValidation(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.service = ScreenshotService(upload_dir=self.tmpdir.name, max_upload_mb=1)

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def test_valid_png_upload_and_dimensions(self) -> None:
        shot = self.service.decode_and_save(SAMPLE_PNG_DATA_URL, "BTCUSD_5m_chart.png")
        self.assertEqual(shot.detected_format, "PNG")
        self.assertEqual(shot.width, 480)
        self.assertEqual(shot.height, 280)
        self.assertEqual(shot.inferred_symbol, "BTCUSD")
        self.assertEqual(shot.inferred_timeframe, "5m")
        self.assertTrue(os.path.isfile(shot.saved_path))

    def test_valid_jpeg_and_webp_headers(self) -> None:
        jpg = make_test_jpeg_bytes(640, 360)
        fmt, mime, w, h = detect_image_format_and_dimensions(jpg)
        self.assertEqual((fmt, mime, w, h), ("jpeg", "image/jpeg", 640, 360))

        webp = make_test_webp_bytes(500, 320)
        fmt2, mime2, w2, h2 = detect_image_format_and_dimensions(webp)
        self.assertEqual((fmt2, mime2, w2, h2), ("webp", "image/webp", 500, 320))

    def test_heic_rejected_with_clear_error(self) -> None:
        fake_heic = b"\x00\x00\x00\x18ftypheic\x00\x00\x00\x00mif1heic" + b"\x00" * 32
        b64 = base64.b64encode(fake_heic).decode("ascii")
        with self.assertRaises(ImageValidationError) as ctx:
            self.service.decode_and_save(b64, "iphone_photo.heic")
        self.assertIn("HEIC", str(ctx.exception))

    def test_oversized_upload_rejected(self) -> None:
        # Service max_upload_mb=1 -> 1.2 MB payload rejected
        big_payload = base64.b64encode(b"\x89PNG\r\n\x1a\n" + b"0" * (1300 * 1024)).decode("ascii")
        with self.assertRaises(ImageValidationError) as ctx:
            self.service.decode_and_save(big_payload, "huge.png")
        self.assertIn("maximum size limit", str(ctx.exception))

    def test_corrupt_bytes_rejected(self) -> None:
        bad = base64.b64encode(b"not an image file at all 1234567890").decode("ascii")
        with self.assertRaises(ImageValidationError):
            self.service.decode_and_save(bad, "bad.txt")

    def test_filename_metadata_inference_conservative(self) -> None:
        sym, ex, tf = infer_metadata_from_filename("NSE_BANKNIFTY_15m_2026.png")
        self.assertEqual(sym, "BANK NIFTY")
        self.assertEqual(ex, "NSE")
        self.assertEqual(tf, "15m")

        sym2, ex2, tf2 = infer_metadata_from_filename("screenshot_unknown.png")
        self.assertIsNone(sym2)
        self.assertIsNone(ex2)
        self.assertIsNone(tf2)


class TestDatabaseAndIsolation(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.db = Database(db_path=os.path.join(self.tmpdir.name, "test.db"))

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def test_signup_signin_password_reset_flow(self) -> None:
        u = self.db.create_user("trader@example.com", "StrongPass99", "Rohan")
        self.assertEqual(u["email"], "trader@example.com")
        self.assertEqual(u["role"], "admin")  # first user

        # Wrong password fails
        self.assertIsNone(self.db.authenticate_user("trader@example.com", "WrongPass99"))
        # Correct password succeeds
        authed = self.db.authenticate_user("trader@example.com", "StrongPass99")
        self.assertIsNotNone(authed)

        # Password reset flow
        code = self.db.create_password_reset_token("trader@example.com")
        self.assertIsNotNone(code)
        self.assertFalse(self.db.reset_password_with_token("trader@example.com", "000000", "NewPass123!"))
        self.assertTrue(self.db.reset_password_with_token("trader@example.com", code or "", "NewPass123!"))
        self.assertIsNotNone(self.db.authenticate_user("trader@example.com", "NewPass123!"))

    def test_user_row_isolation_for_analyses_and_watchlist(self) -> None:
        u1 = self.db.create_user("u1@example.com", "Password123", "User One")
        u2 = self.db.create_user("u2@example.com", "Password123", "User Two")

        saved = self.db.save_analysis(
            u1["id"],
            {
                "instrument": "NIFTY 50",
                "exchange": "NSE",
                "timeframe": "15m",
                "verdict": "WAIT",
                "entry_display": "24,200",
                "stop_loss": "24,120",
                "tp1": "24,350",
                "tp2": "24,420",
                "tp3": "NOT AVAILABLE",
                "risk_reward": "T1 1.88",
                "short_explanation": "Wait for close.",
            },
        )
        # u2 cannot access or delete u1's analysis
        self.assertIsNone(self.db.get_analysis(u2["id"], saved["id"]))
        self.assertIsNone(self.db.delete_analysis(u2["id"], saved["id"]))
        self.assertIsNotNone(self.db.get_analysis(u1["id"], saved["id"]))

        # Watchlist isolation
        w1 = self.db.add_watchlist_item(u1["id"], "NIFTY 50", "NSE", "india")
        self.assertEqual(len(self.db.list_watchlist(u2["id"])), 0)
        self.assertFalse(self.db.remove_watchlist_item(u2["id"], w1["id"]))
        self.assertEqual(self.db.list_watchlist(u1["id"])[0]["last_analysis"]["verdict"], "WAIT")


class TestKnowledgeAndAdapters(unittest.TestCase):
    def test_knowledge_catalog_loads_real_markdown(self) -> None:
        loader = KnowledgeLoader()
        catalog = loader.list_catalog()
        self.assertGreaterEqual(len(catalog), 10)
        hammer = loader.get_article("candlesticks", "hammer")
        self.assertIsNotNone(hammer)
        self.assertIn("hammer", hammer["markdown"].lower())

    def test_adapters_never_fabricate_when_unconfigured(self) -> None:
        # Ensure clean env check
        env_backup = {k: os.environ.pop(k, None) for k in ("GEMINI_API_KEY", "OPENAI_API_KEY", "TI_MARKET_DATA_KEY", "TI_NEWS_KEY")}
        try:
            v = VisionProviderAdapter()
            self.assertFalse(v.status()["configured"])

            m = MarketDataAdapter()
            q = m.fetch_quote_if_configured("BTCUSD")
            self.assertFalse(q["available"])

            n = NewsResearchAdapter()
            news_res = n.fetch_news(instrument="BTCUSD")
            self.assertFalse(news_res["available"])
            self.assertEqual(news_res["articles"], [])
        finally:
            for k, val in env_backup.items():
                if val is not None:
                    os.environ[k] = val


class TestEndToEndHTTPWorkflow(unittest.TestCase):
    """Full end-to-end HTTP test:
    Signup -> Login -> Dashboard/Watchlist -> Upload Screenshot -> Analyze Chart (WAIT, READY, NO TRADE, Unverified)
    -> Quick Result -> Full 22-section Report -> History Reopen -> Settings -> Signout.
    """

    @classmethod
    def setUpClass(cls) -> None:
        os.environ["TI_QUIET_LOGS"] = "1"
        cls.tmpdir = tempfile.TemporaryDirectory()
        cls.app = ApplicationContainer(
            db_path=os.path.join(cls.tmpdir.name, "e2e.db"),
            upload_dir=os.path.join(cls.tmpdir.name, "uploads"),
        )
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), create_handler(cls.app))
        cls.port = cls.server.server_address[1]
        cls.base_url = f"http://127.0.0.1:{cls.port}"
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.tmpdir.cleanup()

    def _req(
        self,
        method: str,
        path: str,
        body: dict | None = None,
        token: str | None = None,
    ) -> tuple[int, dict]:
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(
            f"{self.base_url}{path}", data=data, headers=headers, method=method
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status, json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as err:
            return err.code, json.loads(err.read().decode("utf-8"))

    def test_complete_user_journey(self) -> None:
        # 1. Health check
        st, health = self._req("GET", "/api/health")
        self.assertEqual(st, 200)
        self.assertTrue(health["ok"])

        # 2. Protected route rejects unauthenticated access
        st_unauth, _ = self._req("GET", "/api/analyses")
        self.assertEqual(st_unauth, 401)

        # 3. User Signup
        st_up, signup = self._req(
            "POST",
            "/api/auth/signup",
            {
                "name": "Priya Verma",
                "email": "priya@example.com",
                "password": "SecurePassword1!",
            },
        )
        self.assertEqual(st_up, 201)
        token = signup["token"]

        # 4. User Signin
        st_in, signin = self._req(
            "POST",
            "/api/auth/signin",
            {"email": "priya@example.com", "password": "SecurePassword1!"},
        )
        self.assertEqual(st_in, 200)
        token = signin["token"]

        # 5. Analyze Chart — WAIT scenario (BTCUSD 5m unconfirmed breakdown)
        st_anl, anl_wait = self._req(
            "POST",
            "/api/analyze",
            {
                "image_base64": SAMPLE_PNG_DATA_URL,
                "filename": "BTCUSD_5m.png",
                "sample_preset_id": "btcusd_5m_wait",
                "preferences": {"mode": "quick", "language": "english"},
            },
            token=token,
        )
        self.assertEqual(st_anl, 201)
        rec_wait = anl_wait["analysis"]
        self.assertEqual(rec_wait["verdict"], "WAIT")
        self.assertEqual(rec_wait["instrument"], "BTCUSD")
        self.assertEqual(len(rec_wait["full_report"]["sections"]), 22)

        # 6. Analyze Chart — PAPER-TRADING SETUP READY scenario (NIFTY 15m)
        st_rdy, anl_ready = self._req(
            "POST",
            "/api/analyze",
            {
                "image_base64": SAMPLE_PNG_DATA_URL,
                "filename": "NIFTY_15m.png",
                "sample_preset_id": "nifty_15m_ready",
                "preferences": {"mode": "quick", "language": "hinglish"},
            },
            token=token,
        )
        self.assertEqual(st_rdy, 201)
        self.assertEqual(anl_ready["analysis"]["verdict"], "PAPER-TRADING SETUP READY")

        # 7. Analyze Chart — NO TRADE scenario (blank unverified screenshot with no fabricated prices)
        st_nt, anl_nt = self._req(
            "POST",
            "/api/analyze",
            {
                "image_base64": SAMPLE_PNG_DATA_URL,
                "filename": "blank_unknown_chart.png",
                "preferences": {"mode": "quick"},
            },
            token=token,
        )
        self.assertEqual(st_nt, 201)
        self.assertEqual(anl_nt["analysis"]["verdict"], "NO TRADE")
        self.assertEqual(anl_nt["analysis"]["entry_display"], "NOT CONFIRMED")
        self.assertEqual(anl_nt["analysis"]["stop_loss"], "NOT APPLICABLE")

        # 8. Reopen previous analysis & verify screenshot binary endpoint
        st_get, reopened = self._req("GET", f"/api/analyses/{rec_wait['id']}", token=token)
        self.assertEqual(st_get, 200)
        self.assertEqual(reopened["analysis"]["id"], rec_wait["id"])
        self.assertTrue(reopened["analysis"]["snapshot_sha256"])

        img_req = urllib.request.Request(
            f"{self.base_url}/api/analyses/{rec_wait['id']}/image?token={token}"
        )
        with urllib.request.urlopen(img_req, timeout=10) as img_resp:
            self.assertEqual(img_resp.status, 200)
            self.assertEqual(img_resp.headers.get("Content-Type"), "image/png")

        # 9. Watchlist add & link to latest analysis
        st_wl, wl_add = self._req(
            "POST",
            "/api/watchlist",
            {"symbol": "BTCUSD", "exchange": "Bitstamp", "market": "crypto"},
            token=token,
        )
        self.assertEqual(st_wl, 201)
        self.assertEqual(wl_add["item"]["last_analysis"]["id"], rec_wait["id"])

        # 10. Settings update
        st_set, set_res = self._req(
            "PUT",
            "/api/settings",
            {"language": "hinglish", "theme": "midnight", "preferred_market": "india"},
            token=token,
        )
        self.assertEqual(st_set, 200)
        self.assertEqual(set_res["settings"]["language"], "hinglish")

        # 11. History list & delete single record
        st_list, hist = self._req("GET", "/api/analyses", token=token)
        self.assertEqual(st_list, 200)
        self.assertEqual(len(hist["analyses"]), 3)

        st_del, _ = self._req("DELETE", f"/api/analyses/{anl_nt['analysis']['id']}", token=token)
        self.assertEqual(st_del, 200)

        # 12. Sign out invalidates token
        st_out, _ = self._req("POST", "/api/auth/signout", {}, token=token)
        self.assertEqual(st_out, 200)
        st_after, _ = self._req("GET", "/api/analyses", token=token)
        self.assertEqual(st_after, 401)


if __name__ == "__main__":
    unittest.main()
