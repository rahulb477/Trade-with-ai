# Engine — Prediction Tracking

**Purpose:** make the repository's own accuracy measurable, without allowing retroactive editing.

## 1. Record schema (immutable block)

```yaml
analysis_id:         <instrument>-<YYYYMMDD>-<HHMM>-<hash6>
instrument:          RELIANCE
exchange:            NSE
mode:                RESEARCH | PAPER-TRADING | LEARNING
analysis_timestamp:  2026-11-14T15:31:00+05:30
data_timestamp:      2026-11-14T15:30:00+05:30
data_source:         screenshot | provider:<name> | user-transcription
screenshot_ref:      journal/img/xyz.png | not-retained
timeframes_used:     [1D, 15m]
timeframes_absent:   [1W, 1H]
regime:              trending_up | ranging | high_vol | squeeze | transitional
hypothesis:          one sentence
scenarios:
  A: {trigger, entry_zone, invalidation, t1, t2, t3, rr_t1}
  B: {trigger, entry_zone, invalidation, t1, t2, t3, rr_t1}
  C: {reason}
predicted_primary:   A | B | C
confidence_label:    Strong | Moderate | Weak | Speculative | Not assessable
evidence:            [ {claim, provenance_class, source} ]
missing_data:        [ ... ]
whole_analysis_invalidation: one sentence
```

## 2. Evaluation block (appended later, never merged)

```yaml
evaluation_date:        2026-11-21T16:00:00+05:30
scenario_that_triggered: A | B | none
directional_correct:    true | false | n/a
setup_executable:       true | false      # did the trigger occur AND the invalidation survive?
trap_hypothesis_correct: true | false | n/a
data_quality_material:  true | false
max_favourable_excursion: <price or R>
max_adverse_excursion:   <price or R>
notes:                  free text
correction_to_original: (only if the original contained an error — timestamped, never silent)
```

## 3. The distinction that matters

| Metric | Definition |
|--------|-----------|
| **Directional accuracy** | Did price move in the direction the favoured scenario implied? |
| **Executable success** | Did the trigger occur, and would the stated invalidation have held while the target was reached? |
| **Trap accuracy** | When a trap was hypothesised, was it confirmed? |
| **WAIT quality** | When the verdict was WAIT, did price in fact offer no clean setup? (Measured by whether either scenario's trigger occurred and survived.) |

A forecaster can be directionally right and executably wrong — the stop gets hit before the target. Both must be
tracked, or the statistics will flatter you.

## 4. Aggregation

```python
# monthly
directional_hit_rate = directional_correct / evaluable
wilson_ci            = wilson_interval(k=directional_correct, n=evaluable)
executable_rate      = setup_executable / evaluable
avg_R_executed       = mean(R of executed setups)
wait_rate            = count(verdict == WAIT) / total
data_failure_rate    = count(quality_issue) / total
```

Report all five with sample sizes. A hit rate on 8 analyses has a confidence interval spanning almost the whole
range — say so.

## 5. Rules

1. **Append-only.** No edits to the immutable block, ever.
2. **Record before the outcome.** If an outcome is already known, mark the record `RETROSPECTIVE` and exclude it
   from statistics.
3. **Never delete failures.** Deleting them destroys the evidence.
4. **One analysis = one record.** Do not merge records to improve a rate.
5. **Score honestly.** A directionally-correct-but-unexecutable result is not a win.

## 6. Why this engine exists

Without it, an AI's track record is whatever it remembers — which is the same failure mode as human hindsight bias
(`knowledge/trading-psychology/cognitive-biases.md` §2). The immutable record is the only defence.

## 7. Integration

- Template: `templates/prediction-record.md`
- Workflow: `workflows/prediction-logging.md`
- Consumer: `engines/self-evaluation/README.md`
- Storage: `journal/YYYY/MM/DD/`
