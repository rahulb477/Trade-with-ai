# Agent Compatibility

## 1. The portability contract

Any agent can run this skill if it can do three things:

1. **Read text files** (or be given their contents).
2. **Follow a routing table** (`SKILL.md` §4).
3. **Produce the output contract** (10 sections, closed verdict vocabulary).

Everything else is an optimisation. Vision, browsing, and code execution each *raise the ceiling*; none is required.

## 2. Capability matrix

| Capability | Claude Code | Codex | ChatGPT | Gemini CLI | Cursor | Windsurf | Arena | Generic chat |
|-----------|------------|-------|---------|-----------|--------|----------|-------|--------------|
| Read repo files | ✅ | ✅ | ⚠️ uploads | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| Read images | ✅ | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ⚠️ |
| Web access | ⚠️ | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ✅ tools | ❌ |
| Code execution | ✅ | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | ✅ | ❌ |
| Persist output | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Long context | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ⚠️ |

✅ reliable · ⚠️ configuration-dependent · ❌ unavailable

**This table describes typical configurations, not guarantees.** Verify in your own environment before relying on a
capability — and never let an agent claim one it has not demonstrated.

## 3. What changes per environment

| Environment | Best for | Main limitation | Adapter |
|-------------|----------|-----------------|---------|
| Claude Code | chart analysis + recording | needs the repo locally | `../integrations/agent-adapters/claude-code.md` |
| Codex | maintaining the repository | vision varies | `../integrations/agent-adapters/codex.md` |
| ChatGPT | image-first analysis | no durable repo access | `../integrations/agent-adapters/chatgpt.md` |
| Gemini CLI | bulk reading, long context | vision varies | `../integrations/agent-adapters/gemini-cli.md` |
| Cursor | editing knowledge and code | not a research environment | `../integrations/agent-adapters/cursor.md` |
| Windsurf | multi-step pipelines | cascade drift | `../integrations/agent-adapters/windsurf.md` |
| Arena Agent Mode | workspace repo + shell + vision in one hosted chat | no live data provider ships; memory must not substitute for tools | `../integrations/agent-adapters/arena.md` |
| Generic | anything | no tools at all | `../integrations/agent-adapters/generic.md` |

## 4. Degradation behaviour (normative)

| Missing capability | Required behaviour |
|--------------------|--------------------|
| Vision | Request the transcription template. Never guess OHLC from a description. |
| Files | Use the built-in summaries in `generic.md`; declare reduced depth. |
| Web | Include the standard "web research unavailable" paragraph. |
| Code execution | Show arithmetic step by step, labelled "computed by hand". |
| Persistence | Print the record inline, labelled `NOT SAVED`. |

These are not suggestions. Silent degradation — pretending to have a capability — is the failure mode the whole
repository is built to prevent.

## 5. Output contract (identical everywhere)

```
1  Data & provenance
2  Chart quality score
3  Element inventory
4  Market structure & level map
5  Candle / chart pattern findings (with status codes)
6  Indicator readings (with sources)
7  Volume & participation
8  Three scenarios (bullish / bearish / no-trade)
9  Verdict + confidence + risk arithmetic
10 Limitations & missing data
+  Hinglish beginner explanation
```

Verdict vocabulary, closed: `BULLISH SCENARIO` · `BEARISH SCENARIO` · `WAIT — NO CONFIRMED SETUP` · `NO-TRADE` ·
`INSUFFICIENT DATA — NO VALID SETUP`.

Pattern status vocabulary, closed: `CONFIRMED` · `DEVELOPING` · `POSSIBLE` · `UNCLEAR`.

## 6. Context budget

| Approach | Files | When |
|----------|-------|------|
| Minimal | 3 | `SKILL.md`, `core/decision-engine.md`, `templates/analysis-report.md` |
| Standard | 5–6 | add the workflow + one or two knowledge files |
| Full chart analysis | 6–8 | add pattern and indicator references |

Eight is the ceiling. Beyond that, context is being consumed by documents that do not change the answer.

## 7. Verifying an agent is actually following the skill

Ask these five questions. A compliant agent answers all of them:

1. "Which files did you read for this analysis?" — must name real files.
2. "What is your data mode?" — must be one of the four.
3. "What was the chart quality score and what does it permit?" — must state the consequence.
4. "Which gate failed, if any?" — must name it when the verdict is `WAIT`.
5. "Which claims are assumptions rather than observations?" — must list them.

An agent that cannot answer these is generating plausible text, not performing an analysis.

## 8. Interoperability notes

| Concern | Detail |
|---------|--------|
| File encoding | UTF-8. Some files contain `—`, `≥`, `→`, `₹`; agents with ASCII-only pipelines may mangle them |
| Line endings | LF |
| Markdown dialect | CommonMark + tables (GitHub-flavoured) |
| Mermaid diagrams | One block in `core/system-architecture.md`; degrade gracefully if unsupported |
| Python version | 3.9+ (uses `from __future__ import annotations`, `dict | None`-free syntax) |
| Non-ASCII in code | All docstrings ASCII except a few symbols in comments; safe on any locale |

## 9. Not supported, by design

| Environment | Status |
|-------------|--------|
| Autonomous trading bots | Out of scope; no execution path exists |
| Broker platforms with embedded AI | Out of scope |
| Spreadsheet plugins | Not provided; the arithmetic is documented and reproducible |
| Voice assistants | Output too long for the medium |

## 10. Adding an environment

1. Copy `generic.md`.
2. Document its capability matrix row honestly.
3. Specify how it loads files and persists output.
4. Keep the five portable elements unchanged: role, routing, output contract, prohibitions, degradation.
5. Test it: ask the five verification questions in §7.
