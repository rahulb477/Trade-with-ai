# Discipline and Journaling

## 1. The claim, stated plainly

A documented, rule-following trader with a modest method outperforms an undisciplined trader with a good method —
because the second one cannot know whether their method is good.

The journal is the only instrument that makes this measurable.

---

## 2. What a journal must contain (per trade or per analysis)

| Field | Why |
|-------|-----|
| Date/time and timeframe | Reproducibility |
| Instrument + exchange | Ambiguity kills evaluation |
| Setup type and rule reference | Connects the trade to a tested method |
| Why I took it (evidence, tagged with provenance) | Exposes reasoning errors later |
| Entry / stop / targets (T1–T3) | Enables R computation |
| Risk in R and in currency | Comparison across sizes |
| Invalidation condition | Falsifiability |
| Position size + notional | Exposure record |
| Costs (estimated and actual) | The hidden half of performance |
| Outcome (R) | The measurement |
| Max adverse excursion | How much heat was taken |
| What actually happened vs what I expected | The learning |
| What I would do differently | The improvement |

For **analysis-only** records (no trade), the same structure minus size and outcome, plus the recorded
predictions and whether they were later confirmed or invalidated.

---

## 3. The append-only rule

1. Write the hypothesis **before** the outcome.
2. Never edit it afterwards.
3. Record the evaluation as a **new, separate entry** with a timestamp.

Why: hindsight bias is not a character flaw, it is a memory property. Without an immutable record, you literally
cannot tell whether your process works.

`templates/prediction-record.md` implements this. `engines/prediction-tracking/` specifies the schema.

---

## 4. Pre-trade checklist (print this)

- [ ] Instrument and exchange confirmed
- [ ] Timeframe identified; higher timeframe checked (or declared unknown)
- [ ] Regime classified (trend / range / unclear)
- [ ] Level identified with ≥2 touches
- [ ] Setup has a specific trigger (a close, not a feeling)
- [ ] Invalidation is structural and written down
- [ ] R:R to T1 ≥ 1.5, after costs
- [ ] Size computed by formula, rounded down
- [ ] Notional within ceiling
- [ ] No scheduled event inside the horizon (or size reduced)
- [ ] Conflicting evidence written out
- [ ] I would take this trade if I had no position and no memory of today

If any box fails, the trade is not taken. This is the whole discipline.

---

## 5. Post-trade review (weekly)

```
1. Compute R for every closed trade.
2. Compute: win rate with CI, average win/loss in R, expectancy, profit factor, max consecutive losses.
3. Classify each loss: (a) rule followed, thesis wrong; (b) rule broken; (c) bad luck (gap, news).
4. Count category (b). That count is your discipline metric.
5. Identify the most common *reason* for category (b) — usually impatience, size, or a moved stop.
6. Change ONE process rule for next week. Not five.
```

Category (b) losses are the only ones worth fixing. Category (a) is the cost of doing business. Category (c) is
managed by size, not by skill.

---

## 6. Process vs outcome

| | Good process | Bad process |
|---|---|---|
| **Win** | Deserved; reinforce | Lucky; do NOT reinforce |
| **Loss** | Acceptable; the cost of a positive-expectancy method | Fix it |

The dangerous cell is **bad process + win**, because it teaches the wrong lesson. This is why you grade the
decision, not the outcome, at review time.

---

## 7. Metrics that reveal process failure

| Metric | Signal |
|--------|--------|
| Average loss R > 1.2 | Stops being widened, or gaps |
| Win rate far above the method's baseline | Taking only "sure" trades — or cutting winners early |
| Average win R < 1.0 | Exiting early (disposition effect) |
| Trade count rising after losses | Revenge trading |
| Size variance across similar setups | Inconsistent sizing |
| Rule-breach rate > 10% | Process failure, not market conditions |
| Notional creep | Overconfidence |

---

## 8. Beginner summary (Hinglish)

**Journal kyun?** Kyunki insaan ki yaaddaasht apne fayde mein jhooth bolti hai — jeet yaad rehti hai, haar bhool
jaati hai. Likhne se yeh band ho jata hai.

**Har trade mein likho:** kya setup, kyun liya, entry, stop, targets, size, invalidation, aur **result R mein**.

**Sabse zaroori rule:** hypothesis **pehle** likho, baad mein **kabhi edit mat karo**. Review alag entry mein.

**Weekly review mein har loss ko classify karo:**
- (a) rule follow kiya, par thesis galat → normal business
- (b) rule toda → **yeh asli problem hai**
- (c) gap/news → size se manage karo

**Sirf (b) fix karo.** Aur ek hafte mein **ek** process rule badlo, paanch nahi.

**Sabse khatarnak:** galat process + profit. Woh aapko galat cheez sikha deta hai.

## 9. Exercise

Create a journal file (`journal/YYYY/MM/DD/`) using `templates/prediction-record.md`. Record five analyses with
full evidence and invalidation **before** checking outcomes. Then evaluate them a week later without editing the
originals. Write one sentence about what the immutable record showed that your memory would have hidden.

---
*See also: [`losses-and-tilt.md`](losses-and-tilt.md) · [`../../templates/prediction-record.md`](../../templates/prediction-record.md) ·
[`../../engines/prediction-tracking/README.md`](../../engines/prediction-tracking/README.md)*
