# Premium and Discount

**Plain language:** dividing the current range in half. Above the midpoint is "premium" (expensive relative to the
range); below it is "discount" (cheap). The framework says: buy in discount, sell in premium.

## 1. Mechanical definition

```
range_high = the most recent significant swing high
range_low  = the most recent significant swing low
midpoint   = (range_high + range_low) / 2

premium  zone: price > midpoint  (upper half)
discount zone: price < midpoint  (lower half)
equilibrium  : price ≈ midpoint
```

Optional refinement (often called "OTE" — optimal trade entry): the 0.618–0.786 retracement of the range on the
discount side.

**Everything depends on how you define the range.** Different swing choices give different midpoints, and
therefore different "premium/discount" answers. State your anchors.

## 2. What it is really saying

The framework is a **location filter**, and it is closely related to two ordinary ideas:

1. **Mean reversion within a range** — buy low in the range, sell high.
2. **Retracement depth** — a 50–78.6% retracement of an impulse is a conventional pullback zone.

That is the entire content. It is useful, and it is not new. Presenting it as institutional insight is
over-claiming.

## 3. Using it

```
In an uptrend:
  a pullback into the discount zone (below the 50% of the last impulse leg) with a bullish reaction
  -> a location where a long has a structurally close invalidation (below the swing low)

In a downtrend:
  a bounce into the premium zone with a bearish reaction
  -> a location for a short with a close invalidation (above the swing high)
```

## 4. The trap it creates

In strong trends, price often *does not* return to the discount zone — it keeps making higher highs and shallow
pullbacks. Waiting for a deep discount means missing the trend. Conversely, in a range, "premium/discount" is just
the range position and adds nothing you did not already know.

Guard: use it as a **confluence**, not a gate. A shallow pullback in a strong uptrend at a tested level is a valid
setup even if it is technically still in "premium".

## 5. Common misuses

| Misuse | Why |
|--------|-----|
| Choosing anchors so the current price lands in the desired zone | Confirmation bias |
| Waiting for a deep discount in a strong trend | Misses the trade |
| Using it in a range as if it were new information | It is just position in the range |
| Calling the midpoint "equilibrium" as if it were a physical equilibrium | It is a definition |
| Ignoring the higher timeframe | A daily discount can be a 15m premium |

## 6. Report wording

> ✅ "Using the swing low 1,140 and swing high 1,300 as anchors, the midpoint is 1,220. Price at 1,204 is in the
> discount half, near the 0.618 retracement at 1,201. That is a favourable location for a long if support holds;
> the invalidation would be below 1,140, which is 64 points away — check whether that R:R is acceptable."
>
> ❌ "Price is in discount, so smart money will buy."

Note the second half of the first example: it immediately checks the arithmetic, which is where most
premium/discount analysis dies.

## 7. Beginner summary (Hinglish)

**Premium/discount kya hai?** Ek range ko **aadha** baant do. Upar wala half = premium (mehnga), neeche wala
half = discount (sasta).

**Rule:** uptrend mein **discount** mein kharido, downtrend mein **premium** mein becho. Kyunki tab stop paas
hota hai.

**Sabse bada problem:** range kahan se kahan tak hai — yeh aap choose karte ho. Galat anchors = galat answer.
Anchors likhna zaroori hai.

**Aur:** strong trend mein price discount tak aata hi nahi. Uska intezaar karte rehna = trade miss karna.

**Yaad rakho:** yeh sirf **location filter** hai — "institutional insight" nahi.

## 8. Exercise

Pick a swing and compute the midpoint. Then pick two different but defensible anchors and compute the midpoint
again. Compare the two. Then compute the R:R for a long at the current price using each midpoint's implied stop.
Write down whether the choice of anchor changed the trade decision.

---
*See also: [`liquidity.md`](liquidity.md) · [`../indicators/fibonacci.md`](../indicators/fibonacci.md) ·
[`../price-action/trend-continuation.md`](../price-action/trend-continuation.md)*
