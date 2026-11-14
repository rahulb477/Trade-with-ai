# Engine — Chart Intelligence

**Purpose:** turn an image (or a user's description) into a structured, auditable `ChartObservation`, then into
structure, pattern and trap findings.

**Inputs:** chart screenshot(s) or a text transcription; capability block.
**Outputs:** `ChartObservation`, structure map, candle/pattern findings with status codes, volume assessment,
timeframe table, trap hypotheses.

## Modules

| Module | Function |
|--------|----------|
| `README.md` (this file) | Element inventory, quality scoring, pipeline |
| [`trap-detection.md`](trap-detection.md) | Nine trap types with evidence scoring |

## Pipeline

```
1. Element inventory         -> what is visible, what is not
2. Quality score (0-10)      -> what is permitted downstream
3. Instrument resolution     -> confirm or ask
4. Swing detection (state k) -> structure map
5. Level clustering          -> zones with touch counts
6. Candle pattern audit      -> status codes + rule checks
7. Chart pattern audit       -> state + boundaries + volume
8. Volume assessment         -> relative to 20-bar average
9. Timeframe reconciliation  -> seen vs unknown
10. Trap screening           -> hypotheses with evidence scores
```

## Hard rules

1. **No numeric claim without a source** (axis interpolation counts, but must be marked approximate).
2. **No pattern name without a status code and a rule audit.**
3. **No indicator value that is not printed** on the chart.
4. **No timeframe described that was not shown.**
5. **Unreadable elements are listed**, not guessed.

## Failure modes

| Failure | Handling |
|---------|----------|
| No vision | Request a transcription using the template in `core/capability-detection.md` §4 |
| Quality < 5 | Qualitative structure only; no precise levels |
| Ambiguous ticker | Ask; never guess |
| Non-OHLC chart type (Heikin-Ashi, Renko, line) | Refuse candle-pattern rules; state why |
| Split/bonus discontinuity in the window | Flag as a corporate action; refuse pre/post comparison |

## Output schema (the fields a report must populate)

```
instrument, exchange, last_price, timeframe, chart_type, quality_score,
candles_visible, volume_present, indicators_visible[], drawings_visible[],
unreadable[], absent[],
structure{trend, sequence, swings[], levels[], trendline, range},
candles[{name, status, rules_met[], rules_failed[]}],
chart_patterns[{name, state, boundaries, touches, volume_note}],
volume{panel, relative, climax, divergence},
timeframes[{tf, source, trend, key_level, conflict}],
traps[{type, level, evidence_score, would_confirm}]
```

Any field left empty must be explained in the report's missing-data section.
