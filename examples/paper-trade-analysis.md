# Example — Paper Trade (Hypothetical)

> **FICTIONAL AND HYPOTHETICAL.** Instrument "EPSILONTECH" (fictional). **No order was placed.** All numbers are
> invented to demonstrate the arithmetic. This is not a recommendation for any security.

---

## 1. Trade Identity

| Field | Value |
|-------|-------|
| Paper trade ID | PT-20261114-01 |
| Instrument | EPSILONTECH (fictional, NSE) |
| Timeframes | 1D analysis / 1H entry |
| Plan written | 2026-11-14 16:20 IST |
| Status | **PLANNED** (trigger not yet met) |

## 2. The Ten-Box Entry Checklist

| # | Condition | Pass? | Evidence |
|---|-----------|-------|----------|
| 1 | Instrument positively identified | ✅ | ticker legible |
| 2 | Quality ≥5 with readable scale | ✅ | 9/10 |
| 3 | Structure defined | ✅ | uptrend, 3 HH/HL; swing k=3 |
| 4 | Entry at a tested level | ✅ | 1,232 support, 3 touches, + 20-EMA confluence |
| 5 | Trigger is a close | ✅ | daily close > 1,258 required |
| 6 | Invalidation structural, ≤3 ATR | ✅ | 1,228 = 0.9 ATR from the 1,244 stop reference |
| 7 | Room to next resistance ≥2 ATR | ✅ | 1,232 → 1,312 = 80 pts = 3.4 ATR (ATR ≈ 23.5) |
| 8 | R:R to T1 ≥ 1.5 | ✅ | 2.1R to T1 |
| 9 | No binary event inside horizon | ⚠️ **unknown** | no event calendar available |
| 10 | No unrefuted trap evidence | ✅ | trap score 1/6 |

**Box 9 is `unknown`, not `pass`.** Per the workflow, an unknown event check caps the plan at reduced size — and
the report must say so rather than silently assuming no events.

## 3. Plan

| Field | Value |
|-------|-------|
| Direction | Long |
| Entry trigger | Daily **close** above 1,258, then entry on the next session's open or a 1H retest of 1,250–1,258 |
| Entry zone | 1,250 – 1,260 |
| Stop / invalidation | **1,228** (below the higher low and the 20-EMA) |
| T1 | 1,300 (the minor supply level) |
| T2 | 1,312 (prior swing high) |
| T3 | 1,360 (measured move of the 1,232→1,198 base) |
| Risk per unit | ~28 (from a 1,256 entry) |
| Time stop | 12 sessions |
| Trail rule | After T2, trail below each new daily higher low, never inside 0.5 ATR |

## 4. Explicit Computation

```
entry (planned, mid-zone)   = 1,256
stop                        = 1,228
risk_per_unit               = |1,256 − 1,228| = 28

T1 1,300:  (1,300 − 1,256) / 28 = 1.57R
T2 1,312:  (1,312 − 1,256) / 28 = 2.00R
T3 1,360:  (1,360 − 1,256) / 28 = 3.71R

equity (illustrative)       = 1,000,000
risk budget at 0.75%        = 7,500
units (floored)             = floor(7,500 / 28) = 267
notional                    = 267 × 1,256 = 335,352  (33.5% of equity)
max loss if the stop fills   = 267 × 28 = 7,476     (0.75% of equity)

cost estimate (12 bps round trip, assumed)
  cost_R = 0.0012 × 1,256 / 28 = 0.054R
  net R at T1 = 1.57 − 0.054 = 1.52R
  net R at T2 = 2.00 − 0.054 = 1.95R

break-even win rate at 1.52R net:
  loss = 1 + 0.054 = 1.054 ; win = 1.52
  BE = 1.054 / (1.054 + 1.52) = 40.9%
```

**What these numbers do and do not say:** a 41% break-even win rate means the plan survives being wrong more often
than right *if* the T1 target is reached *and* the stop is never exceeded. Neither is guaranteed: gaps can fill
below the stop, and T1 is a supply level that may reject.

## 5. Target Sources

| Target | Derived from | Type |
|--------|--------------|------|
| T1 1,300 | the minor supply level from the last leg, 2 touches | structure |
| T2 1,312 | the prior swing high | structure |
| T3 1,360 | the height of the 1,198→1,232 base projected from the breakout | measured move |

No target was invented to make the R:R work. T1 comes from a level that exists; that is why it is only 1.57R.

## 6. Trap Audit

| Test | Score |
|------|-------|
| Prior level exists (≥2 touches) | 1 |
| A break occurred | 0 (price has not broken out yet) |
| Close back inside within 1–3 bars | 0 |
| Reaction away | 0 |
| No immediate re-break | 0 |
| Volume evidence | 0 |

**Total 1/6 → no trap claim.** The relevant trap risk is *future*: a break of 1,258 that closes back below it
would score 4–5 and cancel the plan.

## 7. Scenarios

- **A (base):** daily close > 1,258 → entry 1,250–1,260 → T1 1,300 → T2 1,312 → trail.
- **B:** price rejects 1,258 and closes below 1,244 → the pullback deepens; the plan expires, and a *new* plan
  would need a new higher low.
- **C:** nothing happens for 12 sessions between 1,232 and 1,258 → **time stop expires the plan.** Expiry is a
  legitimate outcome, not a failure.

## 8. Invalidation Conditions

| Condition | Action |
|-----------|--------|
| Daily close below 1,228 | Plan void. No renegotiation, no "wider stop". |
| A binary event announced inside 12 sessions | Halve the size or stand aside |
| A close above 1,258 **without** volume ≥1.3× average | Treat as `POSSIBLE`, not `TRIGGERED`; wait for a retest |
| 12 sessions elapse with no trigger | Expire |

## 9. Post-Mortem (to be appended, timestamped)

| Field | Value |
|-------|-------|
| Outcome | *(pending)* |
| Hypothetical R | *(pending)* |
| Process followed? | *(pending)* |

Not yet filled — and that is correct. A post-mortem written before the outcome is a fantasy.

## 10. Disclosure

Hypothetical. Educational. No order placed. Costs are estimates, not quotes. The instrument is fictional. Nothing
here is investment advice, and a paper-trade plan that looks arithmetically sound can still lose.

## 11. Beginner Explanation (Hinglish)

**Plan:** agar price 1,258 ke **upar daily close** kare, to 1,250–1,260 ke beech entry. Stop **1,228** ke neeche.

**Kyun 1,228:** wahan higher low hai aur 20-EMA bhi wahin hai. Iske neeche close = idea galat.

**Targets:** 1,300 / 1,312 / 1,360. Pehle target par **1.57R**.

**Size:** 10 lakh ka account, 0.75% risk = 7,500. Risk per unit 28 → **267 units**. Stop hit ho to ~7,476 ka loss —
plan ke hisaab se.

**Costs:** ~0.05R. Isliye net 1.52R. Break-even win rate **41%** — matlab 10 mein se 6 trade galat bhi ho sakte hain
aur phir bhi bache rahoge — **agar** stop respect ho.

**Sabse zaroori:** stop hit hone par "thoda aur wait karta hoon" **nahi** karna. Wahi ek decision account kharab
karta hai.

## 12. Notes on what makes this example honest

It contains an `unknown` (event check), a target that is only 1.57R (not a heroic 5R), an explicit time stop, and
an empty post-mortem. Those four details are what separate a plan from a wish.
