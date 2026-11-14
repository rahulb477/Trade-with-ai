# Usage Guide

## 1. Pick the mode first

| You want | Mode | What you get |
|----------|------|--------------|
| To understand something | **LEARNING** | explanation, examples, exercises — no verdict |
| To analyse a chart | **RESEARCH** | full report with evidence and a verdict |
| To practise | **PAPER-TRADING** | hypothetical plan with arithmetic, no money |

Never mix them silently. If a user in LEARNING mode asks "so should I buy?", the honest answer is: "that is out of
scope for this mode — here is how to think about it" plus, if they insist, a RESEARCH-mode analysis with its full
disclosures.

## 2. The four data modes

| Mode | Requires | Ceiling on confidence |
|------|----------|----------------------|
| Offline knowledge | nothing | Weak (methodology only) |
| Web research | a browsing tool | Moderate (context cited, no computed indicators) |
| Market-data integration | provider credentials | Moderate–Strong (computed values with provenance) |
| Full research | both | Strong (subject to the gate ladder) |

State the mode at the top of every report. An analysis that silently degrades is worse than one that declares it.

## 3. Common requests and what happens

### "What is this pattern?" (LEARNING)

Load the pattern file, apply the 5-part lesson structure, show the confusable patterns, and state what the pattern
does *not* claim.

```
You:    What is a bullish engulfing?
Output: definition → simple version → technical rules → chart example → mistakes + a drill
        (no verdict, because no chart was supplied)
```

### "Analyse this chart" (RESEARCH)

The 16-stage pipeline. Expect to wait: stages 1–4 are transcription, and they come before any interpretation.

```
You:    [screenshot]
Output: 10-section report, quality score first, three scenarios, one verdict
```

### "Should I buy this?" (RESEARCH, red-flag request)

The skill will not answer yes/no. It will produce scenarios and a verdict, and refuse to give advice.

```
Correct output:  "I cannot advise you. Here is the analysis: the bullish scenario requires X,
                  the invalidation is Y, R:R to T1 is Z. Verdict: WAIT."
Incorrect:       "Yes, buy at 1250 with a stop at 1228."
```

### "Give me a trade plan" (PAPER-TRADING)

The 10-box checklist runs first. If any box fails, the output is `WAIT` with the failing box named.

```
Output: checklist → plan → explicit arithmetic → trap audit → scenarios → disclosure
```

### "Backtest this strategy for me" (RESEARCH)

You will get: a mechanical definition, the data requirements, the execution assumptions, the results *with* CIs, a
bias audit, and an explicit statement of what the backtest cannot tell you. If the data is unavailable, you will get
the specification and an honest "not run".

### "Is this stock a good long-term investment?" (out of scope)

Personalised investment advice is out of scope. The skill can explain valuation concepts, list the questions a
fundamental analysis must answer, and describe how to verify figures — but it will not tell you to buy.

## 4. Reading the output: what to look at first

Most readers start at the verdict. Professionals read in this order:

1. **Quality score and data mode** — can the rest be trusted?
2. **Missing data** — what is the analysis blind to?
3. **Level map** — is the trade at a level or in the middle of nowhere?
4. **R:R arithmetic** — does it pay?
5. **Conflicting evidence** — what argues against?
6. **Verdict** — last, because it is a conclusion.

## 5. Using the Hinglish section

The `EXPLAIN LIKE A BEGINNER` section is not a summary of the English; it is a translation of the *reasoning*.

| Rule | Example |
|------|---------|
| Keep English trading terms in English | "stop loss", "R:R", "support" — not "rok-bandi" |
| Keep numbers identical | if the English says 1.57R, Hinglish says 1.57R |
| Name the invalidation every time | "1,228 ke neeche close = idea cancel" |
| Never promise a direction | not "pakka upar jayega" |

Full rules: `../knowledge/education/hinglish-explanations.md`.

## 6. Recording an analysis

```
1. Copy templates/prediction-record.md
2. Fill the immutable block BEFORE you learn the outcome
3. Save to journal/YYYY/MM/DD/<analysis_id>.md
4. Later, append the evaluation block with its own timestamp
5. Never edit the immutable block
```

The record is what makes accuracy measurable. Without it, the track record is memory, and memory is the least
reliable narrator in trading.

## 7. Working with an agent that lacks capabilities

| Missing | Ask the agent for | Then |
|---------|------------------|------|
| Vision | the transcription template | paste the filled template |
| Files | the built-in summaries | accept reduced depth, stated explicitly |
| Web | nothing — expect the standard paragraph | analyse technically |
| Code execution | step-by-step arithmetic | check the arithmetic yourself |

An agent that claims a capability it lacks is the failure mode this repository exists to prevent. When in doubt, ask
it: "which files did you actually read, and which tools did you actually call?"

## 8. Practical workflow for a beginner, week 1

```
Day 1   Read README + knowledge/education/concept-lessons.md lessons 1-3
Day 2   Read knowledge/candlesticks/README.md (the confirmation hierarchy)
Day 3   Analyse 3 charts in LEARNING mode; no plans
Day 4   Read knowledge/risk-management/position-sizing.md; compute sizes by hand
Day 5   Read workflows/paper-trading.md; write 2 paper plans; take none
Day 6   Read knowledge/trading-psychology/losses-and-tilt.md; write your circuit breakers
Day 7   Review: how many plans would have triggered? Record them with prediction-logging
```

No money in week 1. The goal is to find out whether the process is followable, not whether it is profitable.

## 9. Anti-patterns to avoid

| Anti-pattern | Why it fails |
|--------------|--------------|
| Asking for a verdict on a 3/10 screenshot | The honest answer is `INSUFFICIENT DATA` |
| Requesting a plan and then negotiating the stop | The stop is the invalidation; moving it deletes the thesis |
| Using LEARNING mode to sneak in a recommendation | The mode exists precisely to separate the two |
| Collecting 20 indicators | Family redundancy, not evidence |
| Skipping the prediction record | Makes every future claim unfalsifiable |
| Treating `WAIT` as a failed analysis | It is often the correct output |

## 10. Getting the best out of it

1. **Give context you actually have**: instrument, timeframe, market, and any known events.
2. **Ask "why"**: the reasoning is the product; the verdict is a side effect.
3. **Challenge the evidence**: "which of these claims came from the chart and which are assumptions?"
4. **Ask for the failing gate** when the verdict is `WAIT` — that is where the learning is.
5. **Keep records** and review them monthly with `../engines/self-evaluation/README.md`.
