# Architecture

## 1. Shape of the repository

```
Trade-with-ai/
├── SKILL.md                  entry point + routing contract (§4)
├── AGENTS.md                 agent-facing operating instructions
├── README.md                 human entry point
├── core/                     8 documents defining the pipeline and its gates
├── knowledge/                the domain reference (the largest part)
├── workflows/                10 step-by-step procedures
├── strategies/               4 horizons + the validation gate
├── engines/                  13 engines, each with inputs/outputs/failure modes
├── data-sources/             provider interface, validation, news, credentials
├── markets/                  market-specific rules (India, US, forex, commodities, crypto)
├── integrations/             Python library, adapters, browser/OCR specs
├── templates/                6 copy-paste artefacts
├── examples/                 7 worked examples (fictional data)
├── tests/                    287 stdlib unit tests
├── scripts/                  link check, audit, full test run
├── docs/                     this directory
└── journal/                  where records live (gitignored by default)
```

## 2. Three layers

| Layer | Question it answers | Lives in |
|-------|--------------------|----------|
| **Specification** | What must be true, and how do we know? | `core/`, `knowledge/`, `workflows/`, `SKILL.md` |
| **Computation** | What are the numbers? | `integrations/python/trading_intel/` |
| **Record** | What did we claim, before we knew? | `templates/`, `journal/`, `engines/prediction-tracking/` |

The rule that binds them: **Markdown is the specification, code is tested against it.** A code behaviour that
contradicts a documented convention is a bug in one of the two, and the discrepancy must be resolved, not ignored.

## 3. The analysis pipeline

```
              ┌──────────────────────────────┐
  input  ────▶│ 0. Mode & capability detection │
              └───────────────┬──────────────┘
                              ▼
              ┌──────────────────────────────┐
              │ 1-4. Transcribe (no opinion)   │  ← inventory, quality score, instrument, scale
              └───────────────┬──────────────┘
                              ▼
              ┌──────────────────────────────┐
              │ 5-8. Structure & levels        │  ← swings, zones, regime, room
              └───────────────┬──────────────┘
                              ▼
              ┌──────────────────────────────┐
              │ 9-12. Patterns, indicators,    │  ← status codes, provenance, volume
              │       volume, timeframe table  │
              └───────────────┬──────────────┘
                              ▼
              ┌──────────────────────────────┐
              │ 13-15. Trap audit, scenarios,  │  ← evidence scoring, three scenarios
              │        risk arithmetic         │
              └───────────────┬──────────────┘
                              ▼
              ┌──────────────────────────────┐
              │ 16. Gate ladder → VERDICT      │  ← one of five strings
              └───────────────┬──────────────┘
                              ▼
                    report (10 sections) + record
```

The 16 stages in full are in `workflows/screenshot-analysis.md`. The gate ladder is in `core/decision-engine.md`.
The **transcription-before-interpretation** rule at stage 1–4 is what prevents a plausible narrative from forming
before the evidence is on paper.

## 4. Why the verdict vocabulary is closed

Five strings, no free text:

```
BULLISH SCENARIO · BEARISH SCENARIO · WAIT — NO CONFIRMED SETUP · NO-TRADE ·
INSUFFICIENT DATA — NO VALID SETUP
```

Reasons:

1. **Measurability.** A record can only be scored later if the verdict is one of a known set.
2. **Honesty pressure.** There is no phrase that means "probably up, but I'm hedging". `WAIT` is available and
   must be used when that is the honest answer.
3. **Machine checkability.** `tests/` and `scripts/audit_repo.py` can verify vocabulary compliance.

## 5. Evidence model

Every claim carries a provenance class (`core/evidence-engine.md`):

| Class | Meaning | May influence the verdict? |
|-------|---------|---------------------------|
| `chart-observation` | visible on the supplied image | yes |
| `computed` | calculated from real data by code in this repo | yes |
| `external-cited` | retrieved, with source + timestamp | yes |
| `user-stated` | asserted by the user | only as leverage, not evidence |
| `assumption` | needed to proceed, marked `ASSUMED` | never alone |
| `insufficient` | would be needed but unavailable | triggers a downgrade |

**Independence is audited.** Two indicators from one family are one class. Five engulfing candles from the same
three bars are one class. Confidence depends on the count of *independent* classes, not the count of observations.

## 6. Code architecture

```
integrations/python/trading_intel/
├── indicators.py    pure functions, None where undefined
├── patterns.py      23 detectors → Detection/PatternHit with status + rule audit
├── risk.py          R-multiples, break-even, expectancy, drawdown, TradePlan
├── sizing.py        units = floor(equity × risk% ÷ |entry − stop|)
├── metrics.py       trade-log metrics in R, with Wilson CIs
├── stats.py         descriptive stats, correlation, Sharpe/Sortino, Wilson, multiple testing
├── simulate.py      seeded Monte Carlo, bootstrap, synthetic OHLCV
├── backtest.py      event-driven engine, next-open fills, pessimistic intrabar
├── timeframes.py    aggregation, ratio quality, alignment scoring
├── validation.py    OHLC checks, jumps, gaps, freshness, chart quality
├── observation.py   ChartObservation contract + gate report
└── providers/       Protocol, in-memory reference provider, env detection
```

Design constraints, each with a reason:

| Constraint | Reason |
|-----------|--------|
| Standard library only | The skill must run anywhere, including a bare Python install |
| No I/O in calculation modules | Makes the functions testable and free of hidden state |
| `None` for undefined | A zero would silently corrupt every downstream metric |
| Seeded randomness | Reproducible results are a research requirement |
| No silent repairs | A repaired dataset is a fabricated dataset |

## 7. Extension points

| Want to add | Touch these |
|-------------|-------------|
| A new indicator | `indicators.py` + `tests/indicators/` + `knowledge/indicators/<name>.md` + `SKILL.md` §4 |
| A new candle pattern | `patterns.py` detector + `DETECTORS` + test + `knowledge/candlesticks/<name>.md` |
| A new market | `markets/<market>/README.md` + the session rules + `markets/README.md` index |
| A new agent environment | `integrations/agent-adapters/<name>.md` following `generic.md` |
| A new provider | implement the `Provider` Protocol in `providers/`; never commit credentials |

Each extension has a "definition of done": tests pass, links resolve, the audit is clean, and the docs describe
exactly what the code does.

## 8. What is deliberately absent

| Absent | Why |
|--------|-----|
| Live data adapters | Require provider terms and keys that cannot be assumed; the interface is shipped instead |
| ML pattern models | No labelled dataset, no inter-rater agreement, no out-of-sample work — shipping one would be confident nonsense |
| Order execution | Explicitly out of scope and prohibited |
| A bundled price dataset | Licensing, size, and the certainty that it would age into misleading data |
| Greeks/pricing models | The options engine documents metrics rather than computing them; a half-tested pricer is worse than none |
