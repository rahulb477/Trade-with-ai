# Bullish Engulfing

**Group:** Bullish reversal · **Candles:** 2 · **Reliability band:** Moderate–Higher
**Detector:** `patterns.detect_bullish_engulfing`

---

## 1. What it is

A two-candle pattern after a decline: a **bearish** candle, then a **bullish** candle whose body
completely **engulfs** the first candle's body. The second interval opens at or below the first
close and closes at or above the first open, so the entire previous body is erased within one
interval.

It is a stronger signal than a single hammer because it demonstrates **two-sided evidence**:
sellers had the initiative yesterday, and today buyers took all of it back.

---

## 2. Formation rules

| # | Rule | Threshold |
|---|------|-----------|
| 1 | Candle 1 is **bearish** (`close < open`) | Required |
| 2 | Candle 2 is **bullish** (`close > open`) | Required |
| 3 | `open₂ ≤ close₁` | Opens at or below the prior close |
| 4 | `close₂ ≥ open₁` | Closes at or above the prior open (strict engulfing) |
| 5 | Prior trend is downward | Required — otherwise it is a range bar |
| 6 | Candle 2's body is meaningfully larger | `body₂ ≥ 1.0 × body₁` (≥ 1.2× preferred) |
| 7 | Both candles closed | Otherwise `DEVELOPING` |

Variants:

- **Strict engulfing** (body-on-body, per rules 3–4): the standard definition.
- **Loose engulfing** (real-body plus wicks): weaker; label `POSSIBLE` if wicks are not engulfed too.
- **Engulfing at a retest** of a broken level: the highest-quality version.

Note: if candle 2 opens exactly at candle 1's close and closes at its open, that is a valid
engulfing but edge-case — round-off and gaps make it rare in liquid instruments.

---

## 3. Anatomy

```
  candle 1 (bear)        candle 2 (bull)
   ┌───┐                  ┌─────┐
   │   │                  │     │
   │   │  <-- engulfed -> │     │
   └───┘                  └─────┘
```

---

## 4. Where it means something

| Location | Weight |
|----------|--------|
| At support that held before | High |
| At the lower boundary of a falling channel / trendline | High |
| After a "spring" below support that reclaims it | Very high (this is a trap-plus-engulf combination) |
| At a Fib 0.5–0.786 retracement of a prior advance | Medium–High |
| Mid-range | Low |
| Immediately under a major resistance | Low (no room) |

---

## 5. Interpretation

Bullish engulfing is a **transfer of control** message. The stronger the engulf, the clearer the
transfer: a large candle 2 that closes above candle 1's open (not just its body) is stronger than a
marginal one.

It is *not* a bottom call. In a powerful downtrend, engulfing candles are routinely produced and then
sold. The pattern is a *candidate* reversal; the trend must be confirmed broken.

---

## 6. Confirmation requirements

| Level | Confirmation |
|-------|--------------|
| Minimum | Candle 2 closes above candle 1's open (already part of the pattern) |
| Good | Candle 3 closes above candle 2's high |
| Strong | Price breaks the most recent swing high, or closes above a short-term downtrend line |
| Strongest | Price retests the breakout zone and holds, volume higher on the up move |
| Invalidated | Close below candle 2's low |

---

## 7. Volume

| Volume on candle 2 | Reading |
|--------------------|---------|
| ≥ 1.5× average | Strong: the engulf happened with real participation |
| ≈ average | Acceptable |
| < average | Suspicious: the "engulf" may be thin-market noise or a low-liquidity interval |

Engulfing on **falling** volume after a long decline can also be short-covering rather than new
buying — that bounce often fades. Note the possibility.

---

## 8. Paper-trade entry conditions (illustrative)

```
Long trigger   : close of candle 3 above candle 2's high, OR retest of candle 2 body mid holding
Entry zone     : candle 2 high ± 0.15 × ATR  (or body midpoint on a retest entry)
Invalidation   : below candle 2's low minus 0.25 × ATR
Targets        : T1 nearest swing high / prior consolidation low (the "breakdown level")
                 T2 measured: decline height × 0.5
                 T3 major structural resistance
Aggressive alt : enter on candle 2's close; accept lower reliability, use tighter size
```

---

## 9. Invalidation

1. Close below candle 2's low — the buyers who engulfed are trapped.
2. Two closes inside candle 1's body with no follow-through (absorption).
3. Higher-timeframe support breaking below the pattern.
4. Volume collapsing to well below average on subsequent up bars.

---

## 10. Common false signals

| False signal | Explanation | Guard |
|--------------|-------------|-------|
| Engulfing in a strong downtrend with no support | Routine bear-market noise | Require location + HTF alignment |
| "Engulfing" on an inside-bar sequence | Candle 1 tiny, so anything engulfs it | Require `body₁ ≥ 0.5 × average_range` |
| Engulfing at a gap | Candle 1 close and candle 2 open far apart | Check whether the gap is a real gap or a corporate action |
| Red/green inversion | Colour convention misread (Asian themes invert) | Verify colours against price direction |
| Last-hour reversal on thin volume | Illiquid tail of session | Check volume and session timing |
| Engulfing that closes exactly at resistance | No upside room | R:R gate |

---

## 11. Historical evidence — honest position

Engulfing patterns are among the most studied candle formations and are generally described as
more informative than single-candle patterns because they encode two intervals of information. That
is a structural argument, not a measured performance claim. No win rate is asserted here. To obtain
one for your instrument, follow [`README.md`](README.md) §5.

---

## 12. Worked example (illustrative, fictional)

```
Instrument: DEF · Timeframe: 1H · Context: falling from 512 to 468; support 466–470 held yesterday.
Candle 1: open 471, close 468.6 (bear, body 2.4)
Candle 2: open 468.2, close 472.4 (bull, body 4.2)
          open2 <= close1 (468.2 <= 468.6) ✔  close2 >= open1 (472.4 >= 471) ✔ body2 = 1.75x body1 ✔
Volume  : candle 2 at 1.9x average ✔
Status  : CONFIRMED (both closed)
Setup   : trigger close > 473.1 (candle 2 high) · entry 473.3 · invalidation 466.9
          risk 6.4 · T1 480.0 (prior swing high)  -> 6.7/6.4 = 1.05R  FAIL
Verdict : WAIT on this timeframe. On the 4H, the same location has a target at 495 (3.4R),
          so the setup becomes viable only if the 4H structure supports the 480–495 zone.
```

---

## 13. Beginner summary (Hinglish)

**Bullish engulfing:** pehli candle red (bearish), doosri candle green (bullish) aur doosri candle
ka body pehli ko poora nigal leta hai.

**Matlab:** kal sellers ka control tha, aaj buyers ne woh sara control wapas le liya. Do din ka
evidence hai, isliye single candle se behtar.

**Lekin:** sirf support/resistance ke paas hi matlab rakhta hai. Beech mein kuch bhi nahi.

**Confirmation:** teesri candle ka is candle ki high ke upar close hona.

**Stop loss:** doosri (bullish) candle ki low ke neeche.

---

## 14. Exercise

Take a 15-minute chart and find ten bullish engulfings. For each record: `body₂/body₁`,
volume ratio, distance to nearest support, and whether candle 3 closed above candle 2's high. Then
sort by R:R-to-nearest-resistance. You will usually find the *good* ones are the ones with room
above — not the ones with the biggest bodies. Write that down.

---

*See also: [`bearish-engulfing.md`](bearish-engulfing.md) · [`piercing-pattern.md`](piercing-pattern.md) ·
[`harami.md`](harami.md)*
