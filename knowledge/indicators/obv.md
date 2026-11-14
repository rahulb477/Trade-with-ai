# OBV (On-Balance Volume)

**Family:** Volume/participation · **No parameters** · **Implementation:** `indicators.obv(closes, volumes)`

## 1. Calculation

```
OBV_0 = 0   (or the first bar's volume; the offset is arbitrary)
if close_t > close_{t−1}:  OBV_t = OBV_{t−1} + volume_t
if close_t < close_{t−1}:  OBV_t = OBV_{t−1} − volume_t
if close_t == close_{t−1}: OBV_t = OBV_{t−1}
```

Only the **shape** of the OBV line matters; its absolute level is arbitrary. Two platforms starting from
different offsets will produce parallel lines — that is not an error.

## 2. Interpretation

| Reading | Meaning |
|---------|---------|
| OBV making higher highs with price | Volume confirms the advance — healthy |
| OBV falling while price rises | Distribution: rallies are on shrinking volume (bearish divergence) |
| OBV rising while price falls | Accumulation: selling is being absorbed (bullish divergence) |
| OBV flat while price moves | The move lacks participation — suspect |
| OBV breaking to a new high before price | Volume leadership; the break may follow |

OBV is a **cumulative** measure, which makes it a trend object rather than an oscillator. Read its slope
and its structure (higher highs/lows), not its value.

## 3. Limitations

- **Ignores volume magnitude per bar in a meaningful way.** A huge-volume down bar subtracts only its own
  volume; the cumulative nature means old data never decays.
- **The close is the only input.** A bar that traded 5% up and closed flat contributes nothing.
- **Gaps and splits** distort the series. Use adjusted data.
- **Not comparable across instruments** — no normalisation.
- **Divergence reading is subjective**, like all divergences; pivot selection changes the conclusion.
- **Bad volume data breaks it completely.** Block deals, dark-pool prints, or missing volume produce
  garbage.

## 4. Variants

- **Volume-Weighted OBV / Adjusted OBV** — attempts to weight by the close's position in the range.
- **Relative OBV** — OBV divided by a moving average of volume, for comparability.
- **Cumulative Volume Delta (CVD)** — a genuinely different (and better) measure, but it requires
  bid/ask data, not just bar volume. See `engines/order-flow/`.

## 5. Combining

- **OBV + price structure**: an OBV higher high coinciding with a price breakout is meaningful confirmation.
- **OBV + RSI**: price/RSI divergence *and* OBV divergence together is stronger than either alone (but they
  are not fully independent — both are derived from the same bars).
- **OBV + VWAP/volume profile**: OBV for direction of participation, VWAP/profile for the price at which it
  occurred.
- **Do not** use OBV to time entries. It is a confirmation of participation, not a trigger.

## 6. Reading from a screenshot

Extractable: the OBV line's slope and structure (higher highs/lows); whether it is diverging from price.

Not extractable: the numeric OBV value (meaningless anyway); the volume magnitudes behind it.

If no volume panel exists, OBV cannot exist either — report "not available".

## 7. Worked example

```
Bars (fictional): 
 close 100, vol 1_000 -> OBV 0 (start)
 close 102, vol 1_500 -> OBV 1_500
 close 101, vol 1_200 -> OBV   300
 close 104, vol   800 -> OBV 1_100
 close 106, vol   600 -> OBV 1_700  (new high: price and OBV agree)
 close 107, vol   400 -> OBV 2_100  (price new high but volume shrinking 1_500->800->600->400)
Reading: OBV still rising, but the *rate* is collapsing. In a longer series this pattern (price higher
highs on falling volume) is the classic distribution signature — worth flagging, not sufficient alone.
See tests/indicators/test_obv.py.
```

## 8. Beginner summary (Hinglish)

**OBV kya hai?** Ek cumulative line: jab close upar ho to volume **jodta** hai, jab neeche ho to volume
**ghatata** hai.

**Matlab:**
- OBV price ke saath upar ja raha = volume move ko support kar raha hai (healthy).
- Price upar ja raha par **OBV neeche** = rally kam volume par ho rahi hai — warning (distribution).
- Price neeche ja raha par **OBV upar** = selling absorb ho rahi hai (accumulation).

**Important:** OBV ki **value** matter nahi karti — sirf **shape** aur slope.

**Dhyan:** volume data galat ho to OBV bilkul bekaar hai. Aur split-adjusted data use karo.

## 9. Exercise

Take a stock's daily chart and its OBV. Find three places where price made a new high. For each, note
whether OBV also made a new high, and what happened over the next 15 bars. Then note whether the three
cases were enough to conclude anything — and how many you would need.

---
*See also: [`volume-profile.md`](volume-profile.md) · [`vwap.md`](vwap.md) · [`mfi.md`](mfi.md)*
