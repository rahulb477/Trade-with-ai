"""Timeframe arithmetic: aggregation, ratio checks, alignment scoring.

Multi-timeframe alignment is a claim in every report, so it is computed here
rather than asserted. Rules follow ``workflows/multi-timeframe-analysis.md``.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

# minutes per timeframe label
TIMEFRAME_MINUTES = {
    "1m": 1, "3m": 3, "5m": 5, "15m": 15, "30m": 30,
    "1H": 60, "2H": 120, "4H": 240,
    "1D": 375,   # NSE cash session: 09:15-15:30 = 6h15m
    "1D_us": 390,
    "1W": 1875,
    "1M": 8000,
}

# ratio bands that make two timeframes meaningfully different
IDEAL_RATIO_LOW = 4.0
IDEAL_RATIO_HIGH = 6.0
ACCEPTABLE_RATIO_HIGH = 12.0


def minutes(label: str) -> int:
    if label not in TIMEFRAME_MINUTES:
        raise ValueError(f"unknown timeframe: {label}")
    return TIMEFRAME_MINUTES[label]


def ratio(lower: str, higher: str) -> float:
    """How many ``lower`` bars fit in one ``higher`` bar."""
    lo, hi = minutes(lower), minutes(higher)
    if lo <= 0:
        raise ValueError("timeframe must be positive")
    return hi / lo


def ratio_quality(lower: str, higher: str) -> str:
    """Classify the gap between two timeframes.

    ``good`` (4-6x) keeps the two views genuinely independent without being so
    far apart that they describe different market phases.
    """
    r = ratio(lower, higher)
    if IDEAL_RATIO_LOW <= r <= IDEAL_RATIO_HIGH:
        return "good"
    if r < IDEAL_RATIO_LOW:
        return "too_close" if r > 1 else "invalid"
    if r <= ACCEPTABLE_RATIO_HIGH:
        return "acceptable"
    return "too_far"


def suggest_pair(higher: str, candidates: Sequence[str]) -> Optional[str]:
    """Pick the candidate whose ratio to ``higher`` is closest to the ideal mid-point."""
    target = (IDEAL_RATIO_LOW + IDEAL_RATIO_HIGH) / 2.0
    best: Optional[Tuple[float, str]] = None
    for candidate in candidates:
        r = ratio(candidate, higher)
        if r <= 1:
            continue
        score = abs(r - target)
        if best is None or score < best[0]:
            best = (score, candidate)
    return best[1] if best else None


def aggregate(
    ohlc: Dict[str, Sequence[float]], source: str, target: str
) -> Dict[str, List[float]]:
    """Aggregate bars from a lower to a higher timeframe.

    Grouping is by fixed bar count derived from the ratio; it assumes a
    continuous session with no gaps. For intraday aggregation across a session
    boundary, group by date first (see ``aggregate_intraday_to_daily``).
    """
    r = ratio(source, target)
    if r < 2:
        raise ValueError("target timeframe must be at least 2x the source")
    factor = int(round(r))
    o, h, l, c, v = (list(ohlc[k]) for k in ("open", "high", "low", "close", "volume"))
    n = len(c)
    if not (len(o) == len(h) == len(l) == n):
        raise ValueError("OHLC series must be the same length")
    if v and len(v) != n:
        raise ValueError("volume must match price length")

    out = {"open": [], "high": [], "low": [], "close": [], "volume": []}
    for start in range(0, n - factor + 1, factor):
        end = start + factor
        out["open"].append(o[start])
        out["high"].append(max(h[start:end]))
        out["low"].append(min(l[start:end]))
        out["close"].append(c[end - 1])
        out["volume"].append(sum(v[start:end]) if v else 0.0)
    return out


def aggregate_intraday_to_daily(
    timestamps: Sequence[str],
    ohlc: Dict[str, Sequence[float]],
    volume: Optional[Sequence[float]] = None,
) -> Dict[str, List[object]]:
    """Group intraday bars into daily bars using the date part of the timestamp.

    ``timestamps`` must be ISO strings (``YYYY-MM-DDTHH:MM:SS...``) so the date
    prefix is unambiguous. This is the correct way to build daily bars from an
    intraday feed; a fixed-count aggregation would mix sessions.
    """
    o, h, l, c = (list(ohlc[k]) for k in ("open", "high", "low", "close"))
    n = len(c)
    if len(timestamps) != n:
        raise ValueError("timestamps must match the bar count")

    out: Dict[str, List[object]] = {
        "date": [], "open": [], "high": [], "low": [], "close": [], "volume": [],
    }
    current_date: Optional[str] = None
    vals = volume if volume is not None else [0.0] * n

    for i, ts in enumerate(timestamps):
        date = ts[:10]
        if date != current_date:
            out["date"].append(date)
            out["open"].append(o[i])
            out["high"].append(h[i])
            out["low"].append(l[i])
            out["close"].append(c[i])
            out["volume"].append(vals[i])
            current_date = date
        else:
            out["high"][-1] = max(out["high"][-1], h[i])   # type: ignore[type-var]
            out["low"][-1] = min(out["low"][-1], l[i])     # type: ignore[type-var]
            out["close"][-1] = c[i]
            out["volume"][-1] = out["volume"][-1] + vals[i]  # type: ignore[operator]
    return out


def alignment(trends: Dict[str, str]) -> Dict[str, object]:
    """Score a multi-timeframe trend map.

    ``trends`` maps a timeframe label to ``up`` | ``down`` | ``flat`` | ``unknown``.
    Only ``up``/``down`` count towards agreement; unknown or flat timeframes
    reduce the score and are reported explicitly, because an unseen timeframe
    is not agreement.
    """
    known = {tf: t for tf, t in trends.items() if t in ("up", "down")}
    unknown = [tf for tf, t in trends.items() if t in ("unknown", "flat")]
    if not known:
        return {
            "classification": "no_data",
            "agreement": 0.0,
            "conflicts": [],
            "unknown_timeframes": unknown,
            "note": "no timeframe produced a directional reading",
        }

    up = sum(1 for t in known.values() if t == "up")
    down = len(known) - up
    agreement = max(up, down) / len(known)
    conflicts = []
    if up and down:
        conflicts.append(
            f"{up} timeframe(s) up vs {down} down: "
            + ", ".join(f"{tf}={t}" for tf, t in sorted(known.items()))
        )

    if len(known) >= 3 and agreement == 1.0:
        classification = "fully_aligned"
    elif agreement >= 0.75:
        classification = "mostly_aligned"
    elif agreement > 0.5:
        classification = "mixed"
    elif up == down:
        classification = "conflicting"
    else:
        classification = "mixed"

    return {
        "classification": classification,
        "agreement": round(agreement, 4),
        "dominant_direction": "up" if up >= down else "down",
        "timeframes_counted": len(known),
        "conflicts": conflicts,
        "unknown_timeframes": unknown,
        "note": (
            "timeframes that were not shown are excluded, not assumed"
            if unknown else "all used timeframes produced a reading"
        ),
    }


def operating_timeframe(analysis: str, entry: str) -> Dict[str, str]:
    """Return the recommended split and a plain-language justification."""
    q = ratio_quality(entry, analysis)
    return {
        "analysis_timeframe": analysis,
        "entry_timeframe": entry,
        "ratio": f"{ratio(entry, analysis):.1f}x",
        "quality": q,
        "note": {
            "good": "clean separation: context and trigger are independent views",
            "acceptable": "usable, but the trigger may be too close to the context to add information",
            "too_close": "too close: the entry timeframe mostly repeats the analysis timeframe",
            "too_far": "too far: the timeframes describe different market phases; add an intermediate",
            "invalid": "invalid: the entry timeframe must be lower than the analysis timeframe",
        }[q],
    }
