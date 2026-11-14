# Supertrend

**Family:** Trend (ATR-based) · **Default settings:** period 10, multiplier 3
**Implementation:** `indicators.supertrend(highs, lows, closes, period=10, multiplier=3.0)`

## 1. Calculation

```
ATR_t = ATR(period)_t                                  # Wilder smoothing
mid_t = (high_t + low_t) / 2

basic_upper_t = mid_t + multiplier × ATR_t
basic_lower_t = mid_t − multiplier × ATR_t

# final bands carry forward unless the basic band is violated:
final_upper_t = basic_upper_t if (basic_upper_t < final_upper_{t−1} or close_{t−1} > final_upper_{t−1})
                else final_upper_{t−1}
final_lower_t = basic_lower_t if (basic_lower_t > final_lower_{t−1} or close_{t−1} < final_lower_{t−1})
                else final_lower_{t−1}

# trend:
if close_t > final_upper_t:   trend = UP,   line = final_lower_t (support side)
elif close_t < final_lower_t: trend = DOWN, line = final_upper_t (resistance side)
else: trend unchanged, line stays on the active side
```

The band-carrying logic is what makes Supertrend a *trailing* structure rather than a simple
envelope. Implementations differ in small details — if your platform's Supertrend differs by a few
points, that is why. Document the convention you used.

## 2. Interpretation

| Reading | Meaning |
|---------|---------|
| Line below price (green) | Uptrend; the line is trailing support |
| Line above price (red) | Downtrend; the line is trailing resistance |
| Flip from red to green | Trend change signal — price closed above the upper band |
| Flip from green to red | Trend change signal |
| Price holding above the green line repeatedly | Trend intact |
| Frequent flips | Range; Supertrend is at its worst here |

Because the line trails by `multiplier × ATR`, its distance from price is a volatility-scaled stop. It is
therefore useful as a **mechanical invalidation reference**, not only as a direction filter.

## 3. Common settings

| Period / Multiplier | Character |
|---------------------|-----------|
| 10 / 3 | Standard; balanced |
| 7 / 3 | Faster flips; more whipsaw |
| 10 / 1.5 | Tighter; exits early |
| 10 / 5 | Very slow; fewer flips, larger giveback |
| 20 / 2 | Smoother trend filter for swing |

The multiplier controls how much noise is tolerated. Raising it reduces whipsaws but increases the loss
when a trend finally breaks.

## 4. Limitations

- **Whipsaws in ranges.** The defining weakness: repeated flips each costing a stop.
- **Lagging by design.** ATR-based bands trail price.
- **Parameter sensitivity.** Results change materially with (period, multiplier) — a classic overfitting
  trap (`engines/backtesting/` §overfitting).
- **No volume awareness.** It cannot distinguish a breakout with participation from one without.
- **Repaints on some platforms.** Verify that your platform does not recalculate historical bands.

## 5. Combining

- **Supertrend + ADX**: only act on flips when ADX > ~20. This removes a large share of range whipsaw.
- **Supertrend + structure**: a flip that coincides with a break of a swing high is stronger than a flip
  in the middle of a range.
- **Supertrend as a stop**: use the line as a trailing invalidation. Its ATR scaling makes it adapt to
  volatility better than a fixed %.
- **Supertrend + RSI**: use RSI only for pullback timing inside a Supertrend uptrend, not as a second
  trend confirmation.

## 6. Reading from a screenshot

Extractable: line colour/side; whether a flip occurred recently; distance from price to line in visual
terms; number of flips in the visible window.

Not extractable: the exact line value without a label; the period/multiplier if not printed (state the
assumption: `ASSUMED 10/3`).

## 7. Worked example (procedure)

```
ATR(10) = 12 ; mid = 1_240 -> basic_upper = 1_240 + 3×12 = 1_276 ; basic_lower = 1_204
Suppose prior final_lower was 1_190 and close is above it -> final_lower becomes 1_204 (rising).
Price at 1_252 -> above final_lower, trend UP, trailing support 1_204.
If price later closes below 1_204, the trend flips and the line becomes resistance.
Interpretation: a mechanical trail 48 points below price, = 4 × ATR, wide for an intraday stop.
See tests/indicators/test_supertrend.py.
```

## 8. Beginner summary (Hinglish)

**Supertrend kya hai?** ATR (volatility) ke hisaab se bani ek line jo price ke saath **trail** karti hai.

- Line price ke **neeche** (green) = uptrend.
- Line price ke **upar** (red) = downtrend.
- Line flip ho jaye = trend change ka signal.

**Fayda:** volatility ke hisaab se line adjust hoti hai, isliye stop bhi automatic volatility-adjusted
hota hai.

**Nuksan:** range market mein yeh baar baar flip karega aur har flip ek chhota loss hoga.

**Fix:** ADX ke saath use karo — ADX 20 se neeche ho to Supertrend ke signals ignore karo.

## 9. Exercise

Run Supertrend (10,3) on a ranging stock and a trending stock for one year. Count flips in each and the
average loss per flip (entry at close of the flip bar, exit at the next flip). Compare the two totals.
Then add an ADX > 20 filter and repeat. Write down what changed and what stayed the same.

---
*See also: [`atr.md`](atr.md) · [`adx.md`](adx.md) · [`ema.md`](ema.md) · [`indicator-combinations.md`](indicator-combinations.md)*
