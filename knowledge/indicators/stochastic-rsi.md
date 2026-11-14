# Stochastic RSI

**Family:** Momentum oscillator · **Default settings:** RSI 14, Stochastic 14, %K 3, %D 3
**Range:** 0–100 · **Implementation:** `indicators.stochastic_rsi(closes, rsi_period=14, stoch_period=14, k=3, d=3)`

## 1. Calculation

```
rsi_series = RSI(close, rsi_period)
stoch_rsi_t = (rsi_t − min(rsi[t−n+1..t])) / (max(rsi[t−n+1..t]) − min(...))     n = stoch_period
%K_t = SMA(stoch_rsi, k) × 100
%D_t = SMA(%K, d)
```

Key point: Stochastic RSI is the stochastic of **RSI**, not of price. It measures where the current RSI
sits within its own recent range. The result is far more sensitive than RSI — it reaches 0 or 100
frequently.

If `max == min` over the window, the indicator is undefined; the implementation returns `None` rather
than 0 or 50.

## 2. Interpretation

| Reading | Meaning |
|---------|---------|
| > 80 | RSI is near the top of its recent range — short-term overbought *relative to itself* |
| < 20 | RSI is near the bottom of its recent range — short-term oversold |
| %K crossing above %D below 20 | Short-term bullish momentum shift |
| %K crossing below %D above 80 | Short-term bearish momentum shift |
| Pinned at 100 | RSI has been rising monotonically — a very strong (or a very over-extended) move |
| Frequent 0↔100 swings | The instrument is chopping; the indicator is saturated noise |

The most important caveat: **saturation is the norm, not the exception.** A Stochastic RSI pinned at 100
says "RSI keeps making new highs" — in a strong trend that is a description of the trend, not a reversal
warning.

## 3. Common settings

| RSI / Stoch / K / D | Character |
|---------------------|-----------|
| 14 / 14 / 3 / 3 | Standard |
| 14 / 7 / 3 / 3 | Faster, more whipsaw |
| 21 / 21 / 5 / 5 | Slower, fewer signals |

## 4. Limitations

- **Doubly derived.** It is a transformation of a transformation, so it amplifies RSI's noise.
- **Not independent of RSI.** Using both as "two confirmations" is a category error.
- **Extremes are meaningless in trends.** Exactly where RSI fails, Stochastic RSI fails twice as often.
- **Very noisy on low timeframes.** On 1-minute charts it is effectively random.
- **Late, tiny signals.** The lag of RSI plus the lag of the stochastic averages.

## 5. Combining

- **Stoch RSI + trend filter**: only take bullish %K/%D crosses when price is above the 50/200-EMA. Without
  this, most crosses are noise.
- **Stoch RSI + structure**: a cross at a support level, with a rejection candle, is a timing tool. A cross
  mid-range is nothing.
- **Stoch RSI as a pullback timer** inside a trend: wait for <20 in an uptrend and a %K cross up.
- **Never** pair it with RSI + CCI and call it a triple confirmation.

## 6. Reading from a screenshot

Extractable: whether the lines are above 80 / below 20 (if gridlines are visible); whether a cross happened
recently; whether the lines are pinned.

Not extractable: exact values without labels; the number of prior crosses.

## 7. Worked example (procedure)

```
rsi_window values: 52, 55, 60, 58, 62, 66, 61, 59, 57, 55, 58, 60, 63, 65
stoch_period 14 -> min 52, max 66, current 65 -> stoch = (65-52)/(66-52) = 0.929 -> 92.9
%K = SMA3 of the last three stoch values; %D = SMA3 of %K
Reading: RSI is near its recent high -> short-term momentum stretched, but if this is a fresh breakout,
"stretched" is the entry condition, not the exit.
See tests/indicators/test_stochastic_rsi.py.
```

## 8. Beginner summary (Hinglish)

**Stochastic RSI kya hai?** RSI ka RSI ke apne recent range ke andar kahan hai — 0 se 100.

**Matlab:**
- **80 ke upar** = RSI apne recent high ke paas (short-term overbought).
- **20 ke neeche** = RSI apne recent low ke paas (short-term oversold).

**Bahut important:** yeh indicator **baar baar 0 aur 100 par chipak jata hai** — strong trend mein 100 par
rehna "reversal" nahi, strength hai.

**Kab use karein?** Sirf timing ke liye, trend ke saath. Uptrend mein 20 ke neeche aaye aur %K upar cross
kare = pullback khatam hone ka hint.

**Galti:** RSI + Stoch RSI dono ko "do confirmation" samajhna. Dono ek hi cheez hain.

## 9. Exercise

Find an uptrend and a range on the same instrument. Count how many %K/%D bullish crosses occurred below 20
in each, and how many were followed by a higher close 5 bars later. Compare the two counts and hit rates.
Write one sentence about where this indicator is worth using.

---
*See also: [`rsi.md`](rsi.md) · [`macd.md`](macd.md) · [`indicator-combinations.md`](indicator-combinations.md)*
