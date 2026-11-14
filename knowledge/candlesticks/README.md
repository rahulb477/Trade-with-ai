# Candlestick Encyclopedia — Index and Foundations

26 pattern **variants** across 25 files (abandoned baby covers both directions), each documented
with formation rules, context requirements, confirmation, volume behaviour, paper-trade entry,
invalidation, false signals, evidence honesty, and an exercise.

Read this file first. A pattern without its context rules is decoration.

---

## 1. Anatomy of a candle

```
        │            <- upper wick (shadow): rejected highs
      ┌─┴─┐
      │   │          <- body: open to close
      │   │             bullish: close > open
      └─┬─┘             bearish: close < open
        │            <- lower wick: rejected lows
```

| Field | Meaning | What it reveals |
|-------|---------|-----------------|
| Open | First traded price in the interval | Where participants agreed to start |
| High | Maximum traded price | The extreme buyers reached |
| Low | Minimum traded price | The extreme sellers reached |
| Close | Last traded price | **The most important field** — the settlement of the interval |
| Body | `|close − open|` | Conviction: large body = one side dominated |
| Upper wick | `high − max(open, close)` | Supply above / failed upside |
| Lower wick | `min(open, close) − low` | Demand below / failed downside |
| Range | `high − low` | Volatility in that interval |

Normalised measures used throughout this encyclopedia:

```
body_ratio   = body / range                 (0 = doji, 1 = marubozu)
upper_ratio  = upper_wick / range
lower_ratio  = lower_wick / range
close_pos    = (close − low) / range         (1 = closed at the high)
```

These are what the detectors in `integrations/python/trading_intel/patterns.py` use.

---

## 2. The confirmation hierarchy (most important page in this section)

A candle is a **single-interval observation of a tug-of-war**. It tells you who won that interval.
It does **not** tell you who will win the next one.

Ranked from weakest to strongest evidence:

| Level | Evidence | Comment |
|-------|----------|---------|
| 0 | A candle that looks like a pattern | Noise. Nothing. |
| 1 | Pattern + appears at a meaningful location (S/R, trendline, Fib) | Location is half the signal |
| 2 | Pattern + location + **volume** expansion in the pattern's direction | Participation confirms intent |
| 3 | Pattern + location + volume + **next candle closes** in the pattern's direction | Confirmation |
| 4 | All of the above + **higher timeframe agrees** | Confluence |
| 5 | All of the above + a **structure break** (swing high/low taken) + retest holds | Actionable setup |

The repository's rule: an entry requires level **3 or above** for a candle-based setup, and level
**4** if the higher timeframe is available and contradicts.

Two corollaries:

1. **A pattern is a hypothesis, not a signal.** Name the rules it satisfies.
2. **Location beats shape.** A mediocre hammer at major support beats a textbook hammer in the
   middle of nowhere.

---

## 3. Context rules that apply to every pattern

| Rule | Explanation |
|------|-------------|
| **Prior trend required** | Reversal patterns need a trend to reverse. A "hammer" after three sideways candles is a long-legged doji with a name. |
| **Location required** | At support for bullish, at resistance for bearish, or at a trend extreme. |
| **Size relative to neighbours** | The pattern candle should be visibly larger than the recent average range (≥1.2× is a reasonable screen). |
| **A close is required** | An open/forming candle cannot confirm anything. Status = `DEVELOPING`. |
| **Colour is secondary, position is primary** | Many strong reversal candles have ambiguous colours. Body position and wick structure matter more. |
| **Chart type matters** | Heikin-Ashi, Renko and line charts do not produce valid OHLC patterns. Refuse on those. |
| **Adjustment matters** | Splits and bonuses create fake gaps that look like patterns. Verify the series is adjusted. |

---

## 4. Reliability language used here

You will not find invented win rates in this repository. Instead each pattern carries a
**qualitative reliability band** with its reasoning:

| Band | Meaning |
|------|---------|
| **Higher** | Requires more conditions, therefore rarer and more informative (e.g. morning star, three white soldiers) |
| **Moderate** | Common and useful *with* confluence (e.g. hammer, engulfing) |
| **Lower** | Very common, mostly noise alone (e.g. doji, spinning top, single inside bar) |
| **Contextual** | Meaningful only as a continuation or only inside a trend (e.g. rising three methods) |

Published reference works (Bulkowski's *Encyclopedia of Candlestick Charts*, Nison's
*Japanese Candlestick Charting Techniques*) contain measured performance statistics. **We do not
reproduce their numbers as fact.** If a user wants a base rate, the honest path is
`engines/backtesting/` on their own instrument, timeframe and period. See §5.

---

## 5. How to establish your own base rates

Documented method (implementation in `engines/backtesting/` and
`integrations/python/trading_intel/backtest.py`):

1. Define the rule mechanically (all formation conditions as code).
2. Scan N years of adjusted OHLC for the instrument and timeframe.
3. For each occurrence, define outcome at a fixed horizon AND at first-touch of ±1 ATR.
4. Exclude look-ahead: only use data available at the signal bar's close.
5. Report sample size, win rate with a confidence interval, average R, and max adverse excursion.
6. Split in-sample and out-of-sample; report both.
7. Include costs.

A pattern with 12 occurrences is not evidence. A pattern with 400 occurrences across two
instruments and two regimes is a start.

---

## 6. The pattern catalogue (26 variants / 25 files)

### Bullish reversal

| Pattern | Candles | Reliability | File |
|---------|---------|-------------|------|
| Hammer | 1 | Moderate | [`hammer.md`](hammer.md) |
| Inverted Hammer | 1 | Moderate (weaker) | [`inverted-hammer.md`](inverted-hammer.md) |
| Bullish Engulfing | 2 | Moderate–Higher | [`bullish-engulfing.md`](bullish-engulfing.md) |
| Morning Star | 3 | Higher | [`morning-star.md`](morning-star.md) |
| Piercing Pattern | 2 | Moderate | [`piercing-pattern.md`](piercing-pattern.md) |
| Three White Soldiers | 3 | Higher | [`three-white-soldiers.md`](three-white-soldiers.md) |
| Tweezer Bottom | 2 | Lower–Moderate | [`tweezer-bottom.md`](tweezer-bottom.md) |
| Three Inside Up | 3 | Moderate–Higher | [`three-inside-up.md`](three-inside-up.md) |
| Abandoned Baby (bullish) | 3 | Higher (rare) | [`abandoned-baby.md`](abandoned-baby.md) |

### Bearish reversal

| Pattern | Candles | Reliability | File |
|---------|---------|-------------|------|
| Shooting Star | 1 | Moderate | [`shooting-star.md`](shooting-star.md) |
| Hanging Man | 1 | Moderate (needs confirmation) | [`hanging-man.md`](hanging-man.md) |
| Bearish Engulfing | 2 | Moderate–Higher | [`bearish-engulfing.md`](bearish-engulfing.md) |
| Evening Star | 3 | Higher | [`evening-star.md`](evening-star.md) |
| Dark Cloud Cover | 2 | Moderate | [`dark-cloud-cover.md`](dark-cloud-cover.md) |
| Three Black Crows | 3 | Higher | [`three-black-crows.md`](three-black-crows.md) |
| Tweezer Top | 2 | Lower–Moderate | [`tweezer-top.md`](tweezer-top.md) |
| Three Inside Down | 3 | Moderate–Higher | [`three-inside-down.md`](three-inside-down.md) |
| Abandoned Baby (bearish) | 3 | Higher (rare) | [`abandoned-baby.md`](abandoned-baby.md) |

### Neutral / indecision

| Pattern | Candles | Reliability | File |
|---------|---------|-------------|------|
| Doji | 1 | Lower (information about balance) | [`doji.md`](doji.md) |
| Spinning Top | 1 | Lower | [`spinning-top.md`](spinning-top.md) |
| High Wave | 1 | Lower | [`high-wave.md`](high-wave.md) |
| Inside Bar | 2 | Contextual | [`inside-bar.md`](inside-bar.md) |
| Harami | 2 | Moderate | [`harami.md`](harami.md) |

### Continuation / strength

| Pattern | Candles | Reliability | File |
|---------|---------|-------------|------|
| Rising Three Methods | 5 | Higher | [`rising-three-methods.md`](rising-three-methods.md) |
| Falling Three Methods | 5 | Higher | [`falling-three-methods.md`](falling-three-methods.md) |
| Marubozu | 1 | Contextual | [`marubozu.md`](marubozu.md) |

---

## 7. Naming discipline in reports

Always attach: **name + status + rule audit + location**.

> ✅ "Hammer (`CONFIRMED`, closed today) at the 1_140 support that held twice in October, on
> 1.6× average volume."

> ❌ "Hammer. Bullish."

If a pattern fails one rule, use `POSSIBLE` and name the failure:

> "Bullish engulfing (`POSSIBLE`) — the second body engulfs the first, but the close does not
> exceed the prior swing high, so it lacks structural confirmation."

---

## 8. Common beginner errors

1. Trading every doji as a reversal. Dojis indicate *indecision*, which at a trend extreme is
   useful and mid-trend is noise.
2. Ignoring the preceding trend. Most "reversal patterns" are meaningless without a trend.
3. Counting an open candle as a completed pattern.
4. Forgetting that a hammer's low is the natural invalidation point — if the low is 9% away, the
   setup is untradeable no matter how pretty the candle.
5. Using a lower-timeframe pattern against a strong higher-timeframe trend and calling it a
   reversal. It is a pullback until proven otherwise.
6. Stacking five patterns on the same candle and calling it "high confluence". They are the same
   information counted five times (see `core/evidence-engine.md` §6).

---

*Detectors: `integrations/python/trading_intel/patterns.py` · Tests: `tests/chart-recognition/` ·
Teaching aids: [`../education/`](../education/)*
