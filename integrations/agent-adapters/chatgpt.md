# Adapter — ChatGPT (Web + Code Interpreter)

**Environment:** strong image reading, browsing, code interpreter with file persistence per conversation.

## Setup

Upload (or paste) `SKILL.md` and the two or three files a session needs. ChatGPT has no durable repository access,
so **context management is the main limitation** and this adapter is built around it.

## System block

```
You are a trading analyst and educator. You are given parts of a larger knowledge repository.

BECAUSE YOU MAY NOT HAVE THE WHOLE REPOSITORY
1. State which files you actually have at the start of an analysis.
2. Never pretend to cite a file you were not given. If a rule lives in a file you do not have, say so.
3. If browsing is unavailable for this conversation, include the standard "web research unavailable" paragraph.
4. If you cannot run code, do the arithmetic step by step in the message and say it was done by hand.

RULES
1. Never invent prices, indicator values, volumes, news, or statistics.
2. Verdict vocabulary: BULLISH SCENARIO | BEARISH SCENARIO | WAIT — NO CONFIRMED SETUP |
   NO-TRADE | INSUFFICIENT DATA — NO VALID SETUP.
3. Every plan: trigger, invalidation, T1/T2/T3, R:R, computed arithmetic.
4. 10-section report from templates/analysis-report.md, including the Hinglish beginner section.
5. Educational only. No personalised investment advice. No execution.
```

## Minimum viable upload set

If the user can only upload three files:

| Rank | File | Why |
|------|------|-----|
| 1 | `SKILL.md` | routing + rules + output contract |
| 2 | `core/decision-engine.md` | the gate ladder and verdict vocabulary |
| 3 | `templates/analysis-report.md` | the output shape |

For chart work add `workflows/screenshot-analysis.md`. For a plan add `workflows/paper-trading.md` and
`knowledge/risk-management/position-sizing.md`.

## Using the code interpreter well

```python
# Paste the library into the session, then compute — do not estimate
# (upload integrations/python/trading_intel as a folder, or a zip)
import sys; sys.path.insert(0, "integrations/python")
from trading_intel import indicators, risk, sizing

atr = indicators.atr(highs, lows, closes)
plan = risk.TradePlan("long", entry, stop, [t1, t2, t3])
print(plan.summary(), plan.validation_warnings())
```

If the interpreter is unavailable, show the arithmetic explicitly:

```
risk per unit = |1256 − 1228| = 28
R_T1          = (1300 − 1256) / 28 = 1.57
```

Manual arithmetic that is *shown* is acceptable. Arithmetic that is *asserted* is not.

## ChatGPT-specific cautions

| Caution | Guard |
|---------|-------|
| Long conversations drift from the rules | Re-paste the rules block every ~10 turns |
| It may "remember" a rule it does not have | Ask it to quote the file |
| Browsing results can be stale | Demand publication timestamps |
| It may summarise a paywalled article | Ask explicitly: "did you read the full text?" |
| Images get compressed | Ask for a re-upload if the axis is unreadable |

## Session start template

> "Attached: SKILL.md, core/decision-engine.md, templates/analysis-report.md, and a daily chart of X.
> Please confirm the files you received, state your data mode, then analyse."
