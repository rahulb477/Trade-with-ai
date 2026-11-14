# Correlation and Regression

## 1. Correlation basics

```
Pearson r = cov(X,Y) / (σ_X σ_Y)          linear association, −1 to +1
Spearman ρ = Pearson on ranks              monotonic, robust to outliers
R² = r²                                    fraction of variance explained (linear only)
```

Interpretation traps:

| Trap | Reality |
|------|---------|
| "r = 0.7 means X drives Y" | Correlation is not causation |
| "r is stable" | Correlations change with regime |
| "r = 0 means no relationship" | Only no *linear* relationship |
| "High r means tradable" | Execution, costs and regime shifts still dominate |

## 2. Correlation is unstable — the most important fact

Asset correlations documented to rise during market stress ("correlations go to one in a crisis"). This means:

1. Diversification **weakens exactly when you need it**.
2. A portfolio optimised on calm-period correlations will be under-hedged in stress.
3. Any correlation you quote must include the **sample period** and the **regimes covered**.

Report it as: "r = 0.62 over 2021–2025 daily returns, which included one drawdown >15%; in that drawdown window
r rose to ≈0.8."

## 3. Practical use: portfolio risk

Variance of a two-asset portfolio:

```
σ_p² = w₁²σ₁² + w₂²σ₂² + 2w₁w₂ρσ₁σ₂
```

| ρ | Effect |
|---|--------|
| +1 | No diversification benefit; risk is the weighted sum |
| 0 | Diversification benefit |
| −1 | Maximum benefit; risk is the weighted difference |

For a multi-asset portfolio: `σ_p = sqrt(wᵀ Σ w)`.

**If you cannot estimate `ρ` from data, assume `ρ ≈ 0.8–1.0` for same-sector names.** Underestimating correlation
is the most common portfolio risk error.

## 4. Relative strength (a legitimate correlation use)

```
RS_ratio_t = price_A_t / price_B_t
RS_slope   = slope of RS_ratio over N bars
```

Arising sector shows a rising ratio against the index. Use **risk-adjusted** momentum (ROC ÷ ATR%) to compare
instruments with different volatility, otherwise you just rank by volatility.

## 5. Regression pitfalls

| Pitfall | Description | Guard |
|---------|-------------|-------|
| Spurious regression | Two trending series appear related | Difference them, or use cointegration tests |
| Non-stationarity | Regression on non-stationary series is unreliable | Test with ADF; use returns |
| Autocorrelation | Residuals correlated → wrong standard errors | Use Newey-West or block bootstrap |
| Overfitting | Too many regressors | Fewer variables, out-of-sample |
| Look-ahead | Using future data in a feature | Strict point-in-time construction |
| Extrapolation | Using the model outside the observed range | Do not |

## 6. Beta and hedging

```
β = cov(stock, market) / var(market)
hedge_ratio ≈ β × (position value / futures value)
```

Beta is a regression output with the same caveats: it is unstable, it changes with regime, and company-specific
events are not hedgeable by index futures.

## 7. What to report

```
pair                : STOCK_A vs NIFTY 50
measure             : Pearson r on daily returns
value               : 0.64
period              : 2023-01-01 to 2026-11-01 (n = 940 observations)
sub-period stability: 0.58 (2023), 0.71 (2024), 0.61 (2025) -> reasonably stable
stress note         : in the largest 20-day drawdown of the period, r rose to ≈0.79
interpretation      : moderate positive co-movement; equity beta likely 0.9-1.1
limitation          : daily-return correlation understates intraday co-movement, and correlation
                      is not causation nor a hedge guarantee
```

## 8. Beginner summary (Hinglish)

**Correlation (r):** −1 se +1. Do assets ek saath kitna move karte hain.

**Sabse important:** correlation **stable nahi** hoti. Crisis mein sab kuch ek saath girta hai (r → 1). Isliye
"diversified" portfolio stress mein diversified nahi rehta.

**Portfolio risk:** agar do same-sector stocks hain, `ρ` ko 1 maano. Kam maankar risk underestimate karna sabse
common galti hai.

**Regression ka dhyan:** do trending series ko regress karne se **spurious** result aata hai. Returns par kaam
karo, prices par nahi.

**Har correlation ke saath likho:** kis period ka hai, kitne observations, kaunse regime mein.

## 9. Exercise

Compute the daily-return correlation between two stocks in the same sector over two different years. Compare the
two values. Then compute the same for two stocks in different sectors. Write down how much the value moved between
periods, and what that implies for a portfolio built on one year's estimate.

---
*See also: [`statistics-basics.md`](statistics-basics.md) · [`../engines/quantitative-intelligence/`](../../engines/quantitative-intelligence/)*
