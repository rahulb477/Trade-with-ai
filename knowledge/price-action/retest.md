# Retest

## 1. Definition
A **retest** is price returning to a level it previously broke, to check whether the break holds. In an uptrend
after a breakout, price pulls back to the broken resistance, which should now act as support. In a downtrend after
a breakdown, price bounces to the broken support, which should now act as resistance.

```
Bullish retest                     Bearish retest
   ──── break ────                    ┌────── prior support
       ╱                               ╲
      ╱  run                            ╲  breakdown
     ╱                                   ╲
 ───╱──── retest ───                 ────╱──── retest from below
    ╲  (holds)                            (rejects)
```

## 2. Why it exists
After a level breaks, three groups act:

1. **Breakout traders** who entered late want a better price — they buy the retest.
2. **Trapped traders** from the wrong side want to exit at break-even — they sell into the retest.
3. **Stop hunters** target the cluster of stops just inside the prior range.

The retest is where you find out which of these dominates. That is why it carries information.

## 3. A valid retest has four parts

| Part | Requirement |
|------|-------------|
| **Return** | Price comes back to the broken level (within a small tolerance, e.g. 0.2–0.5 ATR) |
| **Hold** | The level is not closed back through in the wrong direction |
| **Rejection** | A visible reaction: wick rejection, engulfing candle, or a close away from the level |
| **Volume** | Typically *lower* volume on the retest than on the breakout — healthy. Higher volume on the retest can signal failure |

## 4. Using a retest for entry

```
Long (after a breakout):
  trigger      : a bullish candle closes away from the level after touching it
  entry        : the close of that candle, or the level + 0.1 ATR
  invalidation : below the retest low (not below the whole prior range — that is far too wide)
  targets      : measured move from the breakout, next structural resistance

Short (after a breakdown): mirror.
```

The retest entry is usually the **best R:R** because the invalidation is close and structurally meaningful. Its
cost is opportunity: many breakouts run without retesting.

## 5. When a retest fails

| Failure type | Behaviour | Implication |
|--------------|-----------|-------------|
| Deep retest | Price closes back inside the prior range | The breakout failed; likely a trap |
| Slow bleed through | Repeated closes back inside over several bars | Distribution/absorption; trend change risk |
| Retest on rising volume | Sellers/buyers are more aggressive than the breakout's | The breakout was weak — expect failure |

A **failed retest** is itself a trade signal in the opposite direction: it traps the breakout traders.

## 6. Retest vs "second chance"

Do not confuse a retest with a **new test of the original level from the same side**. If price never actually
broke meaningfully, going back to the level is just another test — not a retest. The distinction matters because
a failed retest is only meaningful if the break was real.

## 7. Timeframe interaction

- A retest on the 15m chart may be a single wick; on the 1h chart it may be a multi-bar pullback.
- A retest that coincides with a higher-timeframe level (e.g. the 50-EMA or a prior swing) is stronger.
- A retest that takes longer than the breakout took to develop is often a sign of weakness, not patience.

## 8. Common errors

| Error | Guard |
|-------|-------|
| Calling any pullback a "retest" | Require that the level was actually broken first |
| Waiting for a retest that never comes | Have a plan for both; do not chase |
| Placing the stop below the entire prior range | Use the retest low |
| Ignoring volume on the retest | Volume tells you which side is more aggressive |
| Entering on the touch without a rejection | Require a close/reaction |

## 9. Beginner summary (Hinglish)

**Retest kya hai?** Jab price kisi toote hue level par **wapas** aata hai — yeh check karne ke liye ki break
asli tha ya nahi.

**Uptrend mein:** resistance toota, price wapas us level par aaya, aur wahan se **upar** gaya → level ab support
ban gaya → yeh **valid retest** hai, aur sabse achha entry.

**Downtrend mein:** support toota, price wapas us level par aaya, aur wahan se **neeche** reject hua → level ab
resistance.

**Char cheezein chahiye:** wapas aana, hold karna, rejection dikhna, aur volume kam hona (breakout se).

**Stop:** retest ki low ke neeche (poora range nahi).

**Agar retest fail ho jaye** (price wapas range ke andar close kar de) → breakout trap tha, aur woh khud
opposite direction ka signal hai.

## 10. Exercise

Find three breakouts that produced a clean retest and three that never retested. For the retested ones, compute
the R:R at the retest entry versus at the breakout close. Then answer: what did you give up by waiting, and what
did you gain? Write it in two lines.

---
*See also: [`breakout.md`](breakout.md) · [`breakdown.md`](breakdown.md) · [`rejection.md`](rejection.md) ·
[`../../workflows/trap-detection.md`](../../workflows/trap-detection.md)*
