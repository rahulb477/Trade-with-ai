# MACD (Moving Average Convergence Divergence)

**Family:** Trend/momentum · **Default settings:** 12 / 26 / 9
**Implementation:** `indicators.macd(closes, fast=12, slow=26, signal=9)`

## 1. Calculation

```
MACD_line_t   = EMA(close, 12)_t − EMA(close, 26)_t
signal_line_t = EMA(MACD_line, 9)_t
histogram_t   = MACD_line_t − signal_line_t
```

Notes:

- The EMA seed is the SMA of the first `period` values; thereafter `alpha = 2/(period+1)`.
- The MACD line is only defined once the slow EMA exists (`slow + signal − 1` bars for a full
  histogram). The implementation returns `None` where undefined.
- Some platforms scale the histogram by 2 (a cosmetic choice). If your histogram differs by a factor,
  check this before comparing.

## 2. Interpretation — four distinct readings

| Reading | What it means | Reliability |
|---------|---------------|-------------|
| **MACD above signal** | Shorter-term momentum exceeds longer-term | Moderate — the classic "bullish" state |
| **MACD above zero** | 12-EMA above 26-EMA: medium-term uptrend | Higher as a regime filter |
| **Histogram expanding** | The move is accelerating | Useful for trend health |
| **Histogram contracting** | The move is decelerating | Early warning, not a reversal signal |
| **Zero-line cross** | Regime change (trend flip) | Slower but more meaningful than the signal cross |
| **Signal cross** | Faster, more frequent, more whipsaw | Best used with a trend filter |
| **Divergence** | Price and MACD disagree on a new extreme | Hypothesis only |

**The zero line matters more than the signal line.** A signal cross below zero in a downtrend is
usually noise; the same cross above zero is more informative.

## 3. Common settings

| Fast/Slow/Signal | Character | Use |
|------------------|-----------|-----|
| 12 / 26 / 9 | Standard | Daily and above; the documented default |
| 5 / 35 / 5 | Slower, fewer whipsaws | Positional |
| 8 / 17 / 9 | Faster | Intraday on 15m+ |
| 19 / 39 / 9 | Very slow | Weekly/long-horizon |

Changing settings changes signal timing but never the fundamental lag. Do not optimise settings on the
same data you evaluate on (`engines/backtesting/` §overfitting).

## 4. Limitations

- **Lag.** It is built from two EMAs; by construction it turns after price.
- **Whipsaw in ranges.** The most common failure: repeated signal crosses that each cost a stop.
- **Scale dependence.** MACD values are in price units, so a ₹3,000 stock and a ₹30 stock are not
  comparable. Compare only within an instrument.
- **Not a momentum magnitude measure.** A large histogram means fast EMA separation, not "more upside".
- **Divergences are frequent.** In trending markets they appear constantly and are mostly noise.

## 5. Divergence

```
Bullish : price lower low, MACD higher low (or higher histogram trough)
Bearish : price higher high, MACD lower high
```

Same discipline as RSI: mark `POSSIBLE` until structure breaks. MACD divergences on higher timeframes
(daily/weekly) are more meaningful than intraday ones.

## 6. Combining

Effective combinations:

- **MACD + trend filter (200-EMA)** — only take bullish signal crosses when price is above the 200-EMA.
  This single filter removes most range whipsaw.
- **MACD + volume** — a zero-line cross with volume expansion is materially stronger.
- **MACD + structure** — a signal cross at support, with a bullish candle pattern, is a real setup; the
  same cross mid-range is not.
- **MACD + ADX** — ADX > 20–25 says a trend exists, making MACD crosses meaningful; ADX < 15 says
  ranges, where they are not.

Do not add RSI *and* Stochastic RSI *and* MACD and call it three confirmations: all three are
momentum-derived and often correlated above 0.7.

## 7. Reading from a screenshot

Extractable: whether MACD is above/below zero; whether the histogram is positive/negative; whether a
recent cross occurred; whether the histogram is expanding or contracting; the current numeric label if
printed.

Not extractable: exact historical values, precise cross timing, whether the "divergence" you think you
see is anchored to valid pivots.

## 8. Worked example (procedure, not asserted real data)

```
Given a close series, compute:
  ema12, ema26 -> macd = ema12 - ema26
  signal = ema(macd, 9)
  hist = macd - signal
If macd crosses above signal while price is above the 200-EMA and ADX(14) = 24:
  reading: bullish momentum shift within an established uptrend -> confirmation, not a trigger.
If the same cross occurs with price below the 200-EMA and ADX = 11:
  reading: range noise -> ignore.
The identical pattern has opposite meaning in the two regimes. See tests/indicators/test_macd.py.
```

## 9. Beginner summary (Hinglish)

**MACD kya hai?** Do EMAs (12 aur 26) ka difference, aur uska 9-period average (signal line).

**Teen cheezein dekho:**
1. **MACD line signal line ke upar** → momentum bullish.
2. **MACD zero ke upar** → medium-term uptrend. Yeh zyada important hai.
3. **Histogram bada ho raha hai** → move accelerate ho raha hai; chhota ho raha hai → slow ho raha hai.

**Sabse badi galti:** range market mein MACD ke crosses par trade karna. Wahan woh baar baar galat
hote hain. Pehle trend filter lagao (200-EMA ya ADX).

**Yeh entry trigger nahi hai** — confirmation hai.

## 10. Exercise

Take one year of daily data. Record every MACD signal-line cross. Split them into two groups: crosses
occurring with price above the 200-EMA, and below. Compute the average 10-day forward return of each
group and the share that were "winners" using a 1 ATR target / 1 ATR stop. Then write down whether the
filter helped in your sample — and how large your sample would need to be to trust the answer.

---
*See also: [`ema.md`](ema.md) · [`adx.md`](adx.md) · [`rsi.md`](rsi.md) · [`indicator-combinations.md`](indicator-combinations.md)*
