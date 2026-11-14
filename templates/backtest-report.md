# Backtest Disclosure Sheet

A backtest without this sheet is an advertisement, not research.

## 1. Identification

| Field | Value |
|-------|-------|
| Strategy name | |
| Version / commit | |
| Author | |
| Date run | |
| Code path | `integrations/python/trading_intel/backtest.py` |
| Configuration hash | |

## 2. Strategy Definition (mechanical)

```
Universe:
Entry condition:
Exit conditions:
  - target:
  - stop:
  - time stop:
Sizing rule:
Filters:
```

No discretionary condition is permitted in a validated backtest.

## 3. Data

| Item | Value |
|------|-------|
| Source | |
| Adjusted? | yes / no |
| Period | |
| Instruments | |
| Bars | |
| Known gaps | |
| Survivorship handling | point-in-time / disclosed bias / n/a |

## 4. Execution Assumptions

| Assumption | Value |
|-----------|-------|
| Fill timing | next bar open |
| Intrabar stop/target order | stop first (pessimistic) |
| Gap handling | fill at open when beyond the stop |
| Cost per round trip | __ bps |
| Slippage model | |
| Position sizing | inside the simulation |

## 5. Results

| Metric | In-sample | Validation | Out-of-sample |
|--------|-----------|-----------|---------------|
| Trades (n) | | | |
| Hit rate (+95% CI) | | | |
| Average win / loss (R) | | | |
| Expectancy (R) | | | |
| Profit factor | | | |
| Max drawdown (R) | | | |
| Longest losing streak | | | |
| Cost per trade (R) | | | |
| Net expectancy (R) | | | |

## 6. Robustness

| Gate | Result |
|------|--------|
| Parameter plateau (±20%) | |
| Sub-period stability (≥3 of 4) | |
| Instrument breadth (≥5) | |
| Regime breakdown | |
| Survives 2× costs | |
| Out-of-sample used once | |

## 7. Bias Checklist

- [ ] No look-ahead
- [ ] Survivorship addressed
- [ ] Data leakage excluded
- [ ] Costs and slippage modelled
- [ ] Gaps realistic
- [ ] Sizing inside the loop
- [ ] Parameters pre-registered or walk-forward
- [ ] Number of variants disclosed: ____
- [ ] Sample size and CIs reported
- [ ] Per-year results reported

## 8. Honest Conclusion

> "This is a [DOCUMENTED / BACKTESTED-IN-SAMPLE / PROMISING / VALIDATED-SAMPLE / REJECTED] result on [n]
> trades over [period] across [instruments], including [x] bps round-trip costs. It has [not] been tested out of
> sample. It is a historical sample statistic, not a forecast."

## 9. Known Failure Conditions

1.
2.
3.

## 10. What Would Falsify This

The specific evidence that would make you abandon the strategy — written before it happens.
