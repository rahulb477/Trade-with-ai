# Higher Highs and Higher Lows (Uptrend Structure)

## 1. Definition
An uptrend is a sequence in which each **swing high exceeds the previous swing high** (HH) and each **swing low
exceeds the previous swing low** (HL). Both conditions are required — a series of higher highs alone, with equal
or lower lows, is not an uptrend but an expanding range.

```
                    HH
              ╱╲          ╱
        HH  ╱   ╲   ╱╲  ╱
          ╱      ╲ ╱  ╲╱
        ╱         ╲
   HL ╱              HL
```

## 2. Identification method

1. Choose a swing parameter `k` (2, 3 or 5 bars each side) and state it.
2. Mark all swing highs and lows in the visible window.
3. Check monotonicity: `H_n > H_{n−1}` and `L_n > L_{n−1}`.
4. Count how many consecutive HH/HL pairs hold. One or two pairs is a lean, not a trend; three or more is a
   structure.

## 3. What it tells you

- **Demand is progressively more aggressive.** Buyers are willing to pay higher prices, and sellers are no
  longer able to push price to the previous low.
- The **last higher low is the trend's invalidation reference.** A decisive close below it is the first objective
  evidence that the uptrend structure has failed.
- The trend is a **context**, not an entry. Entries happen at the pullbacks to the higher lows, not at the highs.

## 4. Where the trend is actionable

| Location | Quality |
|----------|---------|
| Pullback to the most recent HL with a bullish confirmation candle | Highest |
| Pullback to a rising trendline drawn through the HLs | High |
| Pullback to a moving average that coincides with an HL | High |
| Breakout above the most recent HH | Medium (chasing risk) |
| Mid-way between HL and HH | Low — no reference for invalidation |

## 5. Confirmation and invalidation

**Confirmation of continuation:** a new HH, or a pullback that holds above the prior HL and then breaks the
pullback's high.

**Invalidation:**

| Event | Meaning |
|-------|---------|
| Close below the most recent HL | The structure has a lower low — the uptrend is in question |
| A LH forms after a HH | First warning (this is a CHoCH in smart-money framing) |
| A close below the HL *and* a failure to reclaim | Trend change confirmed structurally |

Note that "close below" is stricter than "wick below". Wicks through a swing low are common (stop hunts) and are
not structural breaks.

## 6. Common errors

| Error | Guard |
|-------|-------|
| Calling a higher low where the low is only marginally higher | Require a meaningful margin (e.g. ≥0.2 ATR) |
| Using different `k` to make the structure "fit" | Fix `k` before looking at the chart |
| Treating a wick below the HL as a break | Require a close |
| Ignoring that the trend is only on one timeframe | Check at least one higher timeframe |
| Assuming an uptrend must continue | Structure describes the past |
| Buying at the HH instead of the HL | Worse location, worse R:R |

## 7. Interaction with indicators

- **EMA stack** (e.g. 20 > 50 > 200) usually mirrors HH/HL structure — it is the same information smoothed.
- **ADX rising** confirms that the HH/HL sequence has force.
- **RSI holding above 40–50** on pullbacks is consistent with the structure.
- Do not count the EMA stack *and* the ADX *and* the RSI as three confirmations of the same structural fact;
  they are one.

## 8. Beginner summary (Hinglish)

**Uptrend ka matlab:** har naya high pichhle high se upar (HH), aur har naya low pichhle low se upar (HL).

**Sabse important level:** **last higher low**. Agar price uske neeche **close** kar de, to uptrend ka structure
toot gaya — tab tak trend intact maana jata hai.

**Entry kahan?** HH par nahi — **HL par pullback** mein, confirmation candle ke saath. Kyunki wahan stop paas
hoti hai aur R:R behtar hota hai.

**Galti:** wick ko break samajhna. Close chahiye.

## 9. Exercise

Mark swings with `k=3` on a daily chart. Count the consecutive HH/HL pairs. Then identify the last HL and note
how far price is from it in ATR units. If the distance is under 1 ATR, the "setup" has almost no room — write
down what you would do instead.

---
*See also: [`lower-highs-lower-lows.md`](lower-highs-lower-lows.md) · [`trend-continuation.md`](trend-continuation.md) ·
[`../market-structure/trend-phases.md`](../market-structure/trend-phases.md)*
