# CCI (Commodity Channel Index)

**Family:** Momentum oscillator · **Default period:** 20 · **Implementation:** `indicators.cci(h, l, c, 20)`

## 1. Calculation

```
TP_t   = (high + low + close) / 3                    # typical price
MA_t   = SMA(TP, period)_t
MD_t   = mean( |TP_{t−i} − MA_t| ) for i = 0..period−1    # mean absolute deviation
CCI_t  = (TP_t − MA_t) / (0.015 × MD_t)
```

The constant **0.015** is Lambert's scaling factor, chosen so that roughly 70–80% of values fall between
−100 and +100 on his original commodity data. It is a convention, not a law, and it does not guarantee the
same distribution on other instruments.

If `MD = 0` (a perfectly flat window), CCI is undefined — the implementation returns `None`.

## 2. Interpretation

| Reading | Conventional meaning |
|---------|---------------------|
| > +100 | Strong upward momentum (entry signal in the original design); "overbought" in the oscillator reading |
| < −100 | Strong downward momentum; "oversold" |
| +100 → −100 cross | Momentum reversal |
| Beyond ±200 | Extreme; often late-stage |
| Zero-line cross | Trend shift |

**Two contradictory readings coexist in the literature** — momentum (follow the +100 break) and reversion
(fade the ±100 extremes). Which one is correct depends entirely on the regime. In a trend, follow; in a range,
fade. CCI is one of the indicators where the same level means opposite things.

Lambert's original design was a **trend-following** entry: go long when CCI crosses above +100 and the
trend filter is positive. Retail usage often inverts it into a reversion oscillator. Both are in use; state
which you mean.

## 3. Common settings

| Period | Character |
|--------|-----------|
| 20 | Standard |
| 14 | Faster |
| 34 / 50 | Smoother, swing-oriented |

## 4. Limitations

- **Highly regime dependent** (see §2) — the biggest hazard.
- **No bounded range**, so "overbought" has no fixed meaning; ±200 and ±300 both occur.
- **Sensitive to the typical price**; a single large-range bar can dominate the mean deviation.
- **Correlated with RSI and Stochastic.** Not independent evidence.
- **Whipsaw** around ±100 in choppy markets.

## 5. Combining

- **CCI + ADX**: ADX > 25 → treat +100 breaks as continuation entries; ADX < 20 → treat ±100 extremes as
  fade candidates. This resolves the ambiguity above.
- **CCI + structure**: a +100 break through a horizontal resistance is meaningful; a +100 break in the middle
  of a range is not.
- **CCI + volume**: momentum breaks with volume are stronger.
- Use **either** CCI **or** RSI, not both.

## 6. Reading from a screenshot

Extractable: whether the line is above +100 / below −100 (if gridlines show it); whether it is rising or
falling; whether a zero cross happened.

Not extractable: exact values without labels.

## 7. Worked example

```
TP window (period 5): 100, 102, 104, 103, 106
MA = 103.0
deviations: 3, 1, 1, 0, 3 -> MD = 8/5 = 1.6
CCI = (106 − 103) / (0.015 × 1.6) = 3 / 0.024 = 125.0
Reading depends on regime:
  ADX 30 (trend): +125 = momentum continuation signal
  ADX 12 (range): +125 = stretched; fade candidate at resistance
See tests/indicators/test_cci.py.
```

## 8. Beginner summary (Hinglish)

**CCI kya hai?** Typical price (H+L+C)/3 kitna apne average se door hai, usko normalise karke dikhane wala
oscillator. ±100 ke bahar "strong momentum".

**Sabse badi confusion:** kuch log +100 tootne par **kharidte** hain (trend), kuch ±100 par **fade** karte
hain (reversion). Dono literature mein hain.

**Solution:** ADX dekho. ADX > 25 = trend, to follow karo. ADX < 20 = range, to fade karo.

**Yaad rakho:** CCI RSI jaisa hi momentum measure hai — dono ek saath use karna "double confirmation" nahi.

## 9. Exercise

Split one year of data into "ADX > 25" days and "ADX < 20" days. Count how often a CCI +100 break was
followed by a higher close 5 days later in each group. Report both numbers. Write one sentence on why the same
indicator needs two different interpretations.

---
*See also: [`rsi.md`](rsi.md) · [`roc.md`](roc.md) · [`adx.md`](adx.md)*
