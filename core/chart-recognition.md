# Chart Recognition

How to read a trading-chart screenshot reliably — and how to fail honestly when the image does
not contain enough information.

This is the highest-risk stage in the whole pipeline. Everything downstream inherits its errors.

---

## 1. What you are looking at

A trading chart is a compressed visual encoding. Before interpreting anything, enumerate the
*elements*. Do not jump to "it looks bullish" — that is pattern-matching without perception.

### 1.1 Element inventory (complete this before analysis)

| Element | Where to look | Why it matters |
|---------|---------------|----------------|
| Instrument | Top-left header, tab title | Everything depends on it |
| Exchange / broker | Header suffix (`.NS`, `.BO`), platform logo | Session, tick size, holidays |
| Last price | Usually large, near y-axis, plus a highlighted axis label | Anchor for all levels |
| Change / % change | Next to last price | Session context |
| Timeframe | Selector row (`1m 5m 15m 1H 4H 1D 1W`) or a label near the symbol | Determines what a candle means |
| Chart type | Candles vs bars vs line vs Heikin-Ashi vs Renko | Heikin-Ashi does **not** show real OHLC |
| Price axis | Right or left; min/max labels | Without it, levels cannot be quantified |
| Time axis | Bottom; date labels | Gaps, session boundaries, survivorship of weekends |
| Volume panel | Bottom histogram | Confirmation |
| Indicator panels | Separated panes below/above | Their readings and scales |
| Overlays | MAs, VWAP, Bollinger, Supertrend | Interpretation |
| Drawings | Trendlines, horizontal lines, boxes, Fib retracements, text labels | *Someone's* annotations — not necessarily correct |
| Markers | Buy/sell arrows from a strategy tester | Implies backtest overlay; may be misleading |
| Watermark / "delayed" banner | Faint centre text, corner notice | Data is not live |
| Corporate-action adjustments | Sudden unexplained price jumps | Splits/bonus create false "gaps" |

### 1.2 Candle anatomy refresher

For each visible candle record: direction (body colour), body extent (open→close), upper wick,
lower wick, and approximate size relative to neighbours.

Two important traps:

- **Colour conventions differ.** In much of Asia (and in some Indian platform themes) **red = up**
  and **green = down**. If the chart's colours are ambiguous, describe patterns as
  "bullish/bearish" based on *position relative to the trend* rather than colour, and state the
  uncertainty.
- **Heikin-Ashi candles are synthetic.** A "hammer" on HA is not a hammer. If the chart type is
  HA/Renko/Kagi, refuse to apply open/high/low-based candle rules and say so.

---

## 2. Reading the scales (interpolation, with caveats)

To place a horizontal level you need the price axis. Procedure:

1. Identify two gridline labels: `P_low` at pixel `y_low` and `P_high` at pixel `y_high`.
2. Compute `price_per_pixel = (P_high − P_low) / (y_low − y_high)` (note the sign: y grows downward).
3. For a feature at pixel `y_f`: `P_f = P_low + (y_low − y_f) × price_per_pixel`.

**Report interpolated values as approximate** (`≈1_204`, not `1_204.35`). Axis arithmetic on a
screenshot is never exact: images are resampled, gridlines are anti-aliased, and the axis may be
logarithmic.

**Log-scale detection:** if equal price *ratios* occupy equal vertical distance rather than equal
*amounts*, the axis is logarithmic. On a log axis, linear interpolation of price is wrong — either
convert (`price = exp(linear interpolation of log price)`) or refuse precise levels. Most retail
charts default to linear for intraday and are configurable on long-horizon charts.

**Cropped axis:** if the left/right price labels are cut off, you cannot quantify levels. Offer
structure only ("price is above the prior swing high") and mark levels unavailable.

---

## 3. Instrument identification

Never trust a partial ticker. Cross-check the following, in order:

1. Full ticker string, including suffix (`.NS`, `.BO`, `-USD`, `.L`)
2. Company/index display name next to the ticker
3. Price magnitude — a ₹120 price excludes most large caps; BTC/USD ~ tens of thousands
4. Currency symbol (`₹`, `$`, `€`)
5. Trading-hours x-axis shape (Indian equities: 09:15–15:30 IST band; US: 09:30–16:00 ET)
6. Sector hints in overlays or news widgets

### High-collision cases (ask, do not guess)

| Ambiguity | Example |
|-----------|---------|
| Same company, two exchanges | `RELIANCE` (NSE) vs `RELIANCE.BO` (BSE) |
| Similar names | `TATAPOWER` vs `TATAMTRDVR`; `ADANIPORTS` vs `ADANIPOWER` |
| Spot vs futures | `NIFTY 50` index vs `NIFTY-FUT` continuous |
| Index vs ETF | `BANKNIFTY` vs `BANKBEES` |
| ADR vs local | `INFY` (NYSE) vs `INFY.NS` |
| Crypto pair quote currency | `BTC/USDT` vs `BTC/INR` |
| Ticker reuse over time | A delisted symbol later reassigned |

If two candidates survive all checks: **ask**. A wrong instrument silently invalidates structure,
news, sector and levels simultaneously.

---

## 4. Screenshot quality rubric (0–10)

| Criterion | Points | Full credit looks like |
|-----------|--------|------------------------|
| Instrument identifiable | 0–2 | Full ticker + name + exchange marker |
| Price axis readable | 0–2 | At least 4 labelled gridlines spanning the visible range |
| Timeframe identifiable | 0–2 | Explicit label, not inferred |
| Chart type is OHLC-based | 0–1 | Candlestick/bar, not HA/Renko/line-only |
| Candles legible | 0–2 | ≥ 40 candles visible, bodies distinguishable, not overlapping into a blur |
| Volume panel present | 0–1 | Histogram with visible scale or clear relative bars |
| No obstructing overlays | 0–1 | Annotations do not hide the price action; no modal dialogs |

Interpretation:

| Score | Verdict | Allowed output |
|-------|---------|----------------|
| 8–10 | `good` | Full report with levels |
| 5–7 | `partial` | Report without precise levels; verdict ≤ WAIT |
| 2–4 | `poor` | Qualitative structure description only; explicit `INSUFFICIENT DATA` for numeric claims |
| 0–1 | unusable | Stop; request re-capture |

### Common defects and their fix

| Defect | Symptom | Ask for |
|--------|---------|---------|
| Blurry / low-res | Text unreadable, candles merge | Full-resolution screenshot, or crop the header + right 30% |
| Cropped price axis | No numbers on the right | Re-take with the axis visible |
| Cropped right edge | Last candle cut in half | Include 10–20 future-candle whitespace |
| Too few candles | < 20 bars | Zoom out; include 100+ bars |
| Hidden timeframe | No selector visible | State the timeframe in text |
| Indicators cut off | Panels cropped | Separate screenshot of the indicator pane |
| Dark-on-dark | Barely visible grid | A lighter theme, or state the values manually |
| Mobile screenshot with toolbar | Chart occupies <50% of frame | Full-screen chart mode |
| Annotations covering price | Drawings stacked | Hide drawings, or note what they are |

---

## 5. What cannot be recovered from a screenshot

Be explicit about these — they are the most common source of false confidence:

- **Exact OHLC** of any candle (only the last price may be precise, via its axis label).
- **Indicator values** not printed as a label (a line's height does not give you RSI = 58.3).
- **Volume numbers** (only relative bar heights).
- **Levels of drawings** unless the platform prints them.
- **Data adjustment state** (split/dividend adjusted or not) unless a gap pattern implies it.
- **Anything after the right edge** — including whether the pattern "worked".
- **The higher timeframe**, unless a second screenshot is supplied.
- **Whether the chart is live, delayed, or a replay.**

Say "not recoverable from this image" and offer the alternative (a second screenshot, or the user
typing the values).

---

## 6. Multi-screenshot handling

When several images arrive:

1. Label them `IMG1…IMGn` and record what each is (timeframe? different instrument? indicator zoom?).
2. Build one merged `ChartObservation` with a `source_image` field per element.
3. If the same instrument appears at two timeframes, populate the stage-9 table directly.
4. If two images show the same timeframe but disagree (different last price), check timestamps
   first — the older one is history, not a conflict.
5. If images show different instruments, treat them as separate analyses unless the user asked for
   a comparison; for a comparison, build an explicit relative-strength section.

Detect duplicates: identical last price + identical candle sequence ⇒ same image uploaded twice.
Do not treat as two confirmations.

---

## 7. Pattern-status discipline

Do not confuse visually similar patterns. The most frequently mislabelled pairs:

| Looks like | But could be | Distinguishing test |
|-----------|--------------|---------------------|
| Hammer | Hanging man | Position relative to the preceding trend (down vs up) |
| Doji | Spinning top | Body vs total range: doji ≈ body < 5% of range; spinning top has a small but real body |
| Inside bar | Harami | Harami additionally requires opposite-coloured bodies and a prior trend |
| Bull flag | Bear flag | Slope of the drift vs the pole: continuation direction = pole direction |
| Ascending triangle | Rising wedge | Triangle: flat top, rising bottom. Wedge: both boundaries converging upward |
| Double bottom | Rectangle support test | Double bottom needs a neckline break; two touches alone are just a support test |
| Bull trap | Breakout + retest | Trap: close back inside the range. Retest: price holds at/below the level without closing back |

Assign status:

- `CONFIRMED` — the completing candle has **closed** and all formation rules hold
- `DEVELOPING` — structure forming; the decisive candle is open or missing
- `POSSIBLE` — resembles the pattern but one rule fails; name the rule
- `UNCLEAR` — resolution/ambiguity prevents judgement

---

## 8. Vision failure protocol

If you cannot see the image at all as an image (e.g. only a filename was provided):

1. Say so plainly: "I cannot see the image contents — only that a file was attached."
2. Give a short transcription request:
   > Please paste: instrument + exchange · timeframe · last price · last 5 candles (direction and
   > rough shape) · the nearest support and resistance you can see · whether volume is rising or
   > falling · any indicator values shown as numbers.
3. Offer to continue in LEARNING mode on whatever topic they want in the meantime.
4. Never produce a chart analysis from the filename or from assumptions about the instrument.

---

## 9. Checklist before leaving this stage

- [ ] Instrument resolved or a single question asked
- [ ] Timeframe stated (observed, not guessed)
- [ ] Chart type noted (and whether HA/Renko invalidates candle rules)
- [ ] Quality score computed, with the reasons
- [ ] `unreadable` and `absent` lists written
- [ ] Candle colour convention noted if ambiguous
- [ ] Every element tagged with its source image
- [ ] No level quoted without an axis basis or an "approximate" marker

---

*See also: [`../engines/chart-intelligence/README.md`](../engines/chart-intelligence/README.md) ·
[`../integrations/ocr/README.md`](../integrations/ocr/README.md) ·
[`../workflows/screenshot-analysis.md`](../workflows/screenshot-analysis.md)*
