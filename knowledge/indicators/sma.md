# Simple Moving Average (SMA)

**Family:** Trend · **Common periods:** 20, 50, 200 · **Implementation:** `indicators.sma(values, period)`

## 1. Calculation

```
SMA_t = (value_{t−period+1} + … + value_t) / period
```

Undefined for the first `period−1` bars. The implementation returns `None`, not an approximated value.

Incremental form (equal by definition, cheaper to compute):

```
SMA_t = SMA_{t−1} + (value_t − value_{t−period}) / period
```

## 2. Interpretation

| Reading | Meaning |
|---------|---------|
| Price above a *rising* SMA | Healthy uptrend |
| Price above a *falling* SMA | Bounce inside a downtrend — often a trap |
| Price below a *falling* SMA | Healthy downtrend |
| Price below a *rising* SMA | Pullback inside an uptrend |
| Flat SMA + price crossing repeatedly | Range; MAs are useless here |
| Golden cross (50 over 200) | Long-term bullish regime shift (lagging by months) |
| Death cross (50 under 200) | Long-term bearish regime shift (lagging) |

**The slope matters as much as the side.** "Price above the 200-SMA" during a falling 200 is a very
different situation from the same statement during a rising 200. Reports should always include slope.

## 3. Common settings

| Period | Role |
|--------|------|
| 10 | Very short (intraday) |
| 20 | Short-term baseline; also the Bollinger middle band |
| 50 | Medium-term; swing reference |
| 100 | Intermediate |
| 200 | The most widely watched long-term line on daily charts |

Weekly 50-SMA approximates the daily 250-SMA; be careful not to treat them as independent evidence.

## 4. Limitations

- **Equal weighting** means a spike stays in the average for exactly `period` bars, then drops out
  abruptly — creating artificial "moves" in the MA.
- **Very lagging** at long periods.
- **Whipsaws** in ranges, badly.
- **Crossovers are late by construction.** Golden/death crosses are regime descriptions, not entries.
- **Split-unadjusted series** produce garbage.

## 5. Combining

- **SMA + price structure**: the 200-SMA is more meaningful when it coincides with a horizontal level.
- **SMA + Bollinger Bands**: the middle band *is* the 20-SMA; do not count them as two studies.
- **SMA + ADX**: ADX filters out the range whipsaw that ruins MA crossovers.
- **SMA slope + ATR**: a rising 50-SMA with contracting ATR = a coiled trend.

## 6. Reading from a screenshot

Extractable: side of the line, slope, distance in visual terms, stacking order of multiple MAs, numeric
label if printed.

Not extractable: exact values without labels; whether the line is a 50 or a 100 if unlabelled (say so).

## 7. Worked example

```
Closes: 10, 11, 12, 13, 14   period 5
SMA = (10+11+12+13+14)/5 = 60/5 = 12.0
Next close 20 → window 11,12,13,14,20 → SMA = 70/5 = 14.0
Note the jump: the 10 dropped out and a 20 came in, moving the average by 2 points in one bar even
though only one price changed. That is the spike-dropout effect described in §4.
See tests/indicators/test_ema.py (SMA cases are covered there).
```

## 8. Beginner summary (Hinglish)

**SMA kya hai?** Pichhle N candles ke close ka simple average.

**Kaise dekhein:**
- Price SMA ke upar + SMA **upar ja raha** hai = trend up.
- Price SMA ke upar par SMA **neeche ja raha** hai = yeh utni achhi baat nahi, bounce ho sakta hai.
- SMA flat + price baar baar cross kare = range, MA bekaar hai.

**200-SMA** sabse zyada dekha jata hai (daily chart par). Golden cross = 50 ne 200 ko upar cross kiya,
death cross = ulta. Yeh **late** signals hain.

**Yaad rakho:** SMA naye price ko utna hi weight deta hai jitna purane ko — isliye woh slow hai.

## 9. Exercise

Take a stock that trended up for a year and one that ranged for a year. Count the number of times price
crossed the 50-SMA in each. Compute the ratio. Explain in one sentence why the same indicator is useless
in the second case — and what you would check *before* using it.

---
*See also: [`ema.md`](ema.md) · [`bollinger-bands.md`](bollinger-bands.md) · [`adx.md`](adx.md)*
