# Order Blocks

**Plain language:** a price **zone** — usually the last opposite-coloured candle before an impulsive move — that
is treated as a potential reaction area if price returns to it.

## 1. Definition (mechanical, so it can be tested)

```
Bullish order block: the last bearish candle before a bullish impulse of >= 1.5 ATR
                     (some definitions: the last down candle before a break of structure)
Bearish order block: the last bullish candle before a bearish impulse of >= 1.5 ATR

The zone is usually drawn from that candle's open-to-close (or high-to-low), optionally extended
to the imbalance it left behind.
```

Without a mechanical definition like this, an "order block" is whatever zone happens to justify the trade after
the fact. That is curve-fitting, not analysis.

## 2. The honest framing

The name implies institutional orders. **You cannot observe institutional orders.** What you can observe is:

- A zone where price reversed sharply.
- A zone from which an impulse began.

Whether that zone "contains unfilled orders" is an untestable story. What is testable is whether price tends to
react when it returns to such zones on your instrument and timeframe. That must be measured, not assumed.

Legitimate way to use it: **a zone-based reference for a pullback entry with a defined invalidation.** Say exactly
that.

## 3. Drawing rules that keep it honest

| Rule | Reason |
|------|--------|
| Use the candle body (open→close), not the full wick, unless the wick is the reaction point | Consistency |
| Require ≥1.5 ATR displacement out of the zone | Otherwise every candle becomes an order block |
| Maximum one zone per impulse leg | Avoids stacking |
| Zones expire — after N bars (e.g. 20–30) or after two failed visits, retire them | Old zones clutter charts |
| Mark the zone's invalidation: a close beyond it | Without this, the zone is unfalsifiable |

## 4. Entry framing

```
Bullish zone (after an uptrend break of structure):
  entry      : on a return into the zone, with a bullish reaction candle
  invalidation: a close below the zone's low (not "somewhere below")
  targets    : the impulse leg's high, then structural resistance
  quality    : zone coincides with a higher-timeframe level, an MA, or a Fib zone
```

## 5. Why zone confluence matters more than the zone itself

An order block that coincides with a **tested horizontal support**, a **0.618 retracement**, and the **50-EMA**
is far more meaningful than one floating in space. The zone is not the edge; the confluence is.

## 6. Failure modes

| Failure | Meaning |
|---------|---------|
| Price slices through the zone without reacting | The zone is not respected; retire it |
| Price reacts, then closes through | The reaction was a pause, not a reversal |
| Every impulse leg produces several "zones" | Over-definition; pick the primary |
| Zone drawn after the trade is chosen | Confirmation bias |

## 7. Report wording

> ✅ "There is a demand zone at 1,196–1,202 (the body of the last down candle before the 1.6-ATR rally on 12 Nov).
> It coincides with the prior swing support at 1,198. A return there with a bullish reaction candle would be a
> usable pullback reference, with invalidation on a close below 1,192."
>
> ❌ "Institutional order block at 1,198 — smart money is buying here."

## 8. Beginner summary (Hinglish)

**Order block kya hai?** Ek **zone** — aksar woh last opposite-colour candle jahan se ek tez move shuru hua. Log
maante hain ki us zone par agar price wapas aaye to reaction aayega.

**Sach kya hai:** hum institutions ke orders **dekh nahi sakte**. Jo dikh raha hai woh hai: ek zone jahan se tez
move nikla. Uska retest kaam karega ya nahi — yeh **measure** karna padta hai.

**Kaise use karein:**
1. Zone body se draw karo, poori wick se nahi (consistency ke liye).
2. Sirf tab jab zone se **1.5 ATR** ka displacement nikla ho.
3. Entry: zone mein wapas aane par reaction candle ke saath.
4. **Stop:** zone ke neeche close.

**Sabse zaroori:** zone ka matlab tabhi zyada jab woh kisi tested support/EMA/Fib ke saath ho — **confluence**.

## 9. Exercise

Define the zone mechanically (last opposite candle before ≥1.5 ATR impulse, body only). Find five such zones and
record what happened on the first return. Compute the raw hit rate out of five, then state out loud: what sample
would you need before trusting this? Write that number down.

---
*See also: [`fair-value-gaps.md`](fair-value-gaps.md) · [`mitigation-inducement.md`](mitigation-inducement.md) ·
[`../market-structure/level-mapping.md`](../market-structure/level-mapping.md)*
