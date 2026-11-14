# Example — Multi-Timeframe Analysis

> **FICTIONAL.** Instrument "GAMMATECH" (fictional). Three timeframes supplied: weekly, daily, 15-minute.

## 1. Inventory

| Timeframe | Supplied? | Trend | Key level | Source |
|-----------|-----------|-------|-----------|--------|
| 1W | yes | up | 1,050 support (3 touches) | screenshot |
| 1D | yes | up | 1,140 support · 1,285 resistance | screenshot |
| 1H | **no** | unknown | — | not shown |
| 15m | yes | **down** | 1,196 support · 1,222 resistance | screenshot |

**Prices are approximate** (axis-interpolated). The 1H chart is absent, and absence is recorded as `unknown`,
never inferred from the neighbours.

## 2. Ratio quality

| Pair | Ratio | Quality | Comment |
|------|-------|---------|---------|
| 15m → 1D | 25× | too far | These describe different market phases; a 1H view is missing |
| 1D → 1W | 5× | **good** | Clean separation |

This is the finding that shapes the whole analysis: **the missing 1H timeframe is the important one.** The 15m and
1D views are too far apart to reconcile directly.

## 3. Alignment table

| Timeframe | Trend | Market phase | Conflict |
|-----------|-------|--------------|----------|
| 1W | up | Accumulation/markup | — |
| 1D | up | Markup, currently a pullback | — |
| 15m | down | Corrective | **Yes** — 15m is a pullback inside a 1D uptrend |

**Classification: `MIXED`** — 2 up, 1 down, 1 unknown.

But "mixed" here is not a contradiction: a lower timeframe decline inside a higher timeframe advance is the normal
anatomy of a pullback. The classification is about *agreement*, the interpretation is about *context*.

## 4. The three possible readings

| Reading | Requires | Consequence |
|---------|----------|-------------|
| **Healthy pullback** (most likely) | 1D structure intact (higher low above 1,140), 15m decline on falling volume, no impulsive 1D close below support | Look for a 15m reversal at a 1D support |
| **Trend failure** | 1D close below 1,140 | The 1W uptrend is now in question; the 15m downtrend was the first warning |
| **Range development** | Both 1,140 and 1,285 hold for 10+ sessions | Switch tools: fade boundaries, drop trend-following |

## 5. Operating timeframe decision

| Field | Value |
|-------|-------|
| Analysis timeframe | 1D (context) |
| Entry timeframe | 15m (trigger) |
| Ratio | 25× → too far |
| Recommendation | **Add the 1H chart** and use 1H for entry timing, or accept a 15m entry only with an explicit statement that the views are not directly reconcilable |

The honest report says: "I am using a 15m trigger inside a 1D uptrend. The ratio is 25×, which is too wide for the
trigger to be considered a direct expression of the daily context. Adding the 1H chart would resolve this."

## 6. Level hierarchy

| Level | Timeframe of origin | Weight |
|-------|--------------------|--------|
| 1,285 | 1D | High — a daily swing high |
| 1,222 | 15m | Low — intraday only, likely to be crossed |
| 1,196 | 15m | Low |
| 1,140 | 1D | High — the daily higher low; the operative invalidation |
| 1,050 | 1W | Highest — the weekly support; a break here changes the thesis entirely |

**Rule applied:** a level from a higher timeframe overrides a level from a lower one when they conflict. The 15m
levels are entries and exits, not thesis-level invalidation.

## 7. Verdict

**`WAIT — NO CONFIRMED SETUP`** (gate G6: unexplained alignment gap — the 1H timeframe is missing, and the 15m/1D
ratio is 25×).

**The specific confirmation needed:** a 15m close back above 1,222 with a higher low formed above 1,196. That would
be the first objective evidence that the 15m decline has ended inside the intact daily uptrend.

**Whole-analysis invalidation:** a 1D close below 1,140.

## 8. Beginner Explanation (Hinglish)

**Timeframes ka matlab:** weekly = bada trend, daily = medium, 15-minute = chhota.

**Yahan kya hai:** weekly aur daily up hain, 15-minute down. Yeh **contradiction nahi** hai — bade trend ke andar
chhota pullback normal hai.

**Par ek problem hai:** 15m aur daily ke beech ka gap bahut bada hai (25×). Beech ka **1-hour chart nahi mila**.
Isliye main 15-minute ke signal ko daily trend ka seedha proof nahi maan sakta.

**Kaunsa level important hai:** 1,140 (daily higher low) — iske neeche daily close aaya to poora idea badal jayega.
15-minute ke 1,196/1,222 sirf entry-exit ke liye hain.

**Verdict: WAIT.** 1,222 ke upar 15m close + 1,196 ke upar higher low chahiye. Tab setup dekhenge.

## 9. Why this example exists

Most multi-timeframe errors are not analysis errors — they are **inventory** errors. The trader looked at three
charts and never noticed which one was missing. Writing `unknown` in the table is what surfaces it.
