# Chart Intelligence — Trap Detection

Implements [`../../workflows/trap-detection.md`](../../workflows/trap-detection.md) as a scoring procedure.

## Evidence scoring

Each candidate trap is scored 0–6:

| # | Test | Points |
|---|------|--------|
| 1 | A prior identifiable level exists (≥2 touches) | 1 |
| 2 | Price traded beyond the level (a break occurred) | 1 |
| 3 | A **close** back inside within 1–3 bars | 2 |
| 4 | A visible reaction away from the level | 1 |
| 5 | No immediate re-break in the original direction | 1 |
| 6 | Volume evidence (spike on the sweep, or collapse on the break) | 1 |

| Score | Label | Permitted language |
|-------|-------|-------------------|
| 6 | `CONFIRMED` trap | "This is a failed breakout" |
| 4–5 | `POSSIBLE` trap | "This is consistent with a failed breakout" |
| 2–3 | `WEAK` | "The break has not held so far" |
| 0–1 | none | No trap claim at all |

Note test 3 carries double weight because **the close is the whole signal**. A wick beyond a level is common and
mostly meaningless.

## The nine types and their distinguishing evidence

| Type | Distinguishing evidence beyond the base score |
|------|---------------------------------------------|
| Bull trap | Prior resistance + close back below + failing follow-through |
| Bear trap | Prior support + close back above |
| Fake breakout | Break + reversal within 1–3 bars, volume declining |
| Fake breakdown | Mirror |
| Liquidity sweep | Wick beyond equal highs/lows + close back inside + reaction |
| Failed retest | Break holds, retest fails, close back through |
| Stop-hunt hypothesis | Identifiable stop cluster just beyond the level + wick + reclaim |
| False reversal | Structure break + immediate reclaim + new extreme in the old direction |
| Volume divergence | Break with volume < 0.8× average, or rising price on falling volume |

## Output format

```
Trap analysis
  Type            : bull trap
  Level           : 1_240 (3 touches)
  Behaviour       : close 1_243.5, then closes 1_238.2 and 1_236.9 (2 bars back inside)
  Evidence score  : 5/6 (missing: volume spike on the sweep — volume was 0.9x)
  Status          : POSSIBLE
  Would confirm   : a close below 1_231 (the pre-breakout higher low)
  Implication     : the long scenario is cancelled; a short setup becomes available only
                    after 1_231 breaks with volume
```

## Anti-patterns

| Anti-pattern | Why it is wrong |
|--------------|-----------------|
| Calling a trap before the close back inside | It is still a breakout at that point |
| Calling a normal retest a trap | Retest stays outside the level; a trap closes back inside |
| Claiming a trap with no prior level | There is nothing to trap |
| Attributing intent ("they hunted stops") | Unverifiable |
| Ignoring volume entirely | Removes one of the six tests |
| Retro-fitting: finding the trap after the reversal | Hindsight, not detection |

## Why this matters economically

A confirmed trap often produces the best R:R available on a chart: entry on the reclaim, invalidation just beyond
the trap's extreme, and a target back at the opposite side of the prior range. It also prevents the most common
retail loss — buying a failed breakout.
