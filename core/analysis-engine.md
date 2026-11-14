# Analysis Engine

The normative 16-stage pipeline. Every stage declares its inputs, the artifact it produces, and
the gate that can stop or downgrade the analysis.

Gates are not advisory. If a gate fails, the pipeline continues only in degraded form and the
degradation is printed in the report.

---

## Stage 0 — Intake

**Input:** user message, attachments.
**Produce:** `mode`, `question`, `has_image`, `user_locale`.

Classify intent:

| Signal | Mode |
|--------|------|
| "what is / explain / teach / how does" | LEARNING |
| "analyse / review / what's happening / is this a trap" | RESEARCH |
| "entry / stop loss / target / plan a trade / setup" | PAPER-TRADING |
| Both analysis and levels requested | PAPER-TRADING (superset) |

**Gate 0:** if no image and no instrument and no topic → one clarifying question, stop.

Locale: default to the user's region for market conventions (an Indian user asking about "the
market" means NSE unless stated).

---

## Stage 1 — Extract

**Input:** image (or user transcription).
**Produce:** `ChartObservation` — a flat record of everything visible and everything expected
but absent.

Fields to attempt, in priority order:

1. Ticker / company name / logo text
2. Exchange marker (NSE, BSE, NASDAQ, NYSE, Binance…)
3. Last traded price + currency
4. Timeframe selector (`15m`, `1D`, `1H`…)
5. Chart type (candlestick, Heikin-Ashi, line, Renko, bar)
6. Visible date range / x-axis labels
7. Y-axis min/max and gridline labels
8. OHLC of the last 3–5 candles (direction, body size, wick sizes)
9. Volume panel presence and relative bars
10. Indicator panels: name, period, current value, panel range
11. Drawn annotations: horizontal lines, trendlines, boxes, text, Fib levels
12. Watermark / broker platform (implies data delay!)
13. Any "delayed" or timestamp label

Record explicitly: `unreadable: [...]`, `absent: [...]`.

**Gate 1:** if `ticker` is unreadable **and** the user did not state it → ask. If ticker is given
by the user, proceed and mark `ticker_source: user`.

---

## Stage 2 — Quality gate

Score the screenshot with the rubric in
[`chart-recognition.md`](chart-recognition.md) §4 (0–10).

| Score | Consequence |
|-------|-------------|
| 8–10 | Full analysis permitted |
| 5–7 | Analysis permitted; no precise levels; verdict capped at `WAIT` unless structure is unambiguous |
| 2–4 | Qualitative structure only; explicit `INSUFFICIENT DATA` for any level/indicator claim |
| 0–1 | Stop. Request a re-capture with the checklist. |

**Gate 2:** score < 5 and the user asked for exact levels → `INSUFFICIENT DATA — NO VALID SETUP`.

---

## Stage 3 — Identify

Confirm the instrument. Common traps:

- Same company on NSE and BSE (different tickers, near-identical prices).
- Similar names ("Adani Power" vs "Adani Green"), similar tickers (`TATAMOTORS` vs `TATAMTRDVR`).
- Spot vs futures vs options (the chart might be a futures continuous contract).
- ADR vs local listing (INFY vs INFY.NS).
- Index vs index futures vs index ETF.
- Crypto pairs (BTC/USDT vs BTC/INR — very different price levels).

**Gate 3:** two plausible instruments → ask. Never silently pick the more famous one.

---

## Stage 4 — Market research

Only if `web_search`/`web_fetch`/provider is available. Collect, each with source + timestamps:

- Last price and session change (from a provider, not from memory)
- Recent corporate actions / results / announcements
- Sector and index behaviour
- Macro events inside the relevant horizon (RBI/Fed decisions, CPI, expiry)
- Anything that would make technical levels unreliable (halt, circuit, merger news)

**Gate 4:** if unavailable, set `web_research: unavailable` and say so in section 6. Do not
substitute recollection.

---

## Stage 5 — Structure

Build, from the visible candles only:

- Swing highs/lows (with the pivot definition used)
- Trend classification: up / down / range / transition
- HH-HL / LH-LL sequence
- Horizontal support/resistance clusters (require ≥2 touches to call a level "tested")
- Trendlines (require ≥2 touches; a 1-touch line is a "candidate")
- Consolidation boxes and their boundaries
- Visible gaps

Output a compact map, e.g.:

```
Structure (D): uptrend, HH-HL intact since <date if visible>
Swings: H1 1_240 (2 touches) · H2 1_310 (1 touch, untested) · L1 1_140 · L2 1_205
Range: none — trending
Trendline: rising, 2 touches, currently ~1_220
```

**Gate 5:** fewer than ~20 candles visible → structure claims are unreliable; label them
provisional.

---

## Stage 6 — Patterns

Candlestick and chart patterns, each with a status code and the *rule* it satisfies or fails.

Rules for discipline:

- A pattern name is a hypothesis. State the formation rules it meets.
- If the last candle is still forming, the maximum status is `DEVELOPING`.
- If it fails one rule, use `POSSIBLE` and name the failing rule.
- Never stack five patterns to imply certainty. At most: one primary, one secondary.
- Chart patterns need *both* boundary touches and a breakout/retest to be `CONFIRMED`.

---

## Stage 7 — Indicators

Only those visibly present. For each: name, period (printed or assumed), current value,
panel position, and interpretation **with its limitation**.

Forbidden: computing an indicator value from a partial visual reading of the panel. If the
panel shows 62 and you cannot see the scale, report "reads ≈62, scale unverified".

**Gate 7:** if no indicator panel exists, section 5 says "no indicators visible on this chart"
and momentum is assessed from price/volume only.

---

## Stage 8 — Volume

If a volume panel exists:

- Compare last bars to the 20-bar average qualitatively ("above average", "drying up")
- Note climax bars, exhaustion spikes, and divergences from price
- Note whether volume confirms or contradicts the price move

If absent: state `volume: not visible` and list it in section 10's missing-data field.

---

## Stage 9 — Timeframes

Build the table with **only** what you actually saw:

| TF | Source | Trend | Key level | Conflict? |
|----|--------|-------|-----------|-----------|
| 1D | screenshot | up | 1_300 | — |
| 15m | screenshot | down | 1_240 | yes — pullback inside uptrend |
| 1W | not provided | — | — | unknown |

Alignment ladder: higher timeframe sets the *bias*, lower sets the *trigger*. Conflict without
resolution → `WAIT`.

---

## Stage 10 — Traps

Run the trap checklist ([`../workflows/trap-detection.md`](../workflows/trap-detection.md)):
bull trap, bear trap, false breakout, false breakdown, liquidity sweep, failed retest, stop-hunt
hypothesis, false reversal, volume divergence.

Each trap hypothesis needs: the level, the behaviour, and the evidence that would confirm it.
Unsupported trap claims are removed.

---

## Stage 11 — Context synthesis

Now, and only now, combine: structure + patterns + indicators + volume + timeframes + traps +
news. Write one paragraph of "what is actually going on", in plain language.

This paragraph is the input to the decision engine.

---

## Stage 12 — Risk

Derive:

- Volatility proxy: ATR if visible/computable, else recent true range from observed candles
- Candidate invalidation = structural price beyond the pattern/thesis
- Distance to invalidation in price and in % and in "ATR units"
- R:R to each target
- Position-sizing arithmetic **as an illustration** with made-up equity — never the user's money

**Gate 12:** cannot define a structural invalidation → no scenario. Output `WAIT`.

---

## Stage 13 — Scenarios

Always three, never one:

- **A — Bullish:** trigger condition, entry zone, invalidation, T1/T2/T3, R:R
- **B — Bearish:** same structure, mirrored
- **C — No trade:** the specific conditions under which the best action is inaction, and why

Scenario A and B are mutually exclusive *triggers*, not predictions. Both can be described even
when one is clearly more probable — that is the point of conditional planning.

---

## Stage 14 — Decision

Apply [`decision-engine.md`](decision-engine.md). Emit one of the five closed verdicts plus:

- supporting evidence (bullets, each tagged with provenance)
- conflicting evidence (bullets — never omitted for tidiness)
- the single confirmation still outstanding

---

## Stage 15 — Report

Render `templates/analysis-report.md`. All ten sections. Hinglish section is mandatory and must
be genuinely simple — test it by asking: could someone who has never seen a chart follow it?

---

## Stage 16 — Record

If persistence exists, write `journal/YYYY/MM/DD/<instrument>-<id>.md` with the immutable
hypothesis block. Otherwise print it inline. Never retro-edit.

---

## Pipeline shortcut rules

| User asks | Shortcut |
|-----------|----------|
| Pure concept question | Stages 0 → knowledge routing → teaching output. Skip 1–16. |
| "Is this news relevant?" | Stages 0, 4, 10 (partial), 15. |
| Follow-up on the same chart within one session | Reuse stages 1–5 artifacts; re-run 12–15 only if new data arrived. |
| Second screenshot of the same instrument, different timeframe | Re-run 1–2, merge into stage 9 table, then 10–15. |
