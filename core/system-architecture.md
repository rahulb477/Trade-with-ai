# System Architecture

How the repository is wired, what flows where, and which invariants must never be violated.

---

## 1. Design intent

Three forces shape every decision here:

1. **Evidence before opinion.** Every claim carries a provenance class (see
   [`evidence-engine.md`](evidence-engine.md)). Unclassified claims are not allowed to influence
   a decision.
2. **Degradation instead of invention.** The skill must remain useful with no internet, no OCR,
   no code execution, and no API keys — by *narrowing what it asserts*, never by filling gaps
   with plausible-sounding text.
3. **Platform independence.** The knowledge layer is plain Markdown. Everything executable is
   optional. No host-specific mechanism is required for the core to function.

---

## 2. Layer model

```
┌──────────────────────────────────────────────────────────────────┐
│ L5  PRESENTATION         templates/*.md, workflows/beginner-*    │
│     Report shells that enforce the mandatory format              │
├──────────────────────────────────────────────────────────────────┤
│ L4  DECISION             core/decision-engine.md                 │
│     Evidence → scenario set → verdict + confidence language      │
├──────────────────────────────────────────────────────────────────┤
│ L3  ANALYSIS ENGINES     engines/*                                │
│     chart • technical • market • quant • options • order flow     │
├──────────────────────────────────────────────────────────────────┤
│ L2  KNOWLEDGE            knowledge/*, strategies/*, markets/*     │
│     Definitions, rules, thresholds, failure modes                │
├──────────────────────────────────────────────────────────────────┤
│ L1  EVIDENCE & DATA      core/evidence-engine.md, data-sources/*  │
│     Provenance, freshness, validation, provider interfaces        │
├──────────────────────────────────────────────────────────────────┤
│ L0  CAPABILITY           core/capability-detection.md             │
│     What the host agent can actually do right now                │
└──────────────────────────────────────────────────────────────────┘
         ▲                                              │
         │  L0 constrains what L1..L5 may claim          │
         └──────────────────────────────────────────────┘
```

**Rule:** a layer may only use layers strictly below it. The decision layer never reads
`knowledge/` directly for a *rule* — it invokes an engine, which reads knowledge and returns a
finding. This keeps interpretations auditable: you can always ask "which module produced this
statement?"

---

## 3. Component inventory and dependency graph

```
capability-detection ──► data-integrity ──► evidence-engine
                                │                 │
   chart-recognition ◄──────────┘                 │
        │                                         │
        ├──► chart-intelligence ──┐               │
        │                         │               │
        ├──► technical-intelligence ──┐           │
        │                         │    │          │
        └──► market-intelligence ──┤    │          │
                                  ▼    ▼          ▼
                             decision-intelligence ◄── risk-management
                                       │
                    ┌──────────────────┼──────────────────┐
                    ▼                  ▼                  ▼
             research-agent   prediction-tracking   self-evaluation
                                       │
                                       ▼
                              backtesting / strategy-discovery
```

Arrows mean "may be used by". No cycles are permitted between engines. `decision-intelligence`
is the only engine allowed to emit a verdict.

---

## 4. Primary dataflow for one analysis

| Stage | Producer | Artifact | Consumed by |
|-------|----------|----------|-------------|
| 1 | capability-detection | capability block | every stage |
| 2 | chart-recognition | `ChartObservation` | chart-intelligence, evidence-engine |
| 3 | chart-recognition | quality verdict + missing list | decision-intelligence (gate) |
| 4 | chart-recognition | resolved instrument + exchange | market-intelligence |
| 5 | chart-intelligence | structure map (trend, swings, S/R) | technical, decision |
| 6 | chart-intelligence | pattern findings with status codes | decision |
| 7 | technical-intelligence | indicator readings (only visible ones) | decision |
| 8 | chart-intelligence | volume assessment | decision |
| 9 | market-intelligence | cited context items | decision |
| 10 | chart-intelligence | multi-timeframe table | decision |
| 11 | chart-intelligence | trap hypotheses + evidence | decision |
| 12 | risk-management | volatility + invalidation + R:R | decision |
| 13 | decision-intelligence | scenario set A/B/C | research-agent |
| 14 | decision-intelligence | verdict + confidence language | presentation |
| 15 | presentation | Markdown report | user |
| 16 | prediction-tracking | immutable record | self-evaluation later |

Every artifact carries the timestamps from stage 1–4. A finding without a timestamp is dropped.

---

## 5. Invariants (violating any of these is a defect, not a style choice)

| ID | Invariant |
|----|-----------|
| I1 | A pattern may only be labelled `CONFIRMED` if the candle that completes it has **closed** on the displayed timeframe. |
| I2 | No numeric value enters the report unless it is `OBSERVED` (read from the image), `COMPUTED` (derived from observed values, formula shown), `CITED` (source + timestamp), or `ASSUMED` (labelled, with default stated). |
| I3 | Every scenario carries an invalidation level. No invalidation → no scenario. |
| I4 | A timeframe that was not viewed is never described as analysed. |
| I5 | An instrument is never inferred from a partial ticker when two listed companies could match. |
| I6 | Freshness class is attached to every external fact and propagates to the verdict. `STALE` data cannot support an intraday verdict. |
| I7 | Prediction records are append-only. Evaluation is a separate, later artefact. |
| I8 | The verdict vocabulary is closed: `WAIT`, `BULLISH SCENARIO`, `BEARISH SCENARIO`, `INSUFFICIENT DATA`, `NO-TRADE`. Free-text verdicts are a defect. |
| I9 | Confidence is expressed with the qualitative ladder in `evidence-engine.md`, never a fabricated percentage. |
| I10 | No personal-experience claim, no promised return, no real-money instruction. |

---

## 6. Failure handling

| Failure | Detection | Response |
|---------|-----------|----------|
| Image unreadable | quality rubric < threshold | `INSUFFICIENT DATA` + re-capture instructions |
| Ticker ambiguous | two candidates | Ask; forbid guessing |
| No higher timeframe | not supplied | Declare `HTF: not provided`; cap verdict at `WAIT` for continuation claims |
| Indicator period unknown | not printed on chart | Assume documented default, mark `ASSUMED` |
| Provider timeout | 2 retries then fail | Mark source unavailable; continue with lower confidence |
| Conflicting sources | disagreement on a material fact | Report both, state unresolved, lower confidence |
| Malformed provider payload | schema validation | Reject payload, log, do not partially parse |
| No persistence | write fails | Print record inline, flag unsaved |

---

## 7. Extension points

- **New indicator**: add `knowledge/indicators/<name>.md`, add a tested function in
  `integrations/python/trading_intel/indicators.py`, add a case in `tests/indicators/`.
- **New provider**: implement the `Provider` protocol in
  `integrations/python/trading_intel/providers/base.py`; document in `data-sources/providers.md`.
- **New market**: add `markets/<market>/README.md` with sessions, holidays, tick/lot, settlement.
- **New engine**: create `engines/<name>/README.md` describing inputs, outputs, failure modes;
  wire it into the dependency graph above and into `SKILL.md` §4.

An extension is only "done" when its tests pass and its links resolve.

---

## 8. What is deliberately *not* in the architecture

- No price-prediction model. There is no trained forecaster, and none is implied.
- No portfolio execution layer. Sizing exists for **education**, not for live capital.
- No sentiment scraping of social media as evidence — it is not verifiable in the way this
  repository demands.
- No hidden state. Everything that influences a verdict is written into the report.

---

*See also: [`analysis-engine.md`](analysis-engine.md) · [`decision-engine.md`](decision-engine.md) ·
[`../docs/architecture.md`](../docs/architecture.md)*
