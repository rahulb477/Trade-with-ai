# Prediction Record Template

> **Immutable block.** Write this *before* the outcome exists. Never edit it afterwards. The evaluation block is
> appended later with its own timestamp.

```yaml
# ---------- IMMUTABLE BLOCK ----------
analysis_id:            <INSTRUMENT>-<YYYYMMDD>-<HHMM>-<hash6>
created_at:             <ISO 8601 with timezone>
mode:                   LEARNING | RESEARCH | PAPER-TRADING
data_mode:              offline | web research | market-data | full research

instrument:             <ticker>
exchange:               <exchange>
asset_class:            equity | index | futures | options | forex | commodity | crypto
timeframes_used:        [<...>]
timeframes_absent:      [<...>]
chart_quality_score:    <0-10>

data_timestamp:         <ISO 8601>
data_source:            screenshot | provider:<name> | user-transcription
screenshot_retained:    yes (path) | no
regime:                 trending_up | trending_down | ranging | high_volatility | squeeze | transitional
structure_summary:      <one line: HH/HL count, key levels>

hypothesis:             <one sentence, falsifiable>

scenarios:
  A:
    trigger:            <exact condition>
    entry_zone:         <low-high>
    invalidation:       <price + structural meaning>
    t1: <price>  t2: <price>  t3: <price>
    rr_t1:              <number>
  B:
    trigger:            <...>
    entry_zone:         <...>
    invalidation:       <...>
    t1: <...>  t2: <...>  t3: <...>
    rr_t1:              <...>
  C:
    reason:             <why standing aside is the third scenario>

predicted_primary:      A | B | C
verdict:                BULLISH SCENARIO | BEARISH SCENARIO | WAIT — NO CONFIRMED SETUP |
                        NO-TRADE | INSUFFICIENT DATA — NO VALID SETUP
confidence_label:       Strong | Moderate | Weak | Speculative | Not assessable

evidence:
  - claim:              <...>
    provenance_class:   chart-observation | computed | external-cited | user-stated | assumption
    source:             <...>
conflicting_evidence:   [<...>]
missing_data:           [<...>]
assumptions:            [<...>]

whole_analysis_invalidation: <one sentence: what makes the entire analysis wrong>
```

```yaml
# ---------- EVALUATION BLOCK (append; never merge) ----------
evaluated_at:            <ISO 8601>
horizon_end:             <date>
scenario_triggered:      A | B | none
directional_correct:     true | false | n/a
setup_executable:        true | false
trap_hypothesis_correct: true | false | n/a
data_quality_material:   true | false
mfe:                     <price or R>
mae:                     <price or R>
outcome_notes:           <free text>
process_notes:           <was the stated process followed?>
correction_to_original:  <only if the original contained an error; timestamped; never silent>
retrospective:           true | false      # true if the outcome was already known when written
```

## Files

- Store at `journal/YYYY/MM/DD/<analysis_id>.md`
- One record per analysis. Never merge records to improve a rate.
- Screenshots at `journal/img/` are gitignored by default — set `screenshot_retained: no` if not stored.

## Rules (restated because they are always broken under pressure)

1. Record before the outcome; `retrospective: true` if you did not.
2. Append only.
3. Never delete a failed record.
4. Directional accuracy and executable success are different metrics. Report both.
