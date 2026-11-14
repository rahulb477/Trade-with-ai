# Example — Backtest Disclosure and ML Detection

> **FICTIONAL** strategy and results, generated to demonstrate the disclosure format. No number here is a
> performance claim for anything real.

---

## Part 1 — A backtest, disclosed honestly

### 1.1 Strategy

```
Universe   : 12 fictional large-cap names
Entry      : daily close above the 20-EMA AND RSI(14) crossing above 50
Stop       : 2 × ATR(14) below the entry close
Target     : 4 × ATR(14) above the entry close
Time stop  : 25 sessions
Sizing     : 1% of equity per trade, capped at 10% notional
Filter     : none in v1
```

### 1.2 Data and assumptions

| Item | Value |
|------|-------|
| Bars | 5 years of daily data per name (synthetic for this example) |
| Adjusted | yes |
| Fill | next session's open |
| Intrabar order | stop assumed before target |
| Costs | 12 bps round trip |
| Survivorship | **not controlled** — the universe is the current list, which biases results upward |

That last line is the disclosure that most backtests omit. It alone can add several points of apparent edge.

### 1.3 Results

| Metric | Values |
|--------|--------|
| Trades | 412 |
| Hit rate | 38.4% (95% CI 33.7 – 43.3) |
| Average win | +3.6R |
| Average loss | −1.1R (worse than 1.0 because of gaps) |
| Expectancy | +0.21R |
| Profit factor | 1.32 |
| Max drawdown | 14.8R |
| Longest losing streak | **13** |
| Cost per trade | 0.06R |
| Net expectancy | +0.15R |

**Read the losing streak before the expectancy.** At a 38% hit rate with 412 trades, a 13-trade losing run is
expected, not unlucky. Anyone who cannot sit through 13 losses in a row cannot trade this, regardless of its
arithmetic.

### 1.4 Robustness

| Gate | Result |
|------|--------|
| Parameter plateau (ATR stop 1.6 / 2.0 / 2.4) | +0.18R / +0.21R / +0.17R → plateau ✅ |
| Sub-period stability | positive in 4 of 5 years |
| Instrument breadth | 9 of 12 names positive |
| Regime breakdown | **fails in ranging regimes** (expectancy −0.04R when ADX < 20) |
| Survives 2× costs | +0.09R → marginal ✅ |
| Out-of-sample | **not yet used** |

### 1.5 Honest status

**`PROMISING`** — in-sample plus validation only; the holdout has not been touched.

Required disclosure sentence:

> "This is a PROMISING result on 412 trades over 5 years across 12 instruments, including 12 bps round-trip costs.
> It has not been tested out of sample. It fails in ranging regimes, and survivorship bias was not controlled, which
> probably inflates these figures. It is a historical sample statistic, not a forecast."

### 1.6 What would falsify it

1. Holdout expectancy below +0.05R.
2. Any year with a drawdown beyond 25R.
3. Parameter plateau collapse when the ATR multiple is varied by ±40%.

Written before running the holdout. That ordering is the entire point.

### 1.7 A caveat about the max drawdown

14.8R is the *sample* maximum. The realised maximum over the next 400 trades is unknown and will probably be
larger. Sizing that survives 14.8R but not 25R is sizing that assumes the future resembles the sample — which is
exactly the assumption the sample cannot support.

---

## Part 2 — Why ML pattern detection is not shipped

The repository documents ML-based pattern detection; it does not implement it. Reasons, stated plainly:

| Requirement for a defensible ML detector | Status in this repository |
|------------------------------------------|---------------------------|
| A labelled dataset of patterns | **Not available** (would require licensed data) |
| Labelling by multiple annotators + inter-rater agreement | Not done |
| Point-in-time, survivorship-free data | Not available |
| Out-of-sample protocol | Documented, not executed |
| A reproducible, dependency-free pipeline | Would require numerical libraries (this repo is stdlib-only) |
| Evidence that it beats rule-based detection | Not established |

Shipping a model trained on invented labels would produce confident nonsense, which is precisely what the
repository's rules forbid.

### What *is* shipped instead

| Capability | Implementation |
|-----------|----------------|
| 23 rule-based candle detectors with rule audits | `integrations/python/trading_intel/patterns.py` |
| Quality-scored chart observation | `trading_intel/observation.py` |
| Deterministic synthetic data for testing | `trading_intel/simulate.py` |
| A backtest engine with honesty constraints | `trading_intel/backtest.py` |
| A feature-engineering and discovery *specification* | `engines/strategy-discovery/` |
| A bias and multiple-testing framework | `engines/backtesting/`, `quantitative-intelligence/` |

### If you want to build the ML layer

The documented path:

1. Obtain licensed, point-in-time OHLCV with corporate actions.
2. Define labels operationally (e.g. "return over the next 10 bars exceeds 2 ATR") — not by eyeballing patterns.
3. Split chronologically; never shuffle.
4. Measure inter-rater agreement if humans label anything (a κ below 0.6 means the "pattern" is not well defined).
5. Report the base rate first. If 30% of all bars produce the outcome, a 35% "detection rate" is noise.
6. Correct for the number of configurations tried.
7. Test on a holdout once.

Step 5 is where most published pattern-detection work fails.

---

## Beginner Explanation (Hinglish)

**Backtest:** purane data par rules chala kar dekhna. Yahan 412 trades, 38% hit rate, +0.15R expectancy nikla.

**Do numbers jo sabse zyada matter karte hain:**

1. **13 lagatar losses** — yeh normal hai, unlucky nahi. Jo 13 loss nahi jhel sakta, uske liye strategy "achhi" hone
   se kuch nahi hota.
2. **Ranging market mein strategy fail** hoti hai — matlab ADX < 20 ho to trade band.

**Survivorship bias:** humne sirf **aaj** listed companies ka data liya. Jo companies fail ho gayi, wo data se gayab
hain — isliye result asli se **behtar** dikhta hai. Yeh likhna zaroori hai.

**ML kyun nahi:** ML ko **labels** chahiye (kaunsi candle pattern thi). Labels banane ke liye licensed data aur
multiple annotators chahiye. Bina uske model "confident nonsense" dega — jo is repo mein allowed nahi hai.

**Isliye:** rule-based detectors (23) ship kiye hain, jinme har rule check hota hai. ML ki **specification**
documented hai, implementation nahi.
