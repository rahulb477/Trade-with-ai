# OCR / Chart Transcription Integration

Two paths from an image to structured data, and an honest third.

## Path 1 — Native vision (preferred)

If the host agent can see images, read the chart directly and fill the transcription table in
`workflows/screenshot-analysis.md` §2. No OCR tooling is involved.

Rules:
- Read the axis labels; interpolate only between labelled ticks, and mark interpolated values `approximate`.
- Quote indicator values only where they are printed.
- If a number is illegible, write `unreadable` — never guess from a plausible-looking shape.

## Path 2 — External OCR (optional)

An agent with an OCR tool (or a vision model exposed as a tool) can extract text: ticker, timeframe, axis labels,
indicator legends, any printed values.

| Extractable by OCR | Usually not extractable |
|--------------------|-------------------------|
| Ticker / company name | Candle OHLC values |
| Timeframe label | Indicator readings (unless printed as text) |
| Axis tick labels | Trendlines |
| Indicator legend text (e.g. "RSI(14) 58.4") | Volume bar heights |
| Date range on the axis | Pattern names (never printed) |

**OCR gives you text, not structure.** The pattern analysis still has to be done on the pixels by a vision-capable
model, or on a human transcription.

## Path 3 — Human transcription (always works)

The fallback that must never be skipped when vision is unavailable. Template:

```yaml
instrument:            <ticker or "unknown">
exchange:              <NSE/BSE/NASDAQ/...>
timeframe:             <1D / 15m / ...>
chart_type:            candlestick | OHLC bar | line | heikin-ashi | renko
last_price:            <number or "unknown">
candles_visible:       <approximate count>
volume_present:        true | false
indicators_visible:    [<name(period)>, ...]
quality_observed:
  instrument_identifiable: true|false
  timeframe_visible:       true|false
  price_axis_readable:     true|false
  volume_present:          true|false
  indicators_labeled:      true|false
  candles_clear:           true|false
  axes_not_distorted:      true|false
levels:
  - {price: <n>, kind: support|resistance|both, touches: <n>, approximate: true}
trend:                 up | down | range | unknown
timeframes_seen:       [<...>]
unreadable:            [<...>]
```

Feed this to `trading_intel.observation.from_transcription()` to get a validated object with the quality score and
gate report computed.

## Why guessing is forbidden

An OCR'd or vision-read number that is 2% wrong moves every computed level, changes the R:R, and can flip a `WAIT`
into a `BULLISH SCENARIO`. A mark of `approximate` and a stated axis resolution is what makes the error visible to
the reader.

## Quality scoring

```
instrument_identifiable  2    candles_clear            2
price_axis_readable      2    timeframe_visible        1
volume_present           1    indicators_labeled       1
axes_not_distorted       1
```

| Score | Consequence |
|-------|-------------|
| 8–10 | Full analysis |
| 5–7 | No precise levels; verdict capped at WAIT |
| 2–4 | Qualitative only |
| 0–1 | Stop: ask for a better image or a transcription |
