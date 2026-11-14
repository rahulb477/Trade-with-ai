# Inside Bar

**Group:** Indecision / compression · **Candles:** 2 · **Reliability band:** Contextual
**Detector:** `patterns.detect_inside_bar`

## 1. What it is
A candle whose **entire range** (high and low) sits **inside** the previous candle's range. Volatility
compressed: the market traded entirely within the prior interval's territory.

## 2. Formation rules
| # | Rule |
|---|------|
| 1 | `high₂ ≤ high₁` and `low₂ ≥ low₁` |
| 2 | Strictly inside is preferred: `high₂ < high₁` and `low₂ > low₁` |
| 3 | Candle 1 should have a real range (`range₁ ≥ 0.8 × average_range`) — otherwise the "mother bar" is noise |
| 4 | Both closed |

Related terms:

- **Inside bar** = range containment (colour-agnostic).
- **Harami** = *body* containment with opposite colours and a prior trend (see [`harami.md`](harami.md)).
- **NR7 / narrow range** = a bar with the smallest range of the last 7 — a compression measure, not a
  pattern.

## 3. Anatomy
```
 ┌──────────┐   <- mother bar
 │   ┌───┐  │   <- inside bar
 │   └───┘  │
 └──────────┘
```

## 4. Where it means something
- Inside a trend, as a **continuation pause** (most common and most useful)
- At a level, as coiling before a test
- Multiple consecutive inside bars = a genuine compression (a "squeeze") — the most useful version
- After a large expansion candle (a wide-range bar), an inside bar is often a digestion pause

Mid-range in a choppy market, inside bars are ubiquitous and meaningless.

## 5. Interpretation
Compression precedes expansion. The pattern does not tell you **which way** the expansion will go —
only that a resolution is more likely than continued quiet. Direction comes from the trend, the level,
and the breakout candle.

This is why inside bars are traded as **breakout setups** rather than as reversal signals.

## 6. Confirmation requirements
| Level | Confirmation |
|-------|--------------|
| Minimum | A close above the mother bar's high, or below its low |
| Good | Same, with volume ≥ 1.3× average |
| Strong | Breakout then a retest of the mother bar boundary that holds |
| Invalidated | Price returns inside the mother bar and stays there for several candles |

## 7. Volume
Compression usually comes with **falling** volume (participants waiting). The breakout candle's volume
is the critical input: expansion on weak volume is the classic failed breakout.

## 8. Paper-trade entry conditions (illustrative)
```
Bias first    : direction of the higher-timeframe trend.
Long case     : close above mother-bar high + 0.1 × ATR, volume ≥ 1.3× average
                invalidation: mother-bar low (or the inside bar's low for a tighter stop)
                targets: prior swing high, then measured move = mother-bar range projected
Short case    : mirror, close below mother-bar low
Straddle alt  : bracket both sides; accept that one side will be a false trigger and pay the cost
```

## 9. Invalidation
Close back inside the mother bar after a breakout; two consecutive closes inside the range; the
higher-timeframe trend flipping.

## 10. Common false signals
| Signal | Guard |
|--------|-------|
| Breakout on low volume | Volume floor |
| Mother bar itself tiny | Rule 3 |
| Breakout into immediate resistance | Check room |
| Trading the inside bar before resolution | Wait for the close |
| Counting every 2-bar containment as a "setup" | Require a real mother bar and a real level |

## 11. Historical evidence — honest position
Inside-bar breakouts are widely used and equally widely reported to fail on low volume. The mechanism
is structural (compression → expansion), not statistical. Measure your own hit rate; do not assume one.

## 12. Worked example (illustrative, fictional)
```
Instrument: FGH · 15m · uptrend; mother bar o210.4 h213.0 l209.8 c212.6
Inside bar: o212.2 h212.8 l211.0 c211.6 (fully inside ✔)
Volume: mother 1.2× avg, inside 0.6× avg (compression), breakout 1.9× avg
Entry : close above 213.0 → 213.2 · invalidation 209.6 (mother low, buffer) · risk 3.6
T1 216.6 (measured: mother range 3.2 projected) → 0.94R FAIL
T2 219.0 (prior swing high) → 1.61R ✔
Verdict: WAIT on the measured-move target; the swing high target gives an acceptable setup only if
        the stop is tightened to the inside bar's low (risk 2.2 → 2.55R). State which stop you used.
```

## 13. Beginner summary (Hinglish)
**Inside bar:** ek candle jo poori tarah pichhli candle ke **andar** rehti hai — high neeche, low upar.

**Matlab:** volatility compress ho gayi. Compression ke baad expansion aata hai — par **direction**
pattern nahi batata.

**Direction kaise?** Higher timeframe trend aur level se.

**Entry:** mother bar ki high tootne par (long) ya low tootne par (short), volume ke saath.

**Stop:** mother bar ke doosri taraf.

## 14. Exercise
Find a sequence with three or more consecutive inside bars (a squeeze). Record the mother bar's range,
then the breakout direction and the volume. Compare with two single inside bars elsewhere. Write down
whether the multi-bar squeeze broke out more decisively — and whether your sample is big enough to
claim anything.

---
*See also: [`harami.md`](harami.md) · [`three-inside-up.md`](three-inside-up.md) · [`../chart-patterns/rectangle.md`](../chart-patterns/rectangle.md)*
