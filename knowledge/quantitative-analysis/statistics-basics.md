# Statistics Basics for Trading Research

## 1. Why this matters more than any indicator

Most trading claims fail on sample size and selection, not on mathematics. Understanding three ideas prevents
most errors: **sampling error, distributions, and multiple comparisons.**

## 2. Sampling error and confidence intervals

For a win rate measured on `n` trades with observed proportion `p̂`:

```
standard error  SE   = sqrt(p̂(1 − p̂) / n)
95% CI (Wald)        = p̂ ± 1.96 × SE
```

| n | p̂ = 0.5 | 95% CI width |
|---|--------|--------------|
| 10 | 0.5 | 0.19 – 0.81 (enormous) |
| 30 | 0.5 | 0.32 – 0.68 |
| 100 | 0.5 | 0.40 – 0.60 |
| 400 | 0.5 | 0.45 – 0.55 |
| 1 000 | 0.5 | 0.47 – 0.53 |

With 10 trades you cannot distinguish a 50% method from a 20% one. This is why "my pattern wins 7 out of 10"
is not evidence — the interval spans almost the entire range of possibilities.

For proportions near 0 or 1, or small `n`, use Wilson or Clopper-Pearson intervals instead of Wald. The
implementation uses Wilson.

## 3. Distributions — trade returns are not normal

Documented properties of trade-return distributions:

| Property | Implication |
|----------|-------------|
| Fat tails | Extreme losses are more common than a normal model predicts |
| Negative skew (for many strategies) | Many small wins, occasional large losses |
| Positive skew (for trend following) | Many small losses, occasional large wins |
| Non-stationarity | The distribution changes across regimes |

Consequences: the mean is a poor summary; **median, percentiles and the worst cases matter more.** Always report
max drawdown and max adverse excursion, not just the average.

## 4. Significance, honestly

A p-value answers: "if there were no effect, how surprising is this data?" It does **not** answer "how likely is
this strategy to work?"

Practical minimum standards before claiming an edge:

1. **n ≥ 100** completed trades (preferably 300+) in the evaluation set.
2. **Out-of-sample** confirmation on data not used for design.
3. **Costs and slippage** included.
4. **Regime coverage** — includes at least one trending and one ranging period.
5. **Pre-registered rules** — the strategy was defined before looking at the results.

If any is missing, the honest phrasing is "promising in-sample, unverified".

## 5. Multiple comparisons — the killer

If you test 20 variations and report the best, you will always find a "winner". This is not skill; it is
selection bias.

```
P(at least one false positive) = 1 − (1 − α)^k      α = 0.05, k = number of tests
k = 5   -> 23%
k = 20  -> 64%
k = 100 -> 99.4%
```

Guards:

- Pre-register the parameters you will test.
- Hold out a final test set that is used **once**.
- Report how many variations you tried.
- Prefer a parameter region that works over one magic value (plateau, not spike).

## 6. Stationarity

A statistical relationship is stationary if its distribution does not change over time. Markets are not
stationary. Therefore:

- A correlation measured over 3 years may be near zero over the next 3.
- A win rate measured in a bull market may not transfer to a bear market.
- A parameter optimised on one regime will be mis-tuned in another.

Report |item|Period covered| and |item|Regimes included| with every statistic.

## 7. What to report for any measured strategy

```
metric                  value          notes
-------------------------------------------------------
sample size             312 trades
period                  2019-01 to 2025-12
instruments              12 large-cap equities
regimes covered          bull, bear, range
win rate                 41.3%  (95% CI 35.9-46.9%)
average win              +2.1R
average loss             -1.0R
profit factor            1.44
expectancy               +0.28R
max drawdown             -18.4R
costs included           yes, 12 bps round trip
out-of-sample            yes, 2024-2025 held out
```

## 8. Common errors

| Error | Guard |
|-------|-------|
| Claiming a rate from 10 trades | Report the CI; it will be humiliating and correct |
| Reporting mean return only | Report percentiles and drawdown |
| Using a p-value as a probability of success | It is not |
| Testing 30 variants and reporting the best | Pre-register; use a holdout |
| Assuming a relationship persists | Check stability across sub-periods |
| Ignoring costs | Always convert to R |

## 9. Beginner summary (Hinglish)

**Sabse bada problem: sample size.** 10 trades se aap kuch bhi prove nahi kar sakte — 7/10 jeetne par bhi ho
sakta hai ki method 20% wala hai.

**Simple rule:** 100 se kam trades par **koi rate claim mat karo**. 300+ chahiye, aur out-of-sample.

**Distribution normal nahi hoti.** Ek-do bade losses sab kuch badal dete hain. Isliye **average** se zyada
**worst case** dekho.

**Multiple testing trap:** 20 variation test karke best dikhana = selection bias. 20 test karne par 64% chance hai
ki kam se kam ek "winner" sirf luck se milega.

**Har statistic ke saath likho:** kitne trades, kis period mein, kaunse regimes, costs include the ya nahi.

## 10. Exercise

Take any trade log you can find (or generate 20 from a rule). Compute the win rate and its 95% CI. Then compute
what sample size you would need to narrow the CI to ±5 percentage points. Write down whether your log is
conclusive.

---
*See also: [`expectancy.md`](expectancy.md) · [`overfitting-and-bias.md`](overfitting-and-bias.md) ·
[`../../engines/backtesting/README.md`](../../engines/backtesting/README.md)*
