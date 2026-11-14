# Morning Star

**Group:** Bullish reversal · **Candles:** 3 · **Reliability band:** Higher (rarer, more conditions)
**Detector:** `patterns.detect_morning_star`

---

## 1. What it is

A three-candle bottoming structure:

1. A **long bearish** candle continuing the decline.
2. A **small-bodied** candle (star) that gaps or trades below candle 1's body — indecision, selling
   pressure exhausted.
3. A **long bullish** candle that closes well into candle 1's body.

The sequence narrates a full handover: sellers driving, sellers stalling, buyers taking over. That
narrative — rather than the geometry alone — is why it carries more weight than a single candle.

---

## 2. Formation rules

| # | Rule |
|---|------|
| 1 | Candle 1 is bearish with a **long body** (`body₁ ≥ 1.0 × average_body`, commonly ≥ 60% of its range) |
| 2 | Candle 2 has a **small body** (`body₂ ≤ 0.4 × body₁`) — colour is less important than size |
| 3 | Candle 2's body sits **below** candle 1's body (gap down in ideal form; in 24-hour markets the gap is often absent and an overlap is accepted) |
| 4 | Candle 3 is bullish and closes **above the midpoint of candle 1's body** (strict: above candle 1's open) |
| 5 | Candle 3 closes well into candle 1 — `close₃ ≥ open₁ − 0.5 × body₁` at minimum |
| 6 | Prior trend is downward |
| 7 | All three candles closed |

Strictness note: in continuously traded markets (crypto, forex, index futures in liquid hours) true
gaps are rare. Accepting a body-position separation instead of a literal gap is standard practice,
but you must **say** that you did so.

Variants:

- **Morning Doji Star** — candle 2 is a doji (stronger indecision signal).
- **Abandoned Baby (bullish)** — candle 2 gaps away on both sides (see
  [`abandoned-baby.md`](abandoned-baby.md)); the rarest, strongest variant.

---

## 3. Anatomy

```
 1 bear        2 star          3 bull
 ┌────┐
 │    │                       ┌──────┐
 │    │                       │      │
 └────┘                       │      │
        ┌──┐                   └──────┘
        └──┘   <- small body, below candle 1
```

---

## 4. Where it means something

- At a support zone after a sustained decline (2+ weeks on daily, or an extended intraday slide)
- At the lower boundary of a descending channel
- At a measured-move completion (e.g. decline = 1.618 × prior swing)
- After a capitulation volume spike
- At a round psychological level with prior reactions

Weak: three sideways candles in a range that technically satisfy the rules.

---

## 5. Interpretation

The middle candle is the crucial part. It says **the selling stopped working** — every push down was
met with no further progress. Candle 3 then proves buyers were waiting.

Documented treatments rank it among the more reliable reversal formations precisely because it
requires three conditions to align; the cost is rarity. On lower timeframes it appears frequently
and is much less informative.

---

## 6. Confirmation requirements

Candle 3's close *is* the confirmation — the pattern is only valid once it closes per rule 4.
Additional confirmation:

| Level | Extra evidence |
|-------|----------------|
| Good | Candle 4 opens above candle 3's close and holds |
| Strong | Price breaks the swing high that started the decline |
| Strongest | Retest of candle 3's high area holds as support, with volume expansion |

---

## 7. Volume

| Volume profile | Reading |
|----------------|---------|
| High on candle 1 (capitulation), lower on candle 2 (exhaustion), high on candle 3 (reclaim) | Classic, strongest |
| Low on candle 2 only | Still acceptable |
| Very low on candle 3 | Suspect: the "reclaim" is unsupported |
| Rising on all three | Prices falling then rising on rising volume — check for news churn |

---

## 8. Paper-trade entry conditions (illustrative)

```
Long trigger   : candle 3's close (pattern-completion entry), or
                 break above candle 3's high (conservative)
Entry zone     : candle 3 close ± 0.2 × ATR
Invalidation   : below the lowest low of the three candles (usually candle 2's low) − 0.25 × ATR
Targets        : T1 candle 1's open (the top of the bearish body) — a natural magnet
                 T2 the most recent swing high before the decline
                 T3 measured move: height of the decline × 0.5–0.618 projected from the low
Position note  : because the stop is wide (three candles), size accordingly; the R:R must still
                 clear 1.5 to T1
```

---

## 9. Invalidation

1. Close below the pattern's low.
2. Candle 3 gives back more than ~50% of its body within two candles (failed reclaim).
3. The pattern forms directly under heavy resistance (no room).
4. Candle 2 is not actually small — recheck `body₂/body₁`.

---

## 10. Common false signals

| False signal | Guard |
|--------------|-------|
| Loose definition (no real gap/separation, tiny candle 3) | Enforce rule 2 and 4 numerically |
| Appears mid-trend in a range | Require a real preceding decline |
| Candle 3 closes into resistance | R:R gate |
| Three candles after a single red candle (no trend) | Require measurable decline |
| Weekend/holiday gap treated as a star gap | Verify the session calendar |
| Recurring morning stars in a strong downtrend | Each failure reduces the information content; after 2 fails, distrust the third |

---

## 11. Historical evidence — honest position

Multi-candle formations carry more information than single candles by construction (three
independent intervals constrain one another), and the literature generally treats the morning star
as a reliable reversal candidate. No specific success rate is claimed here. Test it on your data —
and note that on 1–5 minute charts it occurs so often that its informational value collapses.

---

## 12. Worked example (illustrative, fictional)

```
Instrument: GHI · Timeframe: Daily · Context: 3-week decline 340 -> 291; support 288–292.
C1: open 305, close 293 (bear, body 12)
C2: open 291, close 290 (body 1, below C1 body) ✔ small
C3: open 290.5, close 300.5 (bull, body 10) -> closes above C1 midpoint 299 ✔
Volume: high on C1, quiet on C2, 1.8x on C3 ✔
Status: CONFIRMED
Setup : entry 300.5 · invalidation 288.2 · risk 12.3
        T1 = 305 (C1 open) -> 4.5/12.3 = 0.37R FAIL
        T2 = 318 (prior swing high) -> 17.5/12.3 = 1.42R
Verdict: WAIT — fails the 1.5R gate to the first structural target.
        A pullback entry near 296 (retest) would give risk 7.8 and T2 at 2.75R ⇒ viable.
```

---

## 13. Beginner summary (Hinglish)

**Morning star = teen candles ka bottom pattern.**

1. Pehli badi red candle — sellers strong.
2. Doosri chhoti candle — sellers thak gaye, kuch progress nahi hua.
3. Teesri badi green candle — buyers ne control le liya, aur pehli candle ke aadhe se upar close kiya.

**Teen candles ka matlab:** ek poori kahani — girawat, rukawat, wapsi.

**Entry:** teesri candle ke close par, ya uski high tootne par.

**Stop loss:** teeno candles ki sabse neeche low ke thoda neeche.

**Dhyan:** stop bada hota hai, isliye position size chhota rakho. Aur agar upar turant resistance hai
to trade ka koi matlab nahi.

---

## 14. Exercise

Find three morning stars on a daily chart. Measure: (a) `body₂/body₁` for each, (b) whether C3 closed
above C1's midpoint, (c) the R:R to C1's open, (d) the R:R to the prior swing high. Then answer:
how many of the three were worth taking *on the arithmetic alone*? Most beginners are surprised by
how often the answer is "zero".

---

*See also: [`evening-star.md`](evening-star.md) · [`morning-star` variants in `abandoned-baby.md`](abandoned-baby.md) ·
[`doji.md`](doji.md)*
