# Engine — Backtesting Lab

**Purpose:** document and implement historical simulation that does not flatter itself.

Implementation: `integrations/python/trading_intel/backtest.py`, `metrics.py`.

## 1. The four performance types — never conflate them

| Type | What it is | What it can tell you |
|------|-----------|----------------------|
| **Historical** | What actually happened | Nothing about the future |
| **Backtested** | Rules applied to past data with assumptions | Whether the rules *would have* worked under those assumptions |
| **Paper-traded** | Rules applied live, no money | Whether execution and psychology are realistic |
| **Live** | Real money | The only number that counts, and still a sample |

A backtest is an upper bound on paper-trading performance, which is an upper bound on live performance. Costs,
slippage, and human error all push realised results down.

## 2. Required pipeline

```
1. DATA VALIDATION
   - point-in-time universe (include delisted names or disclose survivorship bias)
   - adjusted prices for splits/bonus/dividends
   - no missing bars; check for zero-volume days
   - verify timestamps and timezone

2. STRATEGY RULES (mechanically defined, no discretion)
   - entry condition (a close-based trigger)
   - exit conditions (target, stop, time)
   - position sizing rule
   - filters (regime, liquidity, event avoidance)

3. SIMULATION
   - signals computed at bar close, filled at the NEXT bar's open
   - costs applied on both sides
   - slippage scaled by liquidity and volatility
   - gaps: if the open is beyond the stop, fill at the open (not at the stop)
   - position sizing applied within the simulation, not afterwards

4. METRICS
   - trades, win rate (+ CI), average win/loss in R, expectancy, profit factor
   - max drawdown (R and currency), longest losing streak, max adverse excursion
   - Sharpe/Sortino (with the caveat that they need >=100 trades to mean anything)

5. VALIDATION
   - walk-forward (train/test rolling)
   - out-of-sample holdout used once
   - parameter sensitivity (plateau not spike)
   - regime breakdown (bull/bear/range sub-periods)
```

## 3. The bias audit (mandatory)

See `knowledge/quantitative-analysis/overfitting-and-bias.md` §4. Summary checklist:

- [ ] No look-ahead (signal uses only data available at the decision time)
- [ ] Survivorship bias addressed or disclosed
- [ ] No data leakage from the test set into design
- [ ] Costs and slippage modelled
- [ ] Gaps handled realistically
- [ ] Sizing inside the simulation
- [ ] Parameters pre-registered or walk-forward
- [ ] Out-of-sample untouched during design
- [ ] Number of variants disclosed
- [ ] Regime coverage reported
- [ ] Sample size and CIs reported
- [ ] Code/data version recorded

## 4. Statistical guardrails

| Claim | Minimum standard |
|-------|-----------------|
| "This has an edge" | ≥100 out-of-sample trades, costs included, CI reported |
| "Win rate is 60%" | Report the CI; with n=100 that is roughly ±9.5 points |
| "Max drawdown was 12%" | Note that it is a sample statistic; the future can be worse |
| "Sharpe is 1.8" | ≥2 years of data, and the interval disclosed |
| "Robust across regimes" | Show the sub-period table |

## 5. Walk-forward protocol

```
Data:    [============== full history ==============]
Folds:   [train 2y][test 6m]
             [train 2y][test 6m]
                  [train 2y][test 6m]
                       [train 2y][test 6m]
Report: the concatenation of TEST segments only.
Also report: parameter drift across folds (unstable = red flag).
```

## 6. Transaction cost model

```
cost_per_trade_bps = brokerage_bps + taxes_bps + charges_bps + slippage_bps
cost_R             = cost_per_trade_bps/10000 * price / risk_per_unit
```

Report `gross_expectancy_R`, `cost_R`, and `net_expectancy_R`. The net number is the only one that matters.

## 7. Sample dataset (deterministic, for tests)

`tests/fixtures/` contains a small synthetic OHLCV series designed so that a known rule produces a known outcome.
It is **synthetic**, labelled as such, and must never be presented as real market history.

## 8. Failure modes

| Failure | Guard |
|---------|-------|
| Presenting a backtest as a forecast | State the four performance types |
| Optimising and reporting the best variant | Walk-forward + holdout + disclosure |
| Ignoring the short side or costs | Both are mandatory |
| Reporting only the equity curve | Report the metric table |
| Using a tiny sample | n >= 100 for any claim |
| Silently dropping bad years | Report per-year results |
