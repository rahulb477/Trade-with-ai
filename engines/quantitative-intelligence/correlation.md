# Quantitative Intelligence — Correlation

Detailed theory in [`../../knowledge/quantitative-analysis/correlation-and-regression.md`](../../knowledge/quantitative-analysis/correlation-and-regression.md).
This file is the operational procedure.

## Procedure

```
1. Use RETURNS, not prices (prices are non-stationary).
2. Align timestamps; drop non-overlapping observations; report the resulting n.
3. Compute Pearson r on daily log returns over >= 1 year.
4. Compute r in >= 3 sub-periods to test stability.
5. Compute r during the largest drawdown window in the sample.
6. Report all of it. A single number hides the regime dependence.
```

## Reporting template

```
Correlation
  pair          : STOCK_A vs NIFTY 50
  measure       : Pearson r on daily log returns
  full sample   : 0.64  (n = 940, 2023-01 to 2026-11)
  sub-periods   : 0.58 (2023) · 0.71 (2024) · 0.61 (2025)
  stress window : 0.79 (largest 20-day drawdown in the sample)
  interpretation: moderate, stable co-movement that rises under stress. For portfolio purposes,
                  treat this name as roughly a 1.0-beta index proxy rather than an independent bet.
  limitation    : daily correlation understates intraday co-movement; correlation is not causation
                  and is not a hedge guarantee.
```

## Portfolio use

```
σ_p = sqrt(Σ_i Σ_j w_i w_j ρ_ij σ_i σ_j)
```

| Situation | ρ assumption |
|-----------|--------------|
| Measured, stable across sub-periods | Use the measured value, with the stress value noted |
| Measured but unstable | Use the higher (stress) value conservatively |
| Not measurable | Use 0.8 for same-sector, 0.3 for cross-sector, 1.0 if unsure |

## Failure modes

| Failure | Guard |
|---------|-------|
| Correlation on price levels | Use returns |
| One number for all regimes | Report sub-periods and stress |
| Ignoring survivorship in the pair set | Use point-in-time data |
| Treating negative correlation as a hedge | It can flip sign in a crisis |
| Correlating a stock with an index that contains it | Inflated by construction — note it |
