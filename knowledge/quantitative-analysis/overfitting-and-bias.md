# Overfitting and Bias

The reason most backtests are fiction. Read this before believing any result — including one produced by this
repository's own tools.

## 1. The four biases

### 1.1 Look-ahead bias
Using information that was not available at the decision time.

| Example | Why it is wrong |
|---------|-----------------|
| Using the day's **close** to enter at the day's **open** | The close was unknown at the open |
| Using the day's high/low in a signal that fires intraday | Both are only known at the end |
| Using restated financials | Original filing figures differed |
| Using an index's current constituents for historical data | Survivorship (below) |
| Normalising a feature over the whole dataset | Leaks future scale into the past |

Guard: build the signal **bar by bar**, using only data with `timestamp ≤ decision_timestamp`. Shift every input
by at least one bar unless you can prove otherwise. Test: does the signal change if you delete the future? It
must not.

### 1.2 Survivorship bias
Testing only instruments that exist today. Delisted, merged and failed companies are excluded — mechanically
overstating returns.

Guard: use a **point-in-time** universe including delisted names. If you cannot, state the bias explicitly and
expect the result to be optimistic.

### 1.3 Data leakage / snooping
Letting information from the test set influence design.

| Example | Guard |
|---------|-------|
| Choosing the indicator period by looking at full-sample results | Split first, then design |
| Iterating until out-of-sample looks good | Use the holdout **once** |
| Normalising with full-sample statistics | Compute rolling statistics only |
| Using future volatility for position sizing | Point-in-time ATR, shifted |
| Reporting the best of many runs | Report all runs, or pre-register |

### 1.4 Overfitting
Fitting noise. Symptoms:

- Many parameters, each finely tuned.
- Excellent in-sample, poor out-of-sample.
- Performance collapses with a small parameter change (a **spike**, not a **plateau**).
- Rules that describe the sample rather than a mechanism.

Guards:

1. **Few parameters.** Every extra parameter needs more data to justify.
2. **Plateau test.** Vary each parameter ±20%; the result should degrade gracefully, not collapse.
3. **Walk-forward.** Optimise on window 1, test on window 2, roll, repeat. Report the concatenated out-of-sample
   result only.
4. **Out-of-sample holdout.** Reserved data, used once.
5. **Simpler is better.** If two models perform similarly, take the simpler one.
6. **Economic rationale.** If you cannot explain *why* it should work, assume it does not.

## 2. The walk-forward protocol

```
Total data: [==========================================]
Windows:  [train][test]
             [train][test]
                [train][test]
                   [train][test]
Report: the concatenation of the TEST segments only
```

Rules:

- Never re-optimise on the test segment.
- Include costs in every segment.
- Report the parameter drift across windows — unstable parameters are a red flag.
- Minimum: 4–5 folds with a meaningful test window (e.g. 6 months each).

## 3. The multiple-testing correction

If you ran `k` variants, the chance of at least one fluke "winner" at α = 0.05 is `1 − 0.95^k`:

| k | Chance of a fluke winner |
|---|--------------------------|
| 5 | 23% |
| 10 | 40% |
| 20 | 64% |
| 50 | 92% |

Guards: pre-register, use a holdout, or apply a correction (Bonferroni: α/k) — and report how many variants you
tried.

## 4. Backtest audit checklist

- [ ] Signal uses only data available at the decision time
- [ ] Universe is point-in-time (or survivorship bias disclosed)
- [ ] Entry/exit prices are realistic (next-bar open, not the signal bar's close, unless justified)
- [ ] Costs modelled: commission, taxes, slippage
- [ ] Slippage scaled to liquidity and volatility
- [ ] Gaps handled (no fill at the stop price across a gap)
- [ ] Position sizing is part of the test, not applied afterwards
- [ ] Parameters fixed before the test, or walk-forward applied
- [ ] Out-of-sample period untouched during design
- [ ] Number of variants tried is disclosed
- [ ] Regime coverage shown (bull / bear / range)
- [ ] Results reported in R and with drawdown, not just total return
- [ ] Sample size and confidence intervals reported
- [ ] Code and data version recorded for reproducibility

If any box is unchecked, the result is a hypothesis, not evidence.

## 5. The honest reporting sentence

> "This is an in-sample result on 2019–2023 data for 12 instruments, with 14 bps round-trip costs and no slippage
> model. I tested 8 parameter variants and report the best. There is no out-of-sample confirmation. Treat it as a
> hypothesis."

That sentence is worth more than any equity curve, because it tells the reader exactly how much to trust.

## 6. Beginner summary (Hinglish)

**Overfitting:** aapne itne parameters tune kiye ki strategy **sample ko yaad** kar gayi — market ko nahi.

**Pehchaan:** in-sample zabardast, out-of-sample bekaar. Param thoda badlo → result collapse.

**Look-ahead bias:** future ki information use karna. Example: aaj ke close se decide karke aaj hi ke open par
entry — impossible.

**Survivorship bias:** sirf woh stocks test karna jo aaj bhi listed hain. Jo fail ho gaye, woh sample mein nahi —
isliye result optimistic.

**Multiple testing:** 20 variants test karke best dikhana. 20 par 64% chance hai ki ek sirf luck se jeetega.

**Kya karein:** kam parameters, walk-forward test, ek final holdout jo sirf ek baar use ho, aur costs include karo.

## 7. Exercise

Take any simple rule (e.g. "buy when RSI < 30 and price above the 200-EMA"). Test it with three different RSI
periods. Note how different the results are. Then test on a held-out year. Write down: (a) how many variants you
tried, (b) whether the best in-sample was also best out-of-sample, and (c) one sentence on what that says about
optimisation.

---
*See also: [`statistics-basics.md`](statistics-basics.md) · [`../../engines/backtesting/README.md`](../../engines/backtesting/README.md) ·
[`../../strategies/strategy-validation.md`](../../strategies/strategy-validation.md)*
