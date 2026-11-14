# Consolidation

## 1. Definition
**Consolidation** is a period in which price moves sideways within a range, neither making new highs nor new lows
in a sustained way. Volatility typically contracts. It is the market's way of digesting a prior move.

## 2. Types

| Type | Description | Resolution bias |
|------|-------------|-----------------|
| **Rest / pause** | Short, shallow, after a strong move | Continuation |
| **Base** | Longer, after a decline | Uncertain; can break either way |
| **Distribution** | Long sideways after an advance with declining volume | Downward |
| **Accumulation** | Long sideways after a decline with rising volume | Upward |
| **Compression / squeeze** | Very tight range, contracting volatility | Direction unknown, expansion likely |
| **Re-accumulation** | Sideways in an uptrend above a breakout level | Continuation |

Naming a consolidation "accumulation" or "distribution" in real time is a **hypothesis**, not an observation.
You cannot know which it was until it resolves. Say "consistent with" rather than "is".

## 3. Identifying consolidation objectively

| Measure | Threshold |
|---------|-----------|
| Range width | ≤2–3 × ATR over the period |
| Higher highs/lows | Absent or marginal |
| Bollinger bandwidth | At or near a multi-month low |
| ADX | < 20 |
| Volume | Declining or flat |
| Duration | At least 5–10 bars on the analysis timeframe |

## 4. What consolidation implies

1. **Volatility is mean-reverting.** Contraction is generally followed by expansion. This is one of the more
   robust empirical regularities in market data (volatility clustering).
2. **Direction is NOT implied** by the consolidation itself. Only the prior trend gives a lean.
3. **The longer the compression, the larger the eventual expansion** — a tendency, not a law.
4. **The longer the consolidation, the more trapped participants** — which is why resolutions can be violent.

## 5. Trading consolidation

### A. Wait for resolution (default)
```
Long on a close above the range high + volume
Short on a close below the range low + volume
Invalidation: the opposite boundary
Target: range height projected from the breakout
```

### B. Range fade (only in a stable, tested range)
```
Buy support, sell resistance, stop just beyond the boundary
Requires ADX < 20 and clear multi-touch boundaries
Fails when the range breaks — which is guaranteed eventually
```

### C. Anticipatory straddle
```
Bracket both sides; accept that one side loses
Only appropriate when the expansion is expected soon (compression extreme)
Cost: the losing side's slippage and stop
```

Never combine a fade and a breakout plan on the same boundary without saying which you are doing.

## 6. How consolidation ends

| Ending | Signature |
|--------|-----------|
| Breakout with volume | Expansion bar closing beyond the boundary, volume ≥1.5× |
| False breakout | Close beyond, then back inside within 1–3 bars |
| Slow drift out | Multiple small closes beyond the boundary — weaker, but real |
| Volatility explosion without direction | Both boundaries breached in sequence (whipsaw regime) — no trade |

## 7. Common errors

| Error | Guard |
|-------|-------|
| Trading inside consolidation | Most false signals occur here |
| Assuming direction from the consolidation shape | Only the prior trend leans; the resolution decides |
| Calling a 3-bar pause a "base" | Duration requirement |
| Ignoring the higher timeframe's own consolidation | Nested ranges are common |
| Fading the range after two boundary breaks | The range is over |

## 8. Beginner summary (Hinglish)

**Consolidation kya hai?** Price sideway chal raha hai — na naya high, na naya low. Volatility kam.

**Matlab:** market pichhle move ko digest kar raha hai. **Direction pata nahi** — sirf itna pata hai ki jab
range tootegi, move badi hogi.

**Kya karein?** Wait karo. Range ke bahar **close + volume** aane do, phir trade lo.

**Kab range fade karein?** Sirf jab range clear ho, dono boundaries 2+ baar test hui hon, aur ADX 20 se neeche ho.

**Badi galti:** range ke **beech** mein trade lena, aur consolidation ko "accumulation" ya "distribution" bol dena
bina confirm hue. Woh hypothesis hai, observation nahi.

## 9. Exercise

Find two consolidations: one after a strong advance, one after a strong decline. Measure the range in ATR, the
duration in bars, and the volume trend. Then check the resolution direction. Write down whether the prior trend or
the volume trend predicted the direction better — and state your sample size.

---
*See also: [`breakout.md`](breakout.md) · [`../candlesticks/inside-bar.md`](../candlesticks/inside-bar.md) ·
[`../chart-patterns/rectangle.md`](../chart-patterns/rectangle.md) · [`../indicators/bollinger-bands.md`](../indicators/bollinger-bands.md)*
