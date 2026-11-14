"""Candlestick pattern detection.

Every detector takes lists of OHLC(V) and returns a list of ``PatternHit``
(wrapped in :class:`Detection`) aligned to bar index, or ``None`` per bar.

Design rules that mirror the knowledge base:

* A pattern is only evaluated on **closed** bars.
* Every hit carries a ``status``: ``CONFIRMED`` (all rules met in context),
  ``DEVELOPING`` (shape met, waiting for the next bar), ``POSSIBLE`` (shape met
  but context weak), ``UNCLEAR``.
* No detector invents a trend requirement it cannot check. Trend context is
  supplied by :func:`classify_trend` and attached when the caller asks for it.
* Detectors never raise on short input; they return empty results.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence

STATUS_CONFIRMED = "CONFIRMED"
STATUS_DEVELOPING = "DEVELOPING"
STATUS_POSSIBLE = "POSSIBLE"
STATUS_UNCLEAR = "UNCLEAR"


@dataclass
class PatternHit:
    """One detected pattern occurrence."""

    name: str
    index: int
    status: str
    rules_met: List[str] = field(default_factory=list)
    rules_failed: List[str] = field(default_factory=list)
    direction: str = "neutral"  # "bullish" | "bearish" | "neutral"
    notes: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict[str, object]:
        return {
            "name": self.name,
            "index": self.index,
            "status": self.status,
            "direction": self.direction,
            "rules_met": list(self.rules_met),
            "rules_failed": list(self.rules_failed),
            "notes": list(self.notes),
        }


@dataclass
class Detection:
    """Container for a detector's output over a series."""

    name: str
    hits: List[PatternHit] = field(default_factory=list)

    def at(self, index: int) -> Optional[PatternHit]:
        for hit in self.hits:
            if hit.index == index:
                return hit
        return None

    @property
    def last(self) -> Optional[PatternHit]:
        return self.hits[-1] if self.hits else None

    def __len__(self) -> int:
        return len(self.hits)


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _validate(o, h, l, c, v=None) -> int:
    n = len(o)
    if not (len(h) == len(l) == len(c) == n):
        raise ValueError("open/high/low/close must be the same length")
    if v is not None and len(v) != n:
        raise ValueError("volume must match price length")
    return n


def _body(o: float, c: float) -> float:
    return abs(c - o)


def _range(h: float, l: float) -> float:
    return h - l


def _upper_shadow(o: float, h: float, c: float) -> float:
    return h - max(o, c)


def _lower_shadow(o: float, l: float, c: float) -> float:
    return min(o, c) - l


def _is_bull(o: float, c: float) -> bool:
    return c > o


def _is_bear(o: float, c: float) -> bool:
    return c < o


def _avg_range(h: Sequence[float], l: Sequence[float], i: int, lookback: int = 10) -> Optional[float]:
    start = max(0, i - lookback)
    if i - start < 3:
        return None
    rngs = [h[j] - l[j] for j in range(start, i)]
    if not rngs:
        return None
    return sum(rngs) / len(rngs)


def _avg_volume(v: Optional[Sequence[float]], i: int, lookback: int = 20) -> Optional[float]:
    if v is None or i < 2:
        return None
    start = max(0, i - lookback)
    window = [v[j] for j in range(start, i)]
    if len(window) < 3:
        return None
    return sum(window) / len(window)


def classify_trend(closes: Sequence[float], index: int, lookback: int = 20) -> str:
    """Rough prior-trend label: ``up``, ``down`` or ``flat``.

    Compares the mean of the first half of the window with the second half.
    Intended only as pattern *context*, not as a full structure analysis.
    """
    if index < lookback:
        return "unknown"
    window = list(closes[index - lookback + 1 : index + 1])
    half = lookback // 2
    first = sum(window[:half]) / half
    second = sum(window[half:]) / half
    if first == 0:
        return "flat"
    change = (second - first) / abs(first)
    if change > 0.005:
        return "up"
    if change < -0.005:
        return "down"
    return "flat"


# --------------------------------------------------------------------------
# single-candle patterns
# --------------------------------------------------------------------------
def detect_hammer(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None,
) -> Detection:
    """Hammer: small body at the top, long lower shadow, prior downtrend."""
    n = _validate(o, h, l, c, v)
    det = Detection("hammer")
    for i in range(n):
        rng = _range(h[i], l[i])
        body = _body(o[i], c[i])
        if rng <= 0:
            continue
        lower = _lower_shadow(o[i], l[i], c[i])
        upper = _upper_shadow(o[i], h[i], c[i])
        if body / rng > 0.35:
            continue
        if lower < 2.0 * body or lower / rng < 0.55:
            continue
        if upper > 0.15 * rng:
            continue
        met = [
            "body <= 35% of range",
            "lower shadow >= 2x body and >= 55% of range",
            "upper shadow <= 15% of range",
        ]
        prior = classify_trend(c, i)
        failed: List[str] = []
        if prior == "up":
            failed.append("prior trend is up (a hammer needs a decline)")
        elif prior == "unknown":
            failed.append("prior trend could not be established")
        status = STATUS_CONFIRMED if not failed else STATUS_POSSIBLE
        det.hits.append(
            PatternHit(
                "hammer", i, status, met, failed, "bullish",
                [f"prior trend: {prior}"],
            )
        )
    return det


def detect_inverted_hammer(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None,
) -> Detection:
    """Inverted hammer: small body at the bottom, long upper shadow, prior downtrend."""
    n = _validate(o, h, l, c, v)
    det = Detection("inverted_hammer")
    for i in range(n):
        rng = _range(h[i], l[i])
        body = _body(o[i], c[i])
        if rng <= 0:
            continue
        upper = _upper_shadow(o[i], h[i], c[i])
        lower = _lower_shadow(o[i], l[i], c[i])
        if body / rng > 0.35:
            continue
        if upper < 2.0 * body or upper / rng < 0.55:
            continue
        if lower > 0.15 * rng:
            continue
        prior = classify_trend(c, i)
        failed = [] if prior == "down" else [f"prior trend is {prior}, expected down"]
        met = [
            "body <= 35% of range",
            "upper shadow >= 2x body and >= 55% of range",
            "lower shadow <= 15% of range",
        ]
        det.hits.append(
            PatternHit("inverted_hammer", i,
                       STATUS_CONFIRMED if not failed else STATUS_POSSIBLE,
                       met, failed, "bullish", [f"prior trend: {prior}"])
        )
    return det


def detect_shooting_star(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None,
) -> Detection:
    """Shooting star: long upper shadow, small body, prior uptrend."""
    n = _validate(o, h, l, c, v)
    det = Detection("shooting_star")
    for i in range(n):
        rng = _range(h[i], l[i])
        body = _body(o[i], c[i])
        if rng <= 0:
            continue
        upper = _upper_shadow(o[i], h[i], c[i])
        lower = _lower_shadow(o[i], l[i], c[i])
        if body / rng > 0.35:
            continue
        if upper < 2.0 * body or upper / rng < 0.60:
            continue
        if lower > 0.12 * rng:
            continue
        prior = classify_trend(c, i)
        failed = [] if prior == "up" else [f"prior trend is {prior}, expected up"]
        met = ["body <= 35% of range", "upper shadow >= 60% of range", "lower shadow <= 12% of range"]
        det.hits.append(
            PatternHit("shooting_star", i,
                       STATUS_CONFIRMED if not failed else STATUS_POSSIBLE,
                       met, failed, "bearish", [f"prior trend: {prior}"])
        )
    return det


def detect_hanging_man(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None,
) -> Detection:
    """Hanging man: hammer shape but after an advance (bearish)."""
    base = detect_hammer(o, h, l, c, v)
    det = Detection("hanging_man")
    for hit in base.hits:
        prior = classify_trend(c, hit.index)
        if prior == "up":
            det.hits.append(
                PatternHit("hanging_man", hit.index, STATUS_CONFIRMED,
                           hit.rules_met, [], "bearish",
                           ["same shape as a hammer but in an uptrend: bearish reading"])
            )
    return det


def detect_doji(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None, max_body_ratio: float = 0.10,
) -> Detection:
    """Doji: body is at most ``max_body_ratio`` of the range."""
    n = _validate(o, h, l, c, v)
    det = Detection("doji")
    for i in range(n):
        rng = _range(h[i], l[i])
        if rng <= 0:
            continue
        if _body(o[i], c[i]) / rng <= max_body_ratio:
            det.hits.append(
                PatternHit("doji", i, STATUS_POSSIBLE,
                           [f"body <= {max_body_ratio:.0%} of range"], [], "neutral",
                           ["indecision; meaningful only at a level"])
            )
    return det


def detect_marubozu(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None, max_shadow_ratio: float = 0.05,
) -> Detection:
    """Marubozu: full body, almost no shadows."""
    n = _validate(o, h, l, c, v)
    det = Detection("marubozu")
    for i in range(n):
        rng = _range(h[i], l[i])
        if rng <= 0:
            continue
        if _body(o[i], c[i]) / rng < 1.0 - 2 * max_shadow_ratio:
            continue
        direction = "bullish" if _is_bull(o[i], c[i]) else "bearish"
        det.hits.append(
            PatternHit("marubozu", i, STATUS_CONFIRMED,
                       ["body >= 90% of range"], [], direction, [])
        )
    return det


def detect_spinning_top(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None,
) -> Detection:
    """Spinning top: small body with shadows on both sides."""
    n = _validate(o, h, l, c, v)
    det = Detection("spinning_top")
    for i in range(n):
        rng = _range(h[i], l[i])
        body = _body(o[i], c[i])
        if rng <= 0:
            continue
        upper = _upper_shadow(o[i], h[i], c[i])
        lower = _lower_shadow(o[i], l[i], c[i])
        if body / rng <= 0.30 and upper >= 0.25 * rng and lower >= 0.25 * rng:
            det.hits.append(
                PatternHit("spinning_top", i, STATUS_POSSIBLE,
                           ["small body", "shadows on both sides"], [], "neutral",
                           ["indecision; needs confirmation"])
            )
    return det


# --------------------------------------------------------------------------
# two-candle patterns
# --------------------------------------------------------------------------
def detect_bullish_engulfing(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None,
) -> Detection:
    """Bullish engulfing: bearish bar followed by a bullish bar whose body engulfs it."""
    n = _validate(o, h, l, c, v)
    det = Detection("bullish_engulfing")
    for i in range(1, n):
        if not _is_bear(o[i - 1], c[i - 1]) or not _is_bull(o[i], c[i]):
            continue
        if not (c[i] > o[i - 1] and o[i] < c[i - 1]):
            continue
        prev_body = _body(o[i - 1], c[i - 1])
        body = _body(o[i], c[i])
        met = ["prior bar bearish", "current bar bullish",
               "current body engulfs prior body"]
        failed: List[str] = []
        if body <= prev_body:
            failed.append("current body is not larger than the prior body")
        prior = classify_trend(c, i - 1)
        if prior == "up":
            failed.append("appears after an advance; not a reversal context")
        avg_r = _avg_range(h, l, i)
        if avg_r and _range(h[i], l[i]) < 0.8 * avg_r:
            failed.append("range is small relative to recent bars (weak conviction)")
        det.hits.append(
            PatternHit("bullish_engulfing", i,
                       STATUS_CONFIRMED if not failed else STATUS_POSSIBLE,
                       met, failed, "bullish", [f"prior trend: {prior}"])
        )
    return det


def detect_bearish_engulfing(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None,
) -> Detection:
    """Bearish engulfing: bullish bar followed by a bearish bar that engulfs it."""
    n = _validate(o, h, l, c, v)
    det = Detection("bearish_engulfing")
    for i in range(1, n):
        if not _is_bull(o[i - 1], c[i - 1]) or not _is_bear(o[i], c[i]):
            continue
        if not (o[i] > c[i - 1] and c[i] < o[i - 1]):
            continue
        met = ["prior bar bullish", "current bar bearish", "current body engulfs prior body"]
        failed: List[str] = []
        if _body(o[i], c[i]) <= _body(o[i - 1], c[i - 1]):
            failed.append("current body is not larger than the prior body")
        prior = classify_trend(c, i - 1)
        if prior == "down":
            failed.append("appears after a decline; not a reversal context")
        det.hits.append(
            PatternHit("bearish_engulfing", i,
                       STATUS_CONFIRMED if not failed else STATUS_POSSIBLE,
                       met, failed, "bearish", [f"prior trend: {prior}"])
        )
    return det


def detect_piercing_line(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None,
) -> Detection:
    """Piercing line: bullish bar closing above the midpoint of a prior bearish bar."""
    n = _validate(o, h, l, c, v)
    det = Detection("piercing_line")
    for i in range(1, n):
        if not _is_bear(o[i - 1], c[i - 1]) or not _is_bull(o[i], c[i]):
            continue
        mid = (o[i - 1] + c[i - 1]) / 2.0
        if not (o[i] < c[i - 1] and c[i] > mid and c[i] < o[i - 1]):
            continue
        prior = classify_trend(c, i - 1)
        failed = [] if prior == "down" else [f"prior trend is {prior}, expected down"]
        det.hits.append(
            PatternHit("piercing_line", i,
                       STATUS_CONFIRMED if not failed else STATUS_POSSIBLE,
                       ["prior bar bearish", "opens below prior close",
                        "closes above the prior body midpoint", "closes below the prior open"],
                       failed, "bullish", [f"prior trend: {prior}"])
        )
    return det


def detect_dark_cloud_cover(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None,
) -> Detection:
    """Dark cloud cover: bearish bar closing below the midpoint of a prior bullish bar."""
    n = _validate(o, h, l, c, v)
    det = Detection("dark_cloud_cover")
    for i in range(1, n):
        if not _is_bull(o[i - 1], c[i - 1]) or not _is_bear(o[i], c[i]):
            continue
        mid = (o[i - 1] + c[i - 1]) / 2.0
        if not (o[i] > c[i - 1] and c[i] < mid and c[i] > o[i - 1]):
            continue
        prior = classify_trend(c, i - 1)
        failed = [] if prior == "up" else [f"prior trend is {prior}, expected up"]
        det.hits.append(
            PatternHit("dark_cloud_cover", i,
                       STATUS_CONFIRMED if not failed else STATUS_POSSIBLE,
                       ["prior bar bullish", "opens above prior close",
                        "closes below the prior body midpoint", "closes above the prior open"],
                       failed, "bearish", [f"prior trend: {prior}"])
        )
    return det


def detect_harami(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None,
) -> Detection:
    """Harami: a small body contained inside the prior (large) body."""
    n = _validate(o, h, l, c, v)
    det = Detection("harami")
    for i in range(1, n):
        p_top, p_bot = max(o[i - 1], c[i - 1]), min(o[i - 1], c[i - 1])
        c_top, c_bot = max(o[i], c[i]), min(o[i], c[i])
        if not (c_top <= p_top and c_bot >= p_bot):
            continue
        if _body(o[i], c[i]) >= 0.6 * _body(o[i - 1], c[i - 1]):
            continue
        direction = "bullish" if _is_bear(o[i - 1], c[i - 1]) else "bearish"
        det.hits.append(
            PatternHit("harami", i, STATUS_POSSIBLE,
                       ["current body contained in prior body",
                        "current body < 60% of prior body"], [], direction, [])
        )
    return det


def detect_tweezer_top(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None, tolerance: float = 0.0015,
) -> Detection:
    """Tweezer top: two bars sharing almost the same high."""
    n = _validate(o, h, l, c, v)
    det = Detection("tweezer_top")
    for i in range(1, n):
        if h[i - 1] == 0:
            continue
        if abs(h[i] - h[i - 1]) / h[i - 1] > tolerance:
            continue
        if not (_is_bull(o[i - 1], c[i - 1]) and _is_bear(o[i], c[i])):
            continue
        prior = classify_trend(c, i - 1)
        failed = [] if prior == "up" else [f"prior trend is {prior}, expected up"]
        det.hits.append(
            PatternHit("tweezer_top", i,
                       STATUS_CONFIRMED if not failed else STATUS_POSSIBLE,
                       ["two near-identical highs", "bullish then bearish bar"],
                       failed, "bearish", [f"prior trend: {prior}"])
        )
    return det


def detect_tweezer_bottom(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None, tolerance: float = 0.0015,
) -> Detection:
    """Tweezer bottom: two bars sharing almost the same low."""
    n = _validate(o, h, l, c, v)
    det = Detection("tweezer_bottom")
    for i in range(1, n):
        if l[i - 1] == 0:
            continue
        if abs(l[i] - l[i - 1]) / l[i - 1] > tolerance:
            continue
        if not (_is_bear(o[i - 1], c[i - 1]) and _is_bull(o[i], c[i])):
            continue
        prior = classify_trend(c, i - 1)
        failed = [] if prior == "down" else [f"prior trend is {prior}, expected down"]
        det.hits.append(
            PatternHit("tweezer_bottom", i,
                       STATUS_CONFIRMED if not failed else STATUS_POSSIBLE,
                       ["two near-identical lows", "bearish then bullish bar"],
                       failed, "bullish", [f"prior trend: {prior}"])
        )
    return det


# --------------------------------------------------------------------------
# three-candle patterns
# --------------------------------------------------------------------------
def detect_morning_star(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None,
) -> Detection:
    """Morning star: bearish bar, small-bodied gap-down star, bullish close into bar 1."""
    n = _validate(o, h, l, c, v)
    det = Detection("morning_star")
    for i in range(2, n):
        a, b, d = i - 2, i - 1, i
        if not (_is_bear(o[a], c[a]) and _is_bull(o[d], c[d])):
            continue
        if _body(o[b], c[b]) > 0.35 * _body(o[a], c[a]):
            continue
        mid_a = (o[a] + c[a]) / 2.0
        if c[d] <= mid_a:
            continue
        prior = classify_trend(c, a)
        failed = [] if prior == "down" else [f"prior trend is {prior}, expected down"]
        det.hits.append(
            PatternHit("morning_star", i,
                       STATUS_CONFIRMED if not failed else STATUS_POSSIBLE,
                       ["bar 1 bearish", "bar 2 small body", "bar 3 closes above bar 1 midpoint"],
                       failed, "bullish", [f"prior trend: {prior}"])
        )
    return det


def detect_evening_star(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None,
) -> Detection:
    """Evening star: bullish bar, small-bodied star, bearish close into bar 1."""
    n = _validate(o, h, l, c, v)
    det = Detection("evening_star")
    for i in range(2, n):
        a, b, d = i - 2, i - 1, i
        if not (_is_bull(o[a], c[a]) and _is_bear(o[d], c[d])):
            continue
        if _body(o[b], c[b]) > 0.35 * _body(o[a], c[a]):
            continue
        mid_a = (o[a] + c[a]) / 2.0
        if c[d] >= mid_a:
            continue
        prior = classify_trend(c, a)
        failed = [] if prior == "up" else [f"prior trend is {prior}, expected up"]
        det.hits.append(
            PatternHit("evening_star", i,
                       STATUS_CONFIRMED if not failed else STATUS_POSSIBLE,
                       ["bar 1 bullish", "bar 2 small body", "bar 3 closes below bar 1 midpoint"],
                       failed, "bearish", [f"prior trend: {prior}"])
        )
    return det


def detect_three_white_soldiers(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None,
) -> Detection:
    """Three white soldiers: three consecutive higher bullish closes."""
    n = _validate(o, h, l, c, v)
    det = Detection("three_white_soldiers")
    for i in range(2, n):
        idx = [i - 2, i - 1, i]
        if not all(_is_bull(o[j], c[j]) for j in idx):
            continue
        if not (c[i - 1] > c[i - 2] and c[i] > c[i - 1]):
            continue
        if not (o[i - 1] > o[i - 2] and o[i] > o[i - 1]):
            continue
        if any(_upper_shadow(o[j], h[j], c[j]) > 0.35 * _body(o[j], c[j]) for j in idx):
            continue
        det.hits.append(
            PatternHit("three_white_soldiers", i, STATUS_CONFIRMED,
                       ["three bullish bars", "each close above the prior close",
                        "each open above the prior open", "small upper shadows"],
                       [], "bullish", [])
        )
    return det


def detect_three_black_crows(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None,
) -> Detection:
    """Three black crows: three consecutive lower bearish closes."""
    n = _validate(o, h, l, c, v)
    det = Detection("three_black_crows")
    for i in range(2, n):
        idx = [i - 2, i - 1, i]
        if not all(_is_bear(o[j], c[j]) for j in idx):
            continue
        if not (c[i - 1] < c[i - 2] and c[i] < c[i - 1]):
            continue
        if not (o[i - 1] < o[i - 2] and o[i] < o[i - 1]):
            continue
        if any(_lower_shadow(o[j], l[j], c[j]) > 0.35 * _body(o[j], c[j]) for j in idx):
            continue
        det.hits.append(
            PatternHit("three_black_crows", i, STATUS_CONFIRMED,
                       ["three bearish bars", "each close below the prior close",
                        "each open below the prior open", "small lower shadows"],
                       [], "bearish", [])
        )
    return det


def detect_three_inside_up(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None,
) -> Detection:
    """Three inside up: harami (bearish, bullish) then a bullish confirmation close."""
    n = _validate(o, h, l, c, v)
    det = Detection("three_inside_up")
    harami = detect_harami(o, h, l, c, v)
    for hit in harami.hits:
        i = hit.index
        if hit.direction != "bullish" or i + 1 >= n:
            continue
        if not _is_bull(o[i + 1], c[i + 1]) or c[i + 1] <= c[i]:
            continue
        det.hits.append(
            PatternHit("three_inside_up", i + 1, STATUS_CONFIRMED,
                       ["inside bar after a bearish bar", "confirmation bar closes higher"],
                       [], "bullish", [])
        )
    return det


def detect_three_inside_down(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None,
) -> Detection:
    """Three inside down: harami (bullish, bearish) then a bearish confirmation close."""
    n = _validate(o, h, l, c, v)
    det = Detection("three_inside_down")
    harami = detect_harami(o, h, l, c, v)
    for hit in harami.hits:
        i = hit.index
        if hit.direction != "bearish" or i + 1 >= n:
            continue
        if not _is_bear(o[i + 1], c[i + 1]) or c[i + 1] >= c[i]:
            continue
        det.hits.append(
            PatternHit("three_inside_down", i + 1, STATUS_CONFIRMED,
                       ["inside bar after a bullish bar", "confirmation bar closes lower"],
                       [], "bearish", [])
        )
    return det


def detect_three_outside_up(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None,
) -> Detection:
    """Three outside up: bullish engulfing plus a higher confirmation close."""
    n = _validate(o, h, l, c, v)
    det = Detection("three_outside_up")
    eng = detect_bullish_engulfing(o, h, l, c, v)
    for hit in eng.hits:
        i = hit.index
        if i + 1 >= n:
            continue
        if _is_bull(o[i + 1], c[i + 1]) and c[i + 1] > c[i]:
            det.hits.append(
                PatternHit("three_outside_up", i + 1, STATUS_CONFIRMED,
                           ["bullish engulfing", "higher confirmation close"], [], "bullish", [])
            )
    return det


def detect_three_outside_down(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None,
) -> Detection:
    """Three outside down: bearish engulfing plus a lower confirmation close."""
    n = _validate(o, h, l, c, v)
    det = Detection("three_outside_down")
    eng = detect_bearish_engulfing(o, h, l, c, v)
    for hit in eng.hits:
        i = hit.index
        if i + 1 >= n:
            continue
        if _is_bear(o[i + 1], c[i + 1]) and c[i + 1] < c[i]:
            det.hits.append(
                PatternHit("three_outside_down", i + 1, STATUS_CONFIRMED,
                           ["bearish engulfing", "lower confirmation close"], [], "bearish", [])
            )
    return det


def detect_abandoned_baby(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None,
) -> Detection:
    """Abandoned baby: doji isolated by a gap on both sides of a star."""
    n = _validate(o, h, l, c, v)
    det = Detection("abandoned_baby")
    for i in range(2, n):
        a, b, d = i - 2, i - 1, i
        rng_b = _range(h[b], l[b])
        if rng_b <= 0 or _body(o[b], c[b]) / rng_b > 0.10:
            continue
        if _is_bull(o[a], c[a]) and _is_bear(o[d], c[d]):
            if max(o[b], c[b]) < l[a] and max(o[b], c[b]) < l[d] and c[d] < (o[a] + c[a]) / 2:
                det.hits.append(
                    PatternHit("abandoned_baby", i, STATUS_CONFIRMED,
                               ["bullish bar", "gapped doji", "bearish gap-down close"],
                               [], "bearish", ["very rare: verify the gap is not a data error"])
                )
        elif _is_bear(o[a], c[a]) and _is_bull(o[d], c[d]):
            if min(o[b], c[b]) > h[a] and min(o[b], c[b]) > h[d] and c[d] > (o[a] + c[a]) / 2:
                det.hits.append(
                    PatternHit("abandoned_baby", i, STATUS_CONFIRMED,
                               ["bearish bar", "gapped doji", "bullish gap-up close"],
                               [], "bullish", ["very rare: verify the gap is not a data error"])
                )
    return det


# --------------------------------------------------------------------------
# registry
# --------------------------------------------------------------------------
DETECTORS = {
    "hammer": detect_hammer,
    "inverted_hammer": detect_inverted_hammer,
    "hanging_man": detect_hanging_man,
    "shooting_star": detect_shooting_star,
    "doji": detect_doji,
    "marubozu": detect_marubozu,
    "spinning_top": detect_spinning_top,
    "bullish_engulfing": detect_bullish_engulfing,
    "bearish_engulfing": detect_bearish_engulfing,
    "piercing_line": detect_piercing_line,
    "dark_cloud_cover": detect_dark_cloud_cover,
    "harami": detect_harami,
    "tweezer_top": detect_tweezer_top,
    "tweezer_bottom": detect_tweezer_bottom,
    "morning_star": detect_morning_star,
    "evening_star": detect_evening_star,
    "three_white_soldiers": detect_three_white_soldiers,
    "three_black_crows": detect_three_black_crows,
    "three_inside_up": detect_three_inside_up,
    "three_inside_down": detect_three_inside_down,
    "three_outside_up": detect_three_outside_up,
    "three_outside_down": detect_three_outside_down,
    "abandoned_baby": detect_abandoned_baby,
}


def detect_all(
    o: Sequence[float], h: Sequence[float], l: Sequence[float], c: Sequence[float],
    v: Optional[Sequence[float]] = None,
) -> Dict[str, Detection]:
    """Run every detector. Returns a mapping of name -> :class:`Detection`."""
    _validate(o, h, l, c, v)
    return {name: fn(o, h, l, c, v) for name, fn in DETECTORS.items()}


def hits_at(index: int, results: Dict[str, Detection]) -> List[PatternHit]:
    """All patterns whose final bar is ``index``."""
    out: List[PatternHit] = []
    for det in results.values():
        hit = det.at(index)
        if hit is not None:
            out.append(hit)
    return out
