# Engine — Research Agent

**Purpose:** the 10-step autonomous research loop specified for this skill, with explicit module-selection
justification and capability-aware fallbacks.

## The loop

| # | Step | Module | Artifact | Fallback if unavailable |
|---|------|--------|----------|-------------------------|
| 1 | Understand the question | `SKILL.md` §2–3 | mode + scope | Ask one clarifying question |
| 2 | Identify the instrument | `core/chart-recognition.md` §3 | instrument + exchange | Ask; never guess |
| 3 | Load relevant knowledge | `SKILL.md` §4 | module list | Use entry-point summaries; state reduced depth |
| 4 | Analyse the chart | `workflows/screenshot-analysis.md` | structure + patterns | Request a transcription |
| 5 | Retrieve external evidence | `workflows/news-research.md` | cited context | Standard "unavailable" paragraph |
| 6 | Verify the data | `engines/data-integrity/README.md` | freshness + validity | Downgrade claims |
| 7 | Quantitative work | `engines/quantitative-intelligence/` | R:R, statistics | Manual arithmetic, labelled |
| 8 | Compare scenarios | `core/decision-engine.md` | A/B/C + verdict | — (always possible) |
| 9 | Generate the report | `templates/analysis-report.md` | Markdown report | — |
| 10 | Record the analysis | `engines/prediction-tracking/` | prediction record | Print inline, labelled NOT SAVED |

## Module-selection justification (required in the report)

The agent must be able to explain why it loaded what it loaded:

```
Modules selected
  core/chart-recognition.md        -> to score screenshot quality and transcribe elements
  knowledge/candlesticks/README.md -> confirmation hierarchy before naming any pattern
  knowledge/candlesticks/hammer.md -> a hammer is visible on the last closed candle
  knowledge/indicators/rsi.md      -> an RSI panel is visible with a printed value
  workflows/trap-detection.md      -> price closed back below a level after breaking it
  core/risk-management.md          -> to compute R:R and an illustrative size
Modules deliberately not loaded
  knowledge/smart-money/*          -> not requested and adds no verifiable evidence here
  engines/options-intelligence/    -> no option-chain data provided
  markets/united-states/*          -> instrument is NSE-listed
```

This is the audit trail that makes the analysis reproducible.

## Capability-aware behaviour

| Missing | Behaviour |
|---------|-----------|
| Vision | Transcription request; no chart claims |
| Filesystem | Answer from `SKILL.md`; declare reduced depth |
| Web | "Web research unavailable"; technical-only analysis |
| Code execution | Manual arithmetic, shown step by step, labelled |
| Persistence | Record printed inline, labelled NOT SAVED |

## Loop budget

| Loop | Limit | On exhaustion |
|------|-------|---------------|
| Module loading | ≤ 8 files | Stop; list skipped modules |
| Research retries | 2 per source | Mark unavailable |
| Clarifying questions | 2 per turn | Ask the two highest-value |
| Draft revisions | 3 | Emit best draft + open gaps |

## Step-by-step trace (optional, for debugging)

When a user asks "how did you reach that?", emit the loop as a numbered trace with the artifact from each step. This
is required for the repository's own self-evaluation (`engines/self-evaluation/`).

## Failure modes

| Failure | Guard |
|---------|-------|
| Loading 20 modules | Budget of 8 |
| Skipping verification | Step 6 is not optional |
| Producing a verdict with no scenario comparison | Step 8 is not optional |
| Recording after the outcome | Record before publishing the verdict |
| Claiming a step happened when it did not | Steps that failed are named as failed |
