# Risk Management (Core)

The part of trading that survives being wrong. Everything here is **educational arithmetic**,
not personalised advice — the numbers use hypothetical capital.

---

## 1. First principle

> A trader who is right 40% of the time with 1:3 reward-to-risk can survive.
> A trader who is right 80% of the time with 3:1 risk-to-reward eventually does not.

Edge is a product of *win rate* and *payoff*, and it is destroyed by costs, slippage and
position size. Risk management is the discipline of making sure a single wrong call cannot remove
you from the game.

---

## 2. Core formulas

### 2.1 Risk-to-reward

```
risk_per_unit   = |entry − stop|
reward_per_unit = |target − entry|
R:R             = reward_per_unit / risk_per_unit
```

For a plan with three targets, quote R:R for each: `T1 1.5R · T2 2.6R · T3 4.0R`.

### 2.2 Position size by risk

```
risk_amount  = equity × risk_pct
units        = risk_amount / risk_per_unit
notional     = units × entry
```

Worked example (hypothetical):

```
equity = 500,000 (illustrative only)
risk_pct = 1.0%  -> risk_amount = 5,000
entry 1,204 · stop 1,186 -> risk_per_unit = 18
units = 5,000 / 18 = 277.7 -> 277 units (round DOWN)
notional = 277 × 1,204 = 333,508  (66.7% of equity)
```

Note how a tight stop implies a large notional. That is why notional exposure must be checked
separately (§4).

### 2.3 Break-even win rate

```
break_even_win_rate = risk / (risk + reward) = 1 / (1 + R)
```

| R:R | Break-even win rate |
|-----|--------------------|
| 1:1 | 50.0% |
| 1:1.5 | 40.0% |
| 1:2 | 33.3% |
| 1:3 | 25.0% |

Costs raise the required win rate. A 1:1 strategy with 0.3R round-trip cost needs ~65% to break even.

### 2.4 Expectancy

```
expectancy_per_trade (in R) = (win_rate × avg_win_R) − (loss_rate × avg_loss_R)
```

Positive expectancy is the only thing that matters over a sample. A setup with 35% win rate and
avg +2.5R wins has expectancy `0.35×2.5 − 0.65×1 = +0.225R` per trade.

### 2.5 Kelly (and why we do not use it directly)

```
f* = (p × b − q) / b        p = win rate, q = 1−p, b = payoff ratio
```

Full Kelly is aggressive and extremely sensitive to estimation error. Practitioners typically use
**fractional Kelly (¼ to ½)**. In *this* repository, percentage-risk sizing (0.25–1% per idea) is
the documented default because it does not require a trustworthy edge estimate. Where no verified
edge exists, Kelly is meaningless.

---

## 3. Stop-loss design

A stop is a **thesis invalidation**, not a comfort threshold.

| Method | Rule | Use when |
|--------|------|----------|
| Structural | Just beyond the swing/pattern boundary that defines the setup | Default. Preferred. |
| Volatility (ATR) | `entry ± k × ATR`, typically k = 1.5–2.5 for swings | Structure is noisy; no clean swing |
| Percentage | Fixed % from entry | Only when nothing structural exists — flag as crude |
| Time | Exit if the thesis does not resolve in N bars | Stagnant setups, event-driven |
| Level-based | Beyond a tested S/R zone (with a buffer) | Range/mean-reversion |
| Chandelier / trailing | `highest_high − 3×ATR` in an uptrend | Locking in trend profit |

Rules:

1. Never widen a stop after entry. Widening converts a controlled loss into an uncontrolled one.
2. Never place a stop exactly at an obvious level — that is where resting orders cluster.
   Add a buffer of a fraction of ATR (commonly 0.25–0.5×ATR).
3. If the required stop is so wide that size becomes trivial, the setup is wrong for the account.
4. Gap risk means a stop is not a guarantee: overnight or event gaps can fill far beyond the stop.
5. Stop-hunt risk is real around obvious levels during thin sessions.

---

## 4. Exposure and concentration

| Control | Rule of thumb (documented convention, not a mandate) |
|---------|-----------------------------------------------------|
| Risk per idea | 0.25–1.0% of equity |
| Total open risk | ≤ 3–6% of equity across all ideas |
| Single-name notional | Avoid > 20–25% of equity in one illiquid name |
| Correlated exposure | Two banks = one bet. Sum correlated risk as one |
| Sector cap | Cap aggregate sector risk, not just per-name |
| Leverage | Any F&O/CFD leverage multiplies both directions; state it explicitly |
| Cash buffer | Keep dry powder; forced selling at lows is the classic ruin path |

Correlation-adjusted exposure:

```
effective_risk ≈ Σ (risk_i) with highly correlated pairs merged,
                 or sqrt(Σ_i Σ_j w_i w_j ρ_ij σ_i σ_j) for a variance-based view
```

If you cannot estimate `ρ` from data, treat similar-sector positions as `ρ ≈ 1` (conservative).

---

## 5. Drawdown

```
drawdown_t = (equity_t / peak_equity_so_far) − 1
max_drawdown = min_t (drawdown_t)
```

Recovery arithmetic (the reason drawdown control dominates return chasing):

| Drawdown | Gain required to recover |
|----------|--------------------------|
| 10% | 11.1% |
| 20% | 25.0% |
| 33% | 50.0% |
| 50% | 100.0% |
| 75% | 300.0% |

Rules:

- Define a **max drawdown tolerance** before trading, not after.
- Define a **daily loss limit** (e.g. 2–3× per-trade risk) and stop for the day when hit.
- Define a **consecutive-loss circuit breaker** (e.g. after 4 losses, halve size until two wins).
- Track drawdown in R units as well as currency, so size changes do not distort the record.

---

## 6. Transaction costs and slippage (India equities, indicative)

Costs vary by broker and change over time — **verify current rates with your broker**. The
purpose here is to show the modelling structure, with placeholder magnitudes.

| Component | Typical structure |
|-----------|-------------------|
| Brokerage | Flat per order or % of turnover (discount brokers: flat; full-service: %) |
| STT / CTT | % on buy and/or sell depending on segment (delivery vs intraday vs F&O) |
| Exchange transaction charges | Small % of turnover |
| SEBI turnover fee | Very small % |
| Stamp duty | % on buy side |
| GST | % on brokerage + transaction charges |
| DP charges | Per sell transaction on delivery |
| **Slippage** | Difference between expected and filled price — often the largest real cost intraday |

Slippage model (use in backtests):

```
fill_price_buy  = expected + slippage_bps/10000 × expected  (+ half-spread)
fill_price_sell = expected − slippage_bps/10000 × expected  (− half-spread)
```

Conservative defaults for research: **5–10 bps** for liquid large caps, **20–50 bps** for
mid/small caps, and add half the observed spread. State your assumption explicitly.

**Cost in R terms** — always convert, because that is what the account feels:

```
cost_R = round_trip_cost_per_unit / risk_per_unit
```

If risk per unit is ₹4 and round-trip cost is ₹1.2, you are paying 0.3R to enter. A 1:1.5 plan
becomes roughly 1:1.1. This is why scalping strategies need very high win rates.

---

## 7. Gap and event risk

| Risk | Description | Mitigation (educational) |
|------|-------------|--------------------------|
| Overnight gap | Price opens beyond the stop | Reduce size into events; accept that the stop is not a floor |
| Earnings gap | Single-stock moves of 5–20% | Do not hold through results unless that is the explicit thesis |
| Circuit limits | Indian equities have price bands; an illiquid stock can lock at the band | Avoid thin names; know the band |
| Halt / suspension | Trading stops entirely | Position is frozen; no risk control is possible |
| Expiry / roll | Futures roll changes the price basis | Use continuous adjusted series; never mix expiries |
| Liquidity hole | No bid when you need to exit | Size to a fraction of average daily volume |

Sizing to liquidity:

```
max_units_by_liquidity ≈ 0.01 × average_daily_volume   (1% participation, conservative)
```

---

## 8. The risk block every paper-trade scenario must contain

```
Direction            : long / short (hypothetical)
Trigger              : <specific confirmation event>
Entry zone           : <low> – <high>  (basis: <level source>)
Invalidation (stop)  : <price>  (basis: <structure>; = <n> ATR; = <x>% )
Risk per unit        : <entry_mid − stop>
T1 / T2 / T3         : <price> (<R>R) · <price> (<R>R) · <price> (<R>R)
Basis of targets     : <prior swing / measured move / Fib / ATR multiple>
Round-trip cost est.  : <bps> ⇒ <cost_R> in R terms
Net R:R to T1        : <value after costs>
Illustrative size    : equity 500,000 × 0.5% = 2,500 risk ⇒ <units> units at <entry>
Max loss if gapped   : <scenario note>
What voids the thesis: <one sentence>
```

---

## 9. Ten rules that prevent most disasters

1. Size first, direction second. You can be wrong and survive; you cannot be oversized and survive.
2. One idea = one risk unit. Do not double up on the same thesis via a correlated instrument.
3. If you cannot state the invalidation in one sentence, you have no setup.
4. Costs are part of the trade, not an afterthought.
5. Never average down a losing leveraged position.
6. Reduce size when volatility expands, not when it contracts — ATR-based sizing does this
   automatically.
7. Stop trading for the day after your daily loss limit; the market will still be there.
8. Journal every trade; unrecorded trades cannot be improved.
9. Assume your backtest is optimistic. Assume your win rate is lower than measured.
10. Capital preservation is the strategy. Returns are what remain after survival.

---

*See also: [`../knowledge/risk-management/README.md`](../knowledge/risk-management/README.md) ·
[`../strategies/strategy-validation.md`](../strategies/strategy-validation.md)*
