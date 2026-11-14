# Engine — Quantitative Intelligence

**Purpose:** statistical and simulation support for research claims. Never used to produce a price forecast.

**Inputs:** return series, trade logs, parameter sets, option chains.
**Outputs:** descriptive statistics with sample sizes and intervals, simulations with disclosed assumptions.

## Modules

| Module | Function |
|--------|----------|
| `README.md` | Scope and standards |
| [`correlation.md`](correlation.md) | Correlation stability and portfolio risk |

Implementation: `integrations/python/trading_intel/stats.py` (`mean`, `stdev`, `correlation`, `sharpe`,
`sortino`, `max_drawdown`, `wilson_interval`), `simulate.py` (bootstrap, Monte Carlo).

## What this engine may output

| Permitted | Not permitted |
|-----------|--------------|
| Descriptive statistics with n and CI | A price forecast |
| Expectancy in R with CI | A "probability of profit" without assumptions |
| Monte Carlo drawdown distributions with a seed | A claim that a simulation predicts the future |
| Correlation with period and regimes | A claim that correlation implies causation |
| Regime classification from volatility percentiles | A regime forecast |

## Standards

1. **Always report n.** A statistic without a sample size is not reported.
2. **Always report the period.** Including which regimes it covers.
3. **Always report costs** when the subject is a strategy.
4. **Always report the assumptions** of a model.
5. **Never extrapolate** beyond the observed range without labelling it as an extrapolation.

## Sanity checks before publishing a number

- [ ] Is the sample size plausible for the claim?
- [ ] Is the metric defined in the report (Sharpe of what, over what)?
- [ ] Does the number survive a 2× cost assumption?
- [ ] Is the result driven by one or two outliers? (Check by recomputing without the top/bottom 2.)
- [ ] Was the parameter chosen using the same data? (If yes → disclosure required.)
- [ ] Is a confidence interval possible? If not, why not?

## Failure modes

| Failure | Guard |
|---------|-------|
| Reporting a mean return as if it were typical | Report median and percentiles |
| Sharpe on 40 trades | Report the interval, or say "not meaningful" |
| Correlation over a single regime | Report sub-period stability |
| Monte Carlo without a seed | Fix the seed for reproducibility |
| Simulation with no downside scenario in the sample | State that the tail is not represented |
