# Decision Engine

Converting a pile of evidence into exactly one verdict — and knowing when the honest verdict is
"nothing".

---

## 1. Closed verdict vocabulary

Only these five may appear in section 8 of a report:

| Verdict | Meaning | Typical trigger |
|---------|---------|-----------------|
| **BULLISH SCENARIO** | An evidence-backed long-side condition is currently valid **or** reachable with a defined trigger, and R:R ≥ 1.5 to T1 with a structural invalidation. | Trend alignment + confirmed continuation/reversal pattern + volume support + clear invalidation |
| **BEARISH SCENARIO** | Mirror of the above. | As above, inverted |
| **WAIT — NO CONFIRMED SETUP** | Data is sufficient, but no scenario passes the entry checklist. | Conflicting timeframes, unconfirmed pattern, poor location (mid-range), R:R < 1.5 |
| **NO-TRADE** | A positive decision *not* to participate: conditions are actively hostile. | Event risk imminent, liquidity/thin chart, spread/volatility regime untenable, thesis invalidated |
| **INSUFFICIENT DATA — NO VALID SETUP** | Essential inputs are missing or unreliable. | Unreadable ticker, no price scale, unknown timeframe, no structural invalidation available |

`WAIT` and `NO-TRADE` differ: **WAIT** = "not yet, watch for X"; **NO-TRADE** = "not this, even if
X happens". Do not blur them.

---

## 2. The decision is a filter, not a score

Do not average conflicting signals into a number. A weighted score invites false precision and
hides the conflict that the user most needs to see.

Instead, apply **gates** in order. The first gate that fails determines the verdict.

```
G1  DATA INTEGRITY      Do we have instrument + timeframe + readable prices?
        fail -> INSUFFICIENT DATA
G2  EVENT RISK          Is a binary event inside the holding horizon?
        yes  -> NO-TRADE (or explicit "pre-event: no new positions")
G3  STRUCTURE           Is there a definable level that invalidates a thesis?
        fail -> WAIT (or INSUFFICIENT DATA if unreadable)
G4  LOCATION            Is price at a location where R:R can be ≥1.5?
        fail -> WAIT  ("mid-range, poor location")
G5  TRIGGER             Has a specific confirmation occurred (close-through / retest hold /
                        pattern completion)?
        fail -> WAIT  (name the missing trigger)
G6  ALIGNMENT           Does the higher timeframe contradict without explanation?
        conflict -> WAIT
G7  TRAP RISK           Is there unrefuted evidence the move is a trap?
        yes  -> WAIT, or flip to the trap's scenario if the trap is confirmed
G8  VERDICT             Assign direction
```

---

## 3. Gate detail

### G1 — Data integrity

Requirements: resolved instrument, known timeframe, at least a readable last price and enough of
the price axis to place levels. Missing any → `INSUFFICIENT DATA`, with the specific missing item.

### G2 — Event risk

Scan the horizon. If one of these falls inside the intended holding period, prefer `NO-TRADE`:

- Earnings / results (date known)
- Central bank decision (RBI MPC, FOMC)
- Major scheduled data (CPI, GDP, payrolls) for index-level instruments
- Derivative expiry day for F&O (India: weekly/monthly expiries — see `markets/india/`)
- Known corporate action (split, bonus, dividend ex-date) that changes the printed price
- Index rebalancing / inclusion-exclusion

State the event, its date, and the effect on the plan ("gap risk: a 25% overnight move is inside
normal historical range for this event class" — only if you can source the claim; otherwise say
"event risk is unquantified but material").

### G3 — Structure

You need a price that says "my thesis was wrong". That price must come from observed structure
(swing high/low, pattern boundary, gap edge), not from a convenient round number.

| Thesis | Defensible invalidation |
|--------|------------------------|
| Long on breakout | Close back below the broken level (the breakout's own failure point) |
| Long on pullback | Below the swing low that defines the pullback |
| Long on reversal pattern | Below the pattern's low (or its close-confirmation low) |
| Short on breakdown | Close back above the broken support |
| Range trade | Beyond the range boundary by a stated buffer |

### G4 — Location

Compute, using observed prices only:

```
risk  = |entry - invalidation|
reward_i = |target_i - entry|
rr_i  = reward_i / risk        (for the *nearest* valid target)
```

Minimum acceptable: **rr_T1 ≥ 1.5** for paper-trade scenarios. Below that → `WAIT` with the
arithmetic shown ("entry 100, stop 96, T1 104 → 1.0:1 — insufficient").

Also reject "poor location" regardless of arithmetic:

- Price is mid-range with no confluence
- Price is directly under a major untested resistance (for longs)
- Price has just run 2+ ATR in one direction (chasing)

### G5 — Trigger

A pattern's existence is not a trigger. Triggers are events:

| Trigger type | Precise definition |
|--------------|--------------------|
| Close-through | Candle **closes** beyond the level on the analysis timeframe |
| Retest hold | Price returns to the broken level and closes back in the breakout direction |
| Pattern completion | The final candle of the pattern closes, satisfying every formation rule |
| Structure break | A close beyond the most recent swing point in the direction of the thesis |
| Indicator confirmation (secondary only) | e.g. MACD histogram flip *and* price close — never used alone |

### G6 — Alignment

Rank timeframes: `M > W > D > 4H > 1H > 30m > 15m > 5m > 3m > 1m`.

- HTF and LTF agree → strongest case; proceed.
- HTF up, LTF down → the LTF move is a **pullback** unless it breaks a HTF swing; long setups
  preferred *at* HTF support, not mid-pullback.
- HTF and LTF disagree structurally and both are strong → `WAIT`.

Never promote a lower-timeframe signal to a higher-timeframe thesis.

### G7 — Trap risk

If price broke a level and you cannot rule out a trap, the correct verdict is `WAIT` until either:

- a **hold/retest** confirms the break, or
- a **reclaim** confirms the trap.

See [`../workflows/trap-detection.md`](../workflows/trap-detection.md).

### G8 — Verdict

Direction is chosen by which scenario's trigger is currently satisfied or closest to being
satisfied **with** alignment and acceptable R:R. If both directions are plausible and neither is
triggered → `WAIT`, and describe both triggers.

---

## 4. Confidence language (no invented percentages)

Use this ladder. It is relative, not probabilistic, and must be justified by counts of evidence.

| Label | Requirements |
|-------|-------------|
| **Strong** | ≥4 independent evidence classes agree (structure, pattern, volume, indicator, HTF, context); no material conflict; R:R ≥ 2 |
| **Moderate** | 3 classes agree; minor conflict resolved; R:R ≥ 1.5 |
| **Weak** | 2 classes agree; OR ≥4 agree but one material conflict unexplained |
| **Speculative** | 1 class only, or data quality 5–7, or only a developing pattern |
| **Not assessable** | Data gate failed |

Evidence classes are *independent* only if they are not derived from the same pixels. A candlestick
pattern, a trendline, and a support level that all come from the same three candles count as **one**
class, not three. This is the most common inflation of confidence in AI chart analysis — do not do it.

---

## 5. Worked micro-examples

### Example 1 — trend continuation with alignment

```
Observed: D uptrend (HH/HL), price pulled back to prior breakout zone 1_180–1_200,
15m printed a bullish engulfing that closed above 1_198, volume on the engulfing > 20-bar avg.
Invalidation: 15m close below 1_172 (swing low of the pullback).
Entry 1_199 · risk 27 · T1 1_240 (1.5R) · T2 1_275 (2.8R) · T3 1_310 (4.1R)
Gates: G1 pass · G2 no event · G3 pass · G4 1.5R at T1 pass · G5 close-through pass
     · G6 aligned pass · G7 no unrefuted trap evidence
Verdict: BULLISH SCENARIO · Confidence: Moderate (structure + pattern + volume; HTF aligned)
```

### Example 2 — the honest WAIT

```
Observed: 1H range 480–505 for 3 sessions. Last close 492. No pattern completion. Volume flat.
Invalidation would be 478 or 507 → risk 14 or 15 from mid-range.
T1 at range edge = 13 → R:R 0.87.
Verdict: WAIT — NO CONFIRMED SETUP
Reason: mid-range location gives sub-1.5R; correct behaviour is to wait for a boundary
test with confirmation, or a range resolution.
```

### Example 3 — trap-aware WAIT

```
Observed: 15m closes above 1_000 resistance on a 1.4x volume bar, then next two candles
close back below 1_000 with the lower wick of the breakout candle fully retraced.
G7: unrefuted trap evidence (failed hold). Verdict: WAIT.
Note to user: a confirmed trap would favour the short side only after a close below
the pre-breakout swing low at 985; until then, no position.
```

---

## 6. Anti-patterns

| Anti-pattern | Why it is wrong | Correct |
|--------------|-----------------|---------|
| Averaging bull and bear scores into "62% bullish" | Invents precision, hides conflict | Gate-based verdict + qualitative confidence |
| Choosing the direction that "looks more likely" | Unfalsifiable | Choose based on which trigger is satisfied |
| Providing an entry with no invalidation | Unmanageable | No invalidation, no scenario |
| Three targets because the template has three | Padding | Only give targets that map to structure/volatility |
| Upgrading confidence because the user seems eager | Sycophancy | Confidence is a function of evidence only |
| Calling a mid-range bounce a "setup" | Location is half the edge | WAIT until a boundary or a clear level |
| Ignoring an inconvenient HTF signal | Confirmation bias | Conflicts are printed, always |

---

*See also: [`evidence-engine.md`](evidence-engine.md) · [`risk-management.md`](risk-management.md) ·
[`../engines/decision-intelligence/README.md`](../engines/decision-intelligence/README.md)*
