# Contributing

This repository is a **specification with a tested implementation**. Contributions are welcome if they preserve
that relationship. Nothing here is decorative: if a document claims something, either code proves it or the
document says it is unverified.

## 1. The three rules that override everything else

1. **Nothing may be fabricated.** No invented prices, statistics, base rates, quotes, studies, or "research shows".
   If a number cannot be sourced, the honest text is "no verified base rate is known".
2. **Nothing may over-claim.** A file existing is not a feature. Status is earned by evidence, and the status table
   in [`docs/testing-report.md`](docs/testing-report.md) is the record.
3. **No dependencies, no network, no credentials** in library code. Standard-library Python only.

## 2. Definition of done

| Change type | Requirements |
|-------------|--------------|
| New indicator | Function in `indicators.py` + `None`-safe + docstring stating the smoothing convention + tests in `tests/indicators/` + `knowledge/indicators/<name>.md` + routing entry if it is a headline indicator |
| New candle pattern | Detector in `patterns.py` + registration in `DETECTORS` + thresholds documented + tests with hand-built bars (positive and negative cases) + `knowledge/candlesticks/<name>.md` |
| New knowledge page | Same structure as its siblings: definition → simple → technical → example → mistakes → limitations. Relative links that resolve. No borrowed statistics. |
| New market | `markets/<market>/README.md` + session/holiday rules + `markets/README.md` index entry + a "never port rules across markets" statement |
| New adapter | Copy `integrations/agent-adapters/generic.md`; keep the five portable elements; document the capability matrix honestly |
| Code change | Tests added or updated, docs updated in the same change, `scripts/run_all_tests.sh` clean |

## 3. Verification (run before you commit)

```bash
python3 -m unittest discover -s tests -t . -v     # 305 tests
python3 scripts/check_links.py                    # every relative link resolves
python3 scripts/audit_repo.py                     # structure, placeholders, credentials, imports
./scripts/run_all_tests.sh                        # all three
```

A commit that breaks any of these is not ready.

## 4. Writing style

| Do | Don't |
|----|-------|
| State the limitation in the same section as the claim | Bury caveats in a footnote |
| Use "tends to", "is consistent with", "requires confirmation" | Use "will", "always", "guaranteed" |
| Give the arithmetic | Assert the result |
| Name the sample size and period for any statistic | Quote a rate without n |
| Use the fixed vocabulary (verdicts, statuses, provenance classes) | Invent synonyms |
| Prefer a table or a checklist | Long unstructured prose |

## 5. The vocabulary is not yours to change casually

These are contract terms:

- Verdicts: `BULLISH SCENARIO` · `BEARISH SCENARIO` · `WAIT — NO CONFIRMED SETUP` · `NO-TRADE` ·
  `INSUFFICIENT DATA — NO VALID SETUP`
- Pattern statuses: `CONFIRMED` · `DEVELOPING` · `POSSIBLE` · `UNCLEAR`
- Provenance: `chart-observation` · `computed` · `external-cited` · `user-stated` · `assumption`
- Freshness: `LIVE` · `RECENT` · `DELAYED` · `STALE` · `HISTORICAL`

Changing one means changing every template, test, and doc that depends on it — in one commit, with a
`CHANGELOG.md` entry.

## 6. What will be rejected

| Proposed change | Why it is rejected |
|-----------------|--------------------|
| "Add a probability of profit" | Requires assumptions the repository refuses to hide |
| "Add a live broker adapter" | Out of scope; the skill is research-only |
| "Add numpy for speed" | Breaks zero-dependency portability |
| "Remove the WAIT verdict — users find it unhelpful" | It is the most valuable output |
| "Add win rates for patterns" | No verifiable base rate exists; inventing one is fabrication |
| "Add an ML pattern model" | No labelled data, no inter-rater agreement, no out-of-sample work |
| "Soften the limitations section" | The limitations are the product's integrity |
| "Rename files to fix links" | Fix the links instead; the paths are the routing contract |

## 7. Reporting an error

If a formula, threshold, or claim is wrong, open an issue with:

1. The file and line.
2. What it currently says.
3. What it should say, and the source or derivation.
4. Which tests would need to change.

Errors in **arithmetic** get priority over errors in **prose**: a wrong formula propagates into every analysis that
uses it.

## 8. Adding an example

Examples must be labelled `FICTIONAL` at the top and use invented instruments. They exist to demonstrate method, not
to imply market data. Never add a real chart screenshot with real prices to `examples/` — that belongs in a private
journal.

## 9. Licence

Contributions are accepted under the repository's MIT licence. By contributing you confirm you have the right to
submit the material and that it contains no licensed market data.
