# Ichimoku Cloud (Ichimoku Kinko Hyo)

**Family:** Trend + levels · **Default settings:** 9 / 26 / 52 · **Implementation:** `indicators.ichimoku(h, l, c, 9, 26, 52)`

## 1. Calculation

```
tenkan_sen (conversion)  = (highest_high(9)  + lowest_low(9))  / 2
kijun_sen  (base)        = (highest_high(26) + lowest_low(26)) / 2
senkou_span_a (leading A)= (tenkan + kijun) / 2,  plotted 26 periods FORWARD
senkou_span_b (leading B)= (highest_high(52) + lowest_low(52)) / 2, plotted 26 forward
chikou_span (lagging)    = close, plotted 26 periods BACKWARD
kumo (cloud)             = area between span A and span B
```

The forward shift is central: the cloud you see at the current bar was computed from data 26 bars ago,
and the cloud drawn 26 bars ahead is computed from *today's* data. This is why the indicator is described
as "leading" even though its inputs are lagging.

## 2. Interpretation

| Element | Meaning |
|---------|---------|
| Price **above** the cloud | Bullish regime |
| Price **below** the cloud | Bearish regime |
| Price **inside** the cloud | Transition / no regime — weakest state |
| Cloud **thickness** | Support/resistance strength; thin cloud = easily broken |
| Cloud **colour** (A vs B) | Span A above B = bullish cloud; below = bearish |
| **Tenkan above Kijun** | Short-term momentum up |
| **Tenkan/Kijun cross** | Momentum shift (the "TK cross") |
| **Chikou above price 26 bars ago** | Confirmation of bullishness |
| **Flat Kijun** | A magnet level — price often returns to it |

The standard reading hierarchy: regime (price vs cloud) → momentum (TK) → confirmation (chikou).

## 3. Common settings

| Set | Use |
|-----|-----|
| 9 / 26 / 52 | Original; designed around a 6-day trading week, so on modern 5-day charts some practitioners use 9/26/52 anyway |
| 20 / 60 / 120 | "Crypto/24-7" adaptation often cited |
| 9 / 26 / 26 | Simpler variant |

**The 26/52 periods are a documented convention, not a law.** Do not present alternative settings as
"wrong"; do state which you used.

## 4. Limitations

- **Complex and visually dominant.** Beginners over-read the cloud and under-read structure.
- **Lagging inputs, forward plotting.** The forward cloud is not a prediction — it is arithmetic on past data.
  Calling it a forecast is a common error.
- **Poor in ranges.** Price oscillating inside the cloud gives no signal at all.
- **Repaint sensitivity.** Some platforms recalculate the chikou/cloud when new data arrives; verify.
- **Parameter dependence** is significant, particularly the 52 for span B.

## 5. Combining

- **Ichimoku + structure**: a cloud edge that coincides with a horizontal support is far stronger than a
  cloud edge alone.
- **Ichimoku + ATR**: cloud thickness in ATR units tells you whether it is a real barrier.
- **Ichimoku + volume**: a breakout of the cloud on volume is meaningful; a drift through it is not.
- Avoid stacking Ichimoku with three MAs — the tenkan/kijun are moving-average-like and the evidence is not
  independent.

## 6. Reading from a screenshot

Extractable: whether price is above/below/inside the cloud; cloud colour and relative thickness; whether
tenkan is above kijun; whether price is near the kijun.

Not extractable: exact values without labels; historical cloud shape beyond the visible window.

## 7. Worked example (procedure)

```
If highest_high(9) = 1_260 and lowest_low(9) = 1_210 -> tenkan = 1_235
   highest_high(26) = 1_300, lowest_low(26) = 1_190 -> kijun  = 1_245
   span A = (1_235 + 1_245)/2 = 1_240, plotted 26 ahead
   span B = (highest_high(52) + lowest_low(52))/2
Price 1_252, cloud between 1_235 and 1_244 -> price above the cloud = bullish regime.
Tenkan (1_235) below kijun (1_245) -> short-term momentum is *not* confirming.
Reading: bullish regime with weak momentum — a pullback, not a fresh trend.
See tests/indicators/test_ichimoku.py.
```

## 8. Beginner summary (Hinglish)

**Ichimoku cloud kya hai?** Ek "cloud" (kumo) jo support/resistance zone ki tarah kaam karta hai, plus do
lines (tenkan, kijun) aur ek lagging line (chikou).

**Sabse simple reading:**
- Price cloud ke **upar** = bullish, **neeche** = bearish, **andar** = confusion (koi trade nahi).
- Tenkan kijun ke **upar** = short-term momentum up.
- Cloud **moti** = strong support/resistance; **patli** = easily break hogi.

**Badi galti:** cloud aage draw hota hai, isliye log usko "prediction" samajh lete hain. Woh prediction nahi
hai — past data ka arithmetic hai.

## 9. Exercise

On a daily chart, classify 30 consecutive bars as above / inside / below the cloud. Then check the next 5
bars' direction for each group. Count how often "inside the cloud" produced a clear directional outcome.
Write one sentence about what that implies for trading inside the cloud.

---
*See also: [`ema.md`](ema.md) · [`atr.md`](atr.md) · [`indicator-combinations.md`](indicator-combinations.md)*
