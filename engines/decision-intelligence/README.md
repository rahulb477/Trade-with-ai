# Engine — Decision Intelligence

**Purpose:** convert evidence into exactly one verdict. The only engine permitted to emit a verdict.

**Inputs:** structure map, pattern findings, indicator readings, volume assessment, context items, trap scores,
risk arithmetic.
**Outputs:** three scenarios, one verdict from the closed vocabulary, a confidence label, supporting evidence,
conflicting evidence, and the outstanding confirmation.

## The gate ladder (normative)

```
G1 DATA INTEGRITY   fail -> INSUFFICIENT DATA
G2 EVENT RISK       binary event in horizon -> NO-TRADE (or explicit reduce)
G3 STRUCTURE        no definable invalidation -> WAIT
G4 LOCATION         R:R_T1 < 1.5 or poor location -> WAIT
G5 TRIGGER          no confirmation event yet -> WAIT (name it)
G6 ALIGNMENT        unexplained HTF conflict -> WAIT
G7 TRAP RISK        unrefuted trap evidence -> WAIT (or flip if confirmed)
G8 VERDICT          assign direction + confidence
```

The first failing gate determines the verdict. Full detail in
[`../../core/decision-engine.md`](../../core/decision-engine.md).

## Verdict vocabulary (closed)

`BULLISH SCENARIO` · `BEARISH SCENARIO` · `WAIT — NO CONFIRMED SETUP` · `NO-TRADE` ·
`INSUFFICIENT DATA — NO VALID SETUP`

Free-text verdicts are a defect.

## Confidence labels

| Label | Requirement |
|-------|-------------|
| Strong | ≥4 independent evidence classes; no material conflict; R:R ≥ 2 |
| Moderate | 3 classes; minor conflict resolved; R:R ≥ 1.5 |
| Weak | 2 classes, OR 3+ with an unexplained material conflict |
| Speculative | 1 class, or quality 5–7, or a developing pattern only |
| Not assessable | Data gate failed |

**Independence is audited** using the family map in `../technical-intelligence/README.md` and
`core/evidence-engine.md` §6. Five candles from the same three bars are one class.

## Output object

```
{
  verdict: "WAIT — NO CONFIRMED SETUP",
  confidence: "Weak",
  scenarios: [A, B, C],
  gates: {g1: pass, g2: pass, g3: pass, g4: fail, g5: n/a, g6: pass, g7: n/a},
  failing_gate: "G4: R:R to T1 = 0.93 (< 1.5); price mid-range at 492 in a 480-505 range",
  supporting: [ ... ],
  conflicting: [ ... ],
  outstanding_confirmation: "a boundary test with a rejection close",
  missing_data: [ ... ]
}
```

## Failure modes

| Failure | Guard |
|---------|-------|
| Averaging evidence into a score | Use gates |
| Emitting a direction with no trigger | Gate 5 |
| Emitting a direction with no invalidation | Gate 3 |
| Hiding a conflict | `conflicting` is mandatory |
| Inflating confidence | Independence audit |
| Skipping the no-trade scenario | All three are mandatory |
