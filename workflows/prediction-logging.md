# Workflow — Prediction Logging

## When
After any analysis that makes a conditional statement about future price behaviour, if the agent can write files.
If it cannot, print the record inline labelled `NOT SAVED`.

## Step 1 — Create the record
Path: `journal/YYYY/MM/DD/<instrument>-<analysis_id>.md`
Template: `templates/prediction-record.md`

## Step 2 — Fill the immutable block

```
analysis_id        : <instrument>-<YYYYMMDD>-<HHMM>-<short-hash>
instrument         :
exchange           :
analysis_timestamp : ISO + timezone
data_timestamp     : ISO + timezone
data_source        :
screenshot_ref     : path or "not retained" (get consent before storing images)
mode               : RESEARCH / PAPER-TRADING
timeframes_used    : e.g. [1D, 1H, 15m]
timeframes_absent  : e.g. [1W]
regime             : trending up / ranging / ...
hypothesis         : one sentence
scenarios          : A bullish / B bearish / C no-trade, each with trigger + invalidation + targets
predicted_primary  : which scenario the evidence favours, or WAIT
confidence_label   : Strong / Moderate / Weak / Speculative / Not assessable
evidence           : bulleted, each tagged OBSERVED / COMPUTED / CITED / ASSUMED
missing_data       :
invalidation_of_the_whole_analysis :
```

## Step 3 — Leave the evaluation block empty
```
outcome            : (empty)
evaluation_date    : (empty)
scenario_correct   : (empty)
notes              : (empty)
```

## Step 4 — The append-only rule
1. Never edit the immutable block.
2. Evaluation is a **new** section appended later, or a separate file.
3. If you discover an error in the original, add a correction note with a timestamp — do not silently fix it.

Rationale: the record's only value is that it cannot be adjusted after the fact.

## Step 5 — Evaluation protocol (later)
```
1. Retrieve the record.
2. Determine which scenario triggered (or none).
3. Score:
   - directional_correct  : did price move in the favoured direction?
   - setup_executable     : did the trigger occur, and would the invalidation have held?
   - trap_correctly_called: if a trap hypothesis was made, was it right?
   - data_quality_issue   : was missing data material to the outcome?
4. Record max favourable and maximum adverse excursion until the horizon.
5. Append the evaluation with a timestamp.
```

**Distinguish directional correctness from executable success.** Being right about direction but with an
invalidation that gets hit first is not a successful setup. Both metrics must be tracked separately
(`engines/prediction-tracking/`).

## Step 6 — Aggregate honestly
Monthly aggregation:
- Directional hit rate with a confidence interval
- Executable setup rate
- Average R of executed setups
- Data-quality failure count
- Number of analyses where the verdict was WAIT (and what happened after)

Never delete records that performed badly. Deleting them destroys the only evidence you have.

## Privacy note
Do not store screenshots containing personal information (account balances, names, order history panels) without
explicit consent. Default to `screenshot_ref: not retained`.
