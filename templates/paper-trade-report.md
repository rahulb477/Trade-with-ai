# Paper-Trade Report Template

> **Everything here is hypothetical.** No order is placed. No money is at risk. Write in conditional language:
> "would enter", "if price closes", "the plan would be invalidated".

---

## 1. Trade Identity

| Field | Value |
|-------|-------|
| Paper trade ID | PT-YYYYMMDD-NN |
| Instrument / exchange | |
| Timeframe (analysis / entry) | |
| Date & time of the plan | (with timezone) |
| Analysis report reference | |
| Status | PLANNED / TRIGGERED / INVALIDATED / EXPIRED / CLOSED (hypothetical) |

## 2. The Ten-Box Entry Checklist

| # | Condition | Pass? | Evidence |
|---|-----------|-------|----------|
| 1 | Instrument positively identified | | |
| 2 | Chart quality ≥5 with a readable scale | | |
| 3 | Structure defined (trend + swings) | | |
| 4 | Entry at a tested level, not mid-range | | |
| 5 | Trigger is a **close**, not a wick | | |
| 6 | Invalidation is structural, ≤3 ATR | | |
| 7 | Room to next resistance ≥2 ATR | | |
| 8 | R:R to T1 ≥ 1.5 | | |
| 9 | No binary event inside the horizon | | |
| 10 | No unrefuted trap evidence | | |

**Any failure → `WAIT — NO CONFIRMED SETUP`.** Record which box failed.

## 3. Plan

| Field | Value |
|-------|-------|
| Direction | long / short |
| Entry trigger | |
| Entry zone | |
| Stop / invalidation | |
| T1 / T2 / T3 | |
| Risk per unit | |
| R:R to T1 / T2 / T3 | |
| Time stop | (bars or date) |
| Trail rule after T2 | |

## 4. Explicit Computation

```
entry            = ...
stop             = ...
risk_per_unit    = |entry − stop|              = ...
T1 − entry       = ...
R_T1             = (T1 − entry) / risk_per_unit = ...
equity (stated)  = ...
risk budget      = equity × 0.75%               = ...
units (illustrative, floored) = risk budget / risk_per_unit = ...
notional         = units × entry                = ... ( % of equity )
cost_R (est.)    = bps/10000 × entry / risk_per_unit = ...
net R_T1         = R_T1 − cost_R                = ...
break-even WR    = (1 + cost_R) / ((R_T1 − cost_R) + (1 + cost_R)) = ...
```

## 5. Target Sources

| Target | Derived from | Type |
|--------|--------------|------|
| T1 | | structure / measured move / ATR multiple / Fib |
| T2 | | |
| T3 | | |

No target may be invented to make the R:R work. If the structure gives only 1.2R, the honest verdict is WAIT.

## 6. Trap Audit

| Trap type | Evidence | Score /6 | Status |
|-----------|----------|----------|--------|
| | | | |

## 7. Scenarios

- **A (base case):** trigger → ...
- **B (alternative):** ...
- **C (no trade):** ...

## 8. Invalidation Conditions

| Condition | Action |
|-----------|--------|
| Close beyond the stop | Plan is void; do not renegotiate |
| Time stop reached with no trigger | Expire the plan |
| A binary event is announced inside the horizon | Halve size or stand aside |
| Higher timeframe flips | Re-run the alignment table |

## 9. Post-Mortem (filled after the outcome, timestamped)

| Field | Value |
|-------|-------|
| Outcome | triggered / not triggered / invalidated |
| Hypothetical result (R) | |
| Process followed? | yes / no |
| Lesson | |

## 10. Disclosure

Hypothetical analysis for education. Not investment advice. No order placed. Costs are estimates. Past chart
behaviour does not repeat reliably.
