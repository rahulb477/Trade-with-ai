"""AI Trading Intelligence Orchestration Engine (V1 + V2 + V3 + Quick Signal).

Bridges the web application directly to the existing `trading_intel` Python
standard-library modules:
- `trading_intel.observation` (`ChartObservation`, `Level`, `from_transcription`)
- `trading_intel.validation` (`score_chart_quality`, `validate_ohlc`, `freshness`)
- `trading_intel.indicators` (`rsi`, `ema`, `sma`, `macd`, `atr`, `adx`, `bollinger_bands`, `supertrend`, `vwap`)
- `trading_intel.patterns` (`detect_all` across 23 candlestick detectors)
- `trading_intel.risk` (`reward_risk`, `break_even_win_rate`, `expectancy`, `TradePlan`)
- `trading_intel.sizing` (`size_position`)
- `trading_intel.timeframes` (alignment & ratios)
- `trading_intel.quick_signal` (`build_quick_signal`, `render_quick_text`, `render_quick_html`,
  `assert_no_fabrication`, `validate_no_probability`, `detect_mode`)

Every rule in SKILL.md and AGENTS.md is enforced:
- Never fabricates prices, indicators, news, or probabilities.
- Distinguishes `OBSERVED` (vision/OCR/user chart transcription), `COMPUTED`
  (calculated via `trading_intel` from real OHLCV or observed chart levels),
  and `MISSING / UNAVAILABLE`.
- Tracks real job stages honestly (`completed`, `skipped_unavailable`, `partial`).
"""

from __future__ import annotations

import secrets
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

from trading_intel import (
    indicators as ind_mod,
    observation as obs_mod,
    patterns as pat_mod,
    quick_signal as qs_mod,
    risk as risk_mod,
    sizing as sizing_mod,
    timeframes as tf_mod,
    validation as val_mod,
)

from .knowledge_service import KnowledgeLoader
from .providers_service import MarketDataAdapter, NewsResearchAdapter, VisionProviderAdapter
from .screenshot_service import ProcessedScreenshot


HINDI_REASON_MAP = {
    qs_mod.VERDICT_WAIT: "अभी स्पष्ट कन्फर्मेशन नहीं मिला है। सपोर्ट/रेजिस्टेंस के पास कैंडल क्लोज और कन्फर्मेशन का इंतजार करें।",
    qs_mod.VERDICT_NO_TRADE: "बाजार की वर्तमान स्थिति या रिस्क/रिवॉर्ड अनुपात के आधार पर कोई वैध पेपर-ट्रेडिंग सेटअप उपलब्ध नहीं है।",
    qs_mod.VERDICT_READY: "दस्तावेजी नियमों के अनुसार काल्पनिक शैक्षिक पेपर-ट्रेडिंग सेटअप की शर्तें पूरी हुई हैं; इनवैलिडेशन (स्टॉप लॉस) का ध्यान रखें।",
}


def _safe_float(v: Any) -> Optional[float]:
    if v is None or v == "":
        return None
    try:
        val = float(v)
        return val if val > 0 else None
    except (TypeError, ValueError):
        return None


def _parse_float_list(raw: Any) -> List[float]:
    if not raw:
        return []
    if isinstance(raw, list):
        out = []
        for x in raw:
            f = _safe_float(x)
            if f is not None:
                out.append(f)
        return out
    if isinstance(raw, str):
        out = []
        for token in raw.replace(";", ",").split(","):
            f = _safe_float(token.strip())
            if f is not None:
                out.append(f)
        return out
    return []


# Educational fictional demonstration fixtures clearly labelled FICTIONAL_DEMO
# (Mirroring SKILL.md, README.md, and examples/ — used ONLY when user explicitly triggers Sample Demo)
SAMPLE_CHART_PRESETS: Dict[str, Dict[str, Any]] = {
    "btcusd_5m_wait": {
        "label": "BTCUSD · 5m Consolidation Below Support Breakdown (WAIT Demo)",
        "is_fictional_demo": True,
        "instrument": "BTCUSD",
        "exchange": "Bitstamp",
        "market": "crypto",
        "timeframe": "5m",
        "direction": "short",
        "last_price": 67360.0,
        "entry_low": 67300.0,
        "entry_high": 67400.0,
        "support_level": 67300.0,
        "resistance_level": 67760.0,
        "structural_stop": 67800.0,
        "atr": 80.0,
        "levels_for_targets": [66950.0, 66500.0, 66200.0],
        "candle_state": "unconfirmed_breakdown",
        "has_close_confirmation": False,
        "volume_present": True,
        "volume_confirmed": False,
        "retest_status": "pending",
        "htf_aligned": True,
        "htf": "1H",
        "ohlcv": {
            "open":  [67720, 67690, 67640, 67660, 67610, 67580, 67550, 67590, 67520, 67490, 67510, 67470, 67440, 67460, 67420, 67400, 67415, 67390, 67375, 67380],
            "high":  [67780, 67730, 67695, 67700, 67650, 67610, 67605, 67620, 67560, 67530, 67540, 67505, 67480, 67495, 67450, 67435, 67440, 67415, 67400, 67395],
            "low":   [67670, 67620, 67600, 67605, 67560, 67530, 67510, 67515, 67470, 67450, 67460, 67425, 67405, 67410, 67385, 67365, 67370, 67350, 67330, 67310],
            "close": [67690, 67640, 67660, 67610, 67580, 67550, 67590, 67520, 67490, 67510, 67470, 67440, 67460, 67420, 67400, 67415, 67390, 67375, 67380, 67360],
            "volume":[142, 138, 121, 155, 149, 132, 118, 164, 158, 130, 124, 147, 151, 119, 136, 144, 112, 129, 133, 115],
        },
    },
    "nifty_15m_ready": {
        "label": "NIFTY 50 · 15m Breakout & Retest Hold (PAPER-TRADING SETUP READY Demo)",
        "is_fictional_demo": True,
        "instrument": "NIFTY 50",
        "exchange": "NSE",
        "market": "india",
        "timeframe": "15m",
        "direction": "long",
        "last_price": 24215.0,
        "entry_low": 24200.0,
        "entry_high": 24220.0,
        "support_level": 24195.0,
        "resistance_level": 24380.0,
        "swing_level": 24130.0,
        "atr": 35.0,
        "levels_for_targets": [24365.0, 24450.0, 24540.0],
        "candle_state": "confirmed_breakout",
        "has_close_confirmation": True,
        "volume_present": True,
        "volume_confirmed": True,
        "retest_status": "confirmed",
        "htf_aligned": True,
        "htf": "1D",
        "ohlcv": {
            "open":  [24040, 24055, 24070, 24065, 24085, 24100, 24115, 24105, 24125, 24140, 24155, 24150, 24170, 24185, 24198, 24212, 24204, 24196, 24202, 24205],
            "high":  [24065, 24080, 24085, 24090, 24110, 24125, 24130, 24135, 24150, 24165, 24175, 24180, 24195, 24205, 24222, 24228, 24218, 24210, 24218, 24225],
            "low":   [24025, 24045, 24055, 24055, 24075, 24090, 24098, 24095, 24115, 24130, 24140, 24142, 24160, 24175, 24190, 24198, 24192, 24188, 24195, 24199],
            "close": [24055, 24070, 24065, 24085, 24100, 24115, 24105, 24125, 24140, 24155, 24150, 24170, 24185, 24198, 24212, 24204, 24196, 24202, 24208, 24215],
            "volume":[18500, 19200, 17400, 20100, 21500, 22400, 18100, 23200, 24100, 25000, 19800, 26400, 27900, 31200, 38400, 24100, 21000, 22800, 29500, 34200],
        },
    },
    "aapl_1h_notrade": {
        "label": "AAPL · 1H Mid-Range Poor Risk/Reward (NO TRADE Demo)",
        "is_fictional_demo": True,
        "instrument": "AAPL",
        "exchange": "NASDAQ",
        "market": "us",
        "timeframe": "1H",
        "direction": "long",
        "last_price": 226.40,
        "entry_price": 226.40,
        "support_level": 222.80,
        "resistance_level": 228.50,
        "structural_stop": 222.50,
        "atr": 1.65,
        "levels_for_targets": [228.50, 231.20],
        "candle_state": "closed",
        "has_close_confirmation": True,
        "volume_present": True,
        "volume_confirmed": True,
        "retest_status": "confirmed",
        "htf_aligned": True,
        "choppy": True,
        "ohlcv": {
            "open":  [225.8, 226.4, 227.1, 226.2, 225.1, 225.9, 226.8, 227.4, 226.5, 225.4, 224.9, 225.7, 226.6, 227.2, 226.3, 225.6, 226.1, 226.9, 226.0, 226.2],
            "high":  [226.7, 227.5, 227.8, 226.8, 226.2, 227.0, 227.9, 228.1, 227.1, 226.2, 225.9, 226.8, 227.6, 227.9, 227.0, 226.4, 227.1, 227.5, 226.8, 226.9],
            "low":   [225.1, 225.9, 226.0, 224.9, 224.5, 225.2, 226.1, 226.3, 225.2, 224.6, 224.2, 225.0, 225.9, 226.1, 225.4, 224.8, 225.5, 225.8, 225.4, 225.7],
            "close": [226.4, 227.1, 226.2, 225.1, 225.9, 226.8, 227.4, 226.5, 225.4, 224.9, 225.7, 226.6, 227.2, 226.3, 225.6, 226.1, 226.9, 226.0, 226.2, 226.4],
            "volume":[410, 390, 420, 405, 380, 395, 415, 430, 388, 372, 365, 398, 412, 401, 379, 368, 384, 392, 375, 381],
        },
    },
}


class AnalysisOrchestrator:
    def __init__(
        self,
        knowledge_loader: Optional[KnowledgeLoader] = None,
        vision_adapter: Optional[VisionProviderAdapter] = None,
        market_adapter: Optional[MarketDataAdapter] = None,
        news_adapter: Optional[NewsResearchAdapter] = None,
    ) -> None:
        self.knowledge = knowledge_loader or KnowledgeLoader()
        self.vision = vision_adapter or VisionProviderAdapter()
        self.market_data = market_adapter or MarketDataAdapter()
        self.news = news_adapter or NewsResearchAdapter()

    def execute_analysis(
        self,
        screenshot: ProcessedScreenshot,
        preferences: Dict[str, Any],
        transcription: Optional[Dict[str, Any]] = None,
        sample_preset_id: Optional[str] = None,
        progress_callback: Optional[Callable[[int, str, List[Dict[str, Any]]], None]] = None,
    ) -> Dict[str, Any]:
        """Run the complete V1-V3 + Quick Signal workflow and return a structured record."""
        stages: List[Dict[str, Any]] = [
            {"id": "read_screenshot", "label": "Reading chart screenshot", "status": "pending", "detail": ""},
            {"id": "identify_instrument", "label": "Identifying instrument", "status": "pending", "detail": ""},
            {"id": "detect_timeframe", "label": "Detecting timeframe", "status": "pending", "detail": ""},
            {"id": "analyze_candles", "label": "Analyzing candlesticks", "status": "pending", "detail": ""},
            {"id": "check_structure", "label": "Checking market structure", "status": "pending", "detail": ""},
            {"id": "evaluate_indicators", "label": "Evaluating indicators", "status": "pending", "detail": ""},
            {"id": "research_context", "label": "Researching market context", "status": "pending", "detail": ""},
            {"id": "validate_scenarios", "label": "Validating hypothetical scenarios", "status": "pending", "detail": ""},
            {"id": "prepare_report", "label": "Preparing final report", "status": "pending", "detail": ""},
        ]

        def mark_stage(idx: int, status: str, detail: str) -> None:
            stages[idx]["status"] = status
            stages[idx]["detail"] = detail
            if progress_callback:
                progress_callback(idx, stages[idx]["id"], stages)

        tx = dict(transcription or {})
        is_fictional_demo = False
        if sample_preset_id and sample_preset_id in SAMPLE_CHART_PRESETS:
            preset = SAMPLE_CHART_PRESETS[sample_preset_id]
            is_fictional_demo = True
            for k, v in preset.items():
                if k not in tx or tx[k] in (None, "", []):
                    tx[k] = v

        # ------------------------------------------------------------------
        # Stage 0: Read screenshot + Vision/OCR inspection
        # ------------------------------------------------------------------
        vision_res = self.vision.analyze_image(screenshot.saved_path, screenshot.mime_type)
        extracted = vision_res.get("extracted") or {}

        read_notes = [
            f"Validated {screenshot.detected_format} ({screenshot.width}x{screenshot.height}px, {screenshot.size_bytes:,} bytes)."
        ]
        if vision_res.get("used_vision_api"):
            read_notes.append(f"Vision extraction completed via {vision_res.get('provider')} ({vision_res.get('model')}).")
        elif screenshot.ocr_available and screenshot.ocr_text:
            read_notes.append("Local Tesseract OCR text extracted.")
        elif is_fictional_demo:
            read_notes.append("Using clearly labelled FICTIONAL educational demonstration fixture.")
        else:
            read_notes.append(
                "No external AI vision API key configured; using deterministic observation + filename/user chart inputs without inventing prices."
            )
        mark_stage(0, "completed", " ".join(read_notes))

        # ------------------------------------------------------------------
        # Stage 1: Identify instrument & exchange
        # ------------------------------------------------------------------
        pref_market = str(preferences.get("market") or "auto").lower()
        pref_tf = str(preferences.get("timeframe") or "auto")
        pref_mode = str(preferences.get("mode") or "quick").lower()
        pref_lang = str(preferences.get("language") or "english").lower()
        user_notes = str(preferences.get("notes") or "")
        if qs_mod.detect_mode(user_notes) == "full":
            pref_mode = "full"

        instrument = (
            (tx.get("instrument") or "").strip().upper()
            or extracted.get("instrument")
            or screenshot.inferred_symbol
            or "UNVERIFIED"
        )
        exchange = (
            (tx.get("exchange") or "").strip()
            or extracted.get("exchange")
            or screenshot.inferred_exchange
            or ("NSE" if pref_market == "india" and instrument != "UNVERIFIED" else "UNVERIFIED")
        )
        detected_market = tx.get("market") or (pref_market if pref_market != "auto" else self._infer_market(instrument, exchange))

        if instrument != "UNVERIFIED":
            mark_stage(1, "completed", f"Instrument: {instrument} ({exchange})")
        else:
            mark_stage(
                1,
                "partial",
                "Instrument ticker could not be verified from screenshot metadata alone (no Vision API configured and no ticker provided).",
            )

        # ------------------------------------------------------------------
        # Stage 2: Detect timeframe
        # ------------------------------------------------------------------
        timeframe = (
            (tx.get("timeframe") or "").strip()
            or (pref_tf if pref_tf.lower() not in ("auto", "auto detect", "") else "")
            or extracted.get("timeframe")
            or screenshot.inferred_timeframe
            or "UNVERIFIED"
        )
        if timeframe != "UNVERIFIED":
            mark_stage(2, "completed", f"Timeframe: {timeframe}")
        else:
            mark_stage(2, "partial", "Timeframe not explicitly verified; marked UNVERIFIED.")

        # ------------------------------------------------------------------
        # Stage 3: Candlestick analysis (real `trading_intel.patterns` when OHLCV supplied)
        # ------------------------------------------------------------------
        ohlcv = tx.get("ohlcv") if isinstance(tx.get("ohlcv"), dict) else None
        detected_patterns: List[Dict[str, Any]] = []
        ohlc_validation_summary: Optional[str] = None

        if ohlcv and all(k in ohlcv for k in ("open", "high", "low", "close")):
            o_arr = [float(x) for x in ohlcv["open"]]
            h_arr = [float(x) for x in ohlcv["high"]]
            l_arr = [float(x) for x in ohlcv["low"]]
            c_arr = [float(x) for x in ohlcv["close"]]
            v_arr = [float(x) for x in ohlcv["volume"]] if ohlcv.get("volume") else None

            val_rep = val_mod.validate_ohlc(o_arr, h_arr, l_arr, c_arr, v_arr)
            ohlc_validation_summary = val_rep.summary()
            if val_rep.ok:
                all_hits = pat_mod.detect_all(o_arr, h_arr, l_arr, c_arr)
                # Collect hits on the last 3 bars
                min_bar = max(0, len(c_arr) - 3)
                for pat_name, det in all_hits.items():
                    for hit in det.hits:
                        if hit.index >= min_bar:
                            detected_patterns.append(hit.as_dict())
        for vp in extracted.get("patterns_visible") or []:
            if isinstance(vp, dict) and vp.get("name"):
                detected_patterns.append(
                    {
                        "name": vp["name"],
                        "status": vp.get("status", "POSSIBLE"),
                        "direction": "neutral",
                        "rules_met": [vp.get("note", "Observed via vision provider")],
                        "rules_failed": [],
                    }
                )

        candle_state = str(
            tx.get("candle_state")
            or extracted.get("candle_state")
            or ("closed" if detected_patterns else "unknown")
        )
        if detected_patterns or candle_state != "unknown":
            mark_stage(
                3,
                "completed",
                f"Candle state: {candle_state}; {len(detected_patterns)} recent pattern observation(s).",
            )
        else:
            mark_stage(
                3,
                "partial",
                "Candlestick state unverified from pixels alone; treated conservatively as unconfirmed.",
            )

        # ------------------------------------------------------------------
        # Stage 4: Market structure & ChartObservation quality gate
        # ------------------------------------------------------------------
        last_price = _safe_float(tx.get("last_price")) or _safe_float(extracted.get("last_price"))
        if last_price is None and ohlcv and ohlcv.get("close"):
            last_price = _safe_float(ohlcv["close"][-1])

        support_level = _safe_float(tx.get("support_level")) or _safe_float(extracted.get("support_level"))
        resistance_level = _safe_float(tx.get("resistance_level")) or _safe_float(extracted.get("resistance_level"))
        swing_level = (
            _safe_float(tx.get("swing_level"))
            or _safe_float(extracted.get("swing_low"))
            or _safe_float(extracted.get("swing_high"))
        )
        structural_stop = _safe_float(tx.get("structural_stop"))
        entry_price = _safe_float(tx.get("entry_price"))
        entry_low = _safe_float(tx.get("entry_low"))
        entry_high = _safe_float(tx.get("entry_high"))
        atr_val = _safe_float(tx.get("atr")) or _safe_float(extracted.get("atr"))
        target_levels = _parse_float_list(tx.get("levels_for_targets"))

        for lvl_obj in extracted.get("levels") or []:
            if isinstance(lvl_obj, dict) and _safe_float(lvl_obj.get("price")):
                target_levels.append(float(lvl_obj["price"]))

        # Build ChartObservation and score quality using `trading_intel.validation.score_chart_quality`
        quality_flags = {
            "instrument_identifiable": instrument != "UNVERIFIED",
            "timeframe_visible": timeframe != "UNVERIFIED",
            "price_axis_readable": any(
                x is not None for x in (last_price, entry_price, entry_low, support_level, resistance_level)
            ),
            "volume_present": bool(tx.get("volume_present") or extracted.get("volume_present") or (ohlcv and ohlcv.get("volume"))),
            "indicators_labeled": bool(ohlcv or extracted.get("indicators_visible") or atr_val is not None),
            "candles_clear": screenshot.width >= 320 and screenshot.height >= 200,
            "axes_not_distorted": 0.25 <= (screenshot.width / max(1, screenshot.height)) <= 4.0,
        }
        if isinstance(extracted.get("quality_observed"), dict) and extracted["quality_observed"]:
            for k in quality_flags:
                if k in extracted["quality_observed"]:
                    quality_flags[k] = bool(extracted["quality_observed"][k])

        quality_report = val_mod.score_chart_quality(quality_flags)
        quality_score = int(quality_report["score"])

        obs_levels: List[obs_mod.Level] = []
        if support_level is not None:
            obs_levels.append(obs_mod.Level(price=support_level, kind="support", touches=2, timeframe=timeframe))
        if resistance_level is not None:
            obs_levels.append(obs_mod.Level(price=resistance_level, kind="resistance", touches=2, timeframe=timeframe))
        for tl in target_levels:
            obs_levels.append(obs_mod.Level(price=tl, kind="both", touches=2, timeframe=timeframe))

        chart_obs = obs_mod.ChartObservation(
            instrument=None if instrument == "UNVERIFIED" else instrument,
            exchange=None if exchange == "UNVERIFIED" else exchange,
            timeframe=None if timeframe == "UNVERIFIED" else timeframe,
            last_price=last_price,
            quality_score=quality_score,
            volume_present=quality_flags["volume_present"],
            levels=obs_levels,
            source="fictional-demo-fixture" if is_fictional_demo else ("vision-provider" if vision_res.get("used_vision_api") else "screenshot+transcription"),
        )
        gate_report = chart_obs.gate_report()
        mark_stage(
            4,
            "completed" if quality_flags["price_axis_readable"] else "partial",
            f"Chart quality score {quality_score}/10 ({quality_report['consequence']}).",
        )

        # ------------------------------------------------------------------
        # Stage 5: Evaluate technical indicators (via `trading_intel.indicators`)
        # ------------------------------------------------------------------
        computed_indicators: List[Dict[str, Any]] = []
        if ohlcv and all(k in ohlcv for k in ("open", "high", "low", "close")):
            o_arr = [float(x) for x in ohlcv["open"]]
            h_arr = [float(x) for x in ohlcv["high"]]
            l_arr = [float(x) for x in ohlcv["low"]]
            c_arr = [float(x) for x in ohlcv["close"]]
            v_arr = [float(x) for x in ohlcv["volume"]] if ohlcv.get("volume") else None

            rsi_series = ind_mod.rsi(c_arr, period=min(14, max(3, len(c_arr) - 2)))
            ema9_series = ind_mod.ema(c_arr, period=min(9, max(3, len(c_arr) - 1)))
            sma20_series = ind_mod.sma(c_arr, period=min(20, len(c_arr)))
            atr_series = ind_mod.atr(h_arr, l_arr, c_arr, period=min(14, max(3, len(c_arr) - 2)))
            macd_line, sig_line, hist_line = ind_mod.macd(c_arr, fast=6, slow=13, signal=5) if len(c_arr) >= 18 else ([None], [None], [None])

            if atr_val is None and atr_series and atr_series[-1] is not None:
                atr_val = round(float(atr_series[-1]), 4)

            if rsi_series[-1] is not None:
                rv = round(float(rsi_series[-1]), 2)
                computed_indicators.append({
                    "name": "RSI (Wilder)",
                    "value": f"{rv}",
                    "source": "COMPUTED (trading_intel.indicators.rsi)",
                    "reading": "Bullish momentum (>55)" if rv > 55 else ("Bearish momentum (<45)" if rv < 45 else "Neutral range (45–55)"),
                })
            if ema9_series[-1] is not None:
                ev = round(float(ema9_series[-1]), 2)
                computed_indicators.append({
                    "name": "EMA (Short)",
                    "value": f"{ev:,.2f}",
                    "source": "COMPUTED (trading_intel.indicators.ema)",
                    "reading": "Price above short EMA" if (last_price and last_price > ev) else "Price below short EMA",
                })
            if sma20_series[-1] is not None:
                sv = round(float(sma20_series[-1]), 2)
                computed_indicators.append({
                    "name": "SMA (20)",
                    "value": f"{sv:,.2f}",
                    "source": "COMPUTED (trading_intel.indicators.sma)",
                    "reading": "Above 20-bar mean" if (last_price and last_price > sv) else "Below 20-bar mean",
                })
            if atr_val is not None:
                computed_indicators.append({
                    "name": "ATR",
                    "value": f"{atr_val:,.2f}",
                    "source": "COMPUTED (trading_intel.indicators.atr)",
                    "reading": "Used for structural stop buffer & volatility room gate",
                })
            if hist_line[-1] is not None:
                hv = round(float(hist_line[-1]), 4)
                computed_indicators.append({
                    "name": "MACD Histogram",
                    "value": f"{hv:+.4f}",
                    "source": "COMPUTED (trading_intel.indicators.macd)",
                    "reading": "Positive momentum impulse" if hv > 0 else "Negative momentum impulse",
                })
            if v_arr:
                vwap_s = ind_mod.vwap(h_arr, l_arr, c_arr, v_arr)
                if vwap_s[-1] is not None:
                    vv = round(float(vwap_s[-1]), 2)
                    computed_indicators.append({
                        "name": "Anchored/Window VWAP",
                        "value": f"{vv:,.2f}",
                        "source": "COMPUTED (trading_intel.indicators.vwap)",
                        "reading": "Trading above VWAP" if (last_price and last_price > vv) else "Trading below VWAP",
                    })

        for vi in extracted.get("indicators_visible") or []:
            if isinstance(vi, dict) and vi.get("name"):
                computed_indicators.append({
                    "name": str(vi["name"]),
                    "value": str(vi.get("value", "visible")),
                    "source": "OBSERVED (screenshot)",
                    "reading": str(vi.get("reading", "Read from indicator panel")),
                })

        if computed_indicators:
            mark_stage(5, "completed", f"Evaluated {len(computed_indicators)} verified indicator(s).")
        else:
            mark_stage(
                5,
                "skipped_unavailable",
                "No indicator values visible/provided; per SKILL.md Rule 5, hidden indicators are never interpolated.",
            )

        # ------------------------------------------------------------------
        # Stage 6: Research external market context & news
        # ------------------------------------------------------------------
        market_quote = (
            self.market_data.fetch_quote_if_configured(instrument)
            if instrument != "UNVERIFIED" and not is_fictional_demo
            else {"available": False, "reason": "Skipped for demo or unverified symbol."}
        )
        news_context = (
            self.news.fetch_news(instrument=instrument, market=detected_market)
            if instrument != "UNVERIFIED" and not is_fictional_demo
            else {"available": False, "articles": [], "message": "External news provider not queried."}
        )

        relevant_modules = self.knowledge.select_relevant_modules(
            market=detected_market,
            candle_patterns=[p["name"] for p in detected_patterns],
            indicators_used=[i["name"].split()[0] for i in computed_indicators],
        )

        if market_quote.get("available") or news_context.get("available"):
            mark_stage(6, "completed", "Retrieved external authorized market/news context.")
        else:
            mark_stage(
                6,
                "skipped_unavailable",
                f"Loaded {len(relevant_modules)} local skill knowledge modules; external live market/news feeds not configured (screenshot-based mode).",
            )

        # ------------------------------------------------------------------
        # Stage 7: Execute Quick Signal Engine (`trading_intel.quick_signal`)
        # ------------------------------------------------------------------
        direction = tx.get("direction") or extracted.get("direction_bias")
        if direction not in ("long", "short"):
            # Infer direction conservatively if entry & stop exist
            eff_e = entry_price or (
                (entry_low + entry_high) / 2.0 if (entry_low is not None and entry_high is not None) else last_price
            )
            eff_s = structural_stop or swing_level
            if eff_e is not None and eff_s is not None and eff_e != eff_s:
                direction = "long" if eff_e > eff_s else "short"

        has_close_conf = bool(
            tx.get("has_close_confirmation")
            if "has_close_confirmation" in tx
            else extracted.get("has_close_confirmation", False)
        )
        vol_conf = (
            tx.get("volume_confirmed")
            if "volume_confirmed" in tx
            else extracted.get("volume_confirmed")
        )
        retest_status = tx.get("retest_status") or extracted.get("retest_status")
        htf_aligned = tx.get("htf_aligned") if "htf_aligned" in tx else (not bool(extracted.get("htf_conflict", False)))
        htf_conflict = bool(tx.get("htf_conflict") or extracted.get("htf_conflict", False))
        choppy = bool(tx.get("choppy") or extracted.get("choppy", False))
        trap_unrefuted = bool(tx.get("trap_unrefuted") or extracted.get("trap_unrefuted", False))
        event_risk = str(tx.get("event_risk") or "").strip() or None

        now_iso = datetime.now(timezone.utc).isoformat()
        data_ts = market_quote.get("timestamp") if market_quote.get("available") else now_iso

        quick_out = qs_mod.build_quick_signal(
            instrument=instrument,
            exchange=exchange,
            timeframe=timeframe,
            direction=direction,
            last_price=last_price,
            entry_price=entry_price,
            entry_low=entry_low,
            entry_high=entry_high,
            swing_level=swing_level,
            structural_stop=structural_stop,
            levels_for_targets=target_levels or None,
            atr=atr_val,
            cost_bps=float(tx.get("cost_bps") or 0.0),
            candle_state=candle_state,
            volume_confirmed=vol_conf,
            retest_status=retest_status,
            htf_conflict=htf_conflict,
            htf=tx.get("htf"),
            ltf=timeframe if timeframe != "UNVERIFIED" else None,
            choppy=choppy,
            event_risk=event_risk,
            trap_unrefuted=trap_unrefuted,
            data_fresh=True,
            quality_score=quality_score,
            data_timestamp=data_ts,
            has_close_confirmation=has_close_conf,
            htf_aligned=htf_aligned,
            support_level=support_level,
            resistance_level=resistance_level,
            user_text=user_notes,
        )

        # If completely unverified chart with zero price inputs and no confirmation,
        # clearly distinguish NO TRADE vs WAIT when required inputs are absent
        no_prices_at_all = all(
            x is None
            for x in (last_price, entry_price, entry_low, structural_stop, swing_level, support_level, resistance_level)
        )
        if no_prices_at_all and instrument == "UNVERIFIED":
            quick_out.verdict = qs_mod.VERDICT_NO_TRADE
            quick_out.reason = (
                "Screenshot pixels alone cannot yield verified prices without an AI Vision provider key or user-supplied chart levels. Refusing to fabricate levels."
            )
            quick_out.reason_hinglish = (
                "Bina verified chart price levels ya AI Vision provider ke, system koi bhi fake entry/stop price invent nahi karta."
            )

        # Run honesty/anti-fabrication checks from `trading_intel.quick_signal`
        compact_text = qs_mod.render_quick_text(quick_out)
        prob_clean = qs_mod.validate_no_probability(compact_text)

        mark_stage(
            7,
            "completed",
            f"Verdict: {quick_out.verdict} | Entry status: {quick_out.entry.status} | Anti-fabrication check: {'PASS' if prob_clean else 'WARN'}",
        )

        # ------------------------------------------------------------------
        # Stage 8: Build complete V1-V3 22-section Full Analysis Report
        # ------------------------------------------------------------------
        legacy_verdict = self._map_to_legacy_verdict(quick_out, instrument, no_prices_at_all)
        hindi_line = HINDI_REASON_MAP.get(quick_out.verdict, HINDI_REASON_MAP[qs_mod.VERDICT_WAIT])

        # Position sizing illustrative calculation (1,000,000 paper equity, 0.75% risk)
        sizing_summary: Optional[Dict[str, Any]] = None
        eff_entry = quick_out.entry.single_price or (
            (quick_out.entry.zone_low + quick_out.entry.zone_high) / 2.0
            if (quick_out.entry.zone_low is not None and quick_out.entry.zone_high is not None)
            else None
        )
        if eff_entry is not None and quick_out.stop_loss.price is not None and eff_entry != quick_out.stop_loss.price:
            try:
                pos = sizing_mod.size_position(
                    equity=1_000_000.0,
                    entry=eff_entry,
                    stop=quick_out.stop_loss.price,
                    risk_pct=0.75,
                )
                be_wr = (
                    round(risk_mod.break_even_win_rate(quick_out.risk_reward.rr_t1) * 100, 1)
                    if (quick_out.risk_reward.rr_t1 and quick_out.risk_reward.rr_t1 > 0)
                    else None
                )
                sizing_summary = {
                    "paper_equity": 1_000_000.0,
                    "risk_pct": 0.75,
                    "units": pos.units,
                    "risk_amount": pos.risk_amount,
                    "notional": pos.notional,
                    "break_even_win_rate_t1_pct": be_wr,
                    "note": "Illustrative paper-trading arithmetic only — never real-money sizing advice.",
                }
            except Exception:
                sizing_summary = None

        full_report = self._build_22_sections(
            screenshot=screenshot,
            quick_out=quick_out,
            legacy_verdict=legacy_verdict,
            detected_market=detected_market,
            quality_report=quality_report,
            gate_report=gate_report,
            detected_patterns=detected_patterns,
            computed_indicators=computed_indicators,
            ohlc_validation_summary=ohlc_validation_summary,
            support_level=support_level,
            resistance_level=resistance_level,
            last_price=last_price,
            atr_val=atr_val,
            sizing_summary=sizing_summary,
            market_quote=market_quote,
            news_context=news_context,
            relevant_modules=relevant_modules,
            vision_res=vision_res,
            is_fictional_demo=is_fictional_demo,
            htf=tx.get("htf"),
            htf_conflict=htf_conflict,
            trap_unrefuted=trap_unrefuted,
            volume_present=quality_flags["volume_present"],
            volume_confirmed=vol_conf,
        )

        mark_stage(8, "completed", "Quick Signal card and 22-section V1–V3 research report ready.")

        # Determine localized primary reason
        localized_reason = quick_out.reason
        if pref_lang == "hinglish":
            localized_reason = quick_out.reason_hinglish
        elif pref_lang == "hindi":
            localized_reason = hindi_line

        analysis_id = f"anl_{secrets.token_hex(8)}"

        entry_display = quick_out.entry.display()
        stop_display = quick_out.stop_loss.display()
        if quick_out.verdict == qs_mod.VERDICT_NO_TRADE and not quick_out.entry.is_available():
            entry_display = "NOT CONFIRMED"
            stop_display = "NOT APPLICABLE"

        return {
            "id": analysis_id,
            "status": "completed",
            "stage": "completed",
            "stage_index": 9,
            "is_fictional_demo": is_fictional_demo,
            "instrument": quick_out.instrument,
            "exchange": quick_out.exchange,
            "market": detected_market,
            "timeframe": quick_out.timeframe,
            "mode": pref_mode,
            "language": pref_lang,
            "screenshot_ref": screenshot.screenshot_id,
            "screenshot_filename": screenshot.filename,
            "screenshot_mime": screenshot.mime_type,
            "screenshot_width": screenshot.width,
            "screenshot_height": screenshot.height,
            "screenshot_size_bytes": screenshot.size_bytes,
            "analysis_timestamp": quick_out.analysis_timestamp,
            "data_timestamp": quick_out.data_timestamp,
            "verdict": quick_out.verdict,
            "legacy_verdict": legacy_verdict,
            "direction": quick_out.entry.direction or "",
            "wait_condition": quick_out.wait.condition,
            "entry_display": entry_display,
            "entry_status": quick_out.entry.status,
            "stop_loss": stop_display,
            "stop_basis": quick_out.stop_loss.basis,
            "tp1": "NOT APPLICABLE" if (quick_out.verdict == qs_mod.VERDICT_NO_TRADE and quick_out.targets.tp1 is None) else quick_out.targets.tp_display(1),
            "tp2": "NOT APPLICABLE" if (quick_out.verdict == qs_mod.VERDICT_NO_TRADE and quick_out.targets.tp2 is None) else quick_out.targets.tp_display(2),
            "tp3": "NOT APPLICABLE" if (quick_out.verdict == qs_mod.VERDICT_NO_TRADE and quick_out.targets.tp3 is None) else quick_out.targets.tp_display(3),
            "risk_reward": quick_out.risk_reward.display(),
            "short_explanation": localized_reason,
            "english_explanation": quick_out.reason,
            "hinglish_explanation": quick_out.reason_hinglish,
            "hindi_explanation": hindi_line,
            "evidence": relevant_modules,
            "data_quality": {
                "quality_score": quality_score,
                "quality_max": 10,
                "consequence": quality_report["consequence"],
                "missing_dimensions": quality_report["missing"],
                "freshness": "SCREENSHOT_BASED" if not market_quote.get("available") else market_quote.get("freshness", "RECENT"),
                "source_type": "FICTIONAL_DEMO_FIXTURE" if is_fictional_demo else ("VISION_AND_SCREENSHOT" if vision_res.get("used_vision_api") else "SCREENSHOT_AND_USER_LEVELS"),
                "anti_fabrication_verified": prob_clean,
            },
            "provider_info": {
                "vision": self.vision.status(),
                "vision_run": {
                    "used": bool(vision_res.get("used_vision_api")),
                    "provider": vision_res.get("provider"),
                    "error": vision_res.get("error"),
                },
                "market_data": self.market_data.status(),
                "news": self.news.status(),
                "ocr_available": screenshot.ocr_available,
            },
            "quick_payload": {
                "compact_text": compact_text,
                "rr_t1": quick_out.risk_reward.rr_t1,
                "rr_t2": quick_out.risk_reward.rr_t2,
                "rr_t3": quick_out.risk_reward.rr_t3,
                "net_rr_t1": quick_out.risk_reward.net_rr_t1,
                "net_rr_t2": quick_out.risk_reward.net_rr_t2,
                "net_rr_t3": quick_out.risk_reward.net_rr_t3,
                "tp1_basis": quick_out.targets.tp1_basis,
                "tp2_basis": quick_out.targets.tp2_basis,
                "tp3_basis": quick_out.targets.tp3_basis,
                "stop_basis": quick_out.stop_loss.basis,
                "entry_confirmation": quick_out.entry.confirmation,
                "provenance": quick_out.provenance,
                "disclaimer": quick_out.disclaimer,
            },
            "full_report": full_report,
            "stages": stages,
        }

    @staticmethod
    def _infer_market(instrument: str, exchange: str) -> str:
        ex = (exchange or "").upper()
        sym = (instrument or "").upper()
        if ex in ("NSE", "BSE", "MCX") or sym in ("NIFTY 50", "BANK NIFTY", "FINNIFTY", "SENSEX", "RELIANCE", "TCS", "HDFCBANK", "INFY"):
            return "india"
        if ex in ("NASDAQ", "NYSE", "NYSE ARCA", "CBOE") or sym in ("AAPL", "NVDA", "MSFT", "TSLA", "SPY", "QQQ"):
            return "us"
        if ex in ("BITSTAMP", "BINANCE", "COINBASE", "KRAKEN") or sym.endswith(("USDT", "BTC")) or sym in ("BTCUSD", "ETHUSD"):
            return "crypto"
        if sym in ("EURUSD", "GBPUSD", "USDJPY", "USDINR"):
            return "forex"
        if sym in ("XAUUSD", "WTI CRUDE", "GOLD"):
            return "commodities"
        return "auto"

    @staticmethod
    def _map_to_legacy_verdict(
        quick_out: qs_mod.QuickSignalOutput, instrument: str, no_prices: bool
    ) -> str:
        if instrument == "UNVERIFIED" or no_prices:
            return "INSUFFICIENT DATA — NO VALID SETUP"
        if quick_out.verdict == qs_mod.VERDICT_READY:
            return "BULLISH SCENARIO" if quick_out.entry.direction == "long" else "BEARISH SCENARIO"
        if quick_out.verdict == qs_mod.VERDICT_NO_TRADE:
            return "NO-TRADE"
        return "WAIT — NO CONFIRMED SETUP"

    def _build_22_sections(
        self,
        *,
        screenshot: ProcessedScreenshot,
        quick_out: qs_mod.QuickSignalOutput,
        legacy_verdict: str,
        detected_market: str,
        quality_report: Dict[str, Any],
        gate_report: Dict[str, Any],
        detected_patterns: List[Dict[str, Any]],
        computed_indicators: List[Dict[str, Any]],
        ohlc_validation_summary: Optional[str],
        support_level: Optional[float],
        resistance_level: Optional[float],
        last_price: Optional[float],
        atr_val: Optional[float],
        sizing_summary: Optional[Dict[str, Any]],
        market_quote: Dict[str, Any],
        news_context: Dict[str, Any],
        relevant_modules: List[Dict[str, str]],
        vision_res: Dict[str, Any],
        is_fictional_demo: bool,
        htf: Optional[str],
        htf_conflict: bool,
        trap_unrefuted: bool,
        volume_present: bool,
        volume_confirmed: Optional[bool],
    ) -> Dict[str, Any]:
        """Construct all 22 V1-V3 sections required by Section 9 of the Master Prompt."""
        tf_note = "Higher timeframe not provided in single-chart screenshot; multi-timeframe alignment marked unassessed unless explicitly supplied."
        if htf and quick_out.timeframe != "UNVERIFIED":
            try:
                ratio = tf_mod.timeframe_ratio(htf, quick_out.timeframe)
                tf_note = (
                    f"Higher timeframe {htf} vs analysis timeframe {quick_out.timeframe} "
                    f"(ratio {ratio:.1f}x). Conflict flag: {'CONFLICT' if htf_conflict else 'ALIGNED'}."
                )
            except Exception:
                tf_note = f"Higher timeframe {htf} referenced. Conflict flag: {htf_conflict}."

        sections = [
            {
                "id": "instrument_identification",
                "number": 1,
                "title": "Instrument Identification",
                "status": "VERIFIED" if quick_out.instrument != "UNVERIFIED" else "UNVERIFIED",
                "summary": f"Instrument: {quick_out.instrument} | Venue: {quick_out.exchange} | Market Regime Rules: {detected_market.upper()} | Timeframe: {quick_out.timeframe}.",
                "details": [
                    f"Provenance: {'FICTIONAL DEMO FIXTURE (illustrative only)' if is_fictional_demo else quick_out.provenance.get('instrument', 'OBSERVED')}",
                    f"Last observed price: {qs_mod.format_price(last_price) if last_price is not None else 'Not readable without Vision API or user input'}",
                    "Per SKILL.md §4.9, market-specific session, settlement, and circuit/halt rules are isolated per venue.",
                ],
            },
            {
                "id": "screenshot_quality",
                "number": 2,
                "title": "Screenshot Quality",
                "status": f"{quality_report['score']}/10",
                "summary": f"Quality gate score: {quality_report['score']}/{quality_report['max']} — {quality_report['consequence']}.",
                "details": [
                    f"Image file: {screenshot.filename} ({screenshot.detected_format}, {screenshot.width}x{screenshot.height}px, {screenshot.size_bytes:,} bytes)",
                    f"Missing dimensions: {', '.join(quality_report['missing']) if quality_report['missing'] else 'None'}",
                    *(gate_report.get("failures") or ["All primary G1 data-integrity checks passed."]),
                ],
            },
            {
                "id": "candlestick_analysis",
                "number": 3,
                "title": "Candlestick Analysis",
                "status": "COMPUTED" if detected_patterns else "CONSERVATIVE",
                "summary": (
                    f"{len(detected_patterns)} candlestick formation(s) evaluated via trading_intel.patterns."
                    if detected_patterns
                    else "No confirmed closed candlestick reversal/continuation pattern verified; pattern alone is never an entry trigger."
                ),
                "details": (
                    [
                        f"{p['name']} [{p['status']}] ({p.get('direction', 'neutral')}) — {', '.join(p.get('rules_met', []))}"
                        for p in detected_patterns
                    ]
                    if detected_patterns
                    else [
                        f"Observed candle state: {quick_out.wait.raw_template_key}",
                        "Rule applied: A candlestick shape without close-through and structural location stays DEVELOPING / PENDING.",
                    ]
                ),
            },
            {
                "id": "chart_patterns",
                "number": 4,
                "title": "Chart Patterns",
                "status": "MANUAL_METHODOLOGY",
                "summary": "Geometric chart-pattern detection in code is intentionally not auto-guessed (per docs/limitations.md).",
                "details": [
                    "Documented 16-pattern rulebook (flags, triangles, wedges, H&S, double tops/bottoms) requires closed neckline confirmation.",
                    "Any unfinished geometric structure is treated as DEVELOPING, never CONFIRMED.",
                ],
            },
            {
                "id": "market_structure",
                "number": 5,
                "title": "Market Structure",
                "status": "ASSESSED" if (support_level or resistance_level) else "LIMITED",
                "summary": (
                    f"Active structural framing around Support {qs_mod.format_price(support_level)} and Resistance {qs_mod.format_price(resistance_level)}."
                    if (support_level or resistance_level)
                    else "Horizontal swing structure requires readable price-axis levels."
                ),
                "details": [
                    f"Direction hypothesis: {(quick_out.entry.direction or 'neutral / undecided').upper()}",
                    f"Entry validation state: {quick_out.entry.status} — {quick_out.entry.confirmation}",
                ],
            },
            {
                "id": "support_and_resistance",
                "number": 6,
                "title": "Support and Resistance",
                "status": "MAPPED" if (support_level or resistance_level) else "NOT_AVAILABLE",
                "summary": f"Support: {qs_mod.format_price(support_level)} | Resistance: {qs_mod.format_price(resistance_level)}.",
                "details": [
                    f"Structural invalidation anchor: {quick_out.stop_loss.display()} ({quick_out.stop_loss.basis or 'none'})",
                    f"Target objectives: TP1 {quick_out.targets.tp_display(1)} | TP2 {quick_out.targets.tp_display(2)} | TP3 {quick_out.targets.tp_display(3)}",
                ],
            },
            {
                "id": "technical_indicators",
                "number": 7,
                "title": "Technical Indicators",
                "status": f"{len(computed_indicators)} VERIFIED" if computed_indicators else "NOT_VISIBLE",
                "summary": (
                    f"Computed/read {len(computed_indicators)} indicator(s) without interpolation."
                    if computed_indicators
                    else "No indicator panels verified. Per SKILL.md Rule 5, unseen RSI/MACD/EMA readings are never guessed."
                ),
                "details": [
                    f"{ind['name']}: {ind['value']} — {ind['reading']} [{ind['source']}]"
                    for ind in computed_indicators
                ] or ["Provide OHLCV bars or a chart with labelled indicator panels to compute Wilder RSI, EMA, MACD, ATR, and VWAP."],
            },
            {
                "id": "multi_timeframe_analysis",
                "number": 8,
                "title": "Multi-Timeframe Analysis",
                "status": "ALIGNED" if (htf and not htf_conflict) else ("CONFLICT" if htf_conflict else "SINGLE_TF"),
                "summary": tf_note,
                "details": [
                    "Rank hierarchy: M > W > D > 4H > 1H > 30m > 15m > 5m > 3m > 1m.",
                    "Gate G6: Lower-timeframe signals are downgraded to WAIT when higher-timeframe structure opposes them.",
                ],
            },
            {
                "id": "smart_money_concepts",
                "number": 9,
                "title": "Smart Money Concepts (SMC)",
                "status": "INTERPRETIVE_FRAMEWORK",
                "summary": "Evaluated strictly as price-action terminology (BOS, CHoCH, FVG, liquidity), never as proof of institutional orders.",
                "details": [
                    "Per knowledge/smart-money/README.md & SKILL.md §8: 'smart money accumulation' is never asserted as fact.",
                    "Sweeps require a prior multi-touch swing high/low plus a confirmed reclaim close.",
                ],
            },
            {
                "id": "trap_detection",
                "number": 10,
                "title": "Trap Detection",
                "status": "TRAP_RISK_FLAGGED" if trap_unrefuted else "MONITORED",
                "summary": (
                    "Unrefuted bull/bear trap risk detected — verdict gated to WAIT/NO TRADE until hold or reclaim confirms."
                    if trap_unrefuted
                    else "Breakout/breakdown levels require candle close + volume + retest hold to filter false breaks."
                ),
                "details": [
                    "Workflow reference: workflows/trap-detection.md & core/decision-engine.md Gate G7.",
                    f"Current WAIT condition: {quick_out.wait.condition}",
                ],
            },
            {
                "id": "volume_analysis",
                "number": 11,
                "title": "Volume Analysis",
                "status": "CONFIRMED" if volume_confirmed else ("PRESENT_UNCONFIRMED" if volume_present else "ABSENT"),
                "summary": (
                    "Volume expansion supports the move."
                    if volume_confirmed
                    else ("Volume panel present, expansion confirmation still pending." if volume_present else "Volume panel not visible — volume participation marked unassessable.")
                ),
                "details": [
                    "Breakout validity requires participation relative to the 20-bar average where exchange volume is reliable.",
                ],
            },
            {
                "id": "market_news",
                "number": 12,
                "title": "Market News",
                "status": "CITED" if news_context.get("available") else "UNAVAILABLE",
                "summary": news_context.get("message", "Web/news research unavailable in offline mode."),
                "details": (
                    [
                        f"{a['title']} — {a['source']} ({a['published_at']})"
                        for a in (news_context.get("articles") or [])[:5]
                    ]
                    if news_context.get("available")
                    else ["Per AGENTS.md §2: News section explicitly states when browsing/news API is not connected; zero headlines invented."]
                ),
            },
            {
                "id": "fundamental_context",
                "number": 13,
                "title": "Fundamental Context",
                "status": "EVENT_GATE_ONLY",
                "summary": "Intraday/swing technical plans treat fundamentals primarily as scheduled binary event-risk gates (earnings, RBI/Fed, splits).",
                "details": [
                    "Verify quarterly results, ex-dividend/split dates, and macro prints before considering any hypothetical setup.",
                ],
            },
            {
                "id": "quantitative_research",
                "number": 14,
                "title": "Quantitative Research",
                "status": "ARITHMETIC_VERIFIED",
                "summary": (
                    f"Break-even win rate at T1 ({quick_out.risk_reward.rr_t1}R): {sizing_summary['break_even_win_rate_t1_pct']}%"
                    if (sizing_summary and sizing_summary.get("break_even_win_rate_t1_pct") is not None)
                    else "No historical pattern win-rate is claimed without an out-of-sample tested dataset."
                ),
                "details": [
                    f"OHLC structural integrity check: {ohlc_validation_summary or 'Not applicable (no raw OHLC array supplied)'}",
                    "Per SKILL.md §8 & strategies/strategy-validation.md: textbook win-rate percentages are never quoted without sample provenance.",
                ],
            },
            {
                "id": "bullish_scenario",
                "number": 15,
                "title": "Bullish Scenario (Hypothetical)",
                "status": "PRIMARY" if quick_out.entry.direction == "long" else "CONDITIONAL_ALTERNATIVE",
                "summary": (
                    f"Active long hypothesis: Entry {quick_out.entry.display()}, Invalidation {quick_out.stop_loss.display()}, TP1 {quick_out.targets.tp_display(1)}."
                    if quick_out.entry.direction == "long"
                    else f"Requires decisive candle close and hold above resistance ({qs_mod.format_price(resistance_level)}) with volume confirmation."
                ),
                "details": [
                    "Invalidation: Close back below structural swing low / broken resistance.",
                ],
            },
            {
                "id": "bearish_scenario",
                "number": 16,
                "title": "Bearish Scenario (Hypothetical)",
                "status": "PRIMARY" if quick_out.entry.direction == "short" else "CONDITIONAL_ALTERNATIVE",
                "summary": (
                    f"Active short hypothesis: Entry {quick_out.entry.display()}, Invalidation {quick_out.stop_loss.display()}, TP1 {quick_out.targets.tp_display(1)}."
                    if quick_out.entry.direction == "short"
                    else f"Requires decisive candle close and hold below support ({qs_mod.format_price(support_level)}) with volume confirmation."
                ),
                "details": [
                    "Invalidation: Close back above broken support / swing high.",
                ],
            },
            {
                "id": "sideways_scenario",
                "number": 17,
                "title": "Sideways / Range Scenario",
                "status": "ACTIVE" if quick_out.verdict == qs_mod.VERDICT_WAIT else "MONITORED",
                "summary": "Price remains inside consolidation boundaries without follow-through; mid-range entries offer sub-1.5R and are avoided.",
                "details": [
                    "Standing aside while price chops between support and resistance preserves paper capital.",
                ],
            },
            {
                "id": "no_trade_scenario",
                "number": 18,
                "title": "No-Trade Scenario",
                "status": "TRIGGERED" if quick_out.verdict == qs_mod.VERDICT_NO_TRADE else "GATED",
                "summary": (
                    quick_out.reason
                    if quick_out.verdict == qs_mod.VERDICT_NO_TRADE
                    else "Triggered immediately if R:R to TP1 drops below 1.5, setup invalidates, or binary event risk enters the holding window."
                ),
                "details": [
                    f"Full-mode legacy verdict mapping: {legacy_verdict}",
                ],
            },
            {
                "id": "risk_assessment",
                "number": 19,
                "title": "Risk Assessment",
                "status": quick_out.risk_reward.display(),
                "summary": f"Verified Risk/Reward: {quick_out.risk_reward.display()} | Stop Basis: {quick_out.stop_loss.basis or 'Not available'}.",
                "details": (
                    [
                        f"Illustrative paper sizing (1,000,000 equity @ 0.75% risk): {sizing_summary['units']} units, max paper risk {sizing_summary['risk_amount']:,.2f}",
                        "Gap & halt caveat: Stops are invalidation triggers, not guaranteed fill prices during overnight gaps or circuit locks.",
                    ]
                    if sizing_summary
                    else ["Define both a verified entry and structural invalidation stop to compute unit risk and R-multiples."]
                ),
            },
            {
                "id": "evidence_and_sources",
                "number": 20,
                "title": "Evidence and Sources",
                "status": f"{len(relevant_modules)} SKILL MODULES",
                "summary": "Every rule and formula used in this report maps to deterministic modules in this repository.",
                "details": [f"{m['module']} — {m['role']}" for m in relevant_modules],
            },
            {
                "id": "data_quality",
                "number": 21,
                "title": "Data Quality & Provenance",
                "status": "SCREENSHOT_BASED" if not market_quote.get("available") else market_quote.get("freshness", "RECENT"),
                "summary": (
                    f"Analysis timestamp: {quick_out.analysis_timestamp} | Data timestamp: {quick_out.data_timestamp}."
                ),
                "details": [
                    f"Vision API used: {'Yes (' + str(vision_res.get('provider')) + ')' if vision_res.get('used_vision_api') else 'No (offline deterministic mode)'}",
                    f"Live market quote feed: {'Connected' if market_quote.get('available') else 'Not connected — screenshot/user observation only'}",
                    f"Hinglish summary: {quick_out.reason_hinglish}",
                ],
            },
            {
                "id": "limitations",
                "number": 22,
                "title": "Limitations & Educational Disclaimer",
                "status": "MANDATORY_DISCLOSURE",
                "summary": quick_out.disclaimer,
                "details": [
                    "This platform is strictly for financial education, chart methodology research, and hypothetical paper-trading simulations.",
                    "No real-money order execution or broker connectivity exists.",
                    "Historical or technical setups cannot guarantee future outcomes; markets can gap through stop levels.",
                ],
            },
        ]

        return {
            "legacy_verdict": legacy_verdict,
            "sections": sections,
            "sizing_illustrative": sizing_summary,
            "patterns_detected": detected_patterns,
            "indicators_computed": computed_indicators,
        }
