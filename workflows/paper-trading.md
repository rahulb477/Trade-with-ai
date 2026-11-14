# Workflow — Paper-Trading Plan

Precondition: the user asked for entries/stops/targets, or the mode is PAPER-TRADING. **All output is
hypothetical and educational.** Never size with the user's real capital.

## Step 1 — Confirm the entry checklist (all boxes or no plan)

- [ ] Instrument + exchange confirmed
- [ ] Timeframe identified; higher timeframe consulted or declared unavailable
- [ ] Regime classified
- [ ] Specific trigger defined (a close, a retest hold, or a pattern completion)
- [ ] Level drawn from actual price, not invented
- [ ] Volume supports, or explicitly flagged not assessable
- [ ] Invalidation is structural
- [ ] R:R ≥ 1.5 to T1 after costs
- [ ] No unexplained opposing higher-timeframe evidence
- [ ] No binary event inside the horizon (or size reduced and stated)

Any failure → `WAIT — NO CONFIRMED SETUP` plus the specific failing box.

## Step 2 — Build the two directions
Even if one looks far more likely, describe both triggers. They are conditional plans, not predictions.

## Step 3 — Compute everything explicitly

```
Direction      :
Trigger        : <exact condition, e.g. "15m close above 1,243.5">
Entry zone     :
Entry basis    :
Invalidation   :
Invalidation basis : <structure> + <ATR buffer>
Risk per unit  :
T1 / T2 / T3   :
Target basis   : <prior swing / measured move / Fib / ATR multiple>
R for each     :
Round-trip cost: <bps> -> <cost_R>
Net R:R to T1  :
Illustrative size : equity 500,000 x 0.5% = 2,500 -> <units> units at <entry>
Notional       : <value> (<pct>% of equity)
Gap risk note  :
What voids it  :
What to wait for :
```

## Step 4 — Target discipline
Every target must map to something real:

| Target source | Acceptable |
|---------------|-----------|
| Prior swing high/low | Yes |
| Measured move from a pattern | Yes (show the arithmetic) |
| Fib level | Yes (state anchors) |
| Round number | Only as a secondary consideration |
| ATR multiple | Yes for volatility-based targets |
| "Feels right" | Never |

If only one valid target exists, present one. Do not invent T2 and T3 to fill the template.

## Step 5 — Cost conversion
```
cost_R = round_trip_cost_per_unit / risk_per_unit
```
If the net R:R to T1 falls below 1.5, say so and either propose a better entry or return WAIT.

## Step 6 — Position sizing (illustrative only)
Use a hypothetical equity and label it as such. **Never** use the user's actual capital, and never say "you should
buy N shares".

## Step 7 — The Hinglish plan
Render the plan in simple Hinglish using `knowledge/education/hinglish-explanations.md` §4. Numbers must match
exactly.

## Step 8 — Record
If writing is available, save a prediction record with the trigger conditions. Leave the outcome block empty.

## Output template
Use `templates/paper-trade-report.md`.

## Hard prohibitions

- No real-money sizing with the user's capital
- No broker instructions or order-placement language
- No "guaranteed", "sure shot", "high probability" without a cited measured source
- No invented statistics
- No target without a basis
- No trailing stop advice that contradicts the stated invalidation
