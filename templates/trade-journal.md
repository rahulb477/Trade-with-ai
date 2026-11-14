# Trade Journal Template

For an **actual** trade (paper or live). The prediction record is a hypothesis; this is an execution.

## 1. Immutable block (written before entry)

```yaml
trade_id:             <YYYYMMDD>-<seq>
instrument:           <ticker>
setup_name:           <which documented play>
timeframe:            <...>
signal_timestamp:     <ISO 8601>
entry_planned:        <price or zone>
stop:                 <price>
t1: <...>  t2: <...>  t3: <...>
risk_pct:             <0.25-1.0>
size_units:           <number>
reasoning:            <3 sentences maximum>
confidence:           Strong | Moderate | Weak | Speculative
invalidation_meaning: <what price action proves the idea wrong>
circuit_breakers:     <daily loss limit, max trades, time stop>
screenshot:           <path or "none retained">
```

## 2. Execution block (written at entry)

| Field | Value |
|-------|-------|
| Actual entry price | |
| Actual size | |
| Slippage vs plan | |
| Time of entry | |
| Was the plan followed? | yes / no / partially |
| If not, why | |

## 3. Management log (append as events occur)

| Time | Price | Action | Reason |
|------|-------|--------|--------|
| | | | |

## 4. Exit block

| Field | Value |
|-------|-------|
| Exit price / time | |
| Exit reason | target / stop / time / discretionary |
| Realised R | |
| MAE (R) | |
| MFE (R) | |
| Costs (estimated R) | |
| Net R | |

## 5. Review block (written within 24 hours, not later)

| Question | Answer |
|----------|--------|
| Was the process followed exactly? | |
| Would the outcome have differed under perfect execution? | |
| Process quality (A–D) | A: rule followed and edge present · B: rule broken · C: rule followed, no edge · D: no edge and rule broken |
| Outcome (good/bad) | |
| The 2×2 cell | good process + good outcome / good process + bad outcome / bad process + good outcome / bad process + bad outcome |
| One sentence to my future self | |

**The dangerous cell is bad process + good outcome.** It teaches the wrong lesson. Flag it explicitly.

## 6. Loss class (if a loss)

| Class | Definition |
|-------|-----------|
| A | Correct process, adverse outcome (variance) |
| B | Rule broken (discipline problem) |
| C | Correct process, edge absent (research problem) |
| D | Incorrect process and adverse outcome (both) |

Only class B is a discipline failure. Class B entries should trigger a circuit breaker review, not a resolution to
"try harder".
