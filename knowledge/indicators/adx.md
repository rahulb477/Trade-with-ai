# ADX (Average Directional Index)

**Family:** Trend strength (non-directional) · **Default period:** 14
**Implementation:** `indicators.adx(highs, lows, closes, 14)` → returns `(adx, plus_di, minus_di)`

## 1. Calculation

```
up_move   = high_t − high_{t−1}
down_move = low_{t−1} − low_t

+DM = up_move   if up_move > down_move and up_move > 0   else 0
−DM = down_move if down_move > up_move and down_move > 0 else 0

TR  = true range (see atr.md)
smoothed with Wilder's method for all three.

+DI = 100 × smoothed(+DM) / smoothed(TR)
−DI = 100 × smoothed(−DM) / smoothed(TR)
DX  = 100 × |+DI − −DI| / (+DI + −DI)
ADX = Wilder-smoothed DX over `period`      (first value after ~2×period bars)
```

ADX requires about `2 × period` bars before it is valid. Anything computed earlier is noise — the
implementation returns `None`.

## 2. Interpretation

ADX measures **strength of trend, in either direction**. It says nothing about direction — that is what
`+DI` and `−DI` are for.

| ADX | Reading |
|-----|---------|
| 0–15 | No trend / very weak — range conditions. MA crossovers and Supertrend flips are unreliable |
| 15–20 | Weak trend, emerging |
| 20–25 | Trend present (the usual threshold for acting on trend signals) |
| 25–40 | Strong trend |
| 40–60 | Very strong trend (often a mature move) |
| > 60 | Extreme; often late-stage or event-driven |
| Rising ADX | The trend is strengthening |
| Falling ADX | The trend is weakening (price may still rise) |

**Critical nuance:** ADX falling while price rises means the *uptrend is decelerating*, not that it is
over. Conversely, a rising ADX on a decline means the downtrend is accelerating.

## 3. Directional reading

| Condition | Reading |
|-----------|---------|
| `+DI > −DI` and ADX rising | Healthy uptrend |
| `+DI > −DI` and ADX falling | Uptrend losing momentum |
| `−DI > +DI` and ADX rising | Healthy downtrend |
| `−DI > +DI` and ADX falling | Downtrend losing momentum |
| ADX < 15 with DIs crossing repeatedly | Chop; stand aside |

## 4. Common settings

| Period | Use |
|--------|-----|
| 14 | Standard (Wilder's original) |
| 10 | Intraday, more responsive |
| 20 / 28 | Smoother regime classification |

## 5. Limitations

- **Very lagging.** It needs `2 × period` bars and then smooths further.
- **No direction.** Mistaking ADX strength for bullishness is a classic beginner error.
- **Late on regime changes.** By the time ADX > 25, a good part of the move has happened.
- **Thresholds are conventions.** "20" is not magic; on some instruments 18 or 25 works better. Tuning
  the threshold on the same data you evaluate on is overfitting.
- **Mature trends score high.** High ADX can mean "late", not "good".

## 6. Combining — its best use

ADX is most valuable as a **filter**, not a signal:

- **ADX as a filter for MA/Supertrend signals**: only act when ADX > 20. This removes a large share of
  range whipsaw and is the single highest-value use of the indicator.
- **ADX as a filter for Bollinger fades**: only fade band touches when ADX < 20.
- **ADX + ATR**: ADX for "is there a trend", ATR for "how big is the move" → choose strategy family and
  position size.
- **ADX + market structure**: a rising ADX with a confirmed structure break is meaningful; a rising ADX
  inside a range is impossible by definition, which itself is a useful sanity check.

## 7. Reading from a screenshot

Extractable: whether ADX is above/below ~20/25 (if the panel has gridlines); whether it is rising or
falling; whether `+DI` is above `−DI`; numeric labels if printed.

Not extractable: exact values without labels; the DI values' precise separation.

## 8. Worked example (procedure)

```
Given 40+ bars, compute +DM/−DM/TR, Wilder-smooth them, derive +DI/−DI, DX, then ADX.
Suppose ADX = 27, +DI = 24, −DI = 11:
  Reading: a real uptrend with decent strength.
  Action: trend-following signals are usable; range-fade signals are not.
Suppose ADX = 12, +DI = 20, −DI = 18:
  Reading: no trend. Every crossover here is noise.
  Action: stand aside from trend entries; if range trading, require boundary confirmation.
See tests/indicators/test_adx.py.
```

## 9. Beginner summary (Hinglish)

**ADX kya batata hai?** Trend **kitna strong** hai — upar ya neeche, yeh nahi batata.

- **ADX < 15–20** = trend nahi hai, range hai. Trend-following signals ignore karo.
- **ADX 20–25 se upar** = trend hai, ab MA/Supertrend ke signals meaningful hain.
- **ADX 40+** = bahut strong, par aksar late stage.
- **ADX upar ja raha** = trend strong ho raha; **neeche** = kamzor ho raha.

**Direction ke liye** `+DI` aur `−DI` dekho: `+DI > −DI` = up trend.

**Sabse useful use:** filter ki tarah — ADX 20 se neeche ho to trend wale trades skip karo.

## 10. Exercise

Take a year of daily data. List every EMA(20/50) crossover. Split into two groups: ADX > 20 at the cross,
and ADX < 20. For each group compute how many crosses were followed by a move of at least 2 ATR in the
crossover's direction within 10 bars. Report both numbers and the sample sizes. Note whether the split was
worth making in your sample.

---
*See also: [`atr.md`](atr.md) · [`supertrend.md`](supertrend.md) · [`ema.md`](ema.md) · [`indicator-combinations.md`](indicator-combinations.md)*
