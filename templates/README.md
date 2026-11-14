# Templates

Copy-paste artefacts. Every template is a **structure**, not content: the fields are mandatory, the values are
yours.

| Template | Use | Used by |
|----------|-----|---------|
| [`analysis-report.md`](analysis-report.md) | The 10-section analysis report | `workflows/screenshot-analysis.md` |
| [`paper-trade-report.md`](paper-trade-report.md) | A hypothetical trade plan | `workflows/paper-trading.md` |
| [`prediction-record.md`](prediction-record.md) | The immutable prediction log entry | `engines/prediction-tracking/` |
| [`trade-journal.md`](trade-journal.md) | A real trade's journal entry | `knowledge/trading-psychology/discipline-and-journaling.md` |
| [`watchlist.md`](watchlist.md) | A weekly level map | `strategies/swing/` |
| [`backtest-report.md`](backtest-report.md) | A backtest disclosure sheet | `engines/backtesting/` |

## House rules for all templates

1. **No section may be deleted.** If a section does not apply, write "not applicable" and why. A missing section is
   indistinguishable from an overlooked one.
2. **`unknown` is a valid value.** Blank is not.
3. **Every number carries its source** (`printed on chart`, `provider:<name>`, `computed`, `user-stated`).
4. **Every plan carries its invalidation.** No exceptions.
5. **Hypothetical language is mandatory** in paper-trading artefacts: "would be", "if", "hypothetical".
