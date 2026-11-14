"""Data validation, freshness classification and provisioning of chart quality scores.

Mirrors ``engines/data-integrity/`` and ``data-sources/market-data.md``. Every
check returns a structured result; nothing is silently repaired.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Sequence

FRESHNESS_CLASSES = ("LIVE", "RECENT", "DELAYED", "STALE", "HISTORICAL")


@dataclass
class CheckResult:
    check: str
    passed: bool
    detail: str
    action: str = "none"


@dataclass
class ValidationReport:
    results: List[CheckResult] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(r.passed for r in self.results)

    def failures(self) -> List[CheckResult]:
        return [r for r in self.results if not r.passed]

    def summary(self) -> str:
        failed = len(self.failures())
        return f"{len(self.results) - failed}/{len(self.results)} checks passed"


def validate_ohlc(
    open_: Sequence[float],
    high: Sequence[float],
    low: Sequence[float],
    close: Sequence[float],
    volume: Optional[Sequence[float]] = None,
    timestamps: Optional[Sequence[str]] = None,
) -> ValidationReport:
    """Run the structural checks. Does not mutate the input."""
    report = ValidationReport()
    n = len(close)

    lengths = {"open": len(open_), "high": len(high), "low": len(low), "close": len(close)}
    if volume is not None:
        lengths["volume"] = len(volume)
    same = len(set(lengths.values())) == 1
    report.results.append(
        CheckResult(
            "series_lengths",
            same,
            f"lengths={lengths}",
            "reject payload" if not same else "none",
        )
    )
    if not same:
        return report

    report.results.append(
        CheckResult(
            "non_empty",
            n > 0,
            f"bars={n}",
            "reject payload" if n == 0 else "none",
        )
    )
    if n == 0:
        return report

    bad_bounds = [
        i
        for i in range(n)
        if not (high[i] >= max(open_[i], close[i]) and low[i] <= min(open_[i], close[i]) and high[i] >= low[i])
    ]
    report.results.append(
        CheckResult(
            "ohlc_bounds",
            not bad_bounds,
            f"{len(bad_bounds)} bar(s) violate high>=max(o,c) or low<=min(o,c)"
            + (f" at indices {bad_bounds[:5]}" if bad_bounds else ""),
            "reject payload" if len(bad_bounds) > max(1, n * 0.02) else "flag rows",
        )
    )

    non_positive = [i for i in range(n) if close[i] <= 0 or open_[i] <= 0]
    report.results.append(
        CheckResult(
            "positive_prices",
            not non_positive,
            f"{len(non_positive)} non-positive price(s)",
            "reject payload" if non_positive else "none",
        )
    )

    if volume is not None:
        neg = [i for i in range(n) if volume[i] < 0]
        report.results.append(
            CheckResult("non_negative_volume", not neg, f"{len(neg)} negative volume(s)",
                        "reject payload" if neg else "none")
        )

    if timestamps is not None:
        dupes = len(timestamps) - len(set(timestamps))
        ordered = all(timestamps[i] > timestamps[i - 1] for i in range(1, len(timestamps)))
        report.results.append(
            CheckResult("timestamps_unique", dupes == 0, f"{dupes} duplicate timestamp(s)",
                        "de-duplicate" if dupes else "none")
        )
        report.results.append(
            CheckResult("timestamps_ordered", ordered, "strictly increasing" if ordered else "out of order",
                        "sort and log" if not ordered else "none")
        )
        tz_ok = all(("+" in ts[10:] or ts.endswith("Z")) for ts in timestamps)
        report.results.append(
            CheckResult("timestamps_have_timezone", tz_ok,
                        "timezone present on every timestamp" if tz_ok else "timezone missing",
                        "reject payload" if not tz_ok else "none")
        )
    return report


def detect_jumps(closes: Sequence[float], atr_units: float = 8.0,
                 atr_value: float = 0.0) -> List[dict]:
    """Flag moves larger than ``atr_units`` x ATR (or 20% if no ATR given).

    A flag is not a verdict: it is a prompt to check for a split, bonus, or bad tick.
    """
    flags: List[dict] = []
    for i in range(1, len(closes)):
        prev = closes[i - 1]
        if prev <= 0:
            continue
        move = abs(closes[i] - prev)
        threshold = atr_units * atr_value if atr_value > 0 else 0.20 * prev
        if move > threshold:
            flags.append(
                {
                    "index": i,
                    "previous": prev,
                    "current": closes[i],
                    "move_pct": round(100 * (closes[i] - prev) / prev, 3),
                    "note": "check for a split/bonus or a bad tick before using this bar",
                }
            )
    return flags


def detect_gaps(timestamps: Sequence[str], expected_minutes: int) -> List[dict]:
    """Find missing bars between consecutive timestamps."""
    if expected_minutes <= 0:
        raise ValueError("expected_minutes must be positive")
    gaps: List[dict] = []
    for i in range(1, len(timestamps)):
        try:
            prev = datetime.fromisoformat(timestamps[i - 1].replace("Z", "+00:00"))
            cur = datetime.fromisoformat(timestamps[i].replace("Z", "+00:00"))
        except ValueError:
            continue
        delta = (cur - prev).total_seconds() / 60.0
        if delta > expected_minutes * 1.5:
            gaps.append(
                {
                    "index": i,
                    "between": (timestamps[i - 1], timestamps[i]),
                    "minutes": round(delta, 2),
                    "missing_bars_estimate": int(round(delta / expected_minutes)) - 1,
                }
            )
    return gaps


def freshness(as_of: datetime, data_timestamp: datetime,
              intraday: bool = True) -> Dict[str, str]:
    """Classify data age. Both arguments must be timezone-aware."""
    if as_of.tzinfo is None or data_timestamp.tzinfo is None:
        raise ValueError("timestamps must be timezone-aware")
    age = as_of - data_timestamp
    if age < timedelta(0):
        return {"class": "FUTURE", "age": str(age), "use": "reject: timestamp is in the future"}
    if intraday:
        if age <= timedelta(seconds=60):
            cls, use = "LIVE", "any claim permitted"
        elif age <= timedelta(minutes=15):
            cls, use = "RECENT", "any claim permitted; note the delay"
        elif age <= timedelta(hours=6, minutes=15):
            cls, use = "DELAYED", "label it; no 'current price' claims"
        elif age <= timedelta(days=7):
            cls, use = "STALE", "methodology only"
        else:
            cls, use = "HISTORICAL", "education only"
    else:
        if age <= timedelta(days=1):
            cls, use = "RECENT", "current for daily analysis"
        elif age <= timedelta(days=5):
            cls, use = "DELAYED", "label it"
        elif age <= timedelta(days=30):
            cls, use = "STALE", "methodology only"
        else:
            cls, use = "HISTORICAL", "education only"
    return {"class": cls, "age": str(age), "use": use}


# --------------------------------------------------------------------------
# Chart quality scoring (the 0-10 gate used by the screenshot workflow)
# --------------------------------------------------------------------------
QUALITY_DIMENSIONS = [
    ("instrument_identifiable", 2, "ticker or name is legible"),
    ("timeframe_visible", 1, "the timeframe is shown"),
    ("price_axis_readable", 2, "axis labels or a last price are readable"),
    ("volume_present", 1, "a volume panel is visible"),
    ("indicators_labeled", 1, "any indicator has a visible label/period"),
    ("candles_clear", 2, "candles are legible and not compressed"),
    ("axes_not_distorted", 1, "no obvious log/linear distortion or truncation"),
]

QUALITY_CONSEQUENCE = [
    (8, "full analysis: levels, patterns, R:R and a verdict are permitted"),
    (5, "no precise levels: qualitative structure only, verdict capped at WAIT"),
    (2, "qualitative only: describe the trend; no patterns, no numbers"),
    (0, "stop: request a better screenshot or a transcription"),
]


def score_chart_quality(observed: Dict[str, bool]) -> Dict[str, object]:
    """Score a chart from a dict of boolean observations.

    Returns the score, the maximum, the per-dimension breakdown, and the
    consequence that the report must obey.
    """
    total = 0
    maximum = 0
    breakdown = []
    for key, weight, description in QUALITY_DIMENSIONS:
        maximum += weight
        present = bool(observed.get(key, False))
        if present:
            total += weight
        breakdown.append(
            {"dimension": key, "weight": weight, "observed": present, "meaning": description}
        )
    consequence = next(text for threshold, text in QUALITY_CONSEQUENCE if total >= threshold)
    return {
        "score": total,
        "max": maximum,
        "breakdown": breakdown,
        "missing": [b["dimension"] for b in breakdown if not b["observed"]],
        "consequence": consequence,
    }


def normalise_timestamp(value: str, default_tz: str = "+00:00") -> str:
    """Return an ISO 8601 timestamp with an explicit offset."""
    if not value:
        raise ValueError("timestamp is empty")
    candidate = value.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise ValueError(f"unparseable timestamp: {value}") from exc
    if dt.tzinfo is None:
        if not default_tz.startswith(("+", "-")):
            raise ValueError("default_tz must look like '+05:30'")
        sign = 1 if default_tz[0] == "+" else -1
        hours, minutes = default_tz[1:].split(":")
        dt = dt.replace(tzinfo=timezone(sign * timedelta(hours=int(hours), minutes=int(minutes))))
    return dt.isoformat()
