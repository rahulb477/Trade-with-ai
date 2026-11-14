# Hammer

**Group:** Bullish reversal · **Candles:** 1 · **Reliability band:** Moderate (requires confluence)
**Detector:** `patterns.detect_hammer`

---

## 1. What it is

A single candle with a **small body near the top** of its range and a **long lower wick**, appearing
**after a decline**. It records a session in which sellers drove price sharply lower and buyers
absorbed the selling and pushed price back up to close near the open/high.

The visual metaphor — a market "hammering out a bottom" — is memorable but not evidence. The
evidence is the *rejection*: the lower price was offered and refused.

---

## 2. Formation rules

All must hold:

| # | Rule | Reasonable threshold |
|---|------|---------------------|
| 1 | Prior trend is **downward** over the recent window (e.g. last 5–10 candles or a measurable decline) | A decline of at least a few percent, or 3+ consecutive lower closes, or price below a falling short MA |
| 2 | `lower_wick ≥ 2 × body` | The defining feature |
| 3 | `upper_wick ≤ 0.5 × body` (small) | Body sits near the top |
| 4 | `body / range ≤ 0.35` | Small real body |
| 5 | Range is not abnormally tiny (avoid illiquid noise) | `range ≥ 0.5 × average_range(20)` |
| 6 | The candle has **closed** | Open candles are `DEVELOPING` at best |

Optional strengtheners (do not substitute for the rules):

- Lower wick pierces a known support and closes back above it
- Candle range ≥ 1.3 × average range (an *expansion* hammer)
- Candle is the third of a three-candle reversal complex (with a morning star)

---

## 3. Anatomy

```
   ┌───┐   <- small body near the top: open and close close together
   └─┬─┘
     │
     │     <- long lower wick: this is the rejection of lower prices
     │
     ▼
```

Colour is **not** decisive. A green hammer is slightly stronger than a red hammer in most
documented treatments, but a red hammer that closes at the top of its range after a sharp drop
still shows buyers stepped in. Do not reject a pattern on colour alone; do downgrade it.

---

## 4. Where it means something

| Location | Meaning | Weight |
|----------|---------|--------|
| At a horizontal support that already held ≥2 times | Strongest case | High |
| At a rising trendline / channel bottom | Trend continuation | High |
| At a Fibonacci retracement cluster (0.5–0.618) | Confluence | Medium–High |
| At a round psychological level with prior reaction | Medium | Medium |
| In the middle of a range, no level | Almost meaningless | Low |
| At a **new all-time low** with no prior structure | Speculative reversal attempt | Low–Medium |

---

## 5. Interpretation

**What it says:** in that interval, sellers had control and lost it. The close recovered most of
the range.

**What it does not say:** that the downtrend is over. It says the *last seller push failed*. The
downtrend could resume next candle with a small effort if there is no follow-through.

**In a downtrend:** first warning of exhaustion. Treat as a *potential* turning point that requires
confirmation.

**In an uptrend:** a hammer at a pullback support is a **continuation** signal, not a reversal. This
is the most common and often the most reliable use — the trend resumes after a shakeout.

---

## 6. Confirmation requirements

Do **not** enter on the hammer alone.

| Level | Confirmation |
|-------|--------------|
| Minimum | Next candle closes **above the hammer's body** (i.e. above `max(open,close)` of the hammer) |
| Good | Next candle closes above the hammer's high |
| Strong | Price breaks the most recent swing high, or breaks a short-term downtrend line, on rising volume |
| Best | Retest of the hammer's high area as new support holds |

Confirmation window: typically within 1–3 subsequent candles. If price instead closes below the
hammer's **low**, the hammer has failed — this is a bearish continuation signal (failed rejection).

---

## 7. Volume

| Volume behaviour | Reading |
|------------------|---------|
| Above-average volume on the hammer | Genuine absorption; sellers met real demand |
| Below-average volume | Thin, possibly illiquid; low information |
| Volume spike with a long wick and a close back at the high | Often capitulation + absorption — the strongest version |
| Rising volume on the **next** candle in the bullish direction | Confirms participation followed through |

If no volume panel is available, state `volume: not assessable` and treat the pattern as level 1
evidence only.

---

## 8. Paper-trade entry conditions (illustrative, never advice)

```
Long trigger      : close of the next candle above the hammer's high
                   (aggressive variant: above the hammer's body; accept lower reliability)
Entry zone        : hammer high ± 0.1 × hammer range
Invalidation      : below the hammer's low, minus a buffer of 0.25 × ATR
Targets           : T1 = nearest prior swing high / recent breakdown level
                    T2 = 1–1.5 × height of the preceding decline (measured move)
                    T3 = prior consolidation zone / major resistance
Trailing          : after T2, trail below each new higher low or 2×ATR
```

Why the invalidation is where it is: the hammer's low is the exact price that the pattern says was
*rejected*. A close below it means the rejection failed — the thesis is void, not merely
uncomfortable.

R:R sanity: if the distance from entry to the hammer low is more than ~1.5×ATR, the stop is far;
either reduce size, find a retest entry closer to the low, or skip.

---

## 9. Invalidation

The setup is void when:

1. Price closes below the hammer's low (primary).
2. Price stalls for more than ~5 candles without exceeding the hammer's high (momentum death).
3. The higher timeframe breaks a major support, negating the location.
4. The supposed support level is decisively broken on volume.
5. A corporate action (split/bonus) has shifted the price series and the pattern was arithmetic.

---

## 10. Common false signals

| False signal | Why it happens | Guard |
|--------------|----------------|-------|
| Hammer mid-range | No level, no prior trend | Require a location check |
| "Hammer" after a single red candle in an uptrend | No downtrend to reverse | Require a measurable decline |
| Hammer in an illiquid small cap | Random 1-tick moves create long wicks | Require range ≥ some multiple of tick and of average range |
| Hammer on a Heikin-Ashi chart | HA smooths and synthesises OHLC | Refuse on non-OHLC chart types |
| Hammer into overhead resistance | Long lower wick but immediate supply above | Check the distance to the next resistance |
| News-gap hammer | Gap down, then recovery within the gap | Verify whether the "low" is an artifact of the gap |
| Repeated hammers down a trend | Each one is a failed attempt; the trend is stronger | Count prior failed hammers; after 2 failures, stop counting |

---

## 11. Historical evidence — honest position

Documented reference works (Nison; Bulkowski) discuss hammer performance, typically emphasising
that **location and confirmation dominate shape**. Those published figures are from specific
markets and periods and are **not reproduced here as fact**, because quoting a number without its
sample would violate this repository's evidence rules.

To get a usable base rate for *your* instrument and timeframe, run the method in
[`README.md`](README.md) §5 or use `engines/backtesting/`. Until then, describe the hammer as
"moderate reliability, confirmation required" — that statement is honest and sufficient.

---

## 12. Worked example (illustrative numbers, fictional instrument)

```
Instrument: ABC (illustrative)
Timeframe : Daily
Context   : Downtrend from 260 to 198 over 6 weeks.
            Support at 200 held twice in the prior month.
Candle    : open 203, high 206, low 194, close 205
            body = 2, range = 12, lower_wick = 9, upper_wick = 1
            body_ratio = 0.17, lower_wick/body = 4.5  -> rules 2,3,4 satisfied
            Prior trend down: yes. Location: support 200 pierced to 194 and closed back above -> strong
Volume    : 1.5× 20-day average
Status    : CONFIRMED (closed)
Setup     : trigger = close above 206
            entry 206.5, invalidation 193 (below hammer low 194, buffer 1)
            risk = 13.5
            T1 = 214 (prior swing high)  -> 7.5 / 13.5 = 0.56R  <-- fails 1.5R gate
Verdict   : WAIT — the nearest resistance is too close for acceptable R:R.
            Only becomes valid if price consolidates and a higher target (e.g. 232, the 50% retrace)
            gives >= 1.5R, i.e. entry near 206 with T1 226+.
```

That example is deliberately a *failing* case: a perfect hammer with a bad R:R is a `WAIT`.

---

## 13. Beginner summary (Hinglish)

**Hammer kya hai?** Ek candle jiska body chhota ho aur neeche ki wick lambi ho, aur yeh girte
market ke baad aaye.

**Iska matlab:** us din sellers ne price ko bahut neeche giraya, lekin buyers ne wapas upar khareed
liya. Neeche wala price accept nahi hua.

**Lekin:** sirf yeh candle dekh kar trade nahi lete. Agli candle ko hammer ki high ke upar close
hona chahiye — tabhi confirmation milta hai.

**Stop loss kahan?** Hammer ki low ke thoda neeche. Agar price wahan se neeche chala gaya, to matlab
jo rejection dikh raha tha woh fail ho gaya — trade ka reason khatam.

**Sabse badi galti:** beech market mein hammer dekh kar trade lena, jahan koi support/resistance hi
nahi hai. Location ke bina pattern ka koi matlab nahi.

---

## 14. Exercise

1. Open any daily chart with 200+ candles. Find five candles meeting every rule in §2 (write the
   numbers down).
2. For each, record: was there a support/level within 1 ATR? Did the next candle close above the
   hammer's high? What happened over the following 10 candles (best and worst excursion)?
3. Classify your five as `CONFIRMED` / `FAILED` / `NO FOLLOW-THROUGH` and compute a raw hit rate
   out of 5. Then repeat with 50 samples and note how much the number moves. That instability is
   exactly why single-pattern statistics must never be quoted as certainties.

---

*See also: [`inverted-hammer.md`](inverted-hammer.md) · [`hanging-man.md`](hanging-man.md) (same shape,
opposite context) · [`morning-star.md`](morning-star.md) · [`README.md`](README.md) §2*
