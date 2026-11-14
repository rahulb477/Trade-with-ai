# Journal

Where prediction records and trade journals live.

**This directory is gitignored except for this file.** Your predictions, screenshots, and notes are personal. If you
want them versioned, use a private repository and remove the `journal/**` rule from `.gitignore`.

## Layout

```
journal/
├── README.md                    this file (the only tracked file)
├── 2026/
│   └── 11/
│       └── 14/
│           ├── RELIANCE-20261114-1531-a3f9c2.md     prediction record
│           └── PT-20261114-01.md                    paper-trade plan
└── img/
    └── 2026-11-14-reliance-1d.png                   screenshot referenced by the record
```

## Which template?

| You are writing | Template |
|-----------------|----------|
| A hypothesis before any outcome | `../templates/prediction-record.md` |
| A plan for a hypothetical trade | `../templates/paper-trade-report.md` |
| A record of an actual (or paper) execution | `../templates/trade-journal.md` |
| A weekly level map | `../templates/watchlist.md` |
| A backtest disclosure | `../templates/backtest-report.md` |

## The three rules

1. **Write the hypothesis before the outcome.** If you write it after, mark it `retrospective: true` and exclude it
   from statistics.
2. **Append only.** The immutable block is never edited. Corrections go in a new, timestamped evaluation block.
3. **Never delete a failure.** Deleting losses destroys the only evidence that could improve the process.

## What to review, and how often

| Cadence | Action |
|---------|--------|
| Daily (5 min) | Fill the review block while it is still honest |
| Weekly (30 min) | Process grades, rule breaks, circuit-breaker review |
| Monthly (1 hr) | `../engines/self-evaluation/README.md` — error taxonomy and calibration |

The monthly review is where the value is. A journal that is never reviewed is a diary; a journal that is reviewed
with the error taxonomy becomes a feedback loop.

## Privacy

Assume a journal entry could be read by someone else: it may contain your account size, your losses, and your
emotional state. Do not commit it to a public repository, and redact account figures if you share an extract.
