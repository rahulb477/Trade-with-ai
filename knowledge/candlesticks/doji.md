# Doji

**Group:** Neutral / indecision · **Candles:** 1 · **Reliability band:** Lower alone; meaningful at extremes
**Detector:** `patterns.detect_doji`

## 1. What it is
A candle whose **open and close are essentially equal**, producing a very small or non-existent body.
It represents a session in which neither side achieved a decisive close.

## 2. Formation rules
| # | Rule | Threshold |
|---|------|-----------|
| 1 | `body / range ≤ 0.05` | Standard doji |
| 2 | `range ≥ 0.5 × average_range(20)` | Avoid flat/illiquid bars counting as doji |
| 3 | Closed candle | Else `DEVELOPING` |

A stricter screen: `body / range ≤ 0.03`. Some practitioners use an absolute tick tolerance instead
(`|close − open| ≤ 1 tick`), which matters on very liquid instruments where a 0.05 body is still
several ticks.

## 3. Variants

| Variant | Shape | Reading |
|---------|-------|---------|
| **Standard doji** | Small wicks both sides | Pure indecision |
| **Long-legged doji** | Very long wicks both sides, range ≫ average | Extreme indecision, high volatility, no resolution |
| **Dragonfly doji** | Long lower wick, no upper wick | Sellers drove down, buyers fully recovered — bullish at support |
| **Gravestone doji** | Long upper wick, no lower wick | Buyers drove up, sellers fully recovered — bearish at resistance |
| **Four-price doji** | O = H = L = C | Almost no trading; illiquid or a halt — usually not meaningful |

## 4. Anatomy
```
   │          │         ▲            │
   │          │         │            │
 ──┼──      ──┼──     ──┼──        ──┼──
   │          │                      │
   │          │                      │
 standard   long-leg  dragonfly   gravestone
```

## 5. Where it means something
- At a **trend extreme** after an extended move: potential exhaustion.
- At a **major level** (support/resistance, round number): a rejection test.
- At the **top of a gap-up** opening: the gap was not held.
- Inside a **compression** before a breakout: the doji is just part of the range.

Mid-trend dojis are extremely common and carry almost no information. A chart with ten dojis in
twenty candles is a chart with no trend.

## 6. Interpretation
A doji is a **question, not an answer**. It says the auction found equilibrium for one interval.
The answer comes from what price does next.

Dragonfly at support and gravestone at resistance are the only variants with directional lean, and
even they need confirmation.

## 7. Confirmation requirements
- Never trade a doji alone.
- Bullish case: next candle closes above the doji's high, at a support.
- Bearish case: next candle closes below the doji's low, at a resistance.
- Doji within a compression: wait for the range to resolve; the doji itself is not the trigger.

## 8. Volume
Very low volume on a doji = genuine apathy (often before an expansion move — direction unknown).
Very high volume on a doji = a real battle; the winner of the next interval often runs.
Volume therefore tells you *how much* the resolution will matter, not *which* way.

## 9. Paper-trade entry conditions (illustrative)
Dojis are **not** standalone entries. Used as confluence:
```
Bullish case  : dragonfly at tested support + next close above doji high
                entry: above doji high · invalidation: below doji low · targets: prior swing high
Bearish case  : gravestone at tested resistance + next close below doji low
                entry: below doji low · invalidation: above doji high · targets: prior swing low
Never         : enter on the doji's close. There is no directional information in it yet.
```

## 10. Invalidation
For a doji-based thesis: a close beyond the opposite side of the doji's range. For a
dragonfly-at-support thesis: a close below the dragonfly's low, which means the long lower wick was
the market's way of pricing a breakdown that has now happened.

## 11. Common false signals
| Signal | Guard |
|--------|-------|
| Counting every tiny-body candle as a doji | Enforce the ratio and the range floor |
| Interpreting a mid-trend doji as a reversal | Require a trend extreme or a level |
| Treating a four-price doji as significant | Check for illiquidity/halt |
| Reading a doji in a Heikin-Ashi chart as real | HA synthesises bodies; the doji is not real OHLC |
| Entering before the resolution | Wait for the following close |

## 12. Historical evidence — honest position
The literature is consistent that the doji is an *indecision* marker whose usefulness depends
entirely on location. Attempts to assign a directional edge to a bare doji have not produced stable
results. No number is claimed here.

## 13. Worked example (illustrative, fictional)
```
Instrument: WXY · 1D · decline 480 → 442 into support 440–444
Candle: o444.0 h447.2 l440.1 c444.1 · body 0.1 · range 7.1 · body/range = 1.4% ✔ doji
        lower_wick 3.9 · upper_wick 3.1 → long-legged doji
Next  : closes 447.9 (above doji high 447.2) on 1.5× volume ✔
Status: doji DEVELOPING → CONFIRMED as a reversal trigger only after the next close
Setup : entry 448.1 · invalidation 439.8 (below support/doji low) · risk 8.3
        T1 459 (prior swing high) → 1.31R FAIL · T2 468 → 2.40R ✔
Verdict: WAIT on T1; acceptable with T2/T3 as primary targets.
```

## 14. Beginner summary (Hinglish)
**Doji:** aisi candle jisme open aur close lagbhag barabar ho — body na ke barabar.

**Matlab:** us session mein kisi ka control nahi bana — buyers aur sellers barabar the. Yeh **sawal**
hai, **jawab** nahi.

**Kab important?** Jab trend ke end mein ya kisi bade support/resistance par aaye.

**Dragonfly doji** (neeche lambi wick) support par bullish hota hai. **Gravestone doji** (upar lambi
wick) resistance par bearish.

**Entry:** doji par kabhi nahi. Agli candle uski high/low tod de, tab socho.

## 15. Exercise
Find a chart segment with at least eight dojis. Classify each by location (extreme / level /
mid-range / compression). Then check what happened next. You should find that the *location* predicts
the usefulness far better than the shape.

---
*See also: [`spinning-top.md`](spinning-top.md) · [`high-wave.md`](high-wave.md) · [`morning-star.md`](morning-star.md)*
