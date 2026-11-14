# Engine — Self-Evaluation

**Purpose:** turn the repository's own predictions into measurable performance — and identify repeated analytical
mistakes.

## 1. Inputs
Evaluated prediction records from `engines/prediction-tracking/`. A record cannot be evaluated until the
hypothesis's horizon has elapsed.

## 2. Per-record scoring

```
directional_correct : did price move in the favoured direction?
setup_executable    : did the trigger occur AND the invalidation hold until a target?
trap_correct        : if a trap was hypothesised, was it confirmed?
wait_appropriate    : if the verdict was WAIT, did neither scenario's trigger survive?
data_quality_impact : did missing data materially change the outcome?
calibration_bucket  : the stated confidence label vs the actual outcome
```

## 3. Aggregate metrics

| Metric | Formula |
|--------|---------|
| Directional hit rate | correct / evaluable, with a Wilson CI |
| Executable rate | executable / evaluable |
| WAIT quality | appropriate WAITs / total WAITs |
| Calibration | for each confidence label, the observed success rate |
| Data-failure rate | records with a material data gap / total |
| Error taxonomy mix | share of each error type (below) |

## 4. Error taxonomy (the most useful output)

| Error class | Definition | Fix |
|-------------|-----------|-----|
| **Pattern over-call** | Named a pattern that failed a rule | Enforce numeric rule audits |
| **Location blindness** | Setup mid-range with no level | Enforce the location gate |
| **Trigger missing** | Entered on a pattern without a confirmation close | Enforce gate G5 |
| **Timeframe neglect** | Ignored a conflicting higher timeframe | Enforce the timeframe table |
| **Trap misclassification** | Called a retest a trap, or vice versa | Use the six-test evidence score |
| **Data optimism** | Built a conclusion on an `ASSUMED` value | Mark assumptions in the ledger |
| **Confidence inflation** | Said Moderate with only two independent classes | Independence audit |
| **R:R fiction** | Presented a target that failed the 1.5R gate | Show the arithmetic every time |
| **Event blindness** | Ignored a scheduled binary event | Event-risk gate |
| **Sycophancy** | Became more bullish because the user was | Evidence-only confidence |

Run this taxonomy monthly. The dominant class tells you which gate to tighten.

## 5. Calibration

```
For each confidence label, count outcomes:
  Strong       : 14 analyses, 9 correct  -> 64%
  Moderate     : 31 analyses, 15 correct -> 48%
  Weak         : 22 analyses, 9 correct  -> 41%
  Speculative  :  9 analyses, 3 correct  -> 33%
```

If the ordering is not monotonic, the confidence ladder is miscalibrated and should be revised — with the revision
recorded in `CHANGELOG.md`, not applied silently.

## 6. What self-evaluation must never do

| Prohibited | Why |
|-----------|-----|
| Retroactively edit a prediction | Destroys the only valid evidence |
| Delete failed records | Survivorship bias in your own track record |
| Report a rate without a CI and n | Misleading |
| Change the confidence ladder to improve apparent calibration without disclosure | Silent goalpost movement |
| Automatically update the knowledge base from a small sample | `SKILL.md` rule: no unverified knowledge updates |

## 7. Periodic report template

```
SELF-EVALUATION — 2026-11
Records: 43 opened, 31 evaluable, 12 pending horizon
Directional hit rate      : 51.6% (95% CI 34.8-68.1%)  <- wide: n is small
Executable setup rate     : 38.7%
WAIT quality              : 12 of 14 WAITs appropriate
Calibration               : Strong 64% > Moderate 48% > Weak 41% (monotonic, good)
Data-failure rate         : 19% of records had a material gap (mostly missing higher timeframe)
Dominant error class      : location blindness (7 of 19 misses)
Action                    : add an explicit mid-range check to the pre-report checklist
Confidence ladder change  : none
```

## 8. Honest framing

With 31 evaluable records, a 51.6% hit rate is indistinguishable from 40% or 65%. The value of this engine is not a
precise number — it is (a) the error taxonomy, which is diagnostic even in small samples, and (b) the discipline
of not being able to rewrite history.

State this limitation in every self-evaluation report.
