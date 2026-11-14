# Workflow — Screenshot Analysis

The primary path. Budget: 15 stages, ~5 minutes of reasoning.

## Stage 0 — Mode
Identify LEARNING / RESEARCH / PAPER-TRADING from the request. Default to RESEARCH if a chart is supplied and the
user asks "what do you think". State the mode in the report header.

## Stage 1 — Transcribe before interpreting

Fill this table *before* forming any opinion:

```
Instrument (as shown) ........
Exchange marker ..............
Last price ...................
Change / % ...................
Timeframe ....................
Chart type ...................
Visible range (dates) ........
Price axis labels ............
Candles visible (count) ......
Volume panel .................  yes / no
Indicator panels .............  names + values if printed
Drawings .....................  trendlines / lines / boxes / fib / text
Platform watermark ...........  (implies data delay)
Unreadable ...................  list
Absent but expected ..........  list
```

## Stage 2 — Quality gate
Score 0–10 using `core/chart-recognition.md` §4.

| Score | Consequence |
|-------|-------------|
| 8–10 | Full analysis |
| 5–7 | No precise levels; verdict ≤ WAIT |
| 2–4 | Qualitative only; `INSUFFICIENT DATA` for numbers |
| 0–1 | Stop; request re-capture |

## Stage 3 — Identify
Confirm instrument and exchange. Two candidates → ask. Never guess between similar tickers.

## Stage 4 — Structure
State `k` (swing parameter). Map swings, trend, levels (≥2 touches), trendlines (≥2 touches), consolidation.

```
Trend (TF)   : up / down / range / transition
Sequence     : HH-HL x3 / LH-LL x2 / mixed
Levels       : R2 ... R1 ... [price] ... S1 ... S2 ...
Trendline    : rising, 2 touches, currently ~<price>
Range        : none / <low>-<high> for N bars
```

## Stage 5 — Candles
For the last 3–5 candles: direction, body/range, wick ratios, close position. Name patterns **with status codes
and the rules they meet**. At most one primary + one secondary pattern.

## Stage 6 — Chart patterns
Any multi-bar pattern: name, state, boundary prices, touches, volume behaviour.

## Stage 7 — Volume
Relative to the 20-bar average: expanding / contracting / climax / diverging. If absent, state `not visible`.

## Stage 8 — Indicators
Only those on the chart. For each: name/period (or `ASSUMED`), value (or "not printed"), reading, limitation.

## Stage 9 — Context
If browsing exists: index behaviour, sector, instrument news, events inside the horizon — each cited with a
timestamp. If not, insert the standard "web research unavailable" paragraph.

## Stage 10 — Timeframes
Table of every timeframe **actually seen**. Unknown timeframes are marked "not provided". No guessing.

## Stage 11 — Traps
Run `trap-detection.md`. For each hypothesis: level, behaviour, evidence, what would confirm it.

## Stage 12 — Risk
ATR (if available), structural invalidation, distance in ATR and %, R:R arithmetic to each target candidate.

## Stage 13 — Scenarios
A bullish, B bearish, C no-trade. Each with trigger, entry zone, invalidation, T1–T3, R:R.

## Stage 14 — Verdict
One of: `BULLISH SCENARIO` / `BEARISH SCENARIO` / `WAIT — NO CONFIRMED SETUP` / `NO-TRADE` /
`INSUFFICIENT DATA — NO VALID SETUP`. Plus supporting evidence, conflicting evidence, and the outstanding
confirmation.

## Stage 15 — Report
Render `templates/analysis-report.md`. Include the Hinglish section and section 10 (sources and data quality).

## Stage 16 — Record (optional)
If writing is available, save a prediction record. Never edit it later.

---

## Self-check before sending

- [ ] Header complete (instrument, exchange, both timestamps, timeframe, source, mode, quality)
- [ ] Every number traceable
- [ ] Every pattern has a status code
- [ ] Every scenario has an invalidation
- [ ] Hinglish section present and genuinely simple
- [ ] Missing data explicitly listed
- [ ] No advice, no promises, no invented statistics
