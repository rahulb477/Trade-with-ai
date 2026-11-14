# Adapter — OpenAI Codex-style Agents

**Environment:** repository read/write, shell, patch application. Image support varies.

## Setup

Point the agent at the repository. Add the block below as its instructions.

## System block

```
You are working inside a trading-analysis skill repository. Treat it as the single source of truth.

TASK CLASSIFICATION (do this first)
- Knowledge question -> load the matching knowledge/ file; answer in 300-600 words; no verdict.
- Chart analysis     -> follow workflows/screenshot-analysis.md, all 16 stages.
- Trade plan         -> follow workflows/paper-trading.md, all 10 checklist boxes.
- Code task          -> modify integrations/python/trading_intel/ and add tests.

HARD RULES
1. SKILL.md §4 is the routing contract. Do not answer a question from general knowledge when a file covers it.
2. Never fabricate: prices, indicator values, volumes, news, dates, statistics, backtest results, tool outputs.
3. Verdicts come only from: BULLISH SCENARIO | BEARISH SCENARIO | WAIT — NO CONFIRMED SETUP |
   NO-TRADE | INSUFFICIENT DATA — NO VALID SETUP.
4. Every scenario needs a trigger, an invalidation, and arithmetic that is shown.
5. If vision is unavailable, request a transcription (core/capability-detection.md §4).
6. Never claim a file was read if it was not. Never claim a test passed without running it.
7. No broker integration, no real orders, no personalised investment advice.

CODE STANDARDS
- Python standard library only. No numpy, no pandas, no network calls in library code.
- Add a test for every behaviour change. Run: python3 -m unittest discover -s tests -t . -v
- Update the relevant docs in the same change; a code change that outruns its docs is a defect.
```

## Working pattern

```bash
# 1. Orient
sed -n '1,120p' SKILL.md
# 2. Load only what the task needs
# 3. Change code + tests together
python3 -m unittest discover -s tests -t . -v
# 4. Check links and structure
python3 scripts/check_links.py
python3 scripts/audit_repo.py
```

## Codex-specific cautions

| Caution | Reason |
|---------|--------|
| Don't let it "improve" indicator formulas without tests | Silent behaviour changes in trading maths are dangerous |
| Don't accept optimistic backtest output | Ask for the caveats field |
| Keep commits scoped | One behaviour change per change |
| Watch for invented file paths | The repo's own `check_links.py` catches them |

## Output contract for analysis tasks

Use `templates/analysis-report.md`. In this environment you can write the report to a file — do that when the user
wants a record, and print it inline when they just want an answer.
