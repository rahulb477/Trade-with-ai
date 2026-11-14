# Exponential Moving Average (EMA)

**Family:** Trend · **Common periods:** 9, 20, 21, 50, 100, 200
**Implementation:** `indicators.ema(values, period)`

## 1. Calculation

```
alpha = 2 / (period + 1)

seed:  EMA_{period} = SMA(values[0..period−1])        # first defined value
then:  EMA_t = alpha × value_t + (1 − alpha) × EMA_{t−1}
```

The seed convention matters. Some platforms seed with the first value, others with an SMA. Over a few
hundred bars the difference becomes negligible; over 30 bars it can be visible. State the convention
if precision matters.

`alpha` for common periods: 9 → 0.20, 20 → 0.0952, 21 → 0.0909, 50 → 0.0392, 200 → 0.00995.

## 2. Interpretation

| Reading | Meaning |
|---------|---------|
| Price above EMA | Short/medium-term trend up |
| Price below EMA | Trend down |
| EMA slope | Direction of the trend, independent of price position |
| Price touching EMA and bouncing | Trend intact — dynamic support/resistance |
| Price closing decisively through EMA | Possible trend change; needs confirmation |
| Fast EMA above slow EMA (e.g. 20 > 50) | Uptrend structure |
| Cross of fast over slow | Regime flip signal (lagging) |

The **200-period EMA** is a widely watched regime divider on daily charts. The **20/21 EMA** is the
common short-term trend guide on intraday and swing charts.

## 3. EMA vs SMA

| Property | EMA | SMA |
|----------|-----|-----|
| Weighting | Recent data weighted more | Equal weights |
| Reaction speed | Faster | Slower |
| Whipsaw | More | Less |
| Best for | Reacting to recent shifts | Defining a stable level |

Neither is "better". EMA reacts sooner and lies more often; SMA reacts later and is smoother. A useful
convention: use an EMA to *follow* a trend and an SMA where a *level* matters (e.g. institutional
reference lines).

## 4. Common settings and their roles

| Period | Role |
|--------|------|
| 9 | Very short-term momentum guide; noisy |
| 20 / 21 | Short-term trend / pullback zone |
| 50 | Medium-term trend (swing) |
| 100 | Intermediate |
| 200 | Long-term regime line |

Multiple EMAs stacked (9 > 20 > 50 > 200) is a "trend alignment" read. It is one piece of evidence with
four components, not four confirmations.

## 5. Limitations

- **Lag.** A 200-EMA is a slow measure; it will not warn you of a reversal.
- **Whipsaw in ranges.** Price oscillates around flat MAs constantly.
- **Not support/resistance in a causal sense.** Price bounces near an EMA because many participants
  watch it — a self-fulfilling reference, not a physical barrier.
- **Repainting-free but seed-sensitive.** Different platforms can show slightly different values at the
  left edge of the chart.
- **Compounding with splits.** Unadjusted price series produce absurd MAs across a split. Verify
  adjustment.

## 6. Combining

- **EMA + ATR:** distance from the EMA in ATR units tells you whether a pullback is normal (0.5–1.5
  ATR) or a breakdown (>3 ATR).
- **EMA + volume:** a break of the 50-EMA on heavy volume is a different event from a quiet drift through
  it.
- **EMA + structure:** a pullback that holds *both* the 20-EMA and a prior swing low is high quality.
- **EMA + Supertrend:** Supertrend is ATR-based and complements a fixed-period MA. Using both is
  mildly redundant; using one plus ATR is cleaner.

## 7. Reading from a screenshot

Extractable: which side of the EMA price is on; the EMA's slope; whether price is touching or extended;
whether MAs are stacked or tangled; the numeric label if printed.

Not extractable: exact EMA value without a label; how long the price has been above it (unless the
visible window covers it).

## 8. Worked example

```
Period 20, alpha = 0.0952
Assume SMA of the first 20 closes = 100.00 (seed)
Next close = 105 → EMA = 0.0952×105 + 0.9048×100 = 10.00 + 90.48 = 100.48
Next close = 103 → EMA = 0.0952×103 + 0.9048×100.48 = 9.81 + 90.91 = 100.72
Price is 2.3% above a slowly rising EMA -> "extended" but trend intact.
See tests/indicators/test_ema.py for assertions against these values.
```

## 9. Beginner summary (Hinglish)

**EMA kya hai?** Ek average jo **naye prices ko zyada weight** deta hai. Isliye yeh SMA se jaldi react
karta hai.

**Kaise use karein:**
- Price EMA ke **upar** = trend up, **neeche** = trend down.
- EMA ka **slope** bhi dekho — flat EMA ka matlab trend nahi.
- Pullback mein price EMA ko touch karke bounce kare = trend healthy.

**Kaunsa period?** Intraday: 9/20. Swing: 20/50. Long-term: 200.

**Dhyan:** EMA lagging hai, aur range market mein price iske around baar baar whipsaw karega.

## 10. Exercise

Plot the 20 and 50 EMA on a daily chart. For every time the 20 crossed the 50, record: was the 200-EMA
rising or falling at that moment? Compare win rates of crosses taken when the 200 was rising vs falling.
Write one sentence about what that filter does to the number of signals.

---
*See also: [`sma.md`](sma.md) · [`supertrend.md`](supertrend.md) · [`atr.md`](atr.md)*
