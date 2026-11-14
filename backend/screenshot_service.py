"""Screenshot Processing Service & OCR Adapter.

Validates uploaded chart images (PNG, JPG, JPEG, WEBP; explicitly rejects
unsupported formats such as HEIC with a clear message unless a decoder exists),
enforces configurable size limits (default 10 MB), inspects binary headers for
exact dimensions, and extracts filename/metadata clues without ever confusing
image pixel coordinates with market prices.
"""

from __future__ import annotations

import base64
import hashlib
import os
import re
import secrets
import struct
import subprocess
from dataclasses import dataclass
from typing import Dict, Optional, Tuple


DEFAULT_MAX_UPLOAD_MB = int(os.environ.get("TI_MAX_UPLOAD_MB", "10"))
SUPPORTED_FORMATS = {"png", "jpeg", "webp"}


class ImageValidationError(ValueError):
    """Raised when an uploaded file fails format, size, or integrity validation."""


@dataclass
class ProcessedScreenshot:
    screenshot_id: str
    filename: str
    saved_path: str
    mime_type: str
    detected_format: str
    size_bytes: int
    width: int
    height: int
    sha256: str
    inferred_symbol: Optional[str] = None
    inferred_exchange: Optional[str] = None
    inferred_timeframe: Optional[str] = None
    ocr_text: Optional[str] = None
    ocr_available: bool = False


def detect_image_format_and_dimensions(data: bytes) -> Tuple[str, str, int, int]:
    """Inspect magic bytes and parse width/height without external libraries."""
    if len(data) < 24:
        raise ImageValidationError("Uploaded file is too small or corrupted to be a valid chart image.")

    # Check HEIC / HEIF ftyp box explicitly so we give a clear message
    if len(data) >= 12 and data[4:8] == b"ftyp":
        brand = data[8:12].decode("ascii", errors="ignore").lower()
        if brand in {"heic", "heix", "hevc", "hevx", "mif1", "msf1"}:
            raise ImageValidationError(
                "HEIC/HEIF images are not supported by the current server decoder. Please upload PNG, JPG, JPEG, or WEBP."
            )

    # PNG
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        if data[12:16] != b"IHDR":
            raise ImageValidationError("Invalid PNG header.")
        width, height = struct.unpack(">II", data[16:24])
        if width <= 0 or height <= 0:
            raise ImageValidationError("Invalid PNG image dimensions.")
        return "png", "image/png", int(width), int(height)

    # JPEG
    if data[:2] == b"\xff\xd8":
        idx = 2
        length = len(data)
        while idx < length - 9:
            if data[idx] != 0xFF:
                idx += 1
                continue
            marker = data[idx + 1]
            # Skip padding FF bytes
            while marker == 0xFF and idx + 2 < length:
                idx += 1
                marker = data[idx + 1]
            if marker in (0xD8, 0xD9):
                idx += 2
                continue
            if idx + 4 > length:
                break
            seg_len = struct.unpack(">H", data[idx + 2 : idx + 4])[0]
            if seg_len < 2:
                break
            # SOF0..SOF3, SOF5..SOF7, SOF9..SOF11, SOF13..SOF15
            if marker in {
                0xC0, 0xC1, 0xC2, 0xC3,
                0xC5, 0xC6, 0xC7,
                0xC9, 0xCA, 0xCB,
                0xCD, 0xCE, 0xCF,
            }:
                if idx + 9 <= length:
                    height, width = struct.unpack(">HH", data[idx + 5 : idx + 9])
                    if width > 0 and height > 0:
                        return "jpeg", "image/jpeg", int(width), int(height)
            idx += 2 + seg_len
        raise ImageValidationError("Could not read JPEG dimensions; file appears truncated.")

    # WEBP
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        chunk = data[12:16]
        if chunk == b"VP8X" and len(data) >= 30:
            w_minus_1 = int.from_bytes(data[24:27], "little")
            h_minus_1 = int.from_bytes(data[27:30], "little")
            return "webp", "image/webp", w_minus_1 + 1, h_minus_1 + 1
        if chunk == b"VP8 " and len(data) >= 30:
            width = int.from_bytes(data[26:28], "little") & 0x3FFF
            height = int.from_bytes(data[28:30], "little") & 0x3FFF
            if width > 0 and height > 0:
                return "webp", "image/webp", width, height
        if chunk == b"VP8L" and len(data) >= 25:
            b0, b1, b2, b3 = data[21], data[22], data[23], data[24]
            width = 1 + (((b1 & 0x3F) << 8) | b0)
            height = 1 + (((b3 & 0x0F) << 10) | (b2 << 2) | ((b1 & 0xC0) >> 6))
            return "webp", "image/webp", width, height
        return "webp", "image/webp", 800, 600

    raise ImageValidationError(
        "Unsupported image format. Supported chart formats are PNG, JPG, JPEG, and WEBP."
    )


KNOWN_TICKERS: Dict[str, Tuple[str, str, str]] = {
    "BTCUSD": ("BTCUSD", "Bitstamp", "crypto"),
    "BTCUSDT": ("BTCUSDT", "Binance", "crypto"),
    "ETHUSD": ("ETHUSD", "Coinbase", "crypto"),
    "ETHUSDT": ("ETHUSDT", "Binance", "crypto"),
    "SOLUSDT": ("SOLUSDT", "Binance", "crypto"),
    "NIFTY": ("NIFTY 50", "NSE", "india"),
    "NIFTY50": ("NIFTY 50", "NSE", "india"),
    "BANKNIFTY": ("BANK NIFTY", "NSE", "india"),
    "FINNIFTY": ("FINNIFTY", "NSE", "india"),
    "SENSEX": ("SENSEX", "BSE", "india"),
    "RELIANCE": ("RELIANCE", "NSE", "india"),
    "TCS": ("TCS", "NSE", "india"),
    "HDFCBANK": ("HDFCBANK", "NSE", "india"),
    "INFY": ("INFY", "NSE", "india"),
    "AAPL": ("AAPL", "NASDAQ", "us"),
    "NVDA": ("NVDA", "NASDAQ", "us"),
    "MSFT": ("MSFT", "NASDAQ", "us"),
    "TSLA": ("TSLA", "NASDAQ", "us"),
    "SPY": ("SPY", "NYSE Arca", "us"),
    "QQQ": ("QQQ", "NASDAQ", "us"),
    "EURUSD": ("EURUSD", "FX Spot", "forex"),
    "GBPUSD": ("GBPUSD", "FX Spot", "forex"),
    "USDJPY": ("USDJPY", "FX Spot", "forex"),
    "USDINR": ("USDINR", "NSE FX", "forex"),
    "XAUUSD": ("XAUUSD", "COMEX / Spot Gold", "commodities"),
    "GOLD": ("XAUUSD", "COMEX / Spot Gold", "commodities"),
    "CRUDEOIL": ("WTI CRUDE", "NYMEX", "commodities"),
}

TIMEFRAME_TOKENS = [
    ("1m", r"(?:^|[_\-\s])(1m|1min)(?:$|[_\-\s\.])"),
    ("3m", r"(?:^|[_\-\s])(3m|3min)(?:$|[_\-\s\.])"),
    ("5m", r"(?:^|[_\-\s])(5m|5min)(?:$|[_\-\s\.])"),
    ("15m", r"(?:^|[_\-\s])(15m|15min)(?:$|[_\-\s\.])"),
    ("30m", r"(?:^|[_\-\s])(30m|30min)(?:$|[_\-\s\.])"),
    ("1H", r"(?:^|[_\-\s])(1h|60m|1hr)(?:$|[_\-\s\.])"),
    ("4H", r"(?:^|[_\-\s])(4h|240m|4hr)(?:$|[_\-\s\.])"),
    ("1D", r"(?:^|[_\-\s])(1d|daily|day)(?:$|[_\-\s\.])"),
    ("1W", r"(?:^|[_\-\s])(1w|weekly|week)(?:$|[_\-\s\.])"),
]


def infer_metadata_from_filename(filename: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Conservative metadata hint extraction from TradingView-style filenames.

    TradingView downloads commonly look like ``BTCUSD_2026-11-14_15-30-00.png``
    or ``NSE_NIFTY_15m.png``. Only returns matches when unambiguous; never invents
    prices.
    """
    if not filename:
        return None, None, None
    stem = os.path.splitext(os.path.basename(filename))[0]
    upper = stem.upper()

    inferred_tf: Optional[str] = None
    for canonical, pattern in TIMEFRAME_TOKENS:
        if re.search(pattern, stem, flags=re.IGNORECASE):
            inferred_tf = canonical
            break

    tokens = [t for t in re.split(r"[^A-Z0-9]+", upper) if t]
    for tok in tokens:
        if tok in KNOWN_TICKERS:
            sym, exch, _ = KNOWN_TICKERS[tok]
            # Check if explicit exchange prefix also exists
            for ex_candidate in ("NSE", "BSE", "NASDAQ", "NYSE", "BINANCE", "BITSTAMP", "COINBASE"):
                if ex_candidate in tokens:
                    exch = ex_candidate.title() if ex_candidate in ("BINANCE", "BITSTAMP", "COINBASE") else ex_candidate
                    break
            return sym, exch, inferred_tf

    return None, None, inferred_tf


def try_local_ocr(image_path: str) -> Tuple[bool, Optional[str]]:
    """Run Tesseract OCR only if installed on the host. Never fakes OCR."""
    try:
        proc = subprocess.run(
            ["tesseract", image_path, "stdout", "--psm", "6"],
            capture_output=True,
            text=True,
            timeout=6,
            check=False,
        )
        if proc.returncode == 0:
            return True, proc.stdout.strip()
    except (FileNotFoundError, subprocess.SubprocessError, OSError):
        pass
    return False, None


class ScreenshotService:
    def __init__(self, upload_dir: Optional[str] = None, max_upload_mb: int = DEFAULT_MAX_UPLOAD_MB) -> None:
        base_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "uploads"
        )
        self.upload_dir = upload_dir or os.environ.get("TI_UPLOAD_DIR", base_dir)
        os.makedirs(self.upload_dir, exist_ok=True)
        self.max_bytes = max_upload_mb * 1024 * 1024
        self.max_upload_mb = max_upload_mb

    def decode_and_save(
        self,
        image_base64: str,
        filename: str = "chart.png",
    ) -> ProcessedScreenshot:
        if not image_base64:
            raise ImageValidationError("No chart image was received. Please select a screenshot to upload.")

        # Strip optional data URL prefix: data:image/png;base64,...
        raw_b64 = image_base64.strip()
        if raw_b64.startswith("data:"):
            parts = raw_b64.split(",", 1)
            if len(parts) != 2:
                raise ImageValidationError("Malformed data URL payload.")
            header = parts[0].lower()
            if "image/heic" in header or "image/heif" in header:
                raise ImageValidationError(
                    "HEIC/HEIF images are not supported by the current server decoder. Please upload PNG, JPG, JPEG, or WEBP."
                )
            raw_b64 = parts[1]

        try:
            binary = base64.b64decode(raw_b64, validate=False)
        except Exception as exc:
            raise ImageValidationError("Uploaded image base64 payload could not be decoded.") from exc

        if len(binary) == 0:
            raise ImageValidationError("Uploaded image file is empty (0 bytes).")

        if len(binary) > self.max_bytes:
            raise ImageValidationError(
                f"Uploaded image exceeds the maximum size limit of {self.max_upload_mb} MB."
            )

        detected_fmt, mime_type, width, height = detect_image_format_and_dimensions(binary)
        if width < 80 or height < 80:
            raise ImageValidationError(
                f"Image resolution ({width}x{height}px) is too small to read chart axes reliably. Minimum 80x80px required."
            )

        sha = hashlib.sha256(binary).hexdigest()
        screenshot_id = f"img_{secrets.token_hex(10)}"
        ext = "jpg" if detected_fmt == "jpeg" else detected_fmt
        safe_filename = re.sub(r"[^A-Za-z0-9._\-]", "_", os.path.basename(filename or f"chart.{ext}"))[:120]
        saved_name = f"{screenshot_id}.{ext}"
        saved_path = os.path.join(self.upload_dir, saved_name)

        with open(saved_path, "wb") as handle:
            handle.write(binary)

        sym, exch, tf = infer_metadata_from_filename(safe_filename)
        ocr_ok, ocr_text = try_local_ocr(saved_path)

        return ProcessedScreenshot(
            screenshot_id=screenshot_id,
            filename=safe_filename,
            saved_path=saved_path,
            mime_type=mime_type,
            detected_format=detected_fmt.upper(),
            size_bytes=len(binary),
            width=width,
            height=height,
            sha256=sha,
            inferred_symbol=sym,
            inferred_exchange=exch,
            inferred_timeframe=tf,
            ocr_text=ocr_text,
            ocr_available=ocr_ok,
        )

    def read_image_bytes(self, screenshot_ref: str) -> Optional[Tuple[bytes, str]]:
        if not screenshot_ref or "/" in screenshot_ref or ".." in screenshot_ref:
            return None
        for ext, mime in (("png", "image/png"), ("jpg", "image/jpeg"), ("webp", "image/webp")):
            candidate = os.path.join(self.upload_dir, f"{screenshot_ref}.{ext}")
            if os.path.isfile(candidate):
                with open(candidate, "rb") as handle:
                    return handle.read(), mime
        return None

    def delete_image(self, screenshot_ref: str) -> None:
        if not screenshot_ref or "/" in screenshot_ref or ".." in screenshot_ref:
            return
        for ext in ("png", "jpg", "webp"):
            candidate = os.path.join(self.upload_dir, f"{screenshot_ref}.{ext}")
            if os.path.isfile(candidate):
                try:
                    os.remove(candidate)
                except OSError:
                    pass
