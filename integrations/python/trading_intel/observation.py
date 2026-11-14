"""The ChartObservation object.

This is the contract between "what is visible on the chart" and "what may be
claimed in a report". Nothing downstream may reference a field that is empty
here; every empty field must be disclosed in the report's missing-data section.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence

from . import validation


@dataclass
class Level:
    """A horizontal level with its evidence."""

    price: float
    kind: str                 # "support" | "resistance" | "both"
    touches: int = 0
    approximate: bool = False
    timeframe: str = ""
    note: str = ""

    @property
    def tradable(self) -> bool:
        """Levels need at least two touches before they are worth a plan."""
        return self.touches >= 2

    def as_dict(self) -> dict:
        return {
            "price": self.price,
            "kind": self.kind,
            "touches": self.touches,
            "approximate": self.approximate,
            "timeframe": self.timeframe,
            "tradable": self.tradable,
            "note": self.note,
        }


@dataclass
class ChartObservation:
    """Everything the analyst can actually see, and nothing more."""

    instrument: Optional[str] = None
    exchange: Optional[str] = None
    timeframe: Optional[str] = None
    chart_type: str = "candlestick"
    last_price: Optional[float] = None
    quality_score: int = 0
    quality_max: int = 10
    candles_visible: Optional[int] = None
    volume_present: bool = False
    indicators_visible: List[str] = field(default_factory=list)
    drawings_visible: List[str] = field(default_factory=list)
    levels: List[Level] = field(default_factory=list)
    trend: Optional[str] = None            # "up" | "down" | "range" | "unknown"
    timeframes_seen: List[str] = field(default_factory=list)
    unreadable: List[str] = field(default_factory=list)
    absent: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    source: str = "screenshot"
    notes: List[str] = field(default_factory=list)

    # ------------------------------------------------------------------
    def consequence(self) -> str:
        """What the quality score permits."""
        return validation.score_chart_quality({})["consequence"] if self.quality_score < 0 else (
            next(
                text
                for threshold, text in validation.QUALITY_CONSEQUENCE
                if self.quality_score >= threshold
            )
        )

    def permits_precise_levels(self) -> bool:
        return self.quality_score >= 5 and self.last_price is not None

    def permits_verdict(self) -> bool:
        return self.quality_score >= 5 and self.instrument is not None

    def missing(self) -> List[str]:
        """Fields the report must disclose as missing."""
        out = list(self.absent)
        if self.instrument is None:
            out.append("instrument identity")
        if self.timeframe is None:
            out.append("timeframe")
        if self.last_price is None:
            out.append("current price / price scale")
        if not self.volume_present:
            out.append("volume")
        if not self.indicators_visible:
            out.append("indicator values")
        return sorted(set(out))

    def to_dict(self) -> dict:
        return {
            "instrument": self.instrument,
            "exchange": self.exchange,
            "timeframe": self.timeframe,
            "chart_type": self.chart_type,
            "last_price": self.last_price,
            "quality": {"score": self.quality_score, "max": self.quality_max},
            "candles_visible": self.candles_visible,
            "volume_present": self.volume_present,
            "indicators_visible": self.indicators_visible,
            "drawings_visible": self.drawings_visible,
            "levels": [l.as_dict() for l in self.levels],
            "trend": self.trend,
            "timeframes_seen": self.timeframes_seen,
            "unreadable": self.unreadable,
            "absent": self.absent,
            "assumptions": self.assumptions,
            "missing": self.missing(),
            "source": self.source,
            "notes": self.notes,
        }

    # ------------------------------------------------------------------
    def gate_report(self) -> Dict[str, object]:
        """Run the data-integrity gates that precede any verdict."""
        failures: List[str] = []
        if self.instrument is None:
            failures.append("G1: instrument unverified -> INSUFFICIENT DATA — NO VALID SETUP")
        if self.quality_score < 5:
            failures.append(
                f"G1: chart quality {self.quality_score}/10 -> verdict capped at WAIT"
            )
        if self.chart_type not in ("candlestick", "ohlc_bar"):
            failures.append(
                f"G1: chart type '{self.chart_type}' does not support candle-pattern rules"
            )
        if self.last_price is None:
            failures.append("G1: no price scale -> no numeric levels may be reported")
        return {
            "passed": not failures,
            "failures": failures,
            "permitted_verdict_cap": (
                "INSUFFICIENT DATA — NO VALID SETUP"
                if self.instrument is None
                else ("WAIT — NO CONFIRMED SETUP" if self.quality_score < 5 else None)
            ),
            "missing": self.missing(),
        }


def from_transcription(data: dict) -> ChartObservation:
    """Build an observation from a user-supplied transcription.

    The transcription template is documented in ``core/capability-detection.md``.
    Unknown keys are preserved in ``notes`` rather than discarded.
    """
    obs = ChartObservation(
        instrument=data.get("instrument"),
        exchange=data.get("exchange"),
        timeframe=data.get("timeframe"),
        chart_type=data.get("chart_type", "candlestick"),
        last_price=_maybe_float(data.get("last_price")),
        candles_visible=data.get("candles_visible"),
        volume_present=bool(data.get("volume_present", False)),
        indicators_visible=list(data.get("indicators_visible", [])),
        drawings_visible=list(data.get("drawings_visible", [])),
        trend=data.get("trend"),
        timeframes_seen=list(data.get("timeframes_seen", [])),
        unreadable=list(data.get("unreadable", [])),
        absent=list(data.get("absent", [])),
        assumptions=list(data.get("assumptions", [])),
        source="user-transcription",
    )

    for row in data.get("levels", []) or []:
        obs.levels.append(
            Level(
                price=float(row["price"]),
                kind=row.get("kind", "both"),
                touches=int(row.get("touches", 0)),
                approximate=bool(row.get("approximate", True)),
                timeframe=row.get("timeframe", obs.timeframe or ""),
                note=row.get("note", ""),
            )
        )

    quality = data.get("quality_observed")
    if isinstance(quality, dict):
        scored = validation.score_chart_quality(quality)
        obs.quality_score = int(scored["score"])
        obs.quality_max = int(scored["max"])
    else:
        obs.quality_score = int(data.get("quality_score", 0))

    known = {
        "instrument", "exchange", "timeframe", "chart_type", "last_price",
        "candles_visible", "volume_present", "indicators_visible", "drawings_visible",
        "levels", "trend", "timeframes_seen", "unreadable", "absent", "assumptions",
        "quality_observed", "quality_score",
    }
    for key, value in data.items():
        if key not in known:
            obs.notes.append(f"unmapped field '{key}': {value!r}")
    return obs


def _maybe_float(value) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def sort_levels(levels: Sequence[Level], descending: bool = True) -> List[Level]:
    """Resistance-first ordering, which is how a chart should be read top-down."""
    return sorted(levels, key=lambda l: l.price, reverse=descending)


def nearest_level(price: float, levels: Sequence[Level]) -> Optional[Level]:
    if not levels:
        return None
    return min(levels, key=lambda l: abs(l.price - price))


def distance_to_next_resistance(price: float, levels: Sequence[Level]) -> Optional[float]:
    """Absolute distance to the nearest level above ``price``."""
    above = [l.price for l in levels if l.price > price]
    return min(above) - price if above else None


def distance_in_atr(price: float, levels: Sequence[Level], atr_value: float) -> Optional[float]:
    """Room to the next resistance expressed in ATR.

    The trade-readiness gate: >=2 ATR is workable, 1-2 is marginal, <1 leaves no
    room for a target and the setup should be treated as untradeable.
    """
    if atr_value <= 0:
        raise ValueError("ATR must be positive")
    dist = distance_to_next_resistance(price, levels)
    return None if dist is None else dist / atr_value


def room_class(atr_distance: Optional[float]) -> str:
    if atr_distance is None:
        return "unknown"
    if atr_distance >= 2.0:
        return "workable"
    if atr_distance >= 1.0:
        return "marginal"
    return "untradeable"
