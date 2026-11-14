# Liquidity — Pools, Buy-Side, Sell-Side, Sweeps

**Plain language:** "liquidity" here means **resting orders** — and in practice, mostly **stop-losses** —
clustered at predictable prices.

## 1. Where stops cluster (this part is verifiable logic)

| Location | Why stops cluster there |
|----------|------------------------|
| Just above equal highs | Shorts place stops above resistance; breakout buyers place buy-stops above |
| Just below equal lows | Longs place stops below support; breakdown traders sell-stop beneath |
| Just beyond a round number | Psychological reference; many orders |
| Just beyond a prior session high/low | Day traders' standard stop placement |
| Just beyond a pattern boundary | Textbook stop placement — everyone was taught the same level |
| Just beyond the prior day's close | Overnight positioning |

This is not a theory of intent; it is a statement about where people put orders. That much is publicly documented
and is why "stop hunting" is a reasonable description of observable behaviour around such levels.

## 2. Buy-side vs sell-side liquidity

```
Buy-side liquidity  = resting BUY orders (and short stops) ABOVE current price
                      -> typically above highs. Buying it "sweeps" it.
Sell-side liquidity = resting SELL orders (and long stops) BELOW current price
                      -> typically below lows.
```

Note the naming is from the perspective of what gets triggered. Some texts invert it; state your convention.

## 3. Liquidity sweep

**Definition:** price trades briefly beyond a level where stops cluster, then closes back inside — triggering
those orders without accepting the new price.

```
Sweep above:  wick > prior high, close < prior high  (bearish implication)
Sweep below:  wick < prior low,  close > prior low   (bullish implication)
```

Requirements to call it a sweep rather than a breakout:

1. There was a **prior, clearly identifiable level**.
2. Price **traded beyond** it.
3. Price **closed back inside** on the same bar or within 1–2 bars.
4. There is a visible **reaction** away from the level.

Without all four, "sweep" is a story told after the fact.

## 4. What a sweep does and does not prove

| It does prove | It does not prove |
|---------------|-------------------|
| Stops were likely triggered | That a specific participant did it deliberately |
| The level was rejected | That the trend will now reverse |
| There is a reference level for invalidation | That you should enter immediately |

The honest framing: **a sweep is a failed break with a defined invalidation.** That is enough to trade; you do not
need the institutional story.

## 5. Trading a sweep (hypothetical)

```
Sweep below support (bullish reading):
  trigger      : a close back above the swept level
  entry        : on that close, or on a shallow retest of the level from above
  invalidation : below the sweep's low
  targets      : the opposite side of the range; the prior swing high
  quality      : volume spike on the sweep bar; higher timeframe not strongly opposed

Sweep above resistance (bearish reading): mirror.
```

The invalidation is the sweep's extreme — a clean, structural, falsifiable level. That is the practical value of
the concept.

## 6. Failure modes

| Failure | Meaning |
|---------|---------|
| Price sweeps and then continues in the breakout direction | It was a genuine breakout, and the "sweep" reading was wrong |
| Repeated sweeps of the same level | The level is being consumed; it will eventually break |
| Calling every wick a sweep | Requires a prior identifiable level and a close back inside |
| Sweep on a very low-volume bar | Possibly a data artefact or an illiquid print |

## 7. Equal highs / equal lows

Two or more highs (or lows) at nearly the same price create an obvious liquidity reference. Common behaviours:

1. **The level holds repeatedly** — supply/demand is real there.
2. **The level is swept and rejected** — a trap; reversal potential.
3. **The level breaks and holds** — absorption; continuation.

You cannot know which in advance. Plan for all three with explicit triggers.

## 8. Beginner summary (Hinglish)

**Liquidity ka matlab yahan:** logon ke **stop-loss** jahan cluster hote hain.

**Kahan hote hain?** Equal highs ke thoda upar, equal lows ke thoda neeche, round numbers ke bahar, aur pattern
ki boundary ke bahar. Kyunki sabko yahi sikhaya gaya hai.

**Sweep kya hai?** Price us level ke bahar **wick** maar kar wapas andar close ho jaye — stops trigger ho gaye,
par price wahan accept nahi hua.

**Char cheezein chahiye:** pehle se level ho, price bahar jaye, **close wapas andar** aaye, aur reaction dikhe.

**Trade kaise?** Close wapas level ke andar aane par, stop sweep ki extreme ke bahar. Bas itna — "institutions ne
kiya" jaisi kahani ki zaroorat nahi.

**Galti:** har wick ko sweep kehna. Level hona zaroori hai.

## 9. Exercise

Find two equal highs. Track what happened: hold, sweep-and-reject, or break-and-hold. Record the volume on the
deciding bar. Do this for five pairs and tabulate the three outcomes. Report the counts — and note that five
pairs cannot establish frequencies.

---
*See also: [`order-blocks.md`](order-blocks.md) · [`premium-discount.md`](premium-discount.md) ·
[`../../workflows/trap-detection.md`](../../workflows/trap-detection.md) · [`../market-structure/level-mapping.md`](../market-structure/level-mapping.md)*
