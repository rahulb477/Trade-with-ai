# Engine — Technical Intelligence

**Purpose:** compute and interpret indicator readings — only where inputs genuinely exist — and enforce
non-redundancy.

**Inputs:** OHLCV series (from a provider) **or** indicator values read from a chart.
**Outputs:** indicator readings with provenance, an independence audit, and an interpretation consistent with the
regime.

## Two operating modes

| Mode | Input | What is permitted |
|------|-------|-------------------|
| **Computed** | Real OHLCV from a provider | Any indicator, with exact values, via `integrations/python/trading_intel/indicators.py` |
| **Visual** | Values printed on a chart screenshot | Only those values, quoted exactly; no derivation |

**There is no third mode.** Deriving an indicator from pixel heights is fabrication.

## Protocol

```
1. Determine mode and inputs.
2. List indicators actually present (or computable).
3. For each: value, period (printed or ASSUMED default), reading, limitation.
4. Group by family (trend / momentum / volatility / volume / levels).
5. Independence audit: how many distinct families are represented?
6. Regime check: are these indicators appropriate for the current regime?
7. Interpretation, with explicit "this does not mean X" statements.
```

## Family → members map (to prevent false confirmation)

```
Trend      : SMA, EMA, Supertrend, Ichimoku, ADX, Parabolic SAR
Momentum   : RSI, MACD, Stochastic, Stochastic RSI, CCI, ROC, MFI, Williams %R
Volatility : ATR, Bollinger width, Keltner width, historical volatility
Volume     : OBV, VWAP, volume profile, CVD (needs bid/ask), A/D line
Levels     : Pivot points, Fibonacci, volume profile POC, round numbers
```

Two members of the same family are **one** piece of evidence.

## Interpretation rules

| Rule | Detail |
|------|--------|
| State the period | "RSI is oversold" is incomplete without 14 on a specific timeframe |
| Regime first | Oscillator extremes are signals in ranges and noise in trends |
| No single-indicator triggers | Indicators confirm; price events trigger |
| No "overbought = sell" | Trends keep oscillators at extremes for extended periods |
| Divergence = hypothesis | Requires a structural break before it is actionable |
| No invented values | If not printed or computable, say "not available" |

## Implementation map

| Indicator | Function |
|-----------|----------|
| SMA / EMA | `indicators.sma`, `indicators.ema` |
| RSI | `indicators.rsi` |
| MACD | `indicators.macd` → `(macd, signal, hist)` |
| ATR | `indicators.atr` |
| ADX | `indicators.adx` → `(adx, plus_di, minus_di)` |
| Bollinger | `indicators.bollinger_bands` |
| Supertrend | `indicators.supertrend` |
| Stochastic RSI | `indicators.stochastic_rsi` |
| OBV | `indicators.obv` |
| VWAP | `indicators.vwap` |
| Ichimoku | `indicators.ichimoku` |
| Volume profile | `indicators.volume_profile` |
| Pivots | `indicators.pivot_points` |
| CCI / ROC / MFI | `indicators.cci`, `indicators.roc`, `indicators.mfi` |
| Fibonacci | `indicators.fib_levels` |

All are pure-stdlib and return `None` where a value is undefined — never a guessed value.

## Failure modes

| Failure | Handling |
|---------|----------|
| Not enough bars | Return `None`; state "insufficient history" |
| Missing volume | OBV/VWAP/MFI/profile unavailable — say so |
| Period not printed | Assume the documented default, mark `ASSUMED` |
| Two indicators show conflicting momentum | Report both; do not average |
| Indicator contradicts price structure | Structure wins; state the conflict |

## Output template

```
Indicators (visual mode)
  Trend     : price above 20 & 50 EMA (labels visible); EMA stack rising
  Momentum  : RSI(14) = 61.3 (printed); above 50, below 70 -> bullish, not overbought
  Volatility: ATR not displayed; candles visibly larger than the prior 20 -> volatility rising (qualitative)
  Volume    : volume panel present; last up bar ~1.4x the visible average
  Levels    : no pivot/Fib overlay
  Families represented : 4 (trend, momentum, volatility, volume) -> 4 independent classes
  Regime fit : trending up; oscillators are confirmation only
  Not available : MACD, ADX, exact ATR, any higher-timeframe reading
```
