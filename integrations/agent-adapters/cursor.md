# Adapter — Cursor

**Environment:** in-editor, repository indexed, image reading, terminal. Best for *building and maintaining* this
repository rather than for live chart analysis during a session.

## Setup

Add the block below to `.cursorrules` (or the project rules panel).

## System block

```
CONTEXT
This repository is an AI trading-analysis skill. Markdown is the specification; Python is the tested
implementation of the calculations. Code must not claim more than the docs, and docs must not promise
code that does not exist.

WHEN WRITING CODE
- Python standard library only. No third-party dependencies. No network calls in library code.
- Every new function needs a test in tests/, and the test must run with:
  python3 -m unittest discover -s tests -t . -v
- Undefined values are None, never 0 and never a guess.
- Docstrings state the convention used (e.g. "Wilder smoothing", "population standard deviation").
- Never remove a validation check to make a test pass. Fix the expectation or the code.

WHEN WRITING DOCS
- No placeholders, no "TODO", no lorem text.
- Internal links must be relative and must resolve (python3 scripts/check_links.py).
- Every claim about a capability must match an actual file (python3 scripts/audit_repo.py).
- Never describe a feature as complete because its file exists.

WHEN ANALYSING A CHART (if asked)
- Follow workflows/screenshot-analysis.md; use the closed verdict vocabulary.
- Never fabricate prices, indicators, or news.
```

## Cursor-specific workflows

| Task | Approach |
|------|----------|
| Add an indicator | Edit `indicators.py`, add `tests/indicators/test_<name>.py`, add `knowledge/indicators/<name>.md`, update `SKILL.md` §4 if needed |
| Fix a broken link | Run `check_links.py`, then edit — do not rename targets to dodge the check |
| Add a knowledge page | Follow the house structure of a sibling file; add the routing entry |
| Audit before a commit | `check_links.py` + `audit_repo.py` + the test suite |

## Inline-edit cautions

| Caution | Why it matters here |
|---------|---------------------|
| Accepting a "clever" refactor of indicator maths | Numerical behaviour must stay identical; tests catch it |
| Letting the model invent a file path | Common failure; the link checker catches it |
| Auto-importing a library | Breaks the zero-dependency guarantee |
| Rewriting a whole file to change one paragraph | Loses hand-written nuance |

## Definition of done for a code change in this repo

1. Function implemented, `None`-safe, documented convention.
2. Test added and passing.
3. Docstring matches behaviour.
4. Related Markdown mentions the function accurately (or does not mention it).
5. `check_links.py` and `audit_repo.py` clean.
