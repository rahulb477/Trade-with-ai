# Agent Adapters

The same skill, expressed for eight agent environments.

| File | For |
|------|-----|
| [`claude-code.md`](claude-code.md) | Claude Code (filesystem + terminal) |
| [`codex.md`](codex.md) | OpenAI Codex-style coding agents |
| [`chatgpt.md`](chatgpt.md) | ChatGPT with browsing and code interpreter |
| [`gemini-cli.md`](gemini-cli.md) | Gemini CLI |
| [`cursor.md`](cursor.md) | Cursor (in-editor) |
| [`windsurf.md`](windsurf.md) | Windsurf |
| [`arena.md`](arena.md) | Arena Agent Mode (workspace + shell + vision) |
| [`generic.md`](generic.md) | Any agent: the minimal contract |

## The portable core

Every adapter carries the same five things:

1. **The role statement** — analyst and educator, never an advisor or executor.
2. **The routing table** — `SKILL.md` §4 maps a question to the files to load.
3. **The output contract** — the 10-section report and the closed verdict vocabulary.
4. **The prohibition list** — no fabricated data, no execution, no personalised advice.
5. **The degradation ladder** — what to do without vision, web, files, or code execution.

Adapters differ only in *how* they load files, call tools, and persist output.

## Capability matrix

| Capability | Claude Code | Codex | ChatGPT | Gemini CLI | Cursor | Windsurf | Arena | Generic |
|-----------|------------|-------|---------|-----------|--------|----------|-------|---------|
| Read repo files | ✅ | ✅ | ⚠️ uploads | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| See images | ✅ | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ⚠️ |
| Browse web | ⚠️ tools | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ✅ tools | ❌ |
| Execute code | ✅ | ✅ | ✅ (interpreter) | ✅ | ⚠️ | ⚠️ | ✅ | ❌ |
| Persist files | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Long context | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ⚠️ |

✅ reliable · ⚠️ depends on configuration · ❌ unavailable

**No adapter may claim a capability it does not have.** The matrix exists so the agent declares its mode instead of
silently degrading into confident guessing.

## Installing an adapter

There is nothing to compile and no package to install. Copy the repository, then point your agent at the adapter
file (or paste its contents into the system prompt / rules file). Each adapter is self-contained.
