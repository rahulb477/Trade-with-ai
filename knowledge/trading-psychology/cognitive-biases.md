# Cognitive Biases in Market Analysis

Each entry: what the bias is, how it shows up in charts, and the specific procedural countermeasure.

---

## 1. Confirmation bias
**What:** Seeking and weighting evidence that supports an existing view.

**In charts:** Drawing the trendline to fit the conclusion. Noticing the bullish divergence but not the bearish
volume. Reading an ambiguous candle as the pattern you already wanted.

**Countermeasure (built into this repo):** section 8 of the report format has a mandatory **"conflicting
evidence"** field. If the field is empty, the analysis is incomplete. `core/decision-engine.md` §4 counts
*independent* evidence classes, which exposes when five bullets are one fact.

---

## 2. Hindsight bias
**What:** "I knew that would happen."

**In charts:** Remembering a call as correct when it was conditional. Forgetting that the same setup also failed
three other times.

**Countermeasure:** append-only prediction records (`engines/prediction-tracking/`). Written *before* the outcome,
never edited after. The only defence against a memory that flatters you.

---

## 3. Recency bias
**What:** Overweighting recent events.

**In charts:** "The last three breakouts failed, so breakouts don't work." Three is not evidence. Or the reverse:
"the last three worked, so this one will."

**Countermeasure:** report sample sizes. A claim from n=3 is labelled as such or omitted.

---

## 4. Anchoring
**What:** Fixing on an initial number and adjusting insufficiently.

**In charts:** Anchoring to your entry price — "it will come back to my entry". Anchoring to a round number, or to
the price you first saw the stock at. Anchoring to the analyst's target.

**Countermeasure:** define invalidation **before** entry, structurally. Never move a stop. Judge the position by
"would I enter here now?" not by the entry price.

---

## 5. Loss aversion / disposition effect
**What:** Feeling losses roughly twice as strongly as equivalent gains; hence holding losers too long and cutting
winners too early.

**In charts:** Moving a stop further away. Taking a 0.5R profit and then watching the 3R move happen.

**Countermeasure:** pre-committed exits. Partial scale-out rules written in advance. R-quantified targets so that
"small profit" is not a feeling but a number.

---

## 6. Overconfidence and the illusion of control
**What:** Overestimating skill after a run of wins; believing more analysis gives more control.

**In charts:** Size creep. Adding indicators. Trading more instruments. Dropping the checklist.

**Countermeasure:** a fixed risk budget per idea and per day, regardless of recent results. Circuit breakers act
on *streaks*, not on feelings (`losses-and-tilt.md`).

---

## 7. Availability heuristic
**What:** Judging probability by how easily examples come to mind.

**In charts:** "Breakouts always fail" (because you remember two painful ones). "This pattern is famous so it must
work."

**Countermeasure:** measured base rates, or an explicit "no measured base rate" statement. Never a remembered
statistic.

---

## 8. Narrative fallacy
**What:** Preferring a coherent story over incomplete data.

**In charts:** "Smart money is accumulating here." "The market is waiting for the RBI." These feel explanatory but
are unfalsifiable.

**Countermeasure:** `knowledge/smart-money/README.md` §0. Describe behaviour; state what would prove the reading
wrong; never assert intent.

---

## 9. Sunken-cost / commitment
**What:** Letting past effort or losses drive current decisions.

**In charts:** "I've held this for six weeks, I can't sell now." Averaging down.

**Countermeasure:** evaluate every position as if it were new. "Would I open this at the current price with the
current evidence?" If no, close it.

---

## 10. Survivorship in memory
**What:** Remembering the trades that "proved" your method and forgetting the rest.

**Countermeasure:** the journal is mandatory, not optional (`discipline-and-journaling.md`). Unrecorded trades
cannot be evaluated, which means the memory gets to lie.

---

## 11. Multiple-testing bias at the personal level
**What:** Trying variations until something "works", then believing that variant is real.

**Countermeasure:** pre-register the rule and the parameters. Record how many variants you tried. Use a holdout
once.

---

## 12. Authority bias
**What:** Accepting a claim because of the speaker, including an AI.

**Countermeasure:** every factual claim in this repository must be traceable (`core/evidence-engine.md`). If a claim
has no ledger entry, ask for one. This applies to the repository's own outputs.

---

## Bias-to-countermeasure summary

| Bias | Procedure that counters it |
|------|---------------------------|
| Confirmation | Mandatory conflicting-evidence field |
| Hindsight | Append-only prediction records |
| Recency | Sample-size reporting |
| Anchoring | Pre-defined structural invalidation |
| Loss aversion | Pre-committed partial exits in R |
| Overconfidence | Fixed risk budget; streak-based breakers |
| Availability | Measured base rates or explicit "unknown" |
| Narrative | Behaviour described, intent never asserted |
| Sunken cost | "Would I open this now?" test |
| Memory survivorship | Mandatory journal |
| Multiple testing | Pre-registration + holdout |
| Authority | Evidence ledger for every claim |

## Beginner summary (Hinglish)

**Confirmation bias:** aap woh dekh rahe ho jo aap dekhna chahte ho. **Fix:** har analysis mein "against" wali
baat likho.

**Hindsight:** "mujhe pata tha". **Fix:** prediction pehle likho, baad mein mat badlo.

**Recency:** teen trades se rule decide karna. **Fix:** sample size likho — 3 kuch prove nahi karta.

**Anchoring:** apni entry price se chipke rehna. **Fix:** stop pehle hi define karo, baad mein hilana mat.

**Loss aversion:** loss jaldi book nahi karna, profit jaldi le lena. **Fix:** exits pehle likho.

**Narrative:** "smart money kar raha hai" wali kahani. **Fix:** behaviour describe karo, intent mat batao.

**Sabse asaan rule:** agar aap likh nahi sakte ki aapka analysis **galat kaise sabit hoga**, to woh analysis nahi,
opinion hai.

## Exercise

Review your last five analyses. For each, answer: (1) did I list conflicting evidence? (2) did I state an
invalidation? (3) did I use a statistic I could not source? (4) did I describe intent I cannot verify? Count your
hits. That count is your bias score — track it monthly.

---
*See also: [`discipline-and-journaling.md`](discipline-and-journaling.md) · [`../core/evidence-engine.md`](../../core/evidence-engine.md)*
