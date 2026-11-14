# Workflow — Quick Screenshot Analysis (Quick Signal Output Engine)

The primary quick path. Budget: 20 internal checks, ~5 minutes of reasoning, **8–12 short lines** of output.

This workflow wraps the classic `screenshot-analysis.md` pipeline and delegates its user-facing surface to the Quick Signal Output Engine (`core/quick-output-engine.md`). The full 16-stage analysis still runs logically — its results are compressed.

---

## Stage 0 — Mode detection

Detect `QUICK` vs `FULL` from the user's text via `quick_signal.detect_mode`.

* `quick` (default): proceed with this workflow.
* `full`: delegate to `workflows/screenshot-analysis.md` + `templates/analysis-report.md`.

If ambiguous, default to quick and note the assumption in the provenance ledger.

---

## Stage 1 — Transcribe before interpreting

Same table as `screenshot-analysis.md` §1 (instrument, exchange, last price, timeframe, chart type, axes, candles, volume panel, indicators, drawings, watermark, etc.). Mark `unreadable` and `absent` explicitly.

---

## Stage 2 — Quality gate

Score 0–10 using `core/chart-recognition.md` §4.

* 8–10: full analysis permitted — quick report may reach `PAPER-TRADING SETUP READY`.
* 5–7: no precise levels unless structure unambiguous; verdict capped at `WAIT` unless gated otherwise.
* 2–4: qualitative structure only; quick report uses `NOT AVAILABLE — INSUFFICIENT DATA` for numeric claims.
* 0–1: stop; request re-capture.

The score flows into `build_quick_signal(quality_score=...)` and caps a `READY` verdict at `WAIT`.

---

## Stage 3 — Identify

Confirm instrument and exchange. Two candidates → ask. Never guess. See `core/chart-recognition.md` §3.

---

## Stage 4 — Structure

Build swings, trend, HH/HL/LH/LL, S/R clusters (≥2 touches), trendlines (≥2 touches), consolidation boxes — visibly only. Fewer than ~20 candles → mark claims provisional.

Populate `support_level`, `resistance_level`, `volatility_state`, `levels_for_targets`.

---

## Stage 5 — Candles

Last 3–5 candles: direction, body/range, wick ratios. Name patterns with status codes (`CONFIRMED` / `DEVELOPING` / `POSSIBLE` / `UNCLEAR`) and the failing rule if any. At most one primary pattern + one secondary. Produce `candle_state`:

* `forming` — last candle still open
* `closed` — last candle closed, no breakout
* `unconfirmed_breakout` / `unconfirmed_breakdown` — price beyond level but missing close + volume + hold
* `confirmed_breakout` / `confirmed_breakdown` — closes + evidence
* `failed_breakout` / `failed_breakdown` — close back inside

---

## Stage 6 — Indicators

Only those visibly present. For each: name/period, value, reading, limitation. If computation from OHLCV is possible (`atr`, etc.), compute via `integrations/python/trading_intel/indicators.py`. Otherwise mark not assessable.

---

## Stage 7 — Volume

Relative to the 20-bar average: expanding / contracting / climax / diverging. If no panel → `volume_present: false`, `volume_confirmed: None`, and note in missing-data.

---

## Stage 8 — Context

If browsing exists: index behaviour, sector, instrument news, events inside the horizon — each cited with timestamp. If not, mark `web_research: unavailable`. If an upcoming event falls inside the holding horizon, set `event_risk` (string name + date).

---

## Stage 9 — Timeframes

Table of every timeframe actually seen. Unknown → "not provided". No guessing. Set `htf_conflict`, `htf` / `ltf` strings if alignment fails.

---

## Stage 10 — Traps

Run `workflows/trap-detection.md`. For each hypothesis: level, behaviour, evidence, what would confirm it. Set `trap_unrefuted` if any hypothesis cannot be refuted.

---

## Stage 11 — Risk & levels

Derive ATR (if visible/computable), candidate invalidation (structural price beyond pattern/thesis), distance in ATR and %, R:R arithmetic per target. Set `swing_level`, `structural_stop`, `atr`, `levels_for_targets`.

---

## Stage 12 — Scenarios (internal only)

Always three internally (bullish / bearish / no-trade), each with trigger, entry zone, invalidation, T1/T2/T3, R:R. The quick report only surfaces the preferred direction's levels — the full report renders all three on demand.

---

## Stage 13 — Verdict

Call `quick_signal.decide_verdict` via `build_quick_signal`. One of `WAIT` / `NO TRADE` / `PAPER-TRADING SETUP READY`. Also produce the English `reason` and Hinglish line.

---

## Stage 14 — Compact report

Call `quick_signal.render_quick_text` (full compact) or `render_compact_text_minimal` (8–12 lines) and `render_quick_html` for the visual variant. Include:

* Header (instrument | exchange | timeframe)
* Verdict, WAIT UNTIL, ENTRY, STOP LOSS, TP1/TP2/TP3, RISK/REWARD, REASON + Hinglish, timestamps, disclaimer.

No full indicator tables, long news summaries, detailed market structure, long fundamental analysis, historical backtesting tables, or full research methodology.

---

## Stage 15 — Record (optional)

If persistence exists, write `journal/YYYY/MM/DD/<instrument>-<id>.md` with the compact hypothesis. Otherwise print inline. Never edit later.

---

## Checklist before sending

* [ ] Header complete (instrument, exchange, timeframe, both timestamps, freshness, data source)
* [ ] WAIT UNTIL names a condition, never a time
* [ ] Every number traceable (observed / computed) or `NOT AVAILABLE`
* [ ] Every pattern has status code
* [ ] Every scenario has invalidation (or verdict is NO TRADE with the reason)
* [ ] Hinglish section present and genuinely simple
* [ ] Missing data explicitly listed in provenance
* [ ] No fabricated price, no unsupported probability, no promised breakout time
* [ ] Output is 8–12 short lines (or compact labelled blocks)

*See also: `core/quick-output-engine.md` · `workflows/wait-confirmation.md` · `workflows/entry-validation.md` · `workflows/target-calculation.md`.*
