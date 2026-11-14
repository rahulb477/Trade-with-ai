# Indicators — Index and Principles

18 indicators, each with calculation methodology, interpretation, limitations, common settings, and
how to combine them without stacking redundant information.

Tested implementations: `integrations/python/trading_intel/indicators.py`.

---

## 1. What an indicator actually is

An indicator is a **transformation of price and/or volume**. It contains no information that was not
already in the input. Its value is that it makes one property easier to see:

| Family | Makes visible | Examples |
|--------|---------------|----------|
| **Trend** | Direction and persistence | SMA, EMA, Supertrend, Ichimoku, ADX |
| **Momentum** | Speed of change | RSI, MACD, Stochastic RSI, ROC, CCI, MFI |
| **Volatility** | Size of movement | ATR, Bollinger Bands |
| **Volume/participation** | Effort behind moves | OBV, VWAP, Volume Profile, MFI |
| **Levels** | Reference prices | Pivot Points, Fibonacci, Volume Profile POC |

**Consequence:** an indicator cannot tell you something price did not. When an indicator and price
structure disagree, price structure wins — the indicator is a derived quantity.

---

## 2. The eight rules of indicator use

1. **Never use an indicator as a sole reason to enter.** It is confirmation, not a trigger.
2. **Two oscillators measuring the same thing are one piece of evidence.** RSI + Stochastic RSI + CCI
   ≈ one momentum reading, not three.
3. **State the period.** "RSI is oversold" without the period and the value is not a statement.
4. **Respect the setting's context.** RSI 14 on a daily chart and RSI 14 on a 1-minute chart behave
   completely differently.
5. **Divergence is a hypothesis, not a signal.** Divergences can persist for months.
6. **Overbought ≠ short.** In strong trends RSI stays above 70 for extended periods.
7. **Indicators lag by construction.** A 200-EMA knows nothing about the last three minutes.
8. **If it is not visible on the chart, do not invent it.** Report "not visible" (see
   `core/evidence-engine.md`).

---

## 3. Reading an indicator panel from a screenshot

What you can and cannot extract:

| Element | Extractable? |
|---------|--------------|
| Current value, if printed as a number label | Yes — quote it exactly |
| Whether the line is above/below its centreline | Yes |
| Whether two lines recently crossed | Yes (approximate date) |
| Whether the line is at an extreme | Yes, if the panel has a visible scale (e.g. 0/50/100 gridlines) |
| Exact historical values | No |
| Whether a divergence exists | Approximately — this is the riskiest visual reading; flag it as approximate |

**Never** convert a pixel height into an indicator value. If the value is not printed, say
"approximate position on the panel, value not shown".

---

## 4. Catalogue

### Trend

| Indicator | File | Typical settings |
|-----------|------|------------------|
| Simple Moving Average | [`sma.md`](sma.md) | 20, 50, 200 |
| Exponential Moving Average | [`ema.md`](ema.md) | 9, 20, 21, 50, 200 |
| Supertrend | [`supertrend.md`](supertrend.md) | (10, 3) or (7, 3) |
| Ichimoku Cloud | [`ichimoku-cloud.md`](ichimoku-cloud.md) | 9 / 26 / 52 |
| Average Directional Index | [`adx.md`](adx.md) | 14 |

### Momentum

| Indicator | File | Typical settings |
|-----------|------|------------------|
| Relative Strength Index | [`rsi.md`](rsi.md) | 14 |
| MACD | [`macd.md`](macd.md) | 12 / 26 / 9 |
| Stochastic RSI | [`stochastic-rsi.md`](stochastic-rsi.md) | 14, 14, 3, 3 |
| Rate of Change | [`roc.md`](roc.md) | 12 or 9 |
| Commodity Channel Index | [`cci.md`](cci.md) | 20 |
| Money Flow Index | [`mfi.md`](mfi.md) | 14 |

### Volatility

| Indicator | File | Typical settings |
|-----------|------|------------------|
| Average True Range | [`atr.md`](atr.md) | 14 |
| Bollinger Bands | [`bollinger-bands.md`](bollinger-bands.md) | 20, 2σ |

### Volume / participation

| Indicator | File | Typical settings |
|-----------|------|------------------|
| On-Balance Volume | [`obv.md`](obv.md) | — |
| Volume Weighted Average Price | [`vwap.md`](vwap.md) | session (resets daily) |
| Volume Profile | [`volume-profile.md`](volume-profile.md) | session or composite |

### Levels

| Indicator | File | Typical settings |
|-----------|------|------------------|
| Fibonacci Retracement | [`fibonacci.md`](fibonacci.md) | 0.236 / 0.382 / 0.5 / 0.618 / 0.786 |
| Pivot Points | [`pivot-points.md`](pivot-points.md) | Classic / Fibonacci / Camarilla |

### Cross-cutting

[`indicator-combinations.md`](indicator-combinations.md) — how to build a non-redundant set, and the
common stacks that work.

---

## 5. Choosing a set (not a pile)

A workable, non-redundant stack for chart reading:

```
Trend      : one MA family (price vs 20/50 EMA) or Supertrend
Momentum   : ONE oscillator (RSI or MACD — not both as "confirmation")
Volatility : ATR (for stop distance and position sizing)
Volume     : OBV or the raw volume panel
Levels     : pivot points or the visible structure
```

That is 4–5 studies. Ten indicators on a chart is a sign of uncertainty, not rigour.

---

## 6. Indicator–regime mismatch (the most common error)

| Regime | Works | Fails badly |
|--------|-------|-------------|
| Strong trend | MAs, Supertrend, ADX, pullback-to-MA entries | RSI overbought/oversold, mean reversion, Bollinger extremes |
| Range | RSI extremes, Bollinger bands, pivot points | MA crossovers (constant whipsaw), Supertrend |
| Low volatility squeeze | Bollinger bandwidth, inside bars | Breakout indicators that fire on noise |
| High volatility / news | ATR for sizing; nothing for direction | Every oscillator (they saturate) |

Detect the regime **first** (`engines/market-intelligence/market-regime.md`), then choose the study.
Applying a range indicator in a trend is the single most common way beginners lose money with
otherwise-correct analysis.

---

## 7. Honest reporting template

For each visible indicator, report:

```
Name / period : RSI (14) — printed on panel
Value         : 61.3 (label visible)
Reading       : above 50, below 70 → bullish momentum, not overbought
Divergence    : price made a higher high at 14:05 while RSI made a lower high → POSSIBLE bearish
                divergence; flagged approximate because only the last two peaks are visible
Limitation    : RSI 14 on 15m is noisy; on this timeframe it saturates during news
```

If the period is not printed: `ASSUMED 14 (not printed)` — and say so in section 10 of the report.

---

*Tests: `tests/indicators/` · Reference formulas cross-checked against the standard definitions given
in each file.*
