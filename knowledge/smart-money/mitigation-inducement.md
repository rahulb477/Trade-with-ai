# Mitigation and Inducement

Two SMC terms describing *why* price returns to a zone. Both are interpretations. Use them as descriptions of
behaviour, never as claims about intent.

---

## Part 1 — Mitigation

**Plain language:** price returning to the zone where an earlier move originated, so that participants who are
underwater can exit near break-even.

### 1. Definition
A **mitigation block** is the zone from which a prior impulse began that later left traders on the wrong side. When
price returns there, those traders get a chance to exit at a smaller loss. The behaviour is visible as:
price returns to the zone, reacts, and then continues in the original (impulse) direction.

Example: price falls from 1,240 to 1,200, then rallies to 1,280. Traders who bought at 1,240 are underwater; a
return to 1,240 lets them exit at break-even, and that selling is absorbed.

### 2. What is observable vs story
| Observable | Story |
|-----------|-------|
| Price returns to a prior origin zone | "Underwater traders are exiting" |
| A visible reaction there | "That flow has been absorbed" |
| Continuation after the reaction | "The market has been mitigated" |

The first two are observable. The third is a narrative that **only becomes true if price continues**.

### 3. Honest use
It is a **zone-retest** concept. In plain terms: "the origin of the last impulse is a reference zone; a
reaction there with continuation is a valid continuation setup, and a close through the zone invalidates it."
That is exactly the ordinary retest rule (see `knowledge/price-action/retest.md`), with a new name.

---

## Part 2 — Inducement

**Plain language:** a **minor** liquidity grab that tempts traders into a position before the real move happens.

### 1. Definition
Inducement is usually described as a small swing high/low, *inside* the larger structure, that gets swept just
before price moves in the intended direction. Traders who entered on the small break are stopped out.

### 2. The uncomfortable truth
**Inducement can only be identified after the fact.** Any minor swing that gets swept looks like "inducement" in
hindsight. In real time you cannot distinguish:

- a minor liquidity grab before a real move (inducement), from
- an ordinary false breakout, from
- a genuine small continuation that then reverses for unrelated reasons.

Anyone presenting inducement as a real-time signal is describing a retrospective pattern.

### 3. What you *can* do
1. Expect noise around **obvious minor levels** — that is a legitimate planning input.
2. Place stops beyond the minor level *and* the sweep's likely reach (an ATR buffer), not exactly at the minor
   level.
3. Do not add to a position based on an "inducement" you believe you can see forming.

### 4. Practical rule
```
If you would enter on a minor structure break, ask: is there an obvious stop cluster just beyond it?
If yes, widen the invalidation or reduce size — do not assume the break is clean.
```

That is the useful, non-speculative version of the inducement concept.

---

## 3. Combined report wording

> ✅ "The last impulse started at 1,196–1,202. A return into that band with a bullish reaction candle would be a
> continuation reference; a close below 1,192 voids it. Note the minor swing low at 1,210 — stops just below it
> may be targeted, so a stop at 1,208 is at risk of being swept; use 1,205 or reduce size."
>
> ❌ "Price induced retail longs at 1,210 then mitigated the 1,198 block before the real move up."

The second sentence is unfalsifiable and reads as certainty about intent.

---

## 4. Beginner summary (Hinglish)

**Mitigation:** jab price wapas us zone par aata hai jahan se pichhla tez move shuru hua tha — wahan jo log loss
mein phase the, unko exit ka mauka milta hai. **Practical matlab:** yeh ek **zone retest** hai. Bas.

**Inducement:** chhota sa liquidity grab jo aapko galat entry mein phansa deta hai (aapka stop hit ho jata hai),
aur uske baad asli move aata hai.

**Sach:** inducement **baad mein** hi pata chalta hai. Real time mein aap nahi keh sakte ki yeh inducement hai ya
normal false breakout.

**Isse kya karein:**
1. Obvious chhote levels ke around noise expect karo.
2. Stop bilkul level par na rakho — **ATR buffer** ke saath bahar rakho.
3. "Inducement dikh raha hai" bol kar position add mat karo.

---

## 5. Exercise

Take a move with a clear impulse origin. Mark the origin zone and the minor swing inside the structure. Then check:
(a) did price return to the origin zone? (b) was the minor swing swept before the move? (c) how far beyond the
minor swing did the sweep go, in ATR? Use (c) to choose a buffer for future stops — and write down that one
example is not enough to calibrate it.

---
*See also: [`order-blocks.md`](order-blocks.md) · [`liquidity.md`](liquidity.md) · [`bos.md`](bos.md)*
