"""Position sizing.

Core rule from ``knowledge/risk-management/position-sizing.md``::

    units = floor(equity * risk_pct / |entry - stop|)

Units are always rounded **down** — never up — so the realised risk cannot
exceed the stated risk.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional

DEFAULT_RISK_PCT = 0.0075  # 0.75% per idea: mid-point of the 0.25-1.0% band
MAX_RISK_PCT = 0.02
MAX_NOTIONAL_FRACTION = 1.0


@dataclass
class PositionSize:
    """The output of a sizing calculation. Illustrative, never an instruction."""

    equity: float
    risk_pct: float
    entry: float
    stop: float
    units: int
    risk_per_unit: float
    risk_amount: float
    notional: float
    notional_fraction: float
    warnings: list

    def as_dict(self) -> dict:
        return {
            "equity": self.equity,
            "risk_pct": round(self.risk_pct * 100, 4),
            "entry": self.entry,
            "stop": self.stop,
            "units": self.units,
            "risk_per_unit": round(self.risk_per_unit, 4),
            "risk_amount": round(self.risk_amount, 2),
            "notional": round(self.notional, 2),
            "notional_fraction": round(self.notional_fraction, 4),
            "warnings": self.warnings,
        }


def size_position(
    equity: float,
    entry: float,
    stop: float,
    risk_pct: float = DEFAULT_RISK_PCT,
    lot_size: int = 1,
    max_notional_fraction: float = MAX_NOTIONAL_FRACTION,
) -> PositionSize:
    """Size a position from an equity base and a structural stop.

    ``lot_size`` is the minimum tradable increment (1 for equities, 50/75 for
    some index futures, 1 for most crypto pairs). Units are floored to a lot.
    """
    if equity <= 0:
        raise ValueError("equity must be positive")
    if not 0 < risk_pct <= MAX_RISK_PCT:
        raise ValueError(f"risk_pct must be in (0, {MAX_RISK_PCT}]")
    if lot_size < 1:
        raise ValueError("lot_size must be >= 1")
    dist = abs(entry - stop)
    if dist == 0:
        raise ValueError("entry and stop must differ")

    risk_amount = equity * risk_pct
    raw_units = risk_amount / dist
    lots = int(raw_units // lot_size)
    units = lots * lot_size

    warnings = []
    notional = units * entry
    notional_fraction = notional / equity if equity else 0.0

    if notional_fraction > max_notional_fraction:
        allowed_units = int((equity * max_notional_fraction) / entry // lot_size) * lot_size
        units = max(0, allowed_units)
        notional = units * entry
        notional_fraction = notional / equity if equity else 0.0
        warnings.append(
            "notional cap applied: the stop-based size exceeded "
            f"{max_notional_fraction:.0%} of equity"
        )
    if units == 0:
        warnings.append(
            "size rounds to zero: at this lot size, one unit risks more than the "
            "allowed amount. The setup is too wide for this account."
        )

    return PositionSize(
        equity=equity,
        risk_pct=risk_pct,
        entry=entry,
        stop=stop,
        units=units,
        risk_per_unit=dist,
        risk_amount=units * dist,
        notional=notional,
        notional_fraction=notional_fraction,
        warnings=warnings,
    )


def stop_from_atr(level: float, atr_value: float, direction: str = "long",
                  multiplier: float = 0.3) -> float:
    """Hybrid stop: structure +/- a fraction of ATR (default 0.3)."""
    if atr_value <= 0:
        raise ValueError("ATR must be positive")
    if direction == "long":
        return level - multiplier * atr_value
    if direction == "short":
        return level + multiplier * atr_value
    raise ValueError("direction must be 'long' or 'short'")


def stop_width_check(entry: float, stop: float, atr_value: float,
                     max_atr: float = 3.0) -> Optional[str]:
    """Return a warning string if the stop is implausibly wide relative to ATR."""
    if atr_value <= 0:
        raise ValueError("ATR must be positive")
    width = abs(entry - stop) / atr_value
    if width > max_atr:
        return (
            f"stop is {width:.1f} ATR away (limit {max_atr:.1f}) — either the stop is "
            "in the wrong place for this timeframe or the setup is not a setup"
        )
    return None


def scale_out_plan(units: int, targets: int = 3) -> list:
    """Split a position into equal parts across targets, remainder to the last."""
    if units < targets:
        raise ValueError("units must be >= number of targets")
    base = units // targets
    parts = [base] * targets
    parts[-1] += units - base * targets
    return parts


def partial_exit_r(entry: float, stop: float, targets: list, fractions: list,
                   direction: str = "long") -> float:
    """Blended R if every target is hit with the given exit fractions."""
    if len(targets) != len(fractions):
        raise ValueError("targets and fractions must align")
    total = math.fsum(fractions)
    if abs(total - 1.0) > 1e-9:
        raise ValueError("fractions must sum to 1.0")
    dist = abs(entry - stop)
    blended = 0.0
    for target, frac in zip(targets, fractions):
        move = (target - entry) if direction == "long" else (entry - target)
        blended += frac * (move / dist)
    return blended
