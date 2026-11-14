"""AI Vision Provider, Market Data Provider, and Financial News Adapters.

Follows SKILL.md, AGENTS.md, and data-sources/api-configuration.md:
- Never hardcodes credentials.
- Never exposes API keys to clients.
- Detects configured environment capabilities honestly:
  * Vision providers: Gemini (`GEMINI_API_KEY`) or OpenAI-compatible (`OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_VISION_MODEL`)
  * Market data providers: `TI_MARKET_DATA_PROVIDER` + `TI_MARKET_DATA_KEY`
  * Financial news providers: `TI_NEWS_PROVIDER` + `TI_NEWS_KEY`
- Includes timeout handling, retry policy, structured JSON validation, and usage tracking.
- Never fabricates live market quotes or fake news headlines when providers are unconfigured.
"""

from __future__ import annotations

import base64
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from trading_intel import validation as val_mod
from trading_intel.providers import base as provider_base


EXTRACTION_SYSTEM_PROMPT = """You are the OCR & Chart Extraction stage of AI Trading Intelligence.
Inspect ONLY what is visibly printed on the chart screenshot.
NEVER invent or guess prices, indicators, tickers, or timeframes that are blurry or absent.
Return STRICT JSON matching this schema:
{
  "instrument": string | null,
  "exchange": string | null,
  "timeframe": string | null,
  "chart_type": "candlestick" | "ohlc_bar" | "line" | "other",
  "last_price": number | null,
  "support_level": number | null,
  "resistance_level": number | null,
  "swing_high": number | null,
  "swing_low": number | null,
  "atr": number | null,
  "direction_bias": "long" | "short" | null,
  "candle_state": "forming" | "closed" | "confirmed_breakout" | "unconfirmed_breakout" | "failed_breakout" | "confirmed_breakdown" | "unconfirmed_breakdown" | "failed_breakdown" | "unknown",
  "has_close_confirmation": boolean,
  "volume_present": boolean,
  "volume_confirmed": boolean | null,
  "retest_status": "confirmed" | "pending" | "failed" | null,
  "htf_conflict": boolean,
  "choppy": boolean,
  "trap_unrefuted": boolean,
  "indicators_visible": [{"name": string, "value": string, "reading": string}],
  "patterns_visible": [{"name": string, "status": "CONFIRMED" | "DEVELOPING" | "POSSIBLE" | "UNCLEAR", "note": string}],
  "levels": [{"price": number, "kind": "support" | "resistance", "touches": number}],
  "quality_observed": {
    "instrument_identifiable": boolean,
    "timeframe_visible": boolean,
    "price_axis_readable": boolean,
    "volume_present": boolean,
    "indicators_labeled": boolean,
    "candles_clear": boolean,
    "axes_not_distorted": boolean
  },
  "unreadable": [string],
  "notes": [string]
}"""


class VisionProviderAdapter:
    """Provider-independent multimodal chart extraction adapter."""

    def __init__(self) -> None:
        self.usage_calls = 0
        self.usage_errors = 0

    def status(self) -> Dict[str, Any]:
        gemini_key = bool(os.environ.get("GEMINI_API_KEY"))
        openai_key = bool(os.environ.get("OPENAI_API_KEY"))
        custom_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")

        active_provider = "none"
        model_name = None
        if gemini_key:
            active_provider = "gemini"
            model_name = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
        elif openai_key:
            active_provider = "openai_compatible"
            model_name = os.environ.get("OPENAI_VISION_MODEL", "gpt-4o-mini")

        return {
            "configured": active_provider != "none",
            "active_provider": active_provider,
            "model": model_name,
            "supported_providers": ["gemini", "openai_compatible"],
            "openai_base_url_configured": custom_url != "https://api.openai.com/v1",
            "mode_label": (
                f"LIVE MULTIMODAL VISION ({active_provider.upper()})"
                if active_provider != "none"
                else "OFFLINE DETERMINISTIC ENGINE (No external AI vision key configured)"
            ),
            "usage": {
                "calls": self.usage_calls,
                "errors": self.usage_errors,
            },
        }

    def analyze_image(
        self, image_path: str, mime_type: str, timeout_sec: int = 25, retries: int = 1
    ) -> Dict[str, Any]:
        st = self.status()
        if not st["configured"]:
            return {
                "used_vision_api": False,
                "provider": "offline",
                "reason": "No GEMINI_API_KEY or OPENAI_API_KEY configured in server environment.",
                "extracted": None,
            }

        with open(image_path, "rb") as f:
            b64_img = base64.b64encode(f.read()).decode("ascii")

        last_err = ""
        for attempt in range(retries + 1):
            try:
                self.usage_calls += 1
                if st["active_provider"] == "gemini":
                    raw = self._call_gemini(b64_img, mime_type, st["model"], timeout_sec)
                else:
                    raw = self._call_openai_compatible(b64_img, mime_type, st["model"], timeout_sec)
                validated = self._validate_structured_output(raw)
                return {
                    "used_vision_api": True,
                    "provider": st["active_provider"],
                    "model": st["model"],
                    "extracted": validated,
                }
            except Exception as exc:
                self.usage_errors += 1
                last_err = str(exc)
                if attempt < retries:
                    time.sleep(0.6)

        return {
            "used_vision_api": False,
            "provider": st["active_provider"],
            "error": f"Vision provider request failed: {last_err}",
            "extracted": None,
        }

    def _call_gemini(self, b64_img: str, mime_type: str, model: str, timeout_sec: int) -> Dict[str, Any]:
        api_key = os.environ["GEMINI_API_KEY"]
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{urllib.parse.quote(model)}:generateContent?key={urllib.parse.quote(api_key)}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": EXTRACTION_SYSTEM_PROMPT},
                        {"inline_data": {"mime_type": mime_type, "data": b64_img}},
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "responseMimeType": "application/json",
            },
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        text = body["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text)

    def _call_openai_compatible(self, b64_img: str, mime_type: str, model: str, timeout_sec: int) -> Dict[str, Any]:
        api_key = os.environ["OPENAI_API_KEY"]
        base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        url = f"{base_url}/chat/completions"
        payload = {
            "model": model,
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract visible chart information strictly as JSON."},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{mime_type};base64,{b64_img}"},
                        },
                    ],
                },
            ],
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        text = body["choices"][0]["message"]["content"]
        return json.loads(text)

    @staticmethod
    def _validate_structured_output(data: Any) -> Dict[str, Any]:
        if not isinstance(data, dict):
            raise ValueError("Vision provider did not return a JSON object.")

        def num_or_none(v: Any) -> Optional[float]:
            if v is None or v == "":
                return None
            try:
                f = float(v)
                return f if f > 0 else None
            except (TypeError, ValueError):
                return None

        return {
            "instrument": str(data["instrument"]).strip().upper() if data.get("instrument") else None,
            "exchange": str(data["exchange"]).strip() if data.get("exchange") else None,
            "timeframe": str(data["timeframe"]).strip() if data.get("timeframe") else None,
            "chart_type": str(data.get("chart_type") or "candlestick"),
            "last_price": num_or_none(data.get("last_price")),
            "support_level": num_or_none(data.get("support_level")),
            "resistance_level": num_or_none(data.get("resistance_level")),
            "swing_high": num_or_none(data.get("swing_high")),
            "swing_low": num_or_none(data.get("swing_low")),
            "atr": num_or_none(data.get("atr")),
            "direction_bias": data.get("direction_bias") if data.get("direction_bias") in ("long", "short") else None,
            "candle_state": str(data.get("candle_state") or "unknown"),
            "has_close_confirmation": bool(data.get("has_close_confirmation", False)),
            "volume_present": bool(data.get("volume_present", False)),
            "volume_confirmed": data.get("volume_confirmed") if isinstance(data.get("volume_confirmed"), bool) else None,
            "retest_status": data.get("retest_status") if data.get("retest_status") in ("confirmed", "pending", "failed") else None,
            "htf_conflict": bool(data.get("htf_conflict", False)),
            "choppy": bool(data.get("choppy", False)),
            "trap_unrefuted": bool(data.get("trap_unrefuted", False)),
            "indicators_visible": data.get("indicators_visible") if isinstance(data.get("indicators_visible"), list) else [],
            "patterns_visible": data.get("patterns_visible") if isinstance(data.get("patterns_visible"), list) else [],
            "levels": data.get("levels") if isinstance(data.get("levels"), list) else [],
            "quality_observed": data.get("quality_observed") if isinstance(data.get("quality_observed"), dict) else {},
            "unreadable": data.get("unreadable") if isinstance(data.get("unreadable"), list) else [],
            "notes": data.get("notes") if isinstance(data.get("notes"), list) else [],
        }


class MarketDataAdapter:
    """Authorized market data adapter wrapping `trading_intel.providers.base`.

    Never scrapes and never fabricates live prices. Reports honest provider
    configuration status via `describe_environment()`.
    """

    def status(self) -> Dict[str, Any]:
        env_info = provider_base.describe_environment()
        provider_name = os.environ.get("TI_MARKET_DATA_PROVIDER", "").strip().lower()
        has_key = bool(os.environ.get("TI_MARKET_DATA_KEY", "").strip())
        configured = bool(provider_name and has_key)
        return {
            "configured": configured,
            "provider": provider_name or None,
            "mode": env_info["mode"],
            "live_quotes_available": configured,
            "delay_classification": "AUTHORIZED_FEED" if configured else "SCREENSHOT_ONLY",
            "note": (
                f"Connected to authorized provider '{provider_name}'."
                if configured
                else "No external market-data API key configured (TI_MARKET_DATA_PROVIDER / TI_MARKET_DATA_KEY). Live market prices are intentionally hidden rather than simulated."
            ),
        }

    def fetch_quote_if_configured(self, symbol: str) -> Dict[str, Any]:
        st = self.status()
        if not st["configured"]:
            return {
                "available": False,
                "symbol": symbol,
                "source": None,
                "freshness": "UNAVAILABLE",
                "reason": "Authorized market-data provider not configured.",
            }

        provider = st["provider"]
        api_key = os.environ.get("TI_MARKET_DATA_KEY", "")
        now_dt = datetime.now(timezone.utc)

        try:
            if provider == "alphavantage":
                url = (
                    "https://www.alphavantage.co/query?function=GLOBAL_QUOTE"
                    f"&symbol={urllib.parse.quote(symbol)}&apikey={urllib.parse.quote(api_key)}"
                )
                req = urllib.request.Request(url, method="GET")
                with urllib.request.urlopen(req, timeout=10) as resp:
                    payload = json.loads(resp.read().decode("utf-8"))
                gq = payload.get("Global Quote") or {}
                price_str = gq.get("05. price")
                if not price_str:
                    return {
                        "available": False,
                        "symbol": symbol,
                        "source": "Alpha Vantage",
                        "freshness": "UNAVAILABLE",
                        "reason": "Symbol quote not returned or rate-limited by Alpha Vantage.",
                    }
                ts_iso = now_dt.isoformat()
                fresh = val_mod.freshness(now_dt, now_dt, intraday=True)
                return {
                    "available": True,
                    "symbol": symbol,
                    "last": float(price_str),
                    "change_pct": float(str(gq.get("10. change percent", "0")).replace("%", "") or 0),
                    "timestamp": ts_iso,
                    "source": "Alpha Vantage",
                    "freshness": fresh["class"],
                    "delayed": True,
                }
        except (urllib.error.URLError, ValueError, KeyError, TimeoutError) as exc:
            return {
                "available": False,
                "symbol": symbol,
                "source": provider,
                "freshness": "ERROR",
                "reason": f"Market data request failed: {exc}",
            }

        return {
            "available": False,
            "symbol": symbol,
            "source": provider,
            "freshness": "UNSUPPORTED_ADAPTER",
            "reason": f"Provider '{provider}' adapter requires custom endpoint configuration.",
        }


class NewsResearchAdapter:
    """Authorized financial news adapter.

    Follows SKILL.md Rule 3 & 4 and Prompt §13 & §17:
    - Never invents headlines or displays stale articles as current.
    - Fetches real articles only when `TI_NEWS_PROVIDER` and `TI_NEWS_KEY` are configured
      and network access to that authorized provider succeeds.
    - Otherwise returns an explicit `available: False` state with clear documentation
      of the event-risk research methodology from `data-sources/news-data.md`.
    """

    def status(self) -> Dict[str, Any]:
        provider = os.environ.get("TI_NEWS_PROVIDER", "").strip().lower()
        has_key = bool(os.environ.get("TI_NEWS_KEY", "").strip())
        configured = bool(provider and has_key)
        return {
            "configured": configured,
            "provider": provider or None,
            "note": (
                f"Authorized financial news provider '{provider}' configured."
                if configured
                else "No live financial news API key configured (TI_NEWS_PROVIDER / TI_NEWS_KEY). Unverified or synthetic headlines are never shown."
            ),
        }

    def fetch_news(
        self,
        query: str = "",
        market: str = "all",
        instrument: str = "",
    ) -> Dict[str, Any]:
        st = self.status()
        retrieved_at = datetime.now(timezone.utc).isoformat()
        if not st["configured"]:
            return {
                "available": False,
                "provider": None,
                "retrieved_at": retrieved_at,
                "freshness": "UNAVAILABLE",
                "articles": [],
                "message": "Live news feed is not connected. Configure TI_NEWS_PROVIDER and TI_NEWS_KEY with an authorized wire/API provider to fetch real-time cited headlines.",
                "event_risk_checklist": [
                    {
                        "category": "Corporate Earnings & Filings",
                        "market": "india / us",
                        "rule": "Check exchange filings (NSE/BSE corporate announcements or SEC EDGAR) before holding across quarterly results. Gate G2 marks imminent binary earnings as NO TRADE.",
                    },
                    {
                        "category": "Central Bank Rate Decisions",
                        "market": "all",
                        "rule": "RBI MPC, FOMC, ECB, and BoJ policy announcements can gap price across technical stop losses.",
                    },
                    {
                        "category": "Macroeconomic Releases",
                        "market": "us / forex / commodities",
                        "rule": "CPI, Non-Farm Payrolls (NFP), GDP, and EIA inventory prints invalidate tight intraday stops inside a 15m/5m horizon.",
                    },
                    {
                        "category": "Derivative Expiry & Rebalancing",
                        "market": "india / crypto",
                        "rule": "NSE weekly/monthly index expiry and large crypto options/funding resets alter intraday volatility regimes.",
                    },
                ],
            }

        provider = st["provider"]
        api_key = os.environ.get("TI_NEWS_KEY", "")
        search_term = " ".join(x for x in [instrument, query, market if market != "all" else "markets"] if x).strip() or "financial markets"

        try:
            if provider == "newsapi":
                url = (
                    "https://newsapi.org/v2/everything?"
                    f"q={urllib.parse.quote(search_term)}&sortBy=publishedAt&pageSize=12&language=en"
                )
                req = urllib.request.Request(url, headers={"X-Api-Key": api_key}, method="GET")
                with urllib.request.urlopen(req, timeout=10) as resp:
                    payload = json.loads(resp.read().decode("utf-8"))
                raw_articles = payload.get("articles") or []
                articles: List[Dict[str, Any]] = []
                now_dt = datetime.now(timezone.utc)
                for art in raw_articles:
                    pub = art.get("publishedAt") or retrieved_at
                    try:
                        pub_dt = datetime.fromisoformat(pub.replace("Z", "+00:00"))
                        fresh = val_mod.freshness(now_dt, pub_dt, intraday=False)["class"]
                    except Exception:
                        fresh = "UNKNOWN"
                    articles.append(
                        {
                            "title": art.get("title") or "Untitled",
                            "summary": art.get("description") or "",
                            "source": (art.get("source") or {}).get("name") or "NewsAPI",
                            "published_at": pub,
                            "url": art.get("url") or "",
                            "market": market,
                            "instrument": instrument or None,
                            "relevance": "DIRECT" if instrument and instrument.lower() in (art.get("title") or "").lower() else "MACRO_CONTEXT",
                            "freshness": fresh,
                        }
                    )
                return {
                    "available": True,
                    "provider": "newsapi",
                    "retrieved_at": retrieved_at,
                    "freshness": "RECENT",
                    "articles": articles,
                    "message": f"Retrieved {len(articles)} cited article(s).",
                    "event_risk_checklist": [],
                }
        except Exception as exc:
            return {
                "available": False,
                "provider": provider,
                "retrieved_at": retrieved_at,
                "freshness": "ERROR",
                "articles": [],
                "message": f"News provider request failed: {exc}",
                "event_risk_checklist": [],
            }

        return {
            "available": False,
            "provider": provider,
            "retrieved_at": retrieved_at,
            "freshness": "UNSUPPORTED_ADAPTER",
            "articles": [],
            "message": f"Configured news provider '{provider}' is not supported by the built-in adapter.",
            "event_risk_checklist": [],
        }
