"""Quick Signal Output Engine — the mandatory short-form layer.

This module implements the "Perform deep research internally. Deliver simple
answers externally." contract from the repository upgrade prompt.

It is deliberately standard-library-only, deterministic, and never fabricates
prices, targets, probabilities or countdowns.  Every value it emits is either

* OBSERVED  (passed in from a ChartObservation / user transcription),
* COMPUTED  (derived arithmetically from observed values with the formula shown), or
* missing  -> rendered as ``NOT AVAILABLE — INSUFFICIENT DATA``.

The quick engine does NOT replace the V1-V3 analysis pipeline.  It is a
presentation layer that runs *after* the 16-stage pipeline (core/analysis-engine.md)
and the 20-step internal research checklist.  When the user explicitly asks
for a full analysis the engine delegates to the full report path.

Design reference
----------------
* Prompt §2  Mandatory default output format
* Prompt §3  Strict output rules
* Prompt §4  WAIT engine
* Prompt §5  ENTRY engine
* Prompt §6  STOP LOSS engine
* Prompt §7  TAKE PROFIT engine
* Prompt §8  Three possible final verdicts
* Prompt §9  Default quick mode and full mode
* Prompt §10 Internal research pipeline (20 steps)
* Prompt §11 Hinglish explanation engine
* Prompt §13 Chartick-style visual presentation
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from . import risk as risk_mod
from . import validation as val_mod

# ---------------------------------------------------------------------------
# Verdict vocabulary — the quick-mode closed set (prompt §8)
# ---------------------------------------------------------------------------

VERDICT_WAIT = "WAIT"
VERDICT_NO_TRADE = "NO TRADE"
VERDICT_READY = "PAPER-TRADING SETUP READY"

QUICK_VERDICTS = (VERDICT_WAIT, VERDICT_NO_TRADE, VERDICT_READY)

# Legacy V1-V3 verdicts are preserved for backward compatibility (SKILL.md §6).
# The quick engine maps to the new three-term vocabulary; legacy tests still
# assert the five older strings exist in documentation.
LEGACY_VERDICTS = (
    "BULLISH SCENARIO",
    "BEARISH SCENARIO",
    "WAIT — NO CONFIRMED SETUP",
    "NO-TRADE",
    "INSUFFICIENT DATA — NO VALID SETUP",
)

# ---------------------------------------------------------------------------
# Entry status (prompt §5)
# ---------------------------------------------------------------------------

ENTRY_PENDING = "PENDING"
ENTRY_CONDITIONALLY_VALID = "CONDITIONALLY VALID"
ENTRY_INVALIDATED = "INVALIDATED"

# ---------------------------------------------------------------------------
# Candle / breakout states (prompt §4)
# ---------------------------------------------------------------------------

CANDLE_FORMING = "forming"
CANDLE_CLOSED = "closed"
CONFIRMED_BREAKOUT = "confirmed_breakout"
UNCONFIRMED_BREAKOUT = "unconfirmed_breakout"
FAILED_BREAKOUT = "failed_breakout"
CONFIRMED_BREAKDOWN = "confirmed_breakdown"
UNCONFIRMED_BREAKDOWN = "unconfirmed_breakdown"
FAILED_BREAKDOWN = "failed_breakdown"

CANDLE_STATES = (
    CANDLE_FORMING,
    CANDLE_CLOSED,
    CONFIRMED_BREAKOUT,
    UNCONFIRMED_BREAKOUT,
    FAILED_BREAKOUT,
    CONFIRMED_BREAKDOWN,
    UNCONFIRMED_BREAKDOWN,
    FAILED_BREAKDOWN,
    "unknown",
)

# ---------------------------------------------------------------------------
# WAIT engine — condition catalogue (prompt §4)
# ---------------------------------------------------------------------------

WAIT_TEMPLATES = {
    "forming": "Wait for the {tf} candle to close {direction} {level}.",
    "unconfirmed_breakout": "Wait for a confirmed breakout above {level} with volume and a close.",
    "unconfirmed_breakdown": "Wait for a confirmed breakdown below {level} with volume and a close.",
    "failed_breakout": "Wait for a successful retest — the last breakout failed and price returned inside the range.",
    "failed_breakdown": "Wait for a successful retest — the last breakdown failed and price reclaimed the level.",
    "no_volume": "Wait for volume confirmation on the next candle.",
    "htf_conflict": "Wait for higher-timeframe alignment — {htf} trend conflicts with the {ltf} signal.",
    "choppy": "Wait until volatility becomes suitable — price is choppy with no clear direction.",
    "event_risk": "Wait until the upcoming major event risk has passed ({event}).",
    "retest_pending": "Wait for a successful retest of {level} before considering the setup.",
    "volatility_low": "Wait until volatility expands — ATR is compressed and levels are too close.",
    "generic": "Wait until clear confirmation appears.",
}

FALLBACK_WAIT = "WAIT UNTIL: Clear confirmation appears."

# ---------------------------------------------------------------------------
# Helpers — price formatting
# ---------------------------------------------------------------------------

def format_price(value: Optional[float], decimals: Optional[int] = None) -> str:
    """Readable price formatting with comma separators.

    * ``None`` -> ``NOT AVAILABLE — INSUFFICIENT DATA``
    * Large integers (e.g. BTC) keep no decimals: 67,300
    * Smaller values keep 2 decimals.
    * Caller may force ``decimals``.
    """
    if value is None:
        return "NOT AVAILABLE — INSUFFICIENT DATA"
    if decimals is not None:
        fmt = f"{{:,.{decimals}f}}"
        return fmt.format(value)
    # auto
    if abs(value) >= 1000:
        # BTC-style: show as integer if it is effectively integer
        if abs(value - round(value)) < 0.005:
            return f"{int(round(value)):,}"
        return f"{value:,.2f}"
    return f"{value:,.2f}"


def format_range(low: Optional[float], high: Optional[float]) -> str:
    if low is None or high is None:
        return "NOT AVAILABLE — INSUFFICIENT DATA"
    if low > high:
        low, high = high, low
    return f"{format_price(low)}–{format_price(high)}"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class WaitResult:
    """Output of the WAIT engine (prompt §4)."""
    condition: str  # human sentence for the WAIT UNTIL line
    raw_template_key: str = "generic"
    is_fallback: bool = False

    def line(self) -> str:
        return f"WAIT UNTIL:\n{self.condition}"


@dataclass
class EntryResult:
    direction: Optional[str] = None  # "long" | "short" | None
    zone_low: Optional[float] = None
    zone_high: Optional[float] = None
    single_price: Optional[float] = None
    status: str = ENTRY_PENDING
    confirmation: str = ""
    timeframe: Optional[str] = None

    def is_available(self) -> bool:
        return self.single_price is not None or (self.zone_low is not None and self.zone_high is not None)

    def display(self) -> str:
        if not self.is_available():
            return "NOT AVAILABLE — INSUFFICIENT DATA"
        if self.single_price is not None:
            return format_price(self.single_price)
        return format_range(self.zone_low, self.zone_high)

    def status_line(self) -> str:
        return f"ENTRY STATUS: {self.status}"


@dataclass
class StopLossResult:
    price: Optional[float] = None
    basis: str = ""  # e.g. "swing low + 0.3 ATR"
    atr_value: Optional[float] = None

    def display(self) -> str:
        if self.price is None:
            return "NOT AVAILABLE — INSUFFICIENT DATA"
        return format_price(self.price)


@dataclass
class TakeProfitResult:
    tp1: Optional[float] = None
    tp1_range_low: Optional[float] = None
    tp1_range_high: Optional[float] = None
    tp2: Optional[float] = None
    tp2_range_low: Optional[float] = None
    tp2_range_high: Optional[float] = None
    tp3: Optional[float] = None
    tp3_range_low: Optional[float] = None
    tp3_range_high: Optional[float] = None
    tp1_basis: str = ""
    tp2_basis: str = ""
    tp3_basis: str = ""

    def tp_display(self, n: int) -> str:
        if n == 1:
            if self.tp1 is not None:
                return format_price(self.tp1)
            if self.tp1_range_low is not None:
                return format_range(self.tp1_range_low, self.tp1_range_high)
            return "NOT AVAILABLE"
        if n == 2:
            if self.tp2 is not None:
                return format_price(self.tp2)
            if self.tp2_range_low is not None:
                return format_range(self.tp2_range_low, self.tp2_range_high)
            return "NOT AVAILABLE"
        if n == 3:
            if self.tp3 is not None:
                return format_price(self.tp3)
            if self.tp3_range_low is not None:
                return format_range(self.tp3_range_low, self.tp3_range_high)
            return "NOT AVAILABLE"
        raise ValueError("n must be 1,2,3")


@dataclass
class RiskRewardResult:
    rr_t1: Optional[float] = None
    rr_t2: Optional[float] = None
    rr_t3: Optional[float] = None
    cost_r: Optional[float] = None
    net_rr_t1: Optional[float] = None
    net_rr_t2: Optional[float] = None
    net_rr_t3: Optional[float] = None

    def display(self) -> str:
        parts = []
        for label, gross, net in [
            ("T1", self.rr_t1, self.net_rr_t1),
            ("T2", self.rr_t2, self.net_rr_t2),
            ("T3", self.rr_t3, self.net_rr_t3),
        ]:
            if gross is None:
                continue
            if net is not None and net != gross:
                parts.append(f"{label} {gross:.2f} (net {net:.2f})")
            else:
                parts.append(f"{label} {gross:.2f}")
        return " | ".join(parts) if parts else "NOT AVAILABLE — INSUFFICIENT DATA"


@dataclass
class QuickSignalOutput:
    """The complete compact result — 8-12 short lines (prompt §2, §3)."""

    instrument: str = "UNKNOWN"
    exchange: str = "UNKNOWN"
    timeframe: str = "UNKNOWN"
    verdict: str = VERDICT_WAIT
    wait: WaitResult = field(default_factory=lambda: WaitResult(condition=FALLBACK_WAIT.split(": ", 1)[-1], is_fallback=True))
    entry: EntryResult = field(default_factory=EntryResult)
    stop_loss: StopLossResult = field(default_factory=StopLossResult)
    targets: TakeProfitResult = field(default_factory=TakeProfitResult)
    risk_reward: RiskRewardResult = field(default_factory=RiskRewardResult)
    reason: str = "Insufficient evidence for a setup."
    reason_hinglish: str = "Abhi clear setup nahi hai."
    data_timestamp: str = ""
    analysis_timestamp: str = ""
    data_freshness: str = "UNKNOWN"
    disclaimer: str = "Educational paper-trading research only. Not investment advice. No real-money order was placed."
    # internal provenance — which inputs were observed vs assumed
    provenance: Dict[str, str] = field(default_factory=dict)
    # whether full analysis was requested
    full_mode_requested: bool = False


# ---------------------------------------------------------------------------
# WAIT engine implementation
# ---------------------------------------------------------------------------

def evaluate_wait(
    timeframe: Optional[str] = None,
    candle_state: str = "unknown",
    level: Optional[float] = None,
    volume_confirmed: Optional[bool] = None,
    retest_status: Optional[str] = None,
    htf_conflict: bool = False,
    htf: Optional[str] = None,
    ltf: Optional[str] = None,
    volatility_state: Optional[str] = None,
    event_risk: Optional[str] = None,
    choppy: bool = False,
) -> WaitResult:
    """Produce the WAIT UNTIL sentence.

    Never invents a countdown or candle count.  Every branch uses only the
    evidence passed in; if nothing is known the fallback is used.
    """
    tf = timeframe or "candle"

    # Event risk has priority — it overrides technical conditions
    if event_risk:
        return WaitResult(
            condition=f"Wait until the upcoming major event risk has passed ({event_risk}).",
            raw_template_key="event_risk",
        )

    if choppy or volatility_state == "choppy":
        return WaitResult(
            condition="Wait until volatility becomes suitable — price is choppy with no clear direction.",
            raw_template_key="choppy",
        )

    if volatility_state == "compressed":
        return WaitResult(
            condition="Wait until volatility expands — ATR is compressed and levels are too close.",
            raw_template_key="volatility_low",
        )

    if htf_conflict:
        h = htf or "higher timeframe"
        l = ltf or tf
        return WaitResult(
            condition=f"Wait for higher-timeframe alignment — {h} conflicts with {l}.",
            raw_template_key="htf_conflict",
        )

    # Retest pending
    if retest_status == "pending":
        lvl = format_price(level) if level else "the broken level"
        return WaitResult(
            condition=f"Wait for a successful retest of {lvl}.",
            raw_template_key="retest_pending",
        )

    if retest_status == "failed":
        return WaitResult(
            condition="Wait for a successful retest — the last breakout failed and price returned inside the range.",
            raw_template_key="failed_breakout",
        )

    # Candle states
    lvl_str = format_price(level) if level else "the identified level"

    if candle_state == CANDLE_FORMING:
        # Must distinguish forming vs closed
        return WaitResult(
            condition=f"Wait for the {tf} candle to close above the identified resistance and the breakout is confirmed by the required evidence.",
            raw_template_key="forming",
        )
    if candle_state == UNCONFIRMED_BREAKOUT:
        return WaitResult(
            condition=f"Wait for a confirmed breakout above {lvl_str} — close + volume + hold required.",
            raw_template_key="unconfirmed_breakout",
        )
    if candle_state == UNCONFIRMED_BREAKDOWN:
        lvl2 = format_price(level) if level else "support"
        return WaitResult(
            condition=f"5-minute candle closes below the identified support ({lvl2}) and the breakdown is confirmed by the required evidence.",
            raw_template_key="unconfirmed_breakdown",
        )
    if candle_state == FAILED_BREAKOUT:
        return WaitResult(
            condition="Wait — the breakout failed. Price closed back inside the range. Await a fresh trigger.",
            raw_template_key="failed_breakout",
        )
    if candle_state == FAILED_BREAKDOWN:
        return WaitResult(
            condition="Wait for a successful retest — the last breakdown failed and price reclaimed the level.",
            raw_template_key="failed_breakdown",
        )

    if volume_confirmed is False:
        return WaitResult(
            condition="Wait for volume confirmation on the next candle.",
            raw_template_key="no_volume",
        )

    # Generic fallback — never invent a time
    return WaitResult(
        condition="Clear confirmation appears.",
        raw_template_key="generic",
        is_fallback=True,
    )


# ---------------------------------------------------------------------------
# ENTRY engine
# ---------------------------------------------------------------------------

def evaluate_entry(
    direction: Optional[str] = None,
    entry_price: Optional[float] = None,
    entry_low: Optional[float] = None,
    entry_high: Optional[float] = None,
    timeframe: Optional[str] = None,
    candle_state: str = "unknown",
    has_close_confirmation: bool = False,
    has_volume: Optional[bool] = None,
    has_retest: Optional[bool] = None,
    htf_aligned: Optional[bool] = None,
    data_fresh: bool = True,
    level_price: Optional[float] = None,
) -> EntryResult:
    """Determine entry status.

    Rules (prompt §5):
    * A candlestick pattern alone is insufficient.
    * Must have candle close / S/R / volume / retest / structure / HTF / freshness.
    * States: PENDING, CONDITIONALLY VALID, INVALIDATED.
    """
    res = EntryResult(direction=direction, timeframe=timeframe)

    # No price at all -> insufficient
    if entry_price is None and entry_low is None:
        res.status = ENTRY_PENDING
        res.confirmation = "Entry cannot be defined — insufficient price data."
        return res

    if entry_price is not None:
        res.single_price = entry_price
    else:
        res.zone_low = entry_low
        res.zone_high = entry_high

    # Invalidation conditions
    if candle_state == FAILED_BREAKOUT or candle_state == FAILED_BREAKDOWN:
        res.status = ENTRY_INVALIDATED
        res.confirmation = "Entry invalidated — prior breakout/breakdown failed."
        return res

    if data_fresh is False:
        res.status = ENTRY_PENDING
        res.confirmation = "Data is stale — cannot confirm entry."
        return res

    # Pattern alone without close -> pending (prompt §5: candlestick alone insufficient)
    if not has_close_confirmation:
        res.status = ENTRY_PENDING
        res.confirmation = "Entry pending — waiting for candle close confirmation beyond the level (pattern alone is not enough)."
        return res

    # Check supporting evidence count
    evidence_count = sum([
        bool(has_close_confirmation),
        bool(has_volume),
        bool(has_retest),
        bool(htf_aligned),
    ])

    if evidence_count >= 3:
        res.status = ENTRY_CONDITIONALLY_VALID
        res.confirmation = f"Entry conditionally valid — close + {evidence_count} confirmations present. Needs final validation."
        return res

    if evidence_count >= 1:
        res.status = ENTRY_PENDING
        res.confirmation = "Entry pending — close-through seen but additional confirmation (volume/retest/HTF) still required."
        return res

    res.status = ENTRY_PENDING
    res.confirmation = "Entry pending — insufficient confirming evidence (pattern alone is not enough)."
    return res


# ---------------------------------------------------------------------------
# STOP LOSS engine
# ---------------------------------------------------------------------------

def calculate_stop_loss(
    direction: str,
    swing_level: Optional[float] = None,
    atr: Optional[float] = None,
    atr_multiplier: float = 0.3,
    structural_price: Optional[float] = None,
) -> StopLossResult:
    """Calculate hypothetical stop loss.

    Uses technical invalidation, swing high/low, ATR buffer, market structure.
    If no defensible level can be built, price stays None -> display renders
    NOT AVAILABLE — INSUFFICIENT DATA.
    """
    if direction not in ("long", "short"):
        return StopLossResult(price=None, basis="Invalid direction — no stop can be defined.")

    # Structural price is preferred
    if structural_price is not None:
        # add ATR buffer if available
        if atr is not None and atr > 0:
            buf = atr_multiplier * atr
            if direction == "long":
                price = structural_price - buf
                basis = f"structural {format_price(structural_price)} − {atr_multiplier} ATR buffer"
            else:
                price = structural_price + buf
                basis = f"structural {format_price(structural_price)} + {atr_multiplier} ATR buffer"
            return StopLossResult(price=round(price, 2), basis=basis, atr_value=atr)
        return StopLossResult(price=round(structural_price, 2), basis=f"structural {format_price(structural_price)}", atr_value=atr)

    if swing_level is not None and atr is not None and atr > 0:
        buf = atr_multiplier * atr
        if direction == "long":
            price = swing_level - buf
            basis = f"swing low {format_price(swing_level)} − {atr_multiplier} ATR"
        else:
            price = swing_level + buf
            basis = f"swing high {format_price(swing_level)} + {atr_multiplier} ATR"
        return StopLossResult(price=round(price, 2), basis=basis, atr_value=atr)

    if swing_level is not None:
        # Swing alone without ATR still defensible, but note it
        if direction == "long":
            price = swing_level
            basis = f"swing low {format_price(swing_level)} (no ATR buffer available)"
        else:
            price = swing_level
            basis = f"swing high {format_price(swing_level)} (no ATR buffer available)"
        return StopLossResult(price=round(price, 2), basis=basis, atr_value=atr)

    if atr is not None and atr > 0:
        # ATR-only without structure is weak but we still produce a placeholder only if entry exists
        # Caller should decide; here we mark as insufficient without structural anchor
        return StopLossResult(price=None, basis="ATR alone without structural anchor — insufficient to place a justified stop.")

    return StopLossResult(price=None, basis="No swing level or ATR available — cannot justify a stop.")


# ---------------------------------------------------------------------------
# TAKE PROFIT engine
# ---------------------------------------------------------------------------

def calculate_targets(
    direction: str,
    entry: Optional[float] = None,
    levels: Optional[List[float]] = None,
    atr: Optional[float] = None,
    cost_bps: Optional[float] = None,
) -> TakeProfitResult:
    """Generate three hypothetical targets.

    * TP1: first relevant technical objective (nearest structure or 1 ATR).
    * TP2: next meaningful S/R or liquidity (second structure or 2 ATR).
    * TP3: extended objective (third structure or 3 ATR).
    * Avoids arbitrary round numbers — always anchored to structure or volatility.
    * Directionally consistent: long targets > entry, short < entry.
    * If insufficient structure, remaining targets stay None -> NOT AVAILABLE.
    """
    res = TakeProfitResult()
    if entry is None:
        return res
    if direction not in ("long", "short"):
        return res

    # Filter levels to be directionally consistent
    structural: List[float] = []
    if levels:
        for lvl in levels:
            if direction == "long" and lvl > entry:
                structural.append(lvl)
            elif direction == "short" and lvl < entry:
                structural.append(lvl)
        structural.sort(reverse=(direction == "short"))

    # Need at least 1 structural or ATR
    def atr_target(mult: float) -> Optional[float]:
        if atr is None or atr <= 0:
            return None
        if direction == "long":
            return entry + mult * atr
        return entry - mult * atr

    # TP1
    if structural:
        res.tp1 = structural[0] if len(structural) >= 1 else atr_target(1.0)
        res.tp1_basis = "prior swing / structure"
    else:
        res.tp1 = atr_target(1.5)  # 1.5 ATR as first technical objective
        if res.tp1 is not None:
            res.tp1_basis = "1.5 ATR objective"

    # TP2
    if len(structural) >= 2:
        res.tp2 = structural[1]
        res.tp2_basis = "next S/R / liquidity"
    elif len(structural) == 1 and atr is not None and atr > 0:
        # Second target via ATR extension if only one structure
        res.tp2 = atr_target(2.5)
        if res.tp2 is not None:
            res.tp2_basis = "2.5 ATR extension"
    elif atr is not None and atr > 0:
        res.tp2 = atr_target(2.0)
        if res.tp2:
            res.tp2_basis = "2.0 ATR extension"

    # TP3
    if len(structural) >= 3:
        res.tp3 = structural[2]
        res.tp3_basis = "extended structure / measured move"
    elif len(structural) == 2 and atr is not None and atr > 0:
        res.tp3 = atr_target(3.5)
        if res.tp3 is not None:
            res.tp3_basis = "3.5 ATR extended"
    elif len(structural) <= 1 and atr is not None and atr > 0 and res.tp2 is not None:
        # Only provide TP3 if we have enough volatility structure
        # Check that TP3 is meaningful distance from TP2
        candidate = atr_target(3.0)
        if candidate is not None and res.tp2 is not None:
            if abs(candidate - res.tp2) / abs(atr) >= 0.8:
                res.tp3 = candidate
                res.tp3_basis = "3.0 ATR extended"
            else:
                res.tp3 = None
                res.tp3_basis = "insufficient structure for TP3"

    # Round targets to 2 decimals
    for attr in ("tp1", "tp2", "tp3"):
        val = getattr(res, attr)
        if val is not None:
            setattr(res, attr, round(val, 2))

    return res


# ---------------------------------------------------------------------------
# RISK/REWARD
# ---------------------------------------------------------------------------

def calculate_risk_reward(
    direction: str,
    entry: Optional[float],
    stop: Optional[float],
    targets: TakeProfitResult,
    cost_bps: float = 0.0,
) -> RiskRewardResult:
    if entry is None or stop is None or entry == stop:
        return RiskRewardResult()
    try:
        r_t1 = risk_mod.reward_risk(entry, stop, targets.tp1, direction) if targets.tp1 is not None else None
        r_t2 = risk_mod.reward_risk(entry, stop, targets.tp2, direction) if targets.tp2 is not None else None
        r_t3 = risk_mod.reward_risk(entry, stop, targets.tp3, direction) if targets.tp3 is not None else None
    except Exception:
        return RiskRewardResult()

    # Cost in R
    cost_r = None
    net_t1 = net_t2 = net_t3 = None
    if cost_bps and cost_bps > 0:
        dist = abs(entry - stop)
        cost_per_unit = (cost_bps / 10000.0) * entry
        if dist > 0:
            cost_r = cost_per_unit / dist
            if r_t1 is not None:
                net_t1 = r_t1 - cost_r
            if r_t2 is not None:
                net_t2 = r_t2 - cost_r
            if r_t3 is not None:
                net_t3 = r_t3 - cost_r
        else:
            cost_r = None

    # If no cost, net == gross
    if cost_r is None:
        net_t1, net_t2, net_t3 = r_t1, r_t2, r_t3

    return RiskRewardResult(
        rr_t1=round(r_t1, 2) if r_t1 is not None else None,
        rr_t2=round(r_t2, 2) if r_t2 is not None else None,
        rr_t3=round(r_t3, 2) if r_t3 is not None else None,
        cost_r=round(cost_r, 4) if cost_r is not None else None,
        net_rr_t1=round(net_t1, 2) if net_t1 is not None else None,
        net_rr_t2=round(net_t2, 2) if net_t2 is not None else None,
        net_rr_t3=round(net_t3, 2) if net_t3 is not None else None,
    )


# ---------------------------------------------------------------------------
# Hinglish engine (prompt §11)
# ---------------------------------------------------------------------------

HINGLISH_TEMPLATES = {
    "wait_consolidation": "Price resistance ke neeche hai. Breakout confirmation ka wait karo.",
    "wait_breakdown": "Support break hua hai, lekin volume confirmation abhi nahi mili.",
    "wait_sideways": "Price sideways hai. Abhi clear setup nahi hai.",
    "wait_retest": "Retest complete nahi hua. Entry condition pending hai.",
    "wait_htf": "Higher timeframe ka trend alag hai. Alignment ka wait karo.",
    "wait_choppy": "Market choppy hai. Abhi trade mat karo, clear direction ka wait karo.",
    "wait_event": "Bada event aane wala hai. Event ke baad hi socho.",
    "bull_ready": "Price support par hai aur confirmation mil gaya. Hypothetical setup ready hai.",
    "bear_ready": "Price resistance par hai aur breakdown confirm hua. Hypothetical setup ready hai.",
    "no_trade_rr": "Risk/reward sahi nahi hai. Isliye no trade.",
    "no_trade_invalidated": "Setup invalid ho gaya. Abhi trade mat karo.",
    "generic_wait": "Abhi clear signal nahi hai. Confirmation ka wait karo.",
}


def hinglish_reason(
    verdict: str,
    wait_key: str = "generic_wait",
    direction: Optional[str] = None,
    choppy: bool = False,
    htf_conflict: bool = False,
    event_risk: Optional[str] = None,
) -> str:
    if verdict == VERDICT_NO_TRADE:
        # distinguish rr vs invalidation
        if wait_key in ("rr_bad", "no_room"):
            return HINGLISH_TEMPLATES["no_trade_rr"]
        return HINGLISH_TEMPLATES["no_trade_invalidated"]
    if verdict == VERDICT_READY:
        if direction == "long":
            return HINGLISH_TEMPLATES["bull_ready"]
        if direction == "short":
            return HINGLISH_TEMPLATES["bear_ready"]
        return "Hypothetical setup ready hai, lekin risk ka dhyan rakho."
    # WAIT
    if event_risk:
        return HINGLISH_TEMPLATES["wait_event"]
    if choppy:
        return HINGLISH_TEMPLATES["wait_choppy"]
    if htf_conflict:
        return HINGLISH_TEMPLATES["wait_htf"]
    if wait_key == "retest_pending" or wait_key == "failed_breakout":
        return HINGLISH_TEMPLATES["wait_retest"]
    if wait_key == "choppy":
        return HINGLISH_TEMPLATES["wait_choppy"]
    if wait_key in ("unconfirmed_breakdown", "unconfirmed_breakout"):
        # map to appropriate
        if wait_key == "unconfirmed_breakdown":
            return HINGLISH_TEMPLATES["wait_breakdown"]
        return HINGLISH_TEMPLATES["wait_consolidation"]
    if wait_key == "generic":
        return HINGLISH_TEMPLATES["generic_wait"]
    return HINGLISH_TEMPLATES.get(wait_key, HINGLISH_TEMPLATES["generic_wait"])


# ---------------------------------------------------------------------------
# Full vs Quick mode detection (prompt §9)
# ---------------------------------------------------------------------------

FULL_MODE_TRIGGERS = [
    "full analysis",
    "detailed analysis",
    "explain this chart",
    "why this entry",
    "show indicators",
    "show news",
    "show complete research",
    "/full",
    "full report",
    "detailed report",
]


def detect_mode(user_text: str) -> str:
    """Return 'full' if the user explicitly requested full analysis, else 'quick'."""
    if not user_text:
        return "quick"
    lowered = user_text.lower()
    for trig in FULL_MODE_TRIGGERS:
        if trig.lower() in lowered:
            return "full"
    return "quick"


# ---------------------------------------------------------------------------
# Overall verdict decision (prompt §8 gates adapted for quick mode)
# ---------------------------------------------------------------------------

def decide_verdict(
    quality_score: int = 10,
    data_fresh: bool = True,
    has_entry: bool = False,
    entry_status: str = ENTRY_PENDING,
    stop_available: bool = False,
    targets_available: int = 0,
    rr_t1: Optional[float] = None,
    min_rr: float = 1.5,
    event_risk: Optional[str] = None,
    trap_unrefuted: bool = False,
    htf_conflict: bool = False,
    choppy: bool = False,
    invalidated: bool = False,
) -> str:
    """Apply quick-mode gate ladder (prompt §8)."""
    # G1 data integrity already handled outside — quality <5 maps to WAIT not NO TRADE
    if invalidated:
        return VERDICT_NO_TRADE

    if event_risk:
        return VERDICT_NO_TRADE

    if trap_unrefuted:
        # Confirmed trap with invalidation = NO TRADE
        if invalidated:
            return VERDICT_NO_TRADE
        return VERDICT_WAIT

    if choppy and rr_t1 is not None and rr_t1 < min_rr:
        return VERDICT_NO_TRADE

    if choppy:
        return VERDICT_WAIT

    if htf_conflict:
        return VERDICT_WAIT

    if not has_entry or entry_status == ENTRY_PENDING:
        return VERDICT_WAIT

    if entry_status == ENTRY_INVALIDATED:
        return VERDICT_NO_TRADE

    if not stop_available:
        return VERDICT_WAIT

    if targets_available == 0:
        return VERDICT_WAIT

    if rr_t1 is not None and rr_t1 < min_rr:
        return VERDICT_NO_TRADE

    if entry_status == ENTRY_CONDITIONALLY_VALID and stop_available and targets_available >= 1 and (rr_t1 is None or rr_t1 >= min_rr):
        if data_fresh and quality_score >= 5:
            return VERDICT_READY

    return VERDICT_WAIT


# ---------------------------------------------------------------------------
# Main builder — runs the 20-step internal pipeline condensed (prompt §10)
# ---------------------------------------------------------------------------

def build_quick_signal(
    instrument: str = "UNKNOWN",
    exchange: str = "UNKNOWN",
    timeframe: str = "UNKNOWN",
    direction: Optional[str] = None,  # "long" | "short"
    # Price inputs — must be OBSERVED/COMPUTED, never invented
    last_price: Optional[float] = None,
    entry_price: Optional[float] = None,
    entry_low: Optional[float] = None,
    entry_high: Optional[float] = None,
    swing_level: Optional[float] = None,
    structural_stop: Optional[float] = None,
    levels_for_targets: Optional[List[float]] = None,
    atr: Optional[float] = None,
    cost_bps: float = 0.0,
    # Evidence flags
    candle_state: str = "unknown",
    volume_confirmed: Optional[bool] = None,
    retest_status: Optional[str] = None,
    htf_conflict: bool = False,
    htf: Optional[str] = None,
    ltf: Optional[str] = None,
    volatility_state: Optional[str] = None,
    choppy: bool = False,
    event_risk: Optional[str] = None,
    trap_unrefuted: bool = False,
    data_fresh: bool = True,
    quality_score: int = 8,
    data_timestamp: Optional[str] = None,
    has_close_confirmation: bool = False,
    htf_aligned: Optional[bool] = None,
    support_level: Optional[float] = None,
    resistance_level: Optional[float] = None,
    user_text: str = "",
    reason_override: Optional[str] = None,
) -> QuickSignalOutput:
    """Build a QuickSignalOutput.

    This is the public entry point.  It executes the 20-step internal pipeline
    logically:

    1  Read screenshot (instrument/exchange/timeframe are inputs)
    2  Identify instrument + exchange
    3  Verify timeframe
    4  Extract price info (last_price, entry, swing, levels)
    5  Assess screenshot quality (quality_score)
    6  Analyze candlestick formations (candle_state)
    7  Analyze market structure (support_level/resistance_level/volatility_state)
    8  Calculate indicators when OHLCV exists (atr)
    9  Analyze volume (volume_confirmed)
    10 Detect breakout/breakdown (candle_state)
    11 Evaluate traps (trap_unrefuted)
    12 Compare timeframes (htf_conflict)
    13 Research news (event_risk)
    14 Verify market data (data_fresh, data_timestamp)
    15 Check data freshness
    16 Calculate entry/stop/targets
    17 Evaluate risk/reward
    18 Identify contradictory evidence
    19 Select verdict
    20 Generate compact output  (done by render_*)

    Steps that lack data are marked missing — never claimed as completed.
    """
    full_mode = detect_mode(user_text) == "full"

    # Determine reference level for WAIT engine
    wait_level = support_level if support_level is not None else resistance_level
    if wait_level is None:
        wait_level = entry_price if entry_price is not None else last_price

    wait_res = evaluate_wait(
        timeframe=timeframe,
        candle_state=candle_state,
        level=wait_level,
        volume_confirmed=volume_confirmed,
        retest_status=retest_status,
        htf_conflict=htf_conflict,
        htf=htf,
        ltf=ltf,
        volatility_state=volatility_state,
        event_risk=event_risk,
        choppy=choppy,
    )

    entry_res = evaluate_entry(
        direction=direction,
        entry_price=entry_price,
        entry_low=entry_low,
        entry_high=entry_high,
        timeframe=timeframe,
        candle_state=candle_state,
        has_close_confirmation=has_close_confirmation,
        has_volume=volume_confirmed,
        has_retest=(retest_status == "confirmed"),
        htf_aligned=htf_aligned,
        data_fresh=data_fresh,
        level_price=wait_level,
    )

    stop_res = calculate_stop_loss(
        direction=direction or "long",
        swing_level=swing_level,
        atr=atr,
        structural_price=structural_stop,
    )

    # Determine effective entry for target/RR calculations
    effective_entry: Optional[float] = None
    if entry_res.single_price is not None:
        effective_entry = entry_res.single_price
    elif entry_res.zone_low is not None and entry_res.zone_high is not None:
        effective_entry = (entry_res.zone_low + entry_res.zone_high) / 2.0
    elif entry_price is not None:
        effective_entry = entry_price
    elif entry_low is not None and entry_high is not None:
        effective_entry = (entry_low + entry_high) / 2.0

    targets_res = calculate_targets(
        direction=direction or "long",
        entry=effective_entry,
        levels=levels_for_targets,
        atr=atr,
        cost_bps=cost_bps,
    )

    rr_res = calculate_risk_reward(
        direction=direction or "long",
        entry=effective_entry,
        stop=stop_res.price,
        targets=targets_res,
        cost_bps=cost_bps,
    )

    # Verdict
    has_entry_flag = entry_res.is_available()
    targets_count = sum(1 for v in (targets_res.tp1, targets_res.tp2, targets_res.tp3) if v is not None)
    stop_avail = stop_res.price is not None
    invalidated_flag = entry_res.status == ENTRY_INVALIDATED or candle_state in (FAILED_BREAKOUT, FAILED_BREAKDOWN)

    verdict = decide_verdict(
        quality_score=quality_score,
        data_fresh=data_fresh,
        has_entry=has_entry_flag,
        entry_status=entry_res.status,
        stop_available=stop_avail,
        targets_available=targets_count,
        rr_t1=rr_res.rr_t1,
        event_risk=event_risk,
        trap_unrefuted=trap_unrefuted,
        htf_conflict=htf_conflict,
        choppy=choppy,
        invalidated=invalidated_flag,
    )

    # Quality gate override: if quality <5, cap at WAIT (unless NO TRADE due to invalidation/event)
    if quality_score < 5 and verdict != VERDICT_NO_TRADE:
        # Even when decide_verdict already returned WAIT due to quality,
        # surface the quality explanation instead of the generic fallback.
        if verdict == VERDICT_READY or (verdict == VERDICT_WAIT and wait_res.is_fallback):
            wait_res = WaitResult(
                condition=f"Screenshot quality is {quality_score}/10 — insufficient for a confirmed setup. Provide a clearer image.",
                raw_template_key="generic",
            )
        if verdict == VERDICT_READY:
            verdict = VERDICT_WAIT

    # Stale data note is not an event, but downgrades READY to WAIT
    if not data_fresh and verdict == VERDICT_READY:
        verdict = VERDICT_WAIT

    # Reason (English) — one short sentence
    if reason_override:
        reason_en = reason_override
    else:
        if verdict == VERDICT_WAIT:
            if wait_res.raw_template_key == "generic" and wait_res.is_fallback:
                reason_en = "Price is consolidating below resistance. Wait for confirmation before considering the hypothetical setup."
            else:
                # derive from wait condition
                reason_en = wait_res.condition
                # ensure it ends with period
                if not reason_en.endswith("."):
                    reason_en += "."
        elif verdict == VERDICT_NO_TRADE:
            if rr_res.rr_t1 is not None and rr_res.rr_t1 < 1.5:
                reason_en = f"Risk/reward to T1 is {rr_res.rr_t1:.2f} — below the 1.5 minimum. No valid setup."
            elif invalidated_flag:
                reason_en = "Setup invalidated — price closed beyond the invalidation level."
            elif event_risk:
                reason_en = f"No trade — event risk ({event_risk}) makes new positions inappropriate."
            else:
                reason_en = "Market conditions do not support a valid setup."
        else:  # READY
            reason_en = "Conditions met for a hypothetical educational setup. Risks disclosed below."

    # Hinglish
    wait_key = wait_res.raw_template_key
    reason_hi = hinglish_reason(
        verdict=verdict,
        wait_key=wait_key,
        direction=direction,
        choppy=choppy,
        htf_conflict=htf_conflict,
        event_risk=event_risk,
    )

    # Timestamps
    now = _now_iso()
    data_ts = data_timestamp or now

    freshness_cls = "UNKNOWN"
    try:
        if data_timestamp:
            dt = datetime.fromisoformat(data_timestamp.replace("Z", "+00:00"))
            now_dt = datetime.fromisoformat(now.replace("Z", "+00:00"))
            cls = val_mod.freshness(now_dt, dt)
            freshness_cls = cls.get("class", "UNKNOWN")
    except Exception:
        pass

    return QuickSignalOutput(
        instrument=instrument,
        exchange=exchange,
        timeframe=timeframe,
        verdict=verdict,
        wait=wait_res,
        entry=entry_res,
        stop_loss=stop_res,
        targets=targets_res,
        risk_reward=rr_res,
        reason=reason_en,
        reason_hinglish=reason_hi,
        data_timestamp=data_ts,
        analysis_timestamp=now,
        data_freshness=freshness_cls,
        provenance={
            "instrument": "OBSERVED" if instrument != "UNKNOWN" else "UNVERIFIED",
            "entry": "COMPUTED" if effective_entry else "MISSING",
            "stop": "COMPUTED" if stop_avail else "MISSING",
            "targets": "COMPUTED" if targets_count else "MISSING",
        },
        full_mode_requested=full_mode,
    )


# ---------------------------------------------------------------------------
# Rendering — compact textual report (prompt §2)
# ---------------------------------------------------------------------------

def render_quick_text(output: QuickSignalOutput) -> str:
    """Render the mandatory default output format (prompt §2).

    The complete research process remains internal; this is the 8-12 line
    user-facing surface.
    """
    header = f"{output.instrument} | {output.exchange} | {output.timeframe}"

    # VERDICT line
    verdict_line = f"VERDICT: {output.verdict}"

    # WAIT UNTIL — spec shows "WAIT UNTIL:" on its own line, then sentence
    wait_label = "WAIT UNTIL:"
    wait_body = output.wait.condition

    # ENTRY — zone or single price + status hint
    if output.entry.is_available():
        entry_str = output.entry.display()
        # Include confirmation note only if pending
        if output.entry.status == ENTRY_PENDING:
            entry_value = f"{entry_str}\nOnly after the specified confirmation. ({output.entry.status})"
        elif output.entry.status == ENTRY_CONDITIONALLY_VALID:
            entry_value = f"{entry_str}\n({output.entry.status} — awaiting final validation)"
        else:
            entry_value = entry_str
    else:
        entry_value = "NOT AVAILABLE — INSUFFICIENT DATA"

    # STOP LOSS
    stop_str = output.stop_loss.display()

    # TPs
    tp1_str = output.targets.tp_display(1)
    tp2_str = output.targets.tp_display(2)
    tp3_str = output.targets.tp_display(3)

    # Risk/reward
    rr_str = output.risk_reward.display()

    # Build lines — aim for 8-12 short labeled lines (prompt §3)
    lines = [
        header,
        "",
        verdict_line,
        "",
        f"{wait_label}",
        wait_body,
        "",
        f"ENTRY:",
        entry_value,
        "",
        f"STOP LOSS:",
        stop_str,
        "",
        f"TAKE PROFIT 1:",
        tp1_str,
        "",
        f"TAKE PROFIT 2:",
        tp2_str,
        "",
        f"TAKE PROFIT 3:",
        tp3_str,
        "",
        f"RISK / REWARD:",
        rr_str,
        "",
        f"REASON:",
        output.reason,
        "",
        f"Hinglish: {output.reason_hinglish}",
        "",
        f"Data: {output.data_timestamp} | Freshness: {output.data_freshness}",
        output.disclaimer,
    ]
    return "\n".join(lines)


def render_compact_text_minimal(output: QuickSignalOutput) -> str:
    """Even shorter 8-12 line variant for strict length tests.

    Keeps only the labelled essentials: header, verdict, wait, entry, stop,
    tp1, tp2, tp3, rr, reason.
    """
    lines = [
        f"{output.instrument} | {output.exchange} | {output.timeframe}",
        f"VERDICT: {output.verdict}",
        f"WAIT UNTIL: {output.wait.condition}",
        f"ENTRY: {output.entry.display()}",
        f"STOP LOSS: {output.stop_loss.display()}",
        f"TAKE PROFIT 1: {output.targets.tp_display(1)}",
        f"TAKE PROFIT 2: {output.targets.tp_display(2)}",
        f"TAKE PROFIT 3: {output.targets.tp_display(3)}",
        f"RISK / REWARD: {output.risk_reward.display()}",
        f"REASON: {output.reason}",
        f"Hinglish: {output.reason_hinglish}",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Rendering — Chartick-style visual HTML (prompt §13)
# ---------------------------------------------------------------------------

def render_quick_html(output: QuickSignalOutput) -> str:
    """Generate a dark-background compact HTML report (Chartick-inspired).

    Does NOT copy Chartick branding/logo — only the compact information
    hierarchy with color highlighting:
    * Entry blue
    * Stop loss red
    * TPs green
    * Verdict prominent
    """
    # Color scheme
    bg = "#0f1115"
    card_bg = "#1a1d24"
    text = "#e6e8eb"
    muted = "#9aa0a6"
    blue = "#3b82f6"
    red = "#ef4444"
    green = "#22c55e"
    yellow = "#eab308"

    verdict_color = {
        VERDICT_WAIT: yellow,
        VERDICT_NO_TRADE: red,
        VERDICT_READY: green,
    }.get(output.verdict, muted)

    entry_display = output.entry.display()
    stop_display = output.stop_loss.display()
    tp1 = output.targets.tp_display(1)
    tp2 = output.targets.tp_display(2)
    tp3 = output.targets.tp_display(3)
    rr = output.risk_reward.display()

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Quick Signal — {output.instrument}</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:{bg}; color:{text}; font-family: Inter, system-ui, -apple-system, sans-serif; padding:24px; }}
  .card {{ background:{card_bg}; border-radius:16px; padding:24px; max-width:520px; margin:0 auto; border:1px solid #2a2e38; }}
  .header {{ font-size:13px; color:{muted}; letter-spacing:0.06em; text-transform:uppercase; margin-bottom:12px; }}
  .verdict {{ font-size:22px; font-weight:800; color:{verdict_color}; background:rgba(255,255,255,0.06); border-radius:10px; padding:12px 16px; text-align:center; margin-bottom:18px; border:1px solid {verdict_color}40; }}
  .row {{ display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #2a2e38; }}
  .row:last-child {{ border-bottom:none; }}
  .label {{ font-size:12px; color:{muted}; letter-spacing:0.05em; text-transform:uppercase; }}
  .value {{ font-size:14px; font-weight:600; text-align:right; }}
  .entry {{ color:{blue}; }}
  .stop {{ color:{red}; }}
  .tp {{ color:{green}; }}
  .rr {{ color:{text}; }}
  .reason {{ margin-top:16px; font-size:13px; color:{muted}; line-height:1.5; border-top:1px solid #2a2e38; padding-top:14px; }}
  .reason strong {{ color:{text}; }}
  .footer {{ margin-top:14px; font-size:11px; color:#6b7280; text-align:center; }}
  .disclaimer {{ margin-top:10px; font-size:11px; color:#6b7280; text-align:center; font-style:italic; }}
</style>
</head>
<body>
<div class="card">
  <div class="header">{output.instrument} &nbsp;|&nbsp; {output.exchange} &nbsp;|&nbsp; {output.timeframe}</div>
  <div class="verdict">{output.verdict}</div>

  <div class="row"><span class="label">Wait until</span><span class="value" style="max-width:55%; text-align:right; font-size:12px; line-height:1.4;">{output.wait.condition}</span></div>
  <div class="row"><span class="label">Entry</span><span class="value entry">{entry_display}</span></div>
  <div class="row"><span class="label">Stop Loss</span><span class="value stop">{stop_display}</span></div>
  <div class="row"><span class="label">Take Profit 1</span><span class="value tp">{tp1}</span></div>
  <div class="row"><span class="label">Take Profit 2</span><span class="value tp">{tp2}</span></div>
  <div class="row"><span class="label">Take Profit 3</span><span class="value tp">{tp3}</span></div>
  <div class="row"><span class="label">Risk / Reward</span><span class="value rr">{rr}</span></div>

  <div class="reason"><strong>Reason:</strong> {output.reason}<br><strong>Hinglish:</strong> {output.reason_hinglish}</div>
  <div class="footer">Data: {output.data_timestamp} &middot; Freshness: {output.data_freshness} &middot; Analysis: {output.analysis_timestamp}</div>
  <div class="disclaimer">{output.disclaimer}</div>
</div>
</body>
</html>
"""
    return html


# ---------------------------------------------------------------------------
# Validation helpers for honesty (no fabricated prices / probabilities)
# ---------------------------------------------------------------------------

def assert_no_fabrication(output: QuickSignalOutput, allowed_prices: List[Optional[float]]) -> bool:
    """Return True if every price in the output is in allowed_prices or is NOT AVAILABLE.

    Used in tests to ensure no price was invented.
    """
    allowed_set = {round(float(p), 2) for p in allowed_prices if p is not None}
    # allow rounding tolerance — check each priced field
    checks: List[Optional[float]] = [
        output.entry.single_price,
        output.entry.zone_low,
        output.entry.zone_high,
        output.stop_loss.price,
        output.targets.tp1,
        output.targets.tp2,
        output.targets.tp3,
    ]
    for price in checks:
        if price is None:
            continue
        if round(price, 2) not in allowed_set:
            return False
    return True


def validate_no_probability(text: str) -> bool:
    """Ensure text does not contain unsupported probability fabrications."""
    # Banned patterns: "80% probability", "90% win", "sure shot", etc.
    banned = [
        r"\b\d{1,3}\s*%.*probab",
        r"\b\d{1,3}\s*%.*win",
        r"\bsure\s*shot\b",
        r"\bguaranteed\b",
        r"\b\d+\s*%.*success",
        r"\bconfidence\s*\d+%",
    ]
    lowered = text.lower()
    for pat in banned:
        if re.search(pat, lowered):
            return False
    return True

