# Head and Shoulders

**Type:** Reversal (topping) · **Bars:** typically 20–100 · **State vocabulary:** POSSIBLE / DEVELOPING / CONFIRMED / FAILED

## 1. Shape

Three peaks: a **left shoulder**, a **higher head**, and a **lower right shoulder**, with two troughs between
them defining a **neckline**.

```
                    ╱╲
                   ╱  ╲        head (highest)
        ╱╲        ╱    ╲        ╱╲
       ╱  ╲      ╱      ╲      ╱  ╲
      ╱    ╲____╱        ╲____╱    ╲
     L      neckline      neckline   R
```

## 2. Formation rules

| # | Rule |
|---|------|
| 1 | A prior **uptrend** exists (the pattern reverses it) |
| 2 | Three distinct peaks; the middle (head) is the highest |
| 3 | Left and right shoulders are lower than the head, roughly comparable to each other (within ~10% of the pattern height is a reasonable tolerance) |
| 4 | The two troughs form a neckline — horizontal or sloped (a downward slope is more common) |
| 5 | Each peak must be a real swing (multiple bars, not a single spike) |
| 6 | The right shoulder should be lower than the left in most textbook descriptions; a higher right shoulder weakens the pattern |
| 7 | Volume typically declines from left shoulder → head → right shoulder |
| 8 | Confirmation: a **close below the neckline** |

## 3. Volume expectations

| Stage | Expected volume |
|-------|----------------|
| Left shoulder | Rising (the uptrend's participation) |
| Head | Often the highest price on *lower* volume than the left shoulder — divergence |
| Right shoulder | Lower still — the rally lacks conviction |
| Neckline break | **Expanding** — this is the critical bar |

A neckline break on low volume is the single most common prelude to a failed H&S.

## 4. Confirmation and entry

```
Conservative : wait for a close below the neckline, then a retest of the neckline that fails
Standard     : enter on the close below the neckline (accept that some breaks fail)
Aggressive   : enter on the right shoulder's breakdown of its own minor support (earlier, less reliable)
Volume filter: require breakout volume ≥ 1.3–1.5 × the 20-bar average
```

The **retest entry** usually gives the best R:R because the invalidation sits just above the neckline.

## 5. Measurement

```
height = |head − neckline|
target = neckline − height
```

Worked: head 1_320, neckline 1_240 → height 80 → target 1_160.

Report the measured target **and** the nearest structural support. If the measured target lies below a major
support, use the structural level first and say why.

## 6. Invalidation

| Event | Meaning |
|-------|---------|
| Close back above the neckline after the break | Failed pattern — a bear trap. See `workflows/trap-detection.md` |
| Close above the right shoulder's high | The topping structure is void; the uptrend may resume |
| Neckline slopes steeply | Measured move becomes unreliable; treat as a trendline break instead |
| Right shoulder higher than the head | Not an H&S |

## 7. Common false signals

| False signal | Guard |
|--------------|-------|
| "H&S" in a range with no prior uptrend | Rule 1 |
| Symmetrical triangle mislabelled | Check that the middle peak is clearly highest |
| Neckline drawn through the wrong troughs | Use the two reaction lows between the peaks |
| Break on a wick, not a close | Require a close |
| Break on thin volume | Volume filter |
| Pattern on a very short timeframe | Sub-15m patterns are noise-dominated |
| Ignoring a rising 200-EMA below | The pattern may be a pullback in a larger uptrend |

## 8. Failure behaviour (important)

A **failed** H&S is itself a signal. When price breaks the neckline and then reclaims it, the sellers who
short the break are trapped, and the subsequent rally is often sharp. Documenting failures — rather than
deleting them — is what makes a pattern log useful (`engines/prediction-tracking/`).

## 9. Worked example (fictional)

```
Instrument ABC · Daily · prior uptrend 980 → 1_320
Left shoulder 1_265 (vol 1.8M) · head 1_320 (vol 1.5M) · right shoulder 1_258 (vol 1.1M)
Neckline through troughs 1_238 and 1_242 → sloping slightly up, ~1_242 at the break point
Breakout: close 1_236 on 2.1M (1.6× average) → CONFIRMED
height = 1_320 − 1_242 = 78 → measured target 1_164
Structural target: prior consolidation low 1_180 (nearer, stronger)
Invalidation: close above 1_250 (neckline + 0.3 ATR buffer)
Entry on retest at 1_244 · stop 1_251 · risk 7 · T1 1_180 = 9.1R (structural) · T2 1_164 = 11.4R
Note: an 11R target is a measured move, not a plan. Most traders take partials at structure.
```

## 10. Beginner summary (Hinglish)

**Head and shoulders kya hai?** Uptrend ke end mein teen peaks — beech wala sabse upar (head), dono side wale
kam (shoulders). Dono troughs ko jodne wali line **neckline** kehlati hai.

**Matlab:** har naya high banane ke liye zyada effort lag raha hai (volume gir raha hai) — buyers thak rahe
hain. Jab price neckline ke **neeche close** kare, pattern confirm hota hai.

**Target:** neckline se pattern ki height jitna neeche.

**Stop:** neckline ke thoda upar (retest entry par yeh sabse tight hota hai).

**Badi galti:** wick se neckline toot jaye to usko breakout samajhna. Close chahiye. Aur agar pattern fail ho
jaye (price wapas neckline ke upar), to woh khud ek bullish signal ban jata hai.

## 11. Exercise

Find an H&S and check three things: (a) was the head's volume lower than the left shoulder's? (b) did the
neckline break on above-average volume? (c) was there a retest? Then find one *failed* H&S and compare the
same three answers. Write the two-line rule you would use next time.

---
*See also: [`inverse-head-and-shoulders.md`](inverse-head-and-shoulders.md) · [`triple-top.md`](triple-top.md) ·
[`../workflows/trap-detection.md`](../../workflows/trap-detection.md)*
