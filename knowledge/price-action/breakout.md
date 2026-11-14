# Breakout

## 1. Definition
A breakout is a **close beyond a defined resistance level** — a horizontal level, a pattern boundary, a trendline
or a prior swing high — after a period of price compression beneath it.

Not a breakout:
- A wick above the level with a close back below
- Price merely touching the level
- An intraday print above with no closing confirmation

## 2. Anatomy of a high-quality breakout

| Component | Requirement |
|-----------|-------------|
| **Compression before** | A range, triangle, flag or base — volatility contracted |
| **Level quality** | ≥2 prior touches; a well-defined, widely visible level |
| **Close beyond** | Not a wick; a decisive close, ideally by more than a symbolic margin |
| **Volume** | ≥1.3–1.5× the 20-bar average on the breakout bar |
| **Follow-through** | The next bar holds above the level |
| **Retest** | Optional but improves quality: price returns to the level and holds |
| **Room above** | No major resistance immediately overhead |
| **Context** | Higher timeframe not pushing the other way |

## 3. The four breakout outcomes

```
1. Breakout -> follow-through          (the trade works)
2. Breakout -> retest holds -> run     (best quality, best R:R entry)
3. Breakout -> immediate failure       (bull trap; reversal signal)
4. Breakout -> chop around the level   (indecision; no trade)
```

Outcome 3 is the most important to recognise. A failed breakout frequently produces a move of similar magnitude
in the opposite direction. See [`../workflows/trap-detection.md`](../../workflows/trap-detection.md).

## 4. Entry approaches compared

| Approach | Entry | Stop | Pros | Cons |
|----------|-------|------|------|------|
| Breakout close | On the close beyond the level | Back inside the range | Early, captures the full move | Most false signals; worst R:R |
| Breakout + follow-through | Next bar holding above | Back inside | Fewer false signals | Later; worse R:R |
| Retest | On the pullback to the level | Just inside the range | Best R:R; validates the level | Misses breakouts that never retest |
| Intraday pre-empt | Before the close | Tight | Very tight stop | Highest failure rate; wick risk |

No approach is "correct". State which one your scenario assumes, because the R:R arithmetic differs completely.

## 5. Volume: the primary filter

| Breakout volume | Interpretation |
|-----------------|----------------|
| ≥2× average | Strong participation; higher follow-through probability |
| 1.3–2× | Acceptable |
| ~1× | Weak; treat as suspect |
| < 1× | Probable failure; do not present as a valid setup |

Note: in some markets (e.g. index futures at the open) volume is naturally elevated — compare like with like by
using the same time-of-day bars.

## 6. Space above (the most-missed filter)

A breakout is only useful if there is somewhere to go. Before planning targets:

```
distance_to_next_resistance (in ATR units)
  >= 2 ATR  -> acceptable room
  1-2 ATR   -> marginal; likely poor R:R
  < 1 ATR   -> no room; the setup is untradeable
```

## 7. Invalidation

| Event | Meaning |
|-------|---------|
| Close back below the broken level | Failed breakout (trap) |
| Two closes below the level | Confirmed failure |
| Breakout bar's low taken out | The breakout candle's buyers are trapped |
| Volume collapses after the breakout | No follow-through interest |

## 8. Common errors

| Error | Guard |
|-------|-------|
| Buying a wick above the level | Require a close |
| Ignoring volume | Volume filter |
| Breakout into heavy resistance | Room check |
| Breakout against the higher timeframe | Context check |
| Breakout at a nearly-converged apex | Late breakouts have poor follow-through |
| Chasing an extended breakout (>2 ATR from the level) | Wait for a retest |
| Assuming "breakout" means "will go up" | It means "price left a defined range"; direction was already chosen by the close |

## 9. Beginner summary (Hinglish)

**Breakout kya hai?** Price kisi resistance level ke **upar close** kar de — wick se nahi, **close** se.

**Achha breakout kaisa hota hai?**
1. Pehle price **compress** hua ho (range/triangle/flag).
2. Level **do ya zyada baar** test hua ho.
3. Breakout candle par **volume badha** ho.
4. Upar target tak **jagah** ho (agla resistance door ho).

**Sabse achha entry:** retest. Price level par wapas aaye aur hold kare — tab stop sabse paas hota hai.

**Sabse khatarnak:** bina volume ka breakout, aur jahan turant upar resistance ho. Woh aksar **bull trap** hota
hai.

## 10. Exercise

Find five historical breakouts. For each record: pre-breakout compression, volume multiple, distance to the next
resistance in ATR, whether there was a retest, and the outcome 10 bars later. Then rank them and write the two
criteria that most separated the winners — using your own five, and stating that five is not a sample.

---
*See also: [`breakdown.md`](breakdown.md) · [`retest.md`](retest.md) · [`../../workflows/breakout-analysis.md`](../../workflows/breakout-analysis.md)*
