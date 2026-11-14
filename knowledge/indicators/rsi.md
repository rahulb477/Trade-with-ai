# Relative Strength Index (RSI)

**Family:** Momentum oscillator · **Default period:** 14 · **Range:** 0–100
**Implementation:** `indicators.rsi(closes, period=14)`

## 1. Calculation

```
change_t = close_t − close_{t−1}
gain_t   = max(change_t, 0)
loss_t   = max(−change_t, 0)

# first average = simple mean of the first `period` values
avg_gain_1 = Σ gain[1..period] / period
avg_loss_1 = Σ loss[1..period] / period

# thereafter: Wilder smoothing (equivalent to an EMA with alpha = 1/period)
avg_gain_t = (avg_gain_{t−1} × (period−1) + gain_t) / period
avg_loss_t = (avg_loss_{t−1} × (period−1) + loss_t) / period

RS  = avg_gain / avg_loss
RSI = 100 − 100 / (1 + RS)
```

Edge cases (implemented explicitly):

| Case | Result |
|------|--------|
| `avg_loss == 0` and `avg_gain > 0` | RSI = 100 |
| `avg_gain == 0` and `avg_loss > 0` | RSI = 0 |
| both zero (flat price) | RSI = 50 by convention; flag as undefined rather than meaningful |
| fewer than `period+1` closes | `None` (undefined) — never fabricate |

Variants you may encounter: **Cutler's RSI** uses a simple moving average instead of Wilder
smoothing — the values differ, sometimes by several points. If a chart's RSI disagrees with yours,
check the smoothing method first.

## 2. Interpretation

| Zone | Conventional reading | Reality check |
|------|---------------------|---------------|
| > 80 | Extremely overbought | Common in strong uptrends; not a short signal |
| 70–80 | Overbought | Momentum strong; trend continuation likely while above 40–50 |
| 50–70 | Bullish momentum | The useful "healthy trend" band |
| 40–50 | Neutral / weak | Watch for direction |
| 30–40 | Bearish momentum | Trend continuation likely while below 60 |
| 20–30 | Oversold | Common in strong downtrends; not a buy signal |
| < 20 | Extremely oversold | Panic; can persist |

Three readings that actually carry information:

1. **The 50-line as a trend filter.** In an uptrend RSI tends to hold above 40–50 on pullbacks; in a
   downtrend it tends to cap below 50–60 on bounces.
2. **Failure swings.** In an uptrend: RSI makes a high, pulls back, makes a *lower* high while price
   makes a *higher* high → momentum is weakening.
3. **Divergence** (see §5) — treated as a hypothesis, never as an entry trigger.

## 3. Common settings

| Setting | Use | Notes |
|---------|-----|-------|
| 14 | Default everywhere | The documented standard |
| 9 | Faster, noisier | Scalping; many more false extremes |
| 21 / 25 | Slower, smoother | Swing/positional |
| 2 / 50–100 | Very short/long | Rarely useful |

## 4. Limitations

- **Saturates in trends.** During a strong move, RSI can stay >70 for weeks. "Overbought" is a state,
  not a countdown.
- **Lagging.** It is built from past closes; it cannot lead price.
- **Regime dependent.** Best in ranges; worst in trends (for mean-reversion use).
- **Period sensitivity.** RSI 9 and RSI 14 can give opposite signals on the same bar.
- **Not comparable across instruments.** RSI 30 on a volatile small cap and on an index indicate
  different things.
- **Divergence is subjective.** Choice of pivot points changes the conclusion entirely.

## 5. Divergence, properly

```
Bullish divergence : price makes a LOWER low; RSI makes a HIGHER low.
Bearish divergence : price makes a HIGHER high; RSI makes a LOWER high.
Hidden (bullish)   : price higher low, RSI lower low → trend continuation signal.
Hidden (bearish)   : price lower high, RSI higher high → trend continuation signal.
```

Requirements before calling a divergence:

1. Both pivots must be visible and identifiable swing points (not adjacent bars).
2. There must be a meaningful time separation (at least several bars).
3. It must be flagged as `POSSIBLE` until price breaks the intervening structure.
4. On a screenshot, state that the reading is approximate.

Divergences are among the most over-claimed observations in chart analysis. A divergence without a
structural break is not actionable.

## 6. Combining

- RSI + **structure**: RSI overbought *at resistance* with a rejection candle is meaningful; RSI
  overbought mid-trend is not.
- RSI + **ATR/volatility**: after a volatility contraction, an RSI swing out of the 45–55 band often
  precedes a directional move.
- RSI + **volume**: divergence with falling volume on the price highs is a stronger warning.
- Do **not** pair RSI with Stochastic RSI or CCI and call it three confirmations — it is one.

## 7. Reading it from a screenshot

- If the numeric value is printed, quote it: "RSI(14) = 61.3".
- If only the line is visible, describe position relative to 50 and to the 70/30 gridlines, and mark it
  approximate.
- Do not convert pixels to a value.

## 8. Worked example

```
Closes (fictional, 16 values): 100,101,102,101,103,104,103,105,106,104,106,108,107,109,110,108
period = 14
gains: 1,1,0,2,1,0,2,1,0,2,2,0,2,1,0  -> sum 15, first avg_gain = 15/14 = 1.0714
losses:0,0,1,0,0,1,0,0,2,0,0,1,0,0,2  -> sum 7,  first avg_loss = 7/14 = 0.5
RS = 1.0714/0.5 = 2.1429  -> RSI = 100 − 100/3.1429 = 68.2
Reading: bullish momentum, approaching but not at overbought. In an uptrend this is a "healthy" read.
See tests/indicators/test_rsi.py for the assertable version of this calculation.
```

## 9. Beginner summary (Hinglish)

**RSI kya batata hai?** Pichhle kuch candles mein gains aur losses ka ratio — 0 se 100 ke scale par.

**Upar (70+) = overbought:** matlab bahut tezi se upar chala hai. **Yeh sell signal nahi hai** — strong
trend mein RSI 80 par hafton reh sakta hai.

**Neeche (30−) = oversold:** bahut gir gaya. Yeh buy signal nahi hai.

**Asli kaam:** 50 line ke around behaviour dekhna. Uptrend mein RSI pullback par 40–50 ke upar hold
karta hai. Downtrend mein 60 ke neeche ruk jata hai.

**Sabse important limitation:** RSI lagging hai — sirf past data se banta hai. Aur ek hi cheez ko
teen oscillators se "confirm" karna confirmation nahi hai.

## 10. Exercise

1. On a daily chart, mark every RSI reading above 70 over one year. Count how many were followed by a
   lower close 5 days later, and how many by a higher close. Do the same for readings below 30.
2. Compare the "overbought → shorted" result against "overbought in an uptrend → held long". Write two
   sentences on why the regime mattered more than the level.

---
*See also: [`macd.md`](macd.md) · [`stochastic-rsi.md`](stochastic-rsi.md) · [`README.md`](README.md) §2*
