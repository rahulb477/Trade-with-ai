# BOS — Break of Structure

**Plain language:** a close beyond the most recent swing high (in an uptrend) or swing low (in a downtrend),
continuing the existing structure.

## 1. Definition

```
Bullish BOS: close above the most recent confirmed swing high, while the structure is already HH/HL
Bearish BOS: close below the most recent confirmed swing low, while the structure is already LH/LL
```

Requirements:

1. The swing being broken must be **confirmed** (using a stated `k`-bar pivot definition).
2. The break must be a **close**, not a wick.
3. The structure must already be trending in that direction — otherwise it is a CHoCH, not a BOS.
4. Ideally the break has **displacement** (a wide-range bar, not a grind).

## 2. What it means (and does not)

**Means:** the trend's continuation is confirmed. Buyers (or sellers) were able to push beyond the previous
extreme and hold it into the close.

**Does not mean:** the trend will continue indefinitely, or that "institutions" are behind it.

## 3. Trading the BOS

| Approach | Entry | Invalidation | Notes |
|----------|-------|-------------|-------|
| Break close | On the close beyond the swing | Below the broken swing | Early; more false signals |
| Retest of the broken swing | On a hold at the swing level | Below the swing (further) | Better R:R, better quality |
| Continuation after the pullback | At the next higher low | Below that low | Best structure alignment |

The BOS is a **confirmation event**, not an entry trigger on its own. Combine with:

- Volume expansion on the breaking bar
- Room to the next structure (≥2 ATR)
- Higher-timeframe alignment
- A clean pullback reference for the stop

## 4. Failure: the failed BOS

A BOS that immediately reverses (price closes back below the broken swing) is a **failed break** — a trap. In SMC
vocabulary this is sometimes called a "liquidity sweep + reversal". In plain language: the breakout failed.

Failure is informative. It typically sets up the opposite direction, with the trapped breakout traders as fuel.

## 5. Common misuses

| Misuse | Why it is wrong |
|--------|-----------------|
| Calling every new high a BOS | Without a defined prior swing, "new high" is just a new high |
| Using a 1-bar pivot as the swing | Too noisy; every bar breaks something |
| Ignoring that a wick through the swing is not a BOS | Requires a close |
| Labelling a counter-trend break as a BOS | That is a CHoCH by definition |
| Using BOS as a standalone entry | It is confirmation |

## 6. Report wording

> ✅ "Price closed at 1,243.5, above the 15m swing high at 1,240 (confirmed with k=3). This is a bullish break of
> structure on the 15m. The next pullback holding above 1,240 would confirm continuation."
>
> ❌ "BOS confirmed, smart money is in."

## 7. Beginner summary (Hinglish)

**BOS = Break of Structure.** Uptrend mein jab price pichhle **swing high ke upar close** kar de, ya downtrend
mein pichhle **swing low ke neeche close** kar de.

**Matlab:** trend continue ho raha hai — buyers (ya sellers) ne pichhla extreme tod diya aur wahan hold kiya.

**Entry:** sirf BOS dekh kar nahi. BOS + retest + volume + upar jagah — tab.

**Galti:** wick ko BOS samajhna. Close chahiye. Aur ek baar pivot define karo (k=3), warna har bar "BOS" ban
jayega.

**Yaad rakho:** "smart money aa gaya" nahi likhna — woh verify nahi kiya ja sakta.

## 8. Exercise

Define the swing with k=3. Mark every close beyond a confirmed swing on a 15m chart for one day. For each, note
whether a pullback held the level, and what happened in the next 10 bars. Compute how many were genuine continuations
versus failed breaks. Report the count — and note that one day is not a sample.

---
*See also: [`choch.md`](choch.md) · [`../price-action/higher-highs-higher-lows.md`](../price-action/higher-highs-higher-lows.md)*
