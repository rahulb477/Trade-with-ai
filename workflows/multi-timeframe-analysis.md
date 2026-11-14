# Workflow — Multi-Timeframe Analysis

## When to use
Two or more timeframes are supplied, or the user asks "what does the bigger picture say".

## Step 1 — Inventory

Never analyse a timeframe you do not have. Build the table first:

| TF | Source | Provided? |
|----|--------|-----------|
| Monthly | — | no |
| Weekly | — | no |
| Daily | screenshot | yes |
| 4H | — | no |
| 1H | screenshot | yes |
| 15m | screenshot | yes |
| 5m | — | no |

## Step 2 — Analyse each timeframe independently

For each available timeframe:

```
TF     : 1D
Trend  : up (HH-HL x4, k=3)
Key levels: R 1_310 (2 touches) · S 1_196 (2 touches) · S 1_140 (1 touch, untested)
Momentum: RSI 58, rising
Volatility: ATR 18, stable
Conflict?: none within this timeframe
```

Do not mix timeframes in this step. Each gets its own row and its own conclusion.

## Step 3 — Build the alignment table

| TF | Trend | Structure | Momentum | Key level | Relation to the timeframe above |
|----|-------|-----------|----------|-----------|-------------------------------|
| 1D | up | HH/HL | 58 rising | 1_196 | — |
| 1H | down | LH/LL x2 | 44 falling | 1_240 | pullback within 1D uptrend |
| 15m | up | HH/HL x2 | 55 | 1_218 | bounce within 1H downtrend |

## Step 4 — Classify the relationship

| Pattern | Meaning |
|---------|---------|
| All aligned | Highest-conviction continuation |
| High up / low down (shallow) | Pullback — buy at the high-TF support |
| High up / low down (deep, structure broken) | Possible reversal — WAIT |
| High down / low up | Bear rally — sell at the high-TF resistance |
| Genuine conflict | WAIT |

**Quantify the pullback**: what fraction of the last higher-timeframe leg has been retraced? <38.2% = shallow;
38.2–61.8% = normal; >61.8% = the trend is in question.

## Step 5 — Choose the operating timeframe

State explicitly:

```
Bias timeframe      : 1D (up)
Structure timeframe : 1H
Trigger timeframe   : 15m
Trade direction     : long, only at 1D support
Invalid if          : 1D closes below 1_196, or 1H makes a lower high below 1_218 and breaks 1_196
```

## Step 6 — Report

Section 4 of the report must present each timeframe **separately** with its own conclusion, then the combined
statement. Do not average them into a single "mixed" verdict without explaining the relationship.

## Common failures

| Failure | Guard |
|---------|-------|
| Claiming a timeframe you never saw | Table with "not provided" |
| Using 15m to override a 1D trend without a structure break | Quantify the retracement |
| Averaging conflicting readings | Report the conflict; choose WAIT or the higher TF |
| Using timeframes too close together (15m + 20m) | Use 4–6× ratios |
| Ignoring that the lower TF's "downtrend" may be one 1H leg | Always compare degrees |
