# Bollinger Bands

**Family:** Volatility envelope · **Default settings:** 20-period SMA, ±2 standard deviations
**Implementation:** `indicators.bollinger_bands(closes, period=20, num_std=2.0)`

## 1. Calculation

```
middle_t = SMA(close, period)_t
sigma_t  = population standard deviation of the last `period` closes
upper_t  = middle_t + num_std × sigma_t
lower_t  = middle_t − num_std × sigma_t

bandwidth_t = (upper_t − lower_t) / middle_t          # relative width
percent_b_t = (close_t − lower_t) / (upper_t − lower_t)   # position within the bands
```

Notes:

- **Population vs sample σ** changes the bands slightly. Bollinger's own convention is population σ; this
  repository uses that. State the convention if comparing with another platform.
- `%B > 1` means price closed above the upper band; `< 0` below the lower band.
- Bandwidth is the volatility measure that makes the indicator genuinely useful.

## 2. Interpretation

| Reading | Conventional meaning | Reality check |
|---------|---------------------|---------------|
| Price at/beyond upper band | "Overbought" | In a strong trend, price can *ride* the band for weeks — this is strength, not a short |
| Price at/beyond lower band | "Oversold" | Same, inverted |
| Narrow bands (low bandwidth) | Volatility contraction → expansion likely | Direction unknown; the *squeeze* is the signal, not a trade |
| Wide bands | High volatility | Mean-reversion attempts are more dangerous |
| Price walks the upper band with rising bandwidth | Strong trend | The most important pattern: do not fade it |
| Price fails at the band and returns to the middle | Range behaviour | Fade setups work here |
| Bands contracting then price closing outside | Squeeze breakout | Needs volume confirmation |

**Bollinger's own guidance** (from his published work) is that the bands are not a trading system by
themselves, that ~90% of price action occurs between them by construction, and that the touch of a band
is not a signal — the *context* of the touch is.

## 3. Common settings

| Period / σ | Character |
|------------|-----------|
| 20 / 2 | Default |
| 20 / 2.5 | Fewer touches; wider |
| 10 / 1.5 | Intraday; very frequent touches |
| 50 / 2 | Longer-term envelope |

## 4. Limitations

- **Not a mean-reversion machine.** In trends, fading band touches is a reliable way to lose money.
- **σ assumes normality.** Price distributions have fat tails, so "2σ" events happen more often than a
  normal model implies.
- **Bandwidth is scale-free but regime-dependent.** "Narrow" must be judged relative to that
  instrument's own history.
- **Squeeze timing is unknowable.** A squeeze can last far longer than a trader can wait.
- **Redundant with ATR.** Both measure volatility; do not treat them as independent evidence.

## 5. Combining

- **Bands + ADX**: ADX < 20 (range) → band fades are reasonable; ADX > 25 (trend) → band rides are
  reasonable. This single filter fixes most Bollinger misuse.
- **Bands + volume**: a squeeze breakout on 2× volume is materially stronger.
- **Bands + structure**: a squeeze resolving through a horizontal level is a real setup.
- **Bands + ATR**: do not use both for the same purpose; pick one for sizing.

## 6. Reading from a screenshot

Extractable: whether price is at/inside/beyond a band; how wide the bands look relative to recent history;
whether price has been riding a band; whether the bands are compressing.

Not extractable: exact σ values; bandwidth numbers without a label.

## 7. Worked example

```
Last 20 closes (illustrative): mean = 100.0, population σ = 2.0
upper = 104.0 · lower = 96.0 · bandwidth = 8/100 = 8.0%
close = 103.2 -> %B = (103.2 − 96)/8 = 0.90  (near the upper band, inside)
close = 104.8 -> %B = 1.10 (closed above the upper band)
Reading depends on regime:
  ADX 14 -> range:  %B 1.10 is a stretch; fade candidate
  ADX 32 -> trend:  %B 1.10 with rising bandwidth is a trend-ride signal; do not fade
See tests/indicators/test_bollinger.py.
```

## 8. Beginner summary (Hinglish)

**Bollinger Bands kya hain?** 20-SMA ke around ±2 standard deviation ki do lines.

**Matlab:**
- Price upper band par = "zyada upar" — **par strong trend mein price band par chadh kar chalta rehta hai**,
  isliye seedha short mat karo.
- Bands **sikud gayi** (squeeze) = volatility kam, jald hi bada move aane wala hai — **direction pata
  nahi**, sirf move aayega.
- Bands **khul gayi** = high volatility, mean-reversion risky.

**Sabse zaroori filter:** ADX. ADX 20 se neeche = range (band fade theek), ADX 25 se upar = trend (band
ride karo, fade mat karo).

## 9. Exercise

Find two squeeze episodes. For each, record: bandwidth at the squeeze, the breakout direction, the volume
on the breakout candle, and where the bands were relative to a horizontal level. Then answer: was the
direction predictable, or only the *fact* that a move would come?

---
*See also: [`atr.md`](atr.md) · [`sma.md`](sma.md) · [`adx.md`](adx.md) · [`indicator-combinations.md`](indicator-combinations.md)*
