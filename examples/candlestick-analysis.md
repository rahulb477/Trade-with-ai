# Example — Candlestick Pattern Audit

> **FICTIONAL.** Prices invented. Instrument "BETATECH" (fictional).

**Question asked:** "Is this a hammer? Should I buy?"

## 1. What was supplied

A screenshot of a 15-minute chart. Quality score **6/10** (no volume panel, indicator labels unreadable). Per the
consequence table, that permits **analysis but no precise levels**.

Transcription first (the pipeline forbids interpreting before transcribing):

| Bar | Open | High | Low | Close | Shape |
|-----|------|------|-----|-------|-------|
| −5 | 452.0 | 453.1 | 450.2 | 450.6 | bearish |
| −4 | 450.6 | 451.0 | 447.8 | 448.2 | bearish |
| −3 | 448.2 | 448.9 | 445.1 | 445.6 | bearish |
| −2 | 445.6 | 446.2 | 442.0 | 442.4 | bearish |
| −1 | 442.4 | 443.0 | 439.1 | 442.8 | **hammer?** |

## 2. Rule audit — is bar −1 actually a hammer?

| Rule | Requirement | This bar | Verdict |
|------|-------------|----------|---------|
| Body size | ≤35% of range | body 0.4, range 3.9 → 10.3% | ✅ |
| Lower shadow | ≥2× body and ≥55% of range | shadow 3.3 → 8.25× body, 84.6% of range | ✅ |
| Upper shadow | ≤15% of range | 0.2 → 5.1% | ✅ |
| Prior trend | A decline before the pattern | 4 consecutive lower closes | ✅ |
| Location | At a level, not mid-air | **No level map possible** (quality 6, no axis interpolation of prior structure) | ❌ unknown |
| Volume | Not required, but confirmation | **No volume panel** | ⚠️ unavailable |

**Status: `CONFIRMED` by shape and context; `UNVERIFIED` at location.**

That distinction matters: the candle is objectively a hammer, but a hammer in the middle of nowhere is noise.
Without the level map, the honest statement is "a hammer formed, but I cannot tell you whether it formed at a
level that matters."

## 3. What a hammer actually claims

A hammer says: *sellers pushed price down intraday and buyers rejected it, closing near the high*. It is a
**single-bar** statement about the last 15 minutes. It says nothing about:

- whether a larger downtrend continues,
- whether the level matters,
- whether the next bar will follow through.

Documented reading: a hammer is a *potential* reversal signal whose reliability depends almost entirely on
location and confirmation. Without those, it is a shape, not a setup.

## 4. Confirmation requirements (in priority order)

1. **A support level** within roughly 0.5 ATR of the bar's low. — unavailable here.
2. **A follow-through close** above the hammer's high (443.0). — not yet occurred.
3. **Higher-timeframe agreement**: is the 1H chart also at support? — the 1H chart was not supplied.
4. **Volume**: ideally above average on the reversal bar. — not visible.

## 5. Verdict

**`WAIT — NO CONFIRMED SETUP`**

Reasons, in order:

1. Quality score 6 → no precise levels, so the location test cannot be run.
2. No follow-through close yet. A hammer is a hypothesis until the next bar closes above it.
3. The 15-minute downtrend is intact (4 lower closes); no structure break has occurred.

**What would upgrade this to a valid scenario:**

- A 15-minute close above **443.0** (the hammer's high), **and**
- Evidence that 439–440 is a tested support (two prior touches), **and**
- Ideally 1H agreement.

**What would invalidate it immediately:** a close below **439.1** (the hammer's low). That bar would then be a
"failed hammer" — and, more usefully, part of an ongoing downtrend.

## 6. Beginner Explanation (Hinglish)

**Hammer kya hota hai:** candle ka body chhota, neeche lambi shadow. Matlab sellers ne price neeche giraya, par
buyers ne wapas upar kheench liya.

**Par yeh important hai:** hammer **sirf ek candle** ke baare mein batata hai — 15 minute ki kahani. Bada trend
nahi batata.

**3 cheezein chahiye:** (1) support level paas ho — yahan pata nahi chal raha, (2) agli candle hammer ke high ke
upar **close** kare, (3) bade timeframe bhi support par ho.

**Abhi kya hai:** shape sahi hai, par location verify nahi ho sakti (chart quality kam) aur follow-through nahi
aaya.

**Verdict: WAIT.** 443.0 ke upar close aaye to dekhenge; 439.1 ke neeche close aaya to hammer cancel.

## 7. The lesson

Beginners ask "is this a hammer?" Professionals ask "at what level, in what trend, with what follow-through, and
what does it pay?" The pattern name is the cheapest part of the analysis.
