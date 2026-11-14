# Adapter — Arena Agent Mode

**Environment:** hosted agent sandbox with the repository cloned at the workspace root. Shell, filesystem
read/write, image input, web search/fetch, and Python 3 are available; persistence is available but
`journal/**` is git-ignored, so personal records stay local unless the user asks for them to be committed.

## Setup

There is no install step and no package to fetch.

1. Open a chat with this repository attached as the workspace (clone it, or import the repository into the
   session).
2. Keep `SKILL.md` at the repository root. It is the entry point the agent must read before answering any
   chart, market, or trading question.
3. Attach a chart screenshot directly in the message. It arrives as an image the agent can see, not as an
   OCR transcript.
4. State the mode you want (LEARNING / RESEARCH / PAPER-TRADING). If you do not, the agent defaults to
   LEARNING and asks one clarifying question.

Verified in this environment on 2026-11-14:

```
305 tests passing        python3 -m unittest discover -s tests -t .
links: 0 broken          python3 scripts/check_links.py      (212 files, 536 links)
audit: PASS              python3 scripts/audit_repo.py
python: 3.11.2, stdlib only — no pip install needed
```

## System block (keep short; it points at the repository)

```
This workspace is the AI Trading Intelligence skill. Before answering any trading, chart, or market
question, read SKILL.md and AGENTS.md, then follow SKILL.md §4 routing (max 8 files per request).

1. Never invent prices, indicator values, volume, news, statistics, or tool results. If it is not in a
   file, a screenshot, or a tool result, it does not exist.
2. Emit the report from templates/analysis-report.md. The verdict is exactly one of: BULLISH SCENARIO |
   BEARISH SCENARIO | WAIT — NO CONFIRMED SETUP | NO-TRADE | INSUFFICIENT DATA — NO VALID SETUP.
3. Every plan carries an invalidation before any target. No invalidation, no plan.
4. Compute with integrations/python/trading_intel and show the call, not hand arithmetic.
5. End with the Hinglish beginner section.
6. No broker connection, no order generation, no personalised investment advice.
7. Declare your capability block and your data mode in section 10 of the report.
```

## Recommended workflow in this environment

```
1. Read SKILL.md, then AGENTS.md                        # rules + mechanical loading order
2. Run core/capability-detection.md probes             # vision, files, web, code, persistence
3. Read templates/analysis-report.md                   # the output shell
4. python3 -c "import sys; sys.path.insert(0,'integrations/python'); ..."   # compute, never estimate
5. Write the report in chat; offer the prediction record before writing journal/
6. python3 -m unittest discover -s tests -t .           # only if library code was changed
```

## Arena specifics

| Feature | How to use it | Guard |
|---------|---------------|-------|
| Shell tool | `python3`, `git`, `rg`, repository scripts | One-shot commands only; do not leave servers running for analysis |
| Image input | Attach the screenshot in the message | Score quality before interpreting; a downscaled image permits qualitative output only |
| Web search / fetch | Cite publisher, timestamp, URL in section 6 | No result → `web_research: unavailable`; never fill the gap with memory |
| Persistence | Write reports and records under `journal/` | `journal/**` is git-ignored — say `NOT SAVED` if the user expects a committed file |
| Snapshots | Workspace files persist between turns | Never rewrite a recorded hypothesis; add an evaluation entry |
| Long context | The repository is ~1 MB of Markdown | Load on demand; the whole base will crowd out the reasoning it is meant to support |

## Failure modes in this environment

| Failure | Guard |
|---------|-------|
| Trusting training memory for a price or a headline | Only tool output and attached images count as data |
| Claiming live market data because the shell works | There is no provider adapter; offline knowledge is the default mode |
| Treating a sandbox date as the data date | Read the timestamp printed on the chart, and label freshness |
| Over-eager repository edits while "analysing" | Analysis is read-only unless the user asks for a change |
| Silent degradation of vision or web | Print the capability block in section 10 |

## Verifying the skill is actually active

Use the five questions from [`../../docs/agent-compatibility.md`](../../docs/agent-compatibility.md) §7.
A compliant agent in this environment answers:

1. **Which files did you read?** — `SKILL.md`, `AGENTS.md`, `templates/analysis-report.md`, plus the routed
   knowledge modules, by path.
2. **What is your data mode?** — one of offline / web research / market-data integration / full research.
3. **What was the chart quality score, and what does it permit?** — the score out of 10 and its consequence.
4. **Which gate failed?** — named when the verdict is `WAIT — NO CONFIRMED SETUP` or `NO-TRADE`.
5. **Which claims are assumptions?** — every `ASSUMED` default period, approximate level, and inferred market.

An agent that cannot answer these is producing plausible text, not an analysis.
