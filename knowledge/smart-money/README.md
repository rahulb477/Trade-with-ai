# Smart Money Concepts (SMC) — Read This First

## 0. The disclaimer that governs this entire section

**SMC is a descriptive framework, not a proven model of institutional behaviour.**

Nothing in this directory is evidence that "institutions" or "smart money" did anything. There is no public data
that identifies the intent behind a price move. What SMC actually offers is a **vocabulary for describing price
structure** — where liquidity rests, where the market moved fast, where it moved slowly, and where structure
changed. That vocabulary is genuinely useful. The causal story attached to it usually is not verifiable.

Concrete rules for using this material:

| Rule | Reason |
|------|--------|
| Never write "smart money is accumulating" | You cannot know that. Write "price behaviour is consistent with the accumulation framework" or simply describe the structure. |
| Never present an order block as a fact | It is a zone you drew; its predictive value must be measured, not assumed. |
| Never claim an FVG "will be filled" | Gaps are sometimes filled and sometimes not. State it as a watch level. |
| Never use SMC to override risk rules | A "perfect" order block with no invalidation is not a setup. |
| Always prefer plain-language terms in the final report | "Break of structure" is understandable; "MSS with inducement" usually is not. |

If a user asks for SMC analysis, you may use the terminology — but every term must be paired with a plain-language
translation and a statement of what would prove it wrong.

---

## 1. Why the framework appeals

SMC reframes ordinary price action:

| SMC term | Ordinary equivalent |
|----------|---------------------|
| Break of Structure (BOS) | Continuation: a close beyond the last swing in trend direction |
| Change of Character (CHoCH) | The first counter-trend structure break |
| Market Structure Shift (MSS) | A CHoCH plus a displacement leg |
| Order Block | The last opposite-coloured candle before an impulsive move (a zone) |
| Fair Value Gap (FVG) | A three-candle imbalance — a price range with little traded volume |
| Liquidity pool | A cluster of stops above/below equal highs/lows |
| Liquidity sweep | A wick beyond a level that closes back inside |
| Premium / Discount | Where price sits in a range (above/below the 50% midpoint) |
| Mitigation | Price returning to an origin zone |
| Inducement | A minor liquidity grab that traps early entries before the real move |

Every one of these has a plain-price-action equivalent. That is the honest framing: **SMC is a renamed subset of
market structure plus liquidity reasoning.**

---

## 2. Modules

| Topic | File |
|-------|------|
| BOS | [`bos.md`](bos.md) |
| CHoCH | [`choch.md`](choch.md) |
| MSS | [`mss.md`](mss.md) |
| Order blocks | [`order-blocks.md`](order-blocks.md) |
| Fair value gaps | [`fair-value-gaps.md`](fair-value-gaps.md) |
| Liquidity (pools, buy-side, sell-side, sweeps) | [`liquidity.md`](liquidity.md) |
| Premium and discount | [`premium-discount.md`](premium-discount.md) |
| Mitigation and inducement | [`mitigation-inducement.md`](mitigation-inducement.md) |

---

## 3. How to use SMC responsibly in a report

1. **Primary description in plain language.** "Price broke the last swing high at 1,240 and held above it."
2. **Optional SMC label in parentheses.** "(BOS on the 15m.)"
3. **Evidence for the label.** The level, the close, the volume.
4. **Falsification.** What would show the reading is wrong.
5. **No intent claims.** Describe behaviour, not motives.

Example:

> ✅ Price closed above the prior swing high at 1,240 (break of structure on the 15m) and retested it at 1,241
> without closing back below. That is a structural continuation signal. If price closes back below 1,238, the
> break has failed and the trap reading takes over.
>
> ❌ Smart money swept liquidity above 1,240 and is now accumulating for the next leg up.

The second sentence cannot be verified, cannot be falsified, and would lead a beginner to over-trust the setup.

---

## 4. What SMC does not do

- It does not identify institutions.
- It does not predict the next move.
- It does not have published, peer-reviewed support as a trading system.
- It does not remove the need for invalidation, sizing, or regime awareness.
- It does not excuse ignoring volume, higher timeframes, or event risk.

---

## 5. Testing SMC claims

If you want to know whether an SMC construct works, treat it as a hypothesis and measure it:

```
1. Define it mechanically (e.g. "the last bearish candle before a 3-bar impulse of > 1.5 ATR").
2. Define the entry, invalidation and target rules.
3. Scan a long history with costs (engines/backtesting/).
4. Report sample size, hit rate with a confidence interval, expectancy in R.
5. Split in-sample / out-of-sample.
```

Until then, say "this is a framework, not a measured edge". That is the position of this repository.

---

*See also: [`../market-structure/`](../market-structure/) · [`../price-action/`](../price-action/) ·
[`../../workflows/trap-detection.md`](../../workflows/trap-detection.md)*
