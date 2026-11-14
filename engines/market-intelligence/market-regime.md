# Market Intelligence — Regime Detection

**Purpose:** classify the market state before choosing tools. Every indicator and pattern behaves differently by
regime.

## The five regimes

| Regime | Signature | Appropriate tools | Tools that fail |
|--------|-----------|-------------------|-----------------|
| **Trending** | HH/HL or LH/LL, ADX >25, stacked MAs | MA pullbacks, flags, Supertrend trail | Oscillator extremes, band fades |
| **Ranging** | Overlapping swings, ADX <20, flat MAs | Oscillator extremes, band fades, pivots, volume profile | MA crossovers, Supertrend, breakouts without volume |
| **High volatility** | ATR at multi-month highs, wide bars | ATR sizing only; reduce size | Everything directional |
| **Low volatility / squeeze** | ATR and bandwidth at lows | Compression levels + volume; plan both sides | Oscillators (saturate) |
| **Transitional / uncertain** | Mixed markers, ADX 20–25, conflicting timeframes | Nothing; stand aside | Everything |

## Scoring method (four markers)

```
1. Swing structure : 2+ consecutive HH/HL (or LH/LL)   -> trend +1
2. ADX(14)         : >25 -> trend +1 ; <20 -> range +1
3. 50-EMA slope    : |slope over 20 bars| > 0.5 ATR    -> trend +1
4. Bollinger walk  : price outside the 20-BB on one side >= 40% of the last 20 bars -> trend +1

trend_score = sum
  4 -> TRENDING
  3 -> LIKELY TRENDING
  2 -> TRANSITIONAL
  0-1 -> RANGING
```

Then separately classify volatility:

```
ATR percentile over 1-2 years:
  >80th  -> HIGH VOLATILITY
  <20th  -> LOW VOLATILITY (squeeze)
  else   -> NORMAL
```

The final label combines both: e.g. "trending, normal volatility" or "ranging, low volatility (squeeze)".

## Why the combination matters

| Combination | Consequence |
|-------------|-------------|
| Trending + low vol | Smooth continuation; best environment for trend following |
| Trending + high vol | Violent pullbacks; wider stops needed |
| Ranging + low vol | Excellent for boundary fades; tight stops |
| Ranging + high vol | Fakeout-heavy; the worst environment |
| Transitional + anything | No edge; reduce size or stand aside |

## Reporting template

```
Regime            : RANGING, low volatility (squeeze)
Evidence          : swings overlapping (0 consecutive HH/HL); ADX(14) = 13;
                    50-EMA slope 0.08 ATR over 20 bars (flat);
                    price crossed the BB midline 7 times in 20 bars;
                    ATR at the 12th percentile of 2 years
Confidence        : Moderate (3 of 4 markers agree on range)
Consequence       : boundary fades are appropriate at tested levels; breakout entries are not
                    viable until ADX > 20 and volume expands on a close beyond a boundary
Update trigger    : a close beyond either boundary with volume, or ADX crossing 20
```

## Failure modes

| Failure | Guard |
|---------|-------|
| Classifying from one marker | Use four |
| Classifying once per session | Re-check when ADX or structure changes |
| Using "trend" without a direction | A trend has a direction — state it |
| Ignoring the higher timeframe's regime | A 15m range inside a daily trend behaves differently |
| Treating "transitional" as tradeable | It means reduce size or wait |
