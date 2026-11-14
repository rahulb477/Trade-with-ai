# Fair Value Gaps (FVG) / Imbalances

**Plain language:** a three-candle pattern in which candle 1's range and candle 3's range do not overlap, leaving
a **price range that traded with very little volume** during an impulsive move. Also called an imbalance or a
liquidity void.

## 1. Mechanical definition

```
Bullish FVG:  low of candle 3 > high of candle 1          (gap between them)
              zone = [high of candle 1, low of candle 3]
Bearish FVG:  high of candle 3 < low of candle 1
              zone = [high of candle 3, low of candle 1]
```

Candle 2 is the wide-range "displacement" candle. The zone is the part of candle 2's range that candles 1 and 3
did not cover.

**Different sources define the boundaries differently** (wick-based, body-based, or using candle 2's range only).
State which definition you used, or the level you quote will not be reproducible.

## 2. What it means

A fast move leaves price levels where little trading occurred. Two observable consequences:

1. **Price often moves quickly through such zones again** — there is less resting interest to slow it.
2. **Price sometimes returns to them** before continuing.

Consequence 2 is what SMC refers to as "filling the imbalance". It is a **tendency**, not a rule. Many gaps are
never filled; some are filled months later. Never write "the FVG will be filled".

## 3. How to use it

| Use | Framing |
|-----|---------|
| As a **target** | "There is an imbalance at 1,182–1,190 which may act as a magnet" |
| As a **pullback zone** | "A return into 1,196–1,204 (the FVG) with a reaction candle would be a pullback reference" |
| As a **caution** | "Price is inside an imbalance, so movement may be fast and stops unreliable" |
| Not as | "Guaranteed support" or "will fill" |

## 4. Quality filters

| Filter | Why |
|--------|-----|
| Displacement size ≥1.5 ATR | Small imbalances are noise |
| Volume on the displacement bar | Real aggression, not thin-market drift |
| Confluence with a level, MA, or Fib | The zone alone is weak |
| Freshness | Unfilled zones ahead are more interesting than filled ones |
| Timeframe | Higher-timeframe imbalances are more persistent |

## 5. Failure modes

| Failure | Meaning |
|---------|---------|
| Price never returns | Very common — do not build a plan around a fill |
| Price returns and continues through | The imbalance provided no support |
| Gaps defined differently by different tools | Your level may not be anyone else's level |
| Multiple overlapping gaps | Over-definition; pick the primary |

## 6. Relationship to "gaps" in the ordinary sense

Do not confuse an FVG (a three-candle imbalance within continuous trading) with a **session gap** (price jumping
between sessions, e.g. an Indian stock gapping up overnight). Session gaps have their own behaviour and their own
literature. Label them separately.

## 7. Report wording

> ✅ "The rally from 1,196 to 1,216 on 12 Nov left an imbalance at 1,198–1,204 (candle 3's low above candle 1's
> high, body-based definition). If price returns into that band, movement may be fast; it is a potential
> pullback reference, not a guaranteed support."
>
> ❌ "FVG at 1,200 — price has to fill it before going up."

## 8. Beginner summary (Hinglish)

**FVG kya hai?** Teen candles mein tez move ke wajah se ek **price band** aisa ban jata hai jahan practically
trade nahi hua — candle 1 aur candle 3 ke beech ka gap.

**Matlab:** us zone mein orders kam hote hain, isliye price wahan se **tezi se** nikal sakta hai — aur kabhi
kabhi wapas bhi aa jata hai.

**Kaise use karein:** target ya pullback zone ki tarah. **"Price ko yeh gap bharna hi hai" — aisa kabhi mat socho.**
Bahut gaps kabhi fill nahi hote.

**Dhyan:** har tool FVG ko thoda alag tarike se draw karta hai. Aap kaunsa definition use kar rahe ho, likho.

## 9. Exercise

Mark three FVGs on a 15m chart. For each, note whether price returned within 30 bars, and whether it held or
passed through. Compute the raw proportion. Then write one sentence about why you would still not call it a rule.

---
*See also: [`order-blocks.md`](order-blocks.md) · [`mitigation-inducement.md`](mitigation-inducement.md) ·
[`../price-action/consolidation.md`](../price-action/consolidation.md)*
