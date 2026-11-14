# Ranges and Trends — Classifying the Regime

## 1. Why this is the first decision

Every indicator and pattern behaves differently in a trend than in a range. Choosing the wrong regime invalidates
the whole analysis, no matter how good the individual signals are.

| | Trend | Range |
|---|-------|-------|
| Structure | HH/HL or LH/LL | Overlapping swings |
| ADX | > 20–25 | < 20 |
| MAs | Stacked, sloping | Flat, tangled |
| Price vs MA | Mostly one side | Crossing repeatedly |
| Bollinger | Riding a band, bands widening | Bouncing between bands |
| Pullbacks | Shallow, bought | Deep, both sides |
| Best tools | MA pullbacks, Supertrend, flags | Oscillator extremes, band fades, pivots |
| Failure mode | Mean-reversion entries | Breakout entries |

## 2. Objective classification method

Score four measures; do not rely on one:

```
1. Swing structure  : 2+ consecutive HH/HL (or LH/LL) -> trend lean
2. ADX(14)          : > 25 trend · 20-25 transitional · < 20 range
3. MA slope         : 50-EMA slope over the last 20 bars, in ATR units
4. Price location   : bars outside the 20-BB on one side repeatedly -> trend
```

| Score | Classification |
|-------|----------------|
| 4 trend markers | Trending |
| 3 | Likely trending |
| 2 | Mixed / transitional — reduce size or stand aside |
| 0–1 | Ranging |

## 3. Range anatomy

A tradable range has:

1. **Two tested boundaries** (≥2 touches each, preferably 3).
2. **Width ≥ 2 ATR** — narrower than that and costs/slippage destroy any edge.
3. **Stable duration** — the range should have existed long enough to establish boundaries.
4. **Declining volume** inside (typically).

What to avoid inside a range:

- Entries at the **midpoint** — the highest-noise zone.
- Breakout trades without volume.
- Adding indicators; ranges produce maximal indicator noise.

## 4. Trend anatomy

A tradable trend has:

1. **Clean swing structure** with a defined last HL (or LH).
2. **ADX > 20–25**, ideally rising.
3. **Volume expanding on the trend-direction legs.**
4. **Pullbacks to a reference** (MA, prior swing, Fib zone) that hold.

What to avoid in a trend:

- Counter-trend fades based on oscillator extremes.
- Buying extended moves (>2–3 ATR from the reference).
- Assuming the trend's age is irrelevant — mature trends are qualitatively different.

## 5. Transitions — where most money is lost

| Transition | Signature | Approach |
|------------|-----------|----------|
| Trend → range | ADX falling, equal highs, deeper pullbacks | Switch to range logic; stop using breakout entries |
| Range → trend | ADX rising, compression resolution with volume | Switch to trend logic; stop fading |
| Trend → opposite trend | Structure break + failed retest | Wait for confirmation; do not pre-empt |

The most expensive error is using yesterday's regime logic today. Update the classification whenever ADX or the
swing structure changes materially.

## 6. Reporting template

```
Regime classification : Ranging (3 range markers, 1 trend marker)
Evidence              : swings overlapping; ADX(14) = 14; 50-EMA flat (slope 0.1 ATR over 20 bars);
                        price crossed the 20-BB midline 7 times in 20 bars
Confidence            : Moderate
Consequence           : fade entries at tested boundaries with tight stops are appropriate;
                        breakout entries are not, until ADX > 20 and volume expands
```

## 7. Common errors

| Error | Guard |
|-------|-------|
| Calling a regime from one measure | Use four |
| Classifying once and never updating | Re-check when ADX/structure changes |
| Using "trend" to justify any direction | A trend has a direction; state it |
| Ignoring the higher timeframe's regime | A 15m range inside a daily trend behaves differently from a 15m range inside a daily range |
| Treating "mixed" as a reason to trade anyway | Mixed means reduce size or wait |

## 8. Beginner summary (Hinglish)

**Regime pehle decide karo:** trend hai ya range?

**Simple check:**
- **ADX 20 se neeche + EMAs flat + price EMAs ko baar baar cross kare** → **range**.
- **ADX 25 se upar + EMAs stacked + HH/HL saaf** → **trend**.

**Range mein:** boundary par fade karo (support par buy, resistance par sell). Breakout mat karo.
**Trend mein:** pullback par entry karo. Oscillator ke "overbought" par short mat karo.

**Sabse mehnga error:** kal ka regime logic aaj use karna.

## 9. Exercise

Classify five different charts (or five periods of one chart) using the four-marker method. Write the score for
each. Then, for each, state which tool you would use and which you would avoid. Compare your classifications with
a second look a week later — did any change?

---
*See also: [`trend-phases.md`](trend-phases.md) · [`level-mapping.md`](level-mapping.md) ·
[`../../engines/market-intelligence/market-regime.md`](../../engines/market-intelligence/market-regime.md)*
