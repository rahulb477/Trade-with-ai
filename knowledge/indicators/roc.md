# ROC (Rate of Change)

**Family:** Momentum (pure) · **Default period:** 12 (or 9) · **Implementation:** `indicators.roc(closes, 12)`

## 1. Calculation

```
ROC_t = 100 × (close_t − close_{t−n}) / close_{t−n}
```

Some platforms express ROC as a ratio (`close_t / close_{t−n}`) rather than a percentage. Check before
comparing. Undefined if `close_{t−n} == 0`.

## 2. Interpretation

ROC is the simplest possible momentum measure: **percentage change over n bars**. It is unbounded, so
interpretation is relative to the instrument's own history.

| Reading | Meaning |
|---------|---------|
| ROC > 0 | Price higher than n bars ago |
| ROC rising | The advance is accelerating |
| ROC falling while price rises | The advance is decelerating — often the earliest momentum warning |
| ROC crossing zero | Trend flip on that lookback |
| ROC at a multi-year extreme | Unusual; check for a data issue or an event |

Because it is unbounded and simple, ROC is the best momentum measure for **cross-sectional comparison** (see
relative strength, `engines/market-intelligence/`): compare the ROC of ten stocks over the same window.

## 3. Common settings

| Period | Use |
|--------|-----|
| 9 | Short-term (often paired with a 9-period MA of ROC as a signal) |
| 12 | Standard |
| 20 / 21 | Swing |
| 60 / 120 | Positional |

## 4. Limitations

- **One number, no smoothing.** Very noisy at short periods.
- **Unbounded.** "Overbought" has no fixed threshold; must be normalised (percentile or z-score) for comparison.
- **Base-effect distortion.** A large move n bars ago drops out of the window and can flip the reading abruptly.
- **No volume.** Momentum without participation is a weaker statement.
- **Scale differences** mean raw ROC is not comparable across instruments with different volatility — use
  **risk-adjusted** ROC (`ROC / ATR%`) for that.

## 5. Combining

- **ROC + a moving average of ROC**: the classic price-oscillator/signal-line pair.
- **ROC + volatility normalisation**: `ROC / (ATR/close)` gives a volatility-adjusted momentum, comparable
  across instruments. This is the most useful form for relative strength.
- **ROC + structure**: ROC divergence at a resistance is a deceleration warning.
- **ROC + ADX**: ROC measures direction and speed; ADX measures trend strength. Complementary.

## 6. Reading from a screenshot

Extractable: whether the line is above/below zero; its slope; whether it is at an extreme relative to the
visible window.

Not extractable: the numeric value without a label.

## 7. Worked example

```
closes: … 100 (12 bars ago), 108 (now)
ROC(12) = 100 × (108 − 100)/100 = 8.0%
Instrument ATR% = 2% per bar and over 12 bars roughly 2% × sqrt(12) ≈ 6.9% of typical movement
Risk-adjusted: 8.0 / 6.9 ≈ 1.16 -> modest momentum, not an outlier.
Same 8% on a stock with 1% ATR% over 12 bars ≈ 3.5% typical -> 2.3x normal -> genuinely strong.
This is why raw ROC across instruments is misleading.
See tests/indicators/test_roc.py.
```

## 8. Beginner summary (Hinglish)

**ROC kya hai?** Simple: aaj ka price n candles pehle se kitna % upar/neeche hai.

**Matlab:**
- ROC **positive** = price upar hai.
- ROC **badh raha** = move accelerate ho raha.
- ROC **gir raha jabki price upar ja raha** = move slow ho raha — early warning.

**Sabse achha use:** do stocks ko compare karna (relative strength) — kyunki yeh ek simple number hai.

**Dhyan:** raw ROC ko do alag volatility wale stocks ke beech compare mat karo. ATR se divide karo, tab
compare karo.

## 9. Exercise

Take five stocks from the same sector. Compute ROC(20) and ATR%-normalised ROC(20) for each. Rank them by both
measures. Do the rankings agree? Write one sentence about which ranking you would trust for a relative-strength
decision, and why.

---
*See also: [`rsi.md`](rsi.md) · [`atr.md`](atr.md) · [`../engines/market-intelligence/sector-analysis.md`](../../engines/market-intelligence/sector-analysis.md)*
