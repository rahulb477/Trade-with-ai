# Indicator Combinations — Building a Non-Redundant Set

The goal is **independent evidence**, not a large number of lines on a chart.

---

## 1. The redundancy problem

Indicators are transformations of the same two inputs (price and volume). Many are mathematically related:

| Group | Members | Correlation in practice |
|-------|---------|------------------------|
| Momentum oscillators | RSI, Stochastic, Stochastic RSI, CCI, MFI, Williams %R | High (0.6–0.9) — one piece of evidence |
| Trend averages | SMA, EMA, WMA, HMA, Supertrend, Ichimoku lines | Very high — one piece of evidence |
| Volatility | ATR, Bollinger width, standard deviation, Keltner width | Very high — one piece of evidence |
| Cumulative volume | OBV, CVD, A/D line | High (CVD is genuinely different when bid/ask data exists) |

Stacking within a group multiplies the *appearance* of confirmation without adding information. This is the
most common way an AI (or a human) manufactures false confidence — see `core/evidence-engine.md` §6.

**Test:** if you removed all indicators of a group except one, would your conclusion change? If not, the others
were decoration.

---

## 2. Independent evidence classes

Aim for at most **one indicator per class**, plus structure and volume:

```
1. Structure      swing highs/lows, trend, S/R      (not an indicator — the primary evidence)
2. Trend          one of: EMA/SMA stack, Supertrend, Ichimoku
3. Momentum       one of: RSI, MACD, CCI, ROC
4. Volatility     one of: ATR, Bollinger width
5. Participation  one of: volume panel, OBV, VWAP, volume profile
6. Context        news/sector/index (cited)
```

Six classes maximum. Most real analyses use four.

---

## 3. Combinations that work (with reasons)

### 3.1 Trend continuation

```
Structure : HH/HL intact
Trend     : price above rising 20/50 EMA
Momentum  : RSI holds above 40–50 on pullbacks
Volatility: ATR stable or contracting
Trigger   : pullback into EMA/support + bullish candle closing back up
Why it works: four independent statements all describing demand. The trigger is a price event, not an indicator.
```

### 3.2 Range fade

```
Structure : flat range with ≥2 touches each side
Trend     : ADX < 20, MAs flat
Momentum  : RSI/Stoch at an extreme (confirmation only)
Volatility: ATR low and stable
Trigger   : rejection candle at the range boundary with a close back inside
Why it works: the range is the thesis; the oscillator only confirms the boundary was stretched.
```

### 3.3 Squeeze breakout

```
Structure : compression (inside bars, triangle, narrowing range)
Volatility: Bollinger bandwidth at a multi-month low
Trend     : ADX low (pre-trend)
Participation: volume expanding on the breakout bar
Trigger   : close beyond the compression boundary + volume ≥ 1.5× average
Why it works: volatility contraction is a measured fact, and the breakout bar supplies the direction.
Note      : the squeeze does NOT predict direction — only that expansion is likely.
```

### 3.4 Trend reversal (the hardest, and where most losses occur)

```
Structure : trend break (LH after HH, or LL after HL) + level loss
Trend     : MA cross or price closing below the 50-EMA
Momentum  : divergence (supporting, never the reason)
Volatility: ATR rising (reversal moves are volatile)
Trigger   : retest of the broken level fails
Why it works: requires an actual structural change, not just an oscillator reading.
Warning   : reversals are the lowest-probability category. Prefer continuation until structure breaks.
```

---

## 4. Combinations that fail (and why)

| Combination | Problem |
|-------------|---------|
| RSI + Stochastic + CCI "all oversold" | One momentum reading, three times |
| 4 MAs all pointing up | One trend statement |
| Bollinger + ATR + Keltner "volatility confirmed" | One volatility reading |
| MACD cross in a range | Whipsaw generator |
| RSI overbought → short in a strong uptrend | Fighting the regime |
| Indicator divergence with no structural break | Hypothesis, not a signal |
| Ten indicators "agreeing" | Almost certainly redundant; count classes instead |

---

## 5. Regime-first selection table

| Regime (detect first) | Use | Avoid |
|-----------------------|-----|-------|
| Strong trend (ADX > 25, stacked MAs) | EMA pullbacks, Supertrend trail, MACD zero-line, ROC | RSI/Stoch extremes, Bollinger fades |
| Range (ADX < 20, flat MAs) | RSI/Stoch extremes, Bollinger bands, pivots, volume profile | MA crossovers, Supertrend |
| Squeeze (low ATR, low bandwidth) | Compression levels + volume; straddle planning | Oscillators (they saturate) |
| High volatility / event | ATR for sizing only | Everything directional |
| Unclear / transitioning | Nothing — WAIT | Everything |

Regime detection: `engines/market-intelligence/market-regime.md`.

---

## 6. The two-indicator rule (for beginners)

If you must simplify to the extreme, use exactly two:

1. **One trend filter** — e.g. price vs the 50-EMA (or ADX > 20).
2. **One trigger** — e.g. a candle pattern at a level, confirmed by a close.

Everything else is optional. A beginner with two studies and good risk control outperforms one with twelve
studies and no plan — not because the two studies are better, but because the plan is executable.

---

## 7. Reporting template

```
Regime          : trending up (ADX 27, MAs stacked)
Trend evidence  : price above rising 20/50 EMA — class 2
Momentum        : RSI(14) = 58, above 50, not overbought — class 3
Volatility      : ATR(14) = 18, ~1.5% of price, stable — class 4
Participation   : volume 1.4× average on the last up bar — class 5
Structure       : HH/HL intact, pullback held 1_198 — class 1
Independent classes: 5 -> confidence: Moderate (no material conflict)
Redundancy check: no two studies measure the same property
```

If two of those lines measure the same property, delete one and lower the confidence by a rung.

---

*See also: [`README.md`](README.md) §2, §6 · [`adx.md`](adx.md) · [`../core/evidence-engine.md`](../../core/evidence-engine.md) §6*
