"""SQLite database and authentication/session layer.

Implements all collections specified in the architecture:
- users (password PBKDF2-HMAC-SHA256, profile, role, reset tokens)
- sessions (HTTP-only / Bearer session tokens with expiry)
- analyses (immutable Quick Signal + V1-V3 Full Analysis records)
- watchlists (per-user watched instruments linked to latest analysis)
- analysis_history (immutable audit trail per analysis)
- user_settings (language, theme, default_mode, preferred_market, timezone, privacy)
- market_research_cache (cached provider quotes / news items with provenance)
- system_logs (audit log of jobs, auth events, provider status)

Row-level access enforcement ensures users can access or mutate only their own
private records.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import sqlite3
import threading
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class Database:
    def __init__(self, db_path: Optional[str] = None) -> None:
        default_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
        )
        os.makedirs(default_dir, exist_ok=True)
        self.db_path = db_path or os.environ.get(
            "TI_DB_PATH", os.path.join(default_dir, "trading_intel.db")
        )
        parent = os.path.dirname(os.path.abspath(self.db_path))
        if parent:
            os.makedirs(parent, exist_ok=True)
        self._lock = threading.RLock()
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=15.0, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        return conn

    def _init_schema(self) -> None:
        with self._lock, self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    email TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    password_salt TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'user',
                    bio TEXT NOT NULL DEFAULT '',
                    reset_token_hash TEXT,
                    reset_expires_at TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS sessions (
                    token_hash TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    created_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    user_agent TEXT NOT NULL DEFAULT ''
                );

                CREATE TABLE IF NOT EXISTS user_settings (
                    user_id TEXT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
                    language TEXT NOT NULL DEFAULT 'english',
                    theme TEXT NOT NULL DEFAULT 'dark',
                    default_mode TEXT NOT NULL DEFAULT 'quick',
                    preferred_market TEXT NOT NULL DEFAULT 'auto',
                    timezone TEXT NOT NULL DEFAULT 'Asia/Kolkata',
                    save_history INTEGER NOT NULL DEFAULT 1,
                    share_anonymous_diagnostics INTEGER NOT NULL DEFAULT 0,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS analyses (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    status TEXT NOT NULL DEFAULT 'completed',
                    stage TEXT NOT NULL DEFAULT 'completed',
                    stage_index INTEGER NOT NULL DEFAULT 9,
                    instrument TEXT NOT NULL,
                    exchange TEXT NOT NULL,
                    market TEXT NOT NULL DEFAULT 'auto',
                    timeframe TEXT NOT NULL,
                    mode TEXT NOT NULL DEFAULT 'quick',
                    language TEXT NOT NULL DEFAULT 'english',
                    screenshot_ref TEXT NOT NULL DEFAULT '',
                    screenshot_filename TEXT NOT NULL DEFAULT '',
                    screenshot_mime TEXT NOT NULL DEFAULT '',
                    screenshot_width INTEGER NOT NULL DEFAULT 0,
                    screenshot_height INTEGER NOT NULL DEFAULT 0,
                    screenshot_size_bytes INTEGER NOT NULL DEFAULT 0,
                    analysis_timestamp TEXT NOT NULL,
                    data_timestamp TEXT NOT NULL,
                    verdict TEXT NOT NULL,
                    legacy_verdict TEXT NOT NULL DEFAULT '',
                    direction TEXT NOT NULL DEFAULT '',
                    wait_condition TEXT NOT NULL DEFAULT '',
                    entry_display TEXT NOT NULL,
                    entry_status TEXT NOT NULL DEFAULT 'PENDING',
                    stop_loss TEXT NOT NULL,
                    tp1 TEXT NOT NULL,
                    tp2 TEXT NOT NULL,
                    tp3 TEXT NOT NULL,
                    risk_reward TEXT NOT NULL,
                    short_explanation TEXT NOT NULL,
                    hinglish_explanation TEXT NOT NULL DEFAULT '',
                    hindi_explanation TEXT NOT NULL DEFAULT '',
                    evidence_json TEXT NOT NULL DEFAULT '[]',
                    data_quality_json TEXT NOT NULL DEFAULT '{}',
                    provider_info_json TEXT NOT NULL DEFAULT '{}',
                    quick_payload_json TEXT NOT NULL DEFAULT '{}',
                    full_report_json TEXT NOT NULL DEFAULT '{}',
                    stages_json TEXT NOT NULL DEFAULT '[]',
                    immutable_version INTEGER NOT NULL DEFAULT 1
                );

                CREATE INDEX IF NOT EXISTS idx_analyses_user_created
                    ON analyses(user_id, analysis_timestamp DESC);

                CREATE TABLE IF NOT EXISTS analysis_history (
                    id TEXT PRIMARY KEY,
                    analysis_id TEXT NOT NULL,
                    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    instrument TEXT NOT NULL,
                    exchange TEXT NOT NULL,
                    timeframe TEXT NOT NULL,
                    verdict TEXT NOT NULL,
                    recorded_at TEXT NOT NULL,
                    snapshot_sha256 TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS watchlists (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    symbol TEXT NOT NULL,
                    exchange TEXT NOT NULL DEFAULT '',
                    market TEXT NOT NULL DEFAULT 'auto',
                    notes TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL,
                    UNIQUE(user_id, symbol, exchange)
                );

                CREATE TABLE IF NOT EXISTS market_research_cache (
                    cache_key TEXT PRIMARY KEY,
                    category TEXT NOT NULL,
                    source TEXT NOT NULL,
                    fetched_at TEXT NOT NULL,
                    freshness TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS system_logs (
                    id TEXT PRIMARY KEY,
                    level TEXT NOT NULL,
                    event TEXT NOT NULL,
                    user_id TEXT,
                    detail_json TEXT NOT NULL DEFAULT '{}',
                    created_at TEXT NOT NULL
                );
                """
            )

    # ------------------------------------------------------------------
    # Password & token helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _hash_password(password: str, salt_hex: Optional[str] = None) -> Tuple[str, str]:
        salt = bytes.fromhex(salt_hex) if salt_hex else secrets.token_bytes(16)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
        return salt.hex(), dk.hex()

    @staticmethod
    def _hash_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def log_event(
        self,
        level: str,
        event: str,
        user_id: Optional[str] = None,
        detail: Optional[Dict[str, Any]] = None,
    ) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO system_logs (id, level, event, user_id, detail_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    f"log_{secrets.token_hex(8)}",
                    level,
                    event,
                    user_id,
                    json.dumps(detail or {}),
                    utc_now_iso(),
                ),
            )

    # ------------------------------------------------------------------
    # Authentication & Users
    # ------------------------------------------------------------------
    def create_user(self, email: str, password: str, name: str) -> Dict[str, Any]:
        clean_email = (email or "").strip().lower()
        clean_name = (name or "").strip()
        if not clean_email or "@" not in clean_email or "." not in clean_email.split("@")[-1]:
            raise ValueError("Please provide a valid email address.")
        if len(password or "") < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not clean_name:
            raise ValueError("Display name is required.")

        salt_hex, pw_hash = self._hash_password(password)
        user_id = f"usr_{secrets.token_hex(8)}"
        now = utc_now_iso()

        with self._lock, self._connect() as conn:
            existing = conn.execute(
                "SELECT id FROM users WHERE email = ?", (clean_email,)
            ).fetchone()
            if existing:
                raise ValueError("An account with this email already exists.")

            # First registered user also receives admin capability for diagnostics
            count_row = conn.execute("SELECT COUNT(*) AS c FROM users").fetchone()
            role = "admin" if (count_row and count_row["c"] == 0) else "user"

            conn.execute(
                """
                INSERT INTO users (id, email, name, password_salt, password_hash, role, bio, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, '', ?, ?)
                """,
                (user_id, clean_email, clean_name, salt_hex, pw_hash, role, now, now),
            )
            conn.execute(
                """
                INSERT INTO user_settings (user_id, language, theme, default_mode, preferred_market, timezone, save_history, share_anonymous_diagnostics, updated_at)
                VALUES (?, 'english', 'dark', 'quick', 'auto', 'Asia/Kolkata', 1, 0, ?)
                """,
                (user_id, now),
            )

        self.log_event("INFO", "user.signup", user_id=user_id, detail={"email": clean_email})
        return self.get_user_by_id(user_id)  # type: ignore[return-value]

    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        clean_email = (email or "").strip().lower()
        with self._lock, self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE email = ?", (clean_email,)
            ).fetchone()
        if not row:
            return None
        _, candidate_hash = self._hash_password(password, row["password_salt"])
        if not hmac.compare_digest(candidate_hash, row["password_hash"]):
            self.log_event("WARN", "user.signin_failed", user_id=row["id"])
            return None
        self.log_event("INFO", "user.signin", user_id=row["id"])
        return self._public_user(row)

    def create_session(self, user_id: str, user_agent: str = "", days: int = 14) -> str:
        raw_token = f"tis_{secrets.token_urlsafe(32)}"
        token_hash = self._hash_token(raw_token)
        now = datetime.now(timezone.utc)
        expires = now + timedelta(days=days)
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO sessions (token_hash, user_id, created_at, expires_at, user_agent)
                VALUES (?, ?, ?, ?, ?)
                """,
                (token_hash, user_id, now.isoformat(), expires.isoformat(), user_agent[:250]),
            )
        return raw_token

    def get_user_by_session(self, raw_token: Optional[str]) -> Optional[Dict[str, Any]]:
        if not raw_token:
            return None
        token_hash = self._hash_token(raw_token)
        now_iso = utc_now_iso()
        with self._lock, self._connect() as conn:
            row = conn.execute(
                """
                SELECT u.* FROM sessions s
                JOIN users u ON u.id = s.user_id
                WHERE s.token_hash = ? AND s.expires_at > ?
                """,
                (token_hash, now_iso),
            ).fetchone()
        return self._public_user(row) if row else None

    def delete_session(self, raw_token: Optional[str]) -> None:
        if not raw_token:
            return
        token_hash = self._hash_token(raw_token)
        with self._lock, self._connect() as conn:
            conn.execute("DELETE FROM sessions WHERE token_hash = ?", (token_hash,))

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return self._public_user(row) if row else None

    def update_profile(self, user_id: str, name: Optional[str] = None, bio: Optional[str] = None) -> Dict[str, Any]:
        now = utc_now_iso()
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            if not row:
                raise ValueError("User not found.")
            new_name = name.strip() if name is not None and name.strip() else row["name"]
            new_bio = bio.strip() if bio is not None else row["bio"]
            conn.execute(
                "UPDATE users SET name = ?, bio = ?, updated_at = ? WHERE id = ?",
                (new_name, new_bio[:500], now, user_id),
            )
        return self.get_user_by_id(user_id)  # type: ignore[return-value]

    def update_password(self, user_id: str, current_password: str, new_password: str) -> None:
        if len(new_password or "") < 8:
            raise ValueError("New password must be at least 8 characters long.")
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            if not row:
                raise ValueError("User not found.")
            _, candidate = self._hash_password(current_password, row["password_salt"])
            if not hmac.compare_digest(candidate, row["password_hash"]):
                raise ValueError("Current password is incorrect.")
            new_salt, new_hash = self._hash_password(new_password)
            conn.execute(
                "UPDATE users SET password_salt = ?, password_hash = ?, updated_at = ? WHERE id = ?",
                (new_salt, new_hash, utc_now_iso(), user_id),
            )
        self.log_event("INFO", "user.password_changed", user_id=user_id)

    def create_password_reset_token(self, email: str) -> Optional[str]:
        clean_email = (email or "").strip().lower()
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT id FROM users WHERE email = ?", (clean_email,)).fetchone()
            if not row:
                return None
            raw_code = f"{secrets.randbelow(900000) + 100000}"
            code_hash = self._hash_token(raw_code)
            expires = (datetime.now(timezone.utc) + timedelta(minutes=30)).isoformat()
            conn.execute(
                "UPDATE users SET reset_token_hash = ?, reset_expires_at = ?, updated_at = ? WHERE id = ?",
                (code_hash, expires, utc_now_iso(), row["id"]),
            )
        self.log_event("INFO", "user.password_reset_requested", user_id=row["id"])
        return raw_code

    def reset_password_with_token(self, email: str, reset_code: str, new_password: str) -> bool:
        if len(new_password or "") < 8:
            raise ValueError("New password must be at least 8 characters long.")
        clean_email = (email or "").strip().lower()
        code_hash = self._hash_token((reset_code or "").strip())
        now_iso = utc_now_iso()
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT * FROM users WHERE email = ?", (clean_email,)).fetchone()
            if not row or not row["reset_token_hash"] or not row["reset_expires_at"]:
                return False
            if row["reset_expires_at"] < now_iso:
                return False
            if not hmac.compare_digest(code_hash, row["reset_token_hash"]):
                return False
            salt_hex, pw_hash = self._hash_password(new_password)
            conn.execute(
                """
                UPDATE users
                SET password_salt = ?, password_hash = ?, reset_token_hash = NULL, reset_expires_at = NULL, updated_at = ?
                WHERE id = ?
                """,
                (salt_hex, pw_hash, now_iso, row["id"]),
            )
            conn.execute("DELETE FROM sessions WHERE user_id = ?", (row["id"],))
        self.log_event("INFO", "user.password_reset_completed", user_id=row["id"])
        return True

    @staticmethod
    def _public_user(row: sqlite3.Row) -> Dict[str, Any]:
        return {
            "id": row["id"],
            "email": row["email"],
            "name": row["name"],
            "role": row["role"],
            "bio": row["bio"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }

    # ------------------------------------------------------------------
    # Settings
    # ------------------------------------------------------------------
    def get_settings(self, user_id: str) -> Dict[str, Any]:
        with self._lock, self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM user_settings WHERE user_id = ?", (user_id,)
            ).fetchone()
            if not row:
                now = utc_now_iso()
                conn.execute(
                    """
                    INSERT INTO user_settings (user_id, language, theme, default_mode, preferred_market, timezone, save_history, share_anonymous_diagnostics, updated_at)
                    VALUES (?, 'english', 'dark', 'quick', 'auto', 'Asia/Kolkata', 1, 0, ?)
                    """,
                    (user_id, now),
                )
                row = conn.execute(
                    "SELECT * FROM user_settings WHERE user_id = ?", (user_id,)
                ).fetchone()
        return {
            "language": row["language"],
            "theme": row["theme"],
            "default_mode": row["default_mode"],
            "preferred_market": row["preferred_market"],
            "timezone": row["timezone"],
            "save_history": bool(row["save_history"]),
            "share_anonymous_diagnostics": bool(row["share_anonymous_diagnostics"]),
            "updated_at": row["updated_at"],
        }

    def update_settings(self, user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        current = self.get_settings(user_id)
        allowed_languages = {"english", "hinglish", "hindi"}
        allowed_themes = {"dark", "midnight", "light"}
        allowed_modes = {"quick", "full"}
        allowed_markets = {"auto", "india", "us", "forex", "commodities", "crypto"}

        language = str(updates.get("language", current["language"])).lower()
        if language not in allowed_languages:
            language = current["language"]

        theme = str(updates.get("theme", current["theme"])).lower()
        if theme not in allowed_themes:
            theme = current["theme"]

        default_mode = str(updates.get("default_mode", current["default_mode"])).lower()
        if default_mode not in allowed_modes:
            default_mode = current["default_mode"]

        preferred_market = str(updates.get("preferred_market", current["preferred_market"])).lower()
        if preferred_market not in allowed_markets:
            preferred_market = current["preferred_market"]

        tz_name = str(updates.get("timezone", current["timezone"])).strip() or "Asia/Kolkata"
        save_history = 1 if updates.get("save_history", current["save_history"]) else 0
        share_diag = (
            1
            if updates.get(
                "share_anonymous_diagnostics", current["share_anonymous_diagnostics"]
            )
            else 0
        )

        now = utc_now_iso()
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                UPDATE user_settings
                SET language = ?, theme = ?, default_mode = ?, preferred_market = ?,
                    timezone = ?, save_history = ?, share_anonymous_diagnostics = ?, updated_at = ?
                WHERE user_id = ?
                """,
                (
                    language,
                    theme,
                    default_mode,
                    preferred_market,
                    tz_name[:64],
                    save_history,
                    share_diag,
                    now,
                    user_id,
                ),
            )
        return self.get_settings(user_id)

    # ------------------------------------------------------------------
    # Analyses (Immutable once persisted)
    # ------------------------------------------------------------------
    def save_analysis(self, user_id: str, record: Dict[str, Any]) -> Dict[str, Any]:
        settings = self.get_settings(user_id)
        analysis_id = record.get("id") or f"anl_{secrets.token_hex(8)}"
        now = record.get("analysis_timestamp") or utc_now_iso()
        data_ts = record.get("data_timestamp") or now

        quick_json = json.dumps(record.get("quick_payload", {}), ensure_ascii=False)
        full_json = json.dumps(record.get("full_report", {}), ensure_ascii=False)
        evidence_json = json.dumps(record.get("evidence", []), ensure_ascii=False)
        data_quality_json = json.dumps(record.get("data_quality", {}), ensure_ascii=False)
        provider_json = json.dumps(record.get("provider_info", {}), ensure_ascii=False)
        stages_json = json.dumps(record.get("stages", []), ensure_ascii=False)

        snapshot_hash = hashlib.sha256(
            (quick_json + "|" + full_json + "|" + now).encode("utf-8")
        ).hexdigest()

        if settings.get("save_history", True):
            with self._lock, self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO analyses (
                        id, user_id, status, stage, stage_index,
                        instrument, exchange, market, timeframe, mode, language,
                        screenshot_ref, screenshot_filename, screenshot_mime,
                        screenshot_width, screenshot_height, screenshot_size_bytes,
                        analysis_timestamp, data_timestamp,
                        verdict, legacy_verdict, direction, wait_condition,
                        entry_display, entry_status, stop_loss,
                        tp1, tp2, tp3, risk_reward,
                        short_explanation, hinglish_explanation, hindi_explanation,
                        evidence_json, data_quality_json, provider_info_json,
                        quick_payload_json, full_report_json, stages_json,
                        immutable_version
                    ) VALUES (
                        ?, ?, ?, ?, ?,
                        ?, ?, ?, ?, ?, ?,
                        ?, ?, ?,
                        ?, ?, ?,
                        ?, ?,
                        ?, ?, ?, ?,
                        ?, ?, ?,
                        ?, ?, ?, ?,
                        ?, ?, ?,
                        ?, ?, ?,
                        ?, ?, ?,
                        1
                    )
                    """,
                    (
                        analysis_id,
                        user_id,
                        record.get("status", "completed"),
                        record.get("stage", "completed"),
                        int(record.get("stage_index", 9)),
                        record.get("instrument", "UNKNOWN"),
                        record.get("exchange", "UNKNOWN"),
                        record.get("market", "auto"),
                        record.get("timeframe", "UNKNOWN"),
                        record.get("mode", "quick"),
                        record.get("language", "english"),
                        record.get("screenshot_ref", ""),
                        record.get("screenshot_filename", ""),
                        record.get("screenshot_mime", ""),
                        int(record.get("screenshot_width", 0)),
                        int(record.get("screenshot_height", 0)),
                        int(record.get("screenshot_size_bytes", 0)),
                        now,
                        data_ts,
                        record.get("verdict", "WAIT"),
                        record.get("legacy_verdict", "WAIT — NO CONFIRMED SETUP"),
                        record.get("direction", ""),
                        record.get("wait_condition", ""),
                        record.get("entry_display", "NOT AVAILABLE — INSUFFICIENT DATA"),
                        record.get("entry_status", "PENDING"),
                        record.get("stop_loss", "NOT AVAILABLE — INSUFFICIENT DATA"),
                        record.get("tp1", "NOT AVAILABLE"),
                        record.get("tp2", "NOT AVAILABLE"),
                        record.get("tp3", "NOT AVAILABLE"),
                        record.get("risk_reward", "NOT AVAILABLE — INSUFFICIENT DATA"),
                        record.get("short_explanation", ""),
                        record.get("hinglish_explanation", ""),
                        record.get("hindi_explanation", ""),
                        evidence_json,
                        data_quality_json,
                        provider_json,
                        quick_json,
                        full_json,
                        stages_json,
                    ),
                )
                conn.execute(
                    """
                    INSERT INTO analysis_history (
                        id, analysis_id, user_id, instrument, exchange, timeframe, verdict, recorded_at, snapshot_sha256
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        f"his_{secrets.token_hex(8)}",
                        analysis_id,
                        user_id,
                        record.get("instrument", "UNKNOWN"),
                        record.get("exchange", "UNKNOWN"),
                        record.get("timeframe", "UNKNOWN"),
                        record.get("verdict", "WAIT"),
                        now,
                        snapshot_hash,
                    ),
                )
            self.log_event(
                "INFO",
                "analysis.created",
                user_id=user_id,
                detail={"analysis_id": analysis_id, "instrument": record.get("instrument"), "verdict": record.get("verdict")},
            )
            return self.get_analysis(user_id, analysis_id)  # type: ignore[return-value]

        # Privacy mode: save_history disabled -> return transient record with snapshot hash
        transient = dict(record)
        transient["id"] = analysis_id
        transient["user_id"] = user_id
        transient["persisted"] = False
        transient["snapshot_sha256"] = snapshot_hash
        return transient

    def get_analysis(self, user_id: str, analysis_id: str) -> Optional[Dict[str, Any]]:
        with self._lock, self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM analyses WHERE id = ? AND user_id = ?",
                (analysis_id, user_id),
            ).fetchone()
            hist = conn.execute(
                "SELECT snapshot_sha256 FROM analysis_history WHERE analysis_id = ? AND user_id = ?",
                (analysis_id, user_id),
            ).fetchone()
        if not row:
            return None
        return self._hydrate_analysis(row, hist["snapshot_sha256"] if hist else "")

    def list_analyses(self, user_id: str, limit: int = 50, instrument: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._lock, self._connect() as conn:
            if instrument:
                rows = conn.execute(
                    """
                    SELECT * FROM analyses
                    WHERE user_id = ? AND UPPER(instrument) = UPPER(?)
                    ORDER BY analysis_timestamp DESC LIMIT ?
                    """,
                    (user_id, instrument.strip(), limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    """
                    SELECT * FROM analyses
                    WHERE user_id = ?
                    ORDER BY analysis_timestamp DESC LIMIT ?
                    """,
                    (user_id, limit),
                ).fetchall()
        return [self._hydrate_analysis(r, summary_only=True) for r in rows]

    def delete_analysis(self, user_id: str, analysis_id: str) -> Optional[str]:
        """Delete user's own analysis record. Returns screenshot_ref if deleted."""
        with self._lock, self._connect() as conn:
            row = conn.execute(
                "SELECT screenshot_ref FROM analyses WHERE id = ? AND user_id = ?",
                (analysis_id, user_id),
            ).fetchone()
            if not row:
                return None
            conn.execute(
                "DELETE FROM analyses WHERE id = ? AND user_id = ?",
                (analysis_id, user_id),
            )
            conn.execute(
                "DELETE FROM analysis_history WHERE analysis_id = ? AND user_id = ?",
                (analysis_id, user_id),
            )
        self.log_event("INFO", "analysis.deleted", user_id=user_id, detail={"analysis_id": analysis_id})
        return row["screenshot_ref"]

    def clear_all_analyses(self, user_id: str) -> int:
        with self._lock, self._connect() as conn:
            cur = conn.execute("DELETE FROM analyses WHERE user_id = ?", (user_id,))
            conn.execute("DELETE FROM analysis_history WHERE user_id = ?", (user_id,))
            deleted = cur.rowcount
        self.log_event("INFO", "analysis.cleared_all", user_id=user_id, detail={"deleted": deleted})
        return deleted

    @staticmethod
    def _hydrate_analysis(
        row: sqlite3.Row, snapshot_sha256: str = "", summary_only: bool = False
    ) -> Dict[str, Any]:
        base: Dict[str, Any] = {
            "id": row["id"],
            "user_id": row["user_id"],
            "status": row["status"],
            "stage": row["stage"],
            "stage_index": row["stage_index"],
            "instrument": row["instrument"],
            "exchange": row["exchange"],
            "market": row["market"],
            "timeframe": row["timeframe"],
            "mode": row["mode"],
            "language": row["language"],
            "screenshot_ref": row["screenshot_ref"],
            "screenshot_filename": row["screenshot_filename"],
            "screenshot_mime": row["screenshot_mime"],
            "screenshot_width": row["screenshot_width"],
            "screenshot_height": row["screenshot_height"],
            "screenshot_size_bytes": row["screenshot_size_bytes"],
            "analysis_timestamp": row["analysis_timestamp"],
            "data_timestamp": row["data_timestamp"],
            "verdict": row["verdict"],
            "legacy_verdict": row["legacy_verdict"],
            "direction": row["direction"],
            "wait_condition": row["wait_condition"],
            "entry_display": row["entry_display"],
            "entry_status": row["entry_status"],
            "stop_loss": row["stop_loss"],
            "tp1": row["tp1"],
            "tp2": row["tp2"],
            "tp3": row["tp3"],
            "risk_reward": row["risk_reward"],
            "short_explanation": row["short_explanation"],
            "hinglish_explanation": row["hinglish_explanation"],
            "hindi_explanation": row["hindi_explanation"],
            "immutable_version": row["immutable_version"],
            "persisted": True,
        }
        if snapshot_sha256:
            base["snapshot_sha256"] = snapshot_sha256
        if not summary_only:
            base["evidence"] = json.loads(row["evidence_json"] or "[]")
            base["data_quality"] = json.loads(row["data_quality_json"] or "{}")
            base["provider_info"] = json.loads(row["provider_info_json"] or "{}")
            base["quick_payload"] = json.loads(row["quick_payload_json"] or "{}")
            base["full_report"] = json.loads(row["full_report_json"] or "{}")
            base["stages"] = json.loads(row["stages_json"] or "[]")
        return base

    # ------------------------------------------------------------------
    # Watchlist
    # ------------------------------------------------------------------
    def list_watchlist(self, user_id: str) -> List[Dict[str, Any]]:
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM watchlists WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,),
            ).fetchall()
            out: List[Dict[str, Any]] = []
            for r in rows:
                latest = conn.execute(
                    """
                    SELECT id, verdict, timeframe, analysis_timestamp, entry_display, stop_loss, tp1
                    FROM analyses
                    WHERE user_id = ? AND UPPER(instrument) = UPPER(?)
                    ORDER BY analysis_timestamp DESC LIMIT 1
                    """,
                    (user_id, r["symbol"]),
                ).fetchone()
                item: Dict[str, Any] = {
                    "id": r["id"],
                    "symbol": r["symbol"],
                    "exchange": r["exchange"],
                    "market": r["market"],
                    "notes": r["notes"],
                    "created_at": r["created_at"],
                    "last_analysis": (
                        {
                            "id": latest["id"],
                            "verdict": latest["verdict"],
                            "timeframe": latest["timeframe"],
                            "analysis_timestamp": latest["analysis_timestamp"],
                            "entry_display": latest["entry_display"],
                            "stop_loss": latest["stop_loss"],
                            "tp1": latest["tp1"],
                        }
                        if latest
                        else None
                    ),
                }
                out.append(item)
        return out

    def add_watchlist_item(
        self,
        user_id: str,
        symbol: str,
        exchange: str = "",
        market: str = "auto",
        notes: str = "",
    ) -> Dict[str, Any]:
        clean_symbol = (symbol or "").strip().upper()
        if not clean_symbol or len(clean_symbol) > 32:
            raise ValueError("Please enter a valid instrument symbol (1-32 characters).")
        clean_exchange = (exchange or "").strip().upper()[:32]
        clean_market = (market or "auto").strip().lower()[:24]
        item_id = f"wch_{secrets.token_hex(8)}"
        now = utc_now_iso()
        with self._lock, self._connect() as conn:
            existing = conn.execute(
                "SELECT id FROM watchlists WHERE user_id = ? AND symbol = ? AND exchange = ?",
                (user_id, clean_symbol, clean_exchange),
            ).fetchone()
            if existing:
                raise ValueError(f"{clean_symbol} is already in your watchlist.")
            conn.execute(
                """
                INSERT INTO watchlists (id, user_id, symbol, exchange, market, notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (item_id, user_id, clean_symbol, clean_exchange, clean_market, (notes or "")[:240], now),
            )
        items = self.list_watchlist(user_id)
        for item in items:
            if item["id"] == item_id:
                return item
        raise RuntimeError("Failed to create watchlist item.")

    def remove_watchlist_item(self, user_id: str, item_id: str) -> bool:
        with self._lock, self._connect() as conn:
            cur = conn.execute(
                "DELETE FROM watchlists WHERE id = ? AND user_id = ?",
                (item_id, user_id),
            )
            return cur.rowcount > 0

    # ------------------------------------------------------------------
    # Admin / Diagnostics stats
    # ------------------------------------------------------------------
    def get_system_diagnostics(self, requesting_user: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock, self._connect() as conn:
            user_count = conn.execute("SELECT COUNT(*) AS c FROM users").fetchone()["c"]
            analysis_count = conn.execute("SELECT COUNT(*) AS c FROM analyses").fetchone()["c"]
            watchlist_count = conn.execute("SELECT COUNT(*) AS c FROM watchlists").fetchone()["c"]
            my_analyses = conn.execute(
                "SELECT COUNT(*) AS c FROM analyses WHERE user_id = ?",
                (requesting_user["id"],),
            ).fetchone()["c"]
            verdict_rows = conn.execute(
                "SELECT verdict, COUNT(*) AS c FROM analyses WHERE user_id = ? GROUP BY verdict",
                (requesting_user["id"],),
            ).fetchall()
            recent_logs = conn.execute(
                """
                SELECT id, level, event, created_at, detail_json
                FROM system_logs
                WHERE user_id = ? OR (? = 'admin')
                ORDER BY created_at DESC LIMIT 25
                """,
                (requesting_user["id"], requesting_user.get("role", "user")),
            ).fetchall()

        return {
            "role": requesting_user.get("role", "user"),
            "totals": {
                "users": user_count if requesting_user.get("role") == "admin" else 1,
                "analyses_global": analysis_count if requesting_user.get("role") == "admin" else my_analyses,
                "analyses_personal": my_analyses,
                "watchlist_items_global": watchlist_count if requesting_user.get("role") == "admin" else 0,
            },
            "personal_verdict_breakdown": {r["verdict"]: r["c"] for r in verdict_rows},
            "recent_logs": [
                {
                    "id": r["id"],
                    "level": r["level"],
                    "event": r["event"],
                    "created_at": r["created_at"],
                    "detail": json.loads(r["detail_json"] or "{}"),
                }
                for r in recent_logs
            ],
        }
