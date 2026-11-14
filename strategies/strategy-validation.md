# Strategy Validation — The Mandatory Gate

**No strategy in this repository may be described as "good", "profitable", or "has an edge" unless it passes every
gate below.** Otherwise the only permitted description is "documented method, unvalidated".

---

## Gate 1 — Mechanical definition

- [ ] Entry rule expressed as a condition on closed-bar data
- [ ] Exit rules (target, stop, time) fully specified
- [ ] Position sizing rule specified
- [ ] Filters specified (regime, liquidity, events)
- [ ] No discretionary words ("if it looks strong")

A rule that requires judgement cannot be validated; it can only be described.

## Gate 2 — Data integrity

- [ ] Point-in-time universe (or survivorship bias disclosed)
- [ ] Adjusted prices
- [ ] Sufficient history (≥3 years, covering bull, bear, range)
- [ ] Costs and slippage modelled
- [ ] Gaps handled (fill at the open, not at the stop)

## Gate 3 — Sample size

| Sample | Permitted claim |
|--------|-----------------|
| < 30 trades | "Anecdote. No claim possible." |
| 30–99 | "Preliminary signal. Wide uncertainty." |
| 100–299 | "Suggestive, with a reported confidence interval." |
| ≥ 300 | "Reasonably estimated (still a sample)." |

## Gate 4 — Out-of-sample

- [ ] In-sample / out-of-sample split, chronological
- [ ] Out-of-sample used **once**
- [ ] Walk-forward used where parameters exist
- [ ] Parameter drift across folds reported

## Gate 5 — Robustness

- [ ] Parameter plateau (not a spike)
- [ ] Sub-period stability (positive in ≥3 of 4 quartiles)
- [ ] Instrument breadth (≥5 instruments)
- [ ] Regime breakdown reported
- [ ] Survives 2× costs

## Gate 6 — Economics

- [ ] A stated mechanism for why the edge should exist
- [ ] Cost per trade converted to R
- [ ] The edge is larger than the cost

## Gate 7 — Risk profile

- [ ] Max drawdown reported in R and currency
- [ ] Longest losing streak reported
- [ ] Max adverse excursion reported
- [ ] Sizing that would have survived the worst streak

## Gate 8 — Disclosure

- [ ] Number of variants tested
- [ ] Period covered
- [ ] All assumptions listed
- [ ] Known failure conditions listed

---

## Status labels (use exactly one)

| Label | Meaning |
|-------|---------|
| `DOCUMENTED` | Rules written down; no testing performed |
| `BACKTESTED-IN-SAMPLE` | Tested on the design data only; no out-of-sample |
| `PROMISING` | Passed in-sample + validation; holdout not used |
| `VALIDATED-SAMPLE` | Passed all gates; results are sample statistics, not guarantees |
| `REJECTED` | Failed a gate; kept in the record with the reason |

There is deliberately **no label for "profitable"**. A validated sample still is not a promise.

---

## The required disclosure sentence

> "This is a [STATUS] result on [n] trades over [period] across [instruments], including costs of [x] bps round
> trip. It has [has/has not] been tested out of sample. It is a historical sample statistic, not a forecast of
> future returns."

---

## Why this exists

Strategies are the most over-claimed artefact in trading. Every one of the eight gates corresponds to a documented
way that backtests become fiction: overfitting (5), look-ahead (2), survivorship (2), multiple testing (8), cost
neglect (6), small samples (3), and narrative without mechanism (7).

A strategy that cannot pass the gates is still useful — as a documented hypothesis. Say that.
