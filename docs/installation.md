# Installation

## 1. TL;DR

**There is nothing to install.** Clone or copy the repository, point your agent at it, and start using it.

```bash
git clone <repository-url> trade-with-ai
cd trade-with-ai
```

That is the whole install for every supported agent.

## 2. Requirements

| Requirement | Needed for | Notes |
|-------------|-----------|-------|
| Any filesystem access | Reading the knowledge base | Markdown only |
| Python 3.9+ | Running the calculation library and tests | Standard library only — no pip install |
| An image-capable model | Chart analysis from screenshots | Otherwise use a transcription |
| A web tool | Research mode | Optional; the skill works offline |
| Market-data credentials | Computed indicators on live data | Optional; nothing works worse without them |

**No API key is required** at any point. The skill runs in offline knowledge mode with no configuration at all.

## 3. Verify the installation

```bash
python3 -m unittest discover -s tests -t . -v     # 287 tests
python3 scripts/check_links.py                    # internal links
python3 scripts/audit_repo.py                     # structure + placeholder scan
./scripts/run_all_tests.sh                        # all three in sequence
```

Expected: tests OK, every relative link resolves, audit PASS.

## 4. Agent setup by environment

### Claude Code

```bash
cd trade-with-ai
claude
```

`SKILL.md` is read as project instructions. For a single-file setup, copy
`integrations/agent-adapters/claude-code.md` into `CLAUDE.md`.

### Codex-style agents

Point the agent at the repository root; add the block from `integrations/agent-adapters/codex.md` to its
instructions. It can run the verification commands itself.

### ChatGPT

Upload three files: `SKILL.md`, `core/decision-engine.md`, `templates/analysis-report.md`. Add
`workflows/screenshot-analysis.md` for chart work. If the code interpreter is available, upload
`integrations/python/trading_intel/` as well.

### Gemini CLI

```bash
cd trade-with-ai
gemini
```

Add the block from `integrations/agent-adapters/gemini-cli.md` to `GEMINI.md`.

### Cursor / Windsurf

Add the corresponding adapter block to `.cursorrules` / `.windsurfrules`. These environments are best for
maintaining the repository rather than for live chart analysis.

### Anything else

Use `integrations/agent-adapters/generic.md`. It is self-contained: a role statement, the routing summary, the
output contract, the prohibitions, the degradation ladder, and a paste-ready prompt.

## 5. Optional: Python library on the path

```bash
export PYTHONPATH="$PWD/integrations/python:$PYTHONPATH"
python3 -c "
from trading_intel import indicators, risk
print(indicators.rsi([100,101,102,101,103,104,103,105,106,104,106,108,107,109,110,108], 14)[-1])
print(risk.TradePlan('long', 100, 95, [110, 120]).summary())
"
```

Persist it in your shell profile if you use it often.

## 6. Optional: market-data credentials

Only if you want computed indicators on live data. Set **environment variables** — never a file in the repository:

```bash
export TI_MARKET_DATA_PROVIDER="<provider>"
export TI_MARKET_DATA_KEY="<key>"       # never paste this into a chat
python3 -m trading_intel.providers.health
```

The health check reports **which** variables are set, never their values. See
`../data-sources/api-configuration.md`.

> This repository ships no working network adapter. The `Provider` protocol in
> `integrations/python/trading_intel/providers/base.py` is the contract; writing an adapter for your provider is a
> documented extension (`docs/architecture.md` §7).

## 7. Keeping your records out of Git

`journal/` is gitignored by default because it will contain your predictions, screenshots, and possibly licensed
data. To keep records locally while excluding them from the repository:

```bash
ls journal/            # README only after a fresh clone
```

If you *want* to version your journal in a private repository, remove the `journal/` line from `.gitignore` — and
never do that in a public fork.

## 8. Updating

```bash
git pull
./scripts/run_all_tests.sh
```

If tests fail after an update, the repository is inconsistent — report it rather than working around it.

## 9. Uninstalling

Delete the directory. There is no package, no global state, no cache outside the repo (apart from
`TI_CACHE_DIR` if you configured one).

## 10. Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError: trading_intel` | Library not on the path | `export PYTHONPATH="$PWD/integrations/python:$PYTHONPATH"` |
| `Error: module not found` when running tests | Wrong working directory | Run from the repo root with `-t .` |
| Agent says it cannot see images | No vision capability | Ask for the transcription template (`core/capability-detection.md` §4) |
| Agent refuses to give a verdict | Possibly a correct refusal | Check the gate report; `WAIT` is often the right answer |
| `check_links.py` fails | A renamed file broke a link | Fix the link; do not rename the target to dodge the check |
| Tests pass but numbers look odd | Check the units | R-multiples, not currency; ATR in price units, not percent |
