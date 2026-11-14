# Workflow — Breakout Analysis

## Step 1 — Is there a level?
- [ ] ≥2 prior touches at the level
- [ ] The level is visible/horizontal, not a vague zone
- [ ] There was compression beneath it (range, triangle, flag, base)

If not → this is not a breakout setup. Stop.

## Step 2 — Has the break happened?
| State | Definition |
|-------|-----------|
| Pre-break | Price approaching; no close beyond |
| Break (unconfirmed) | Close beyond, but no follow-through yet |
| Confirmed | Close beyond + next bar holds + volume expanded |
| Failed | Close back inside within 1–3 bars |

## Step 3 — Volume check
`breakout_bar_volume / 20-bar_average`:

| Ratio | Reading |
|-------|---------|
| ≥2.0 | Strong |
| 1.3–2.0 | Acceptable |
| 1.0–1.3 | Weak |
| <1.0 | Probable failure — do not present as a valid setup |

If no volume panel: state `volume not assessable` and downgrade confidence one rung.

## Step 4 — Room check
```
distance_to_next_resistance (ATR units)
  >=2      acceptable
  1-2      marginal
  <1       no room -> untradeable
```

## Step 5 — Trap audit
Run `trap-detection.md`. Specifically:
- Did the breakout bar close near its low instead of its high?
- Did volume collapse on the following bar?
- Is there an obvious stop cluster just above the level (equal highs)?
- Is the breakout into a major resistance or a round number?

Two or more "yes" → downgrade to WAIT.

## Step 6 — Entry design

Pick one and state it:

| Style | Entry | Risk |
|-------|-------|------|
| Breakout close | On the closing break | Highest failure rate |
| Follow-through | Next bar holding above | Moderate |
| Retest | On the pullback that holds | Best R:R, misses runners |

## Step 7 — Arithmetic
```
entry, invalidation (back inside the range + buffer), risk per unit
T1 = nearest structural resistance
T2 = measured move (range height projected)
T3 = next major level
R for each; gate at 1.5R to T1
```

## Step 8 — Output
```
Level          : 1_240 (3 touches, 4 weeks)
Compression    : ascending triangle, 18 bars
Break state    : CONFIRMED (close 1_243.5, volume 2.2x)
Room           : 2.4 ATR to 1_265
Trap audit     : 0 red flags
Entry          : retest 1_241
Invalidation   : 1_231 (last higher low + buffer)
Risk           : 10
T1 1_265 (2.4R) · T2 1_275 (3.4R) · T3 1_310 (6.9R)
Verdict        : BULLISH SCENARIO on the retest trigger
```
