# Engine — Strategy Discovery

**Purpose:** find recurring patterns systematically without manufacturing false positives.

## 1. Feature extraction

Candidates to extract per bar (all point-in-time safe):

| Family | Features |
|--------|----------|
| Structure | distance from swing high/low (ATR units), position in range (0–1), bars since structure break |
| Trend | MA slopes, ADX, price/MA distance in ATR |
| Momentum | RSI, ROC(n), MACD histogram normalised by ATR |
| Volatility | ATR%, Bollinger bandwidth, ATR percentile |
| Volume | volume z-score, OBV slope |
| Regime | regime label from `engines/market-intelligence/market-regime.md` |
| Session/time | time-of-day bucket, day-of-week (for intraday) |
| Context | distance to scheduled events (bars), days to expiry |

**Normalise everything by ATR or by a rolling z-score.** Absolute prices and raw indicator levels are not
comparable across instruments or regimes.

## 2. Discovery procedure

```
1. Define a forward outcome: e.g. return over the next N bars in R units relative to an ATR-based exit.
2. Split the data chronologically: discovery (60%), validation (20%), holdout (20%).
3. On the DISCOVERY set only, screen features for monotonic relationship with the outcome.
   (Quintile analysis is more robust than a single threshold.)
4. Form candidate rules from features with a monotonic relationship.
5. Test on VALIDATION. Discard anything that fails.
6. Apply the robustness gates (section 4).
7. Test surviving rules on HOLDOUT exactly once.
8. Report everything, including the failures and the number of candidates tried.
```

## 3. Statistical significance

- Minimum **100 occurrences** in validation for any claim (better: 300).
- Report a confidence interval on the hit rate (Wilson).
- Correct for multiple testing: with `k` candidates at α=0.05, the chance of a fluke is `1 − 0.95^k`.
- Prefer a **monotonic relationship across quintiles** over a single threshold; thresholds are where overfitting
  lives.

## 4. Robustness gates (all must pass)

| Gate | Test |
|------|------|
| **Plateau** | Vary each parameter ±20%: performance should degrade gradually, not collapse |
| **Sub-period stability** | Positive in ≥3 of 4 chronological quartiles |
| **Regime stability** | Works in at least trending and ranging subsets, or is explicitly regime-specific |
| **Instrument breadth** | Works across ≥5 instruments, not just one |
| **Cost survival** | Positive net after 2× the assumed costs |
| **Simplicity** | ≤3 parameters |
| **Economic rationale** | A stated reason why it should work |

Failing any gate → the rule is documented as a **rejected hypothesis**, with the reason. Rejections are valuable
and are kept.

## 5. What counts as an edge

```
net_expectancy_R > 0 with a 95% CI excluding 0, on >= 100 out-of-sample trades,
after costs, across >= 5 instruments and >= 3 regimes.
```

Anything less is "promising in-sample, unverified". That phrase is acceptable; "profitable strategy" is not.

## 6. Failure modes

| Failure | Guard |
|---------|-------|
| Testing 200 candidates and reporting the best | Disclosure + multiple-testing correction |
| Threshold chosen from the data with no penalty | Quintile analysis + plateau test |
| Single instrument | Breadth gate |
| Single regime | Regime stability gate |
| Ignoring costs | Cost survival gate |
| Reporting only survivors | Log rejected hypotheses |
| A "discovered" edge with no mechanism | Economic rationale gate |

## 7. Output format

```
Candidate                         : "RSI<30 + price above 200EMA on daily"
Discovery set (2015-2021)         : n=412, hit 58.2%, expectancy +0.21R
Validation set (2022-2023)        : n=96,  hit 54.1%, expectancy +0.11R
Holdout (2024-2026)               : NOT YET USED
Plateau test                      : RSI 25/30/35 -> +0.18 / +0.21 / +0.16 R  (plateau: PASS)
Sub-period stability              : 3 of 4 quartiles positive (PASS)
Instrument breadth                : 8 of 12 instruments positive (PASS)
Cost survival (2x costs)          : expectancy +0.06R (marginal PASS)
Regime dependency                 : fails in ranging regimes -> must be gated by ADX > 20
Status                            : PROMISING IN-SAMPLE, PENDING HOLDOUT
```
