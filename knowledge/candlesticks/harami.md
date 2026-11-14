# Harami (Bullish and Bearish)

**Group:** Reversal / pause · **Candles:** 2 · **Reliability band:** Moderate
**Detector:** `patterns.detect_harami`

## 1. What it is
A two-candle pattern in which the **second candle's body is entirely contained within the first
candle's body**, with **opposite colours**, after a trend. "Harami" means *pregnant* in Japanese — the
second body sits inside the first.

- **Bullish harami:** bearish candle 1, bullish candle 2 inside it, after a decline.
- **Bearish harami:** bullish candle 1, bearish candle 2 inside it, after an advance.

## 2. Formation rules
| # | Rule |
|---|------|
| 1 | Candle 1 has a real body (`body₁ ≥ 0.6 × average_range`) |
| 2 | Candle 2 body is inside candle 1 body: `max(open₂,close₂) ≤ max(open₁,close₁)` and `min(open₂,close₂) ≥ min(open₁,close₁)` |
| 3 | Opposite colours |
| 4 | Candle 2's body is clearly smaller: `body₂ ≤ 0.6 × body₁` |
| 5 | Prior trend exists (down for bullish, up for bearish) |
| 6 | Both closed |

## 3. Difference from an inside bar
An inside bar constrains **ranges** (high/low); a harami constrains **bodies** and additionally
requires opposite colours and a prior trend. A candle can be an inside bar without being a harami, and
vice versa. Do not use the terms interchangeably in a report.

## 4. Anatomy
```
Bullish harami                 Bearish harami
 ┌────────┐                    ┌────────┐
 │        │   ┌──┐             │        │   ┌──┐
 │        │   └──┘             │        │   └──┘
 └────────┘                    └────────┘
 (bear, then small bull)       (bull, then small bear)
```

## 5. Where it means something
At support (bullish) or resistance (bearish); at the end of an extended move; as the first sign of a
stall inside a trend. It is an **early** signal — earlier than engulfing and therefore less reliable.

## 6. Interpretation
The market lost the ability to extend in the trend's direction. Candle 2's small body inside candle 1
means participants could not push price beyond the previous day's opening range. It is a warning of
weakening momentum, not a reversal by itself.

Documented treatments treat the harami as a *pause* that becomes a reversal only when the third candle
breaks out in the new direction (see [`three-inside-up.md`](three-inside-up.md) and
[`three-inside-down.md`](three-inside-down.md)).

## 7. Confirmation requirements
| Level | Bullish confirmation |
|-------|---------------------|
| Minimum | Candle 3 closes above candle 1's open |
| Good | Candle 3 closes above candle 1's high, with volume |
| Strong | Prior swing high breaks; retest holds |
| Invalidated | Close below candle 2's low (or candle 1's low for a structural stop) |

## 8. Volume
Contracting volume on candle 2 is normal and supports "indecision". Volume expansion on candle 3 is
the confirmation. A harami on *expanding* volume is ambiguous — a battle, not a pause.

## 9. Paper-trade entry conditions (illustrative)
```
Bullish:
  trigger    : close above candle 1's open (minimum) or high (preferred)
  entry zone : trigger ± 0.1 × ATR
  invalidation: below min(low₁, low₂) − 0.25 × ATR
  targets    : T1 candle 1's high · T2 prior swing high · T3 measured decline × 0.5
Bearish: mirror.
Preference : trade the three-candle resolution, not the harami itself.
```

## 10. Invalidation
As above; additionally, if price sits inside the harami's range for more than ~4 candles the pattern
has gone stale — the compression is now just a range.

## 11. Common false signals
| Signal | Guard |
|--------|-------|
| Calling any small candle a harami | Rules 2, 3, 4 numerically |
| Ignoring the prior trend | Rule 5 |
| Trading the harami without the third candle | Require the resolution |
| Tiny candle 1 | Rule 1 |
| Confusing with inside bar | Use the definitions in §3 |

## 12. Historical evidence — honest position
The literature treats the harami as a lower-conviction pattern than the engulfing, for the structural
reason that it requires no decisive close. Three-candle versions add that close. No statistic is
claimed here.

## 13. Worked example (illustrative, fictional)
```
Instrument: IJK · 1D · decline 620 → 578
C1: o596 c580 (bear, body 16) · C2: o584 h586 l581 c585 (bull, body 1, inside C1 body 580–596 ✔)
C3: o585.5 c597.5 (closes above C1 open 596 ✔) volume 1.6× ✔
Status: CONFIRMED (as three-inside-up)
Entry 598 · stop 576.5 (risk 21.5) · T1 596 (negative) · T2 612 (0.65R FAIL)
Verdict: WAIT — stop is far too wide for the available targets. This is a pattern worth watching,
        not a setup worth taking. The honest report says exactly that.
```

## 14. Beginner summary (Hinglish)
**Harami:** do candles — doosri candle ki body poori tarah pehli candle ki body ke **andar** ho, aur
rang ulta ho.

**Matlab:** market ne trend ki direction mein aage badhna band kar diya — momentum kamzor ho raha hai.

**Yeh reversal nahi hai** — sirf pause ka signal. Reversal tab banta hai jab **teesri candle** nayi
direction mein pehli candle ke open/high ko tod de.

**Entry:** teesri candle ke breakout par. **Stop:** dono candles ki sabse neeche low ke neeche.

## 15. Exercise
Find a bullish harami that was followed by a third candle closing above candle 1's open, and one that
was not. Compare what happened over the next 10 candles. Then write a one-sentence rule explaining why
the third candle is the actual signal.

---
*See also: [`inside-bar.md`](inside-bar.md) · [`three-inside-up.md`](three-inside-up.md) · [`bullish-engulfing.md`](bullish-engulfing.md)*
