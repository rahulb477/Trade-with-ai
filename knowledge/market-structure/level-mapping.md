# Level Mapping

## 1. Purpose
A support/resistance map is a small set of price levels that have produced visible reactions. It is the skeleton
of every trade plan: entries, stops and targets all reference it.

## 2. Building the map — a repeatable procedure

```
1. Fix the swing parameter k (e.g. 3) and state it.
2. Mark all swing highs and lows in the visible window.
3. Cluster nearby swings: swings within ~0.3-0.5 ATR of each other form ONE zone, not separate levels.
4. Count touches per cluster. Keep clusters with >= 2 touches.
5. Note which clusters are "fresh" (untested recently) vs "exhausted" (tested many times).
6. Add non-swing references: prior day/week high-low, opening range, round numbers, VWAP, POC.
7. Rank the resulting zones by (touches x recency x confluence).
8. Keep at most 4-6 levels for the analysis timeframe. More than that is noise.
```

## 3. Zone vs line

Levels are **zones**, not lines. A support at "1,200" is really "1,196–1,204". Reasons:

- Different participants use different reference prices.
- Wicks and closes give slightly different values.
- Round-number psychology spreads orders over a band.

Report zones with a width, and place stops **outside** the zone, not inside it.

## 4. Level quality ranking

| Factor | Strengthens the level |
|--------|----------------------|
| Touches | 3+ > 2 > 1 (1 is a candidate only) |
| Reaction size | A large rejection (≥1 ATR) is stronger than a small one |
| Recency | Recent reactions matter more for short-term trading |
| Volume at the reaction | High volume reaction = more participants remember it |
| Confluence | Coincides with a Fib level, MA, pivot, VWAP, POC, or round number |
| Timeframe | Higher-timeframe level > lower-timeframe level |
| Freshness | Untested levels ahead are stronger; heavily tested levels weaken |

## 5. Exhaustion of a level

A level tested many times tends to weaken, not strengthen — the orders that defended it get consumed. This is why
the "fourth test of support" often breaks. Counter-intuitively, this means:

- A level with 2–3 good touches is **strong**.
- A level tested 6–8 times is often a **coil** about to resolve.

State which reading you are using and why.

## 6. Non-swing references worth adding

| Reference | Why |
|-----------|-----|
| Prior session/period high-low | Widely watched; day traders' reference |
| Opening range (first 15/30 min) | Defines the day's initial balance |
| Round numbers (100s, 1000s) | Order clustering |
| Previous day's close | Overnight positioning reference |
| VWAP | Average participant's cost |
| Volume profile POC / value area | Acceptance zones |
| Pivot points | Computed by many participants identically |
| Gap edges | Unfilled gaps attract price |
| Fib retracement of the dominant swing | Widely watched |

## 7. Stops relative to levels

```
Never place a stop exactly at a level: that is where resting orders cluster.
Rule: stop = beyond the level by 0.25-0.5 x ATR
```

If the resulting stop distance makes the position size trivial or the R:R unacceptable, the setup is wrong for
the account — not an invitation to widen the stop to make the arithmetic work.

## 8. Reading a map in a report

```
Levels (analysis timeframe: 1D)
  R2  1_310-1_318  2 touches, untested 6 weeks, near Fib 1.272      strong
  R1  1_238-1_245  3 touches, latest reaction 1.6 ATR, high volume  strong
  --- price 1_204 ---
  S1  1_196-1_204  2 touches (today's low inside); also 0.618 Fib   strong (price is AT it)
  S2  1_140-1_150  4 touches but exhausted after the 4th test       weakening
  S3  1_080-1_090  prior consolidation low, untested since          strong if reached
```

## 9. Common errors

| Error | Guard |
|-------|-------|
| Drawing 15 lines | Keep 4–6 |
| Lines through wicks only | Use closes primarily, wicks as zone edges |
| Ignoring confluence | Rank levels by multiple factors |
| Treating a 1-touch level as established | Minimum 2 touches |
| Stops exactly at the level | Add an ATR buffer |
| Forgetting higher-timeframe levels | Always check one timeframe up |
| Levels "discovered" after the trade idea | Draw the map before deciding the trade |

## 10. Beginner summary (Hinglish)

**Level mapping kya hai?** Chart par un prices ko mark karna jahan price ne pehle react kiya — yahi aapke entry,
stop aur target ka base hain.

**Rules:**
1. Sirf **2 ya zyada touches** wale levels rakho. Ek touch = sirf "candidate".
2. Level ek **zone** hai, line nahi (e.g. 1,196–1,204).
3. **4–6 levels** kaafi hain. 15 lines = noise.
4. **Stop level ke thoda bahar** rakho (0.25–0.5 ATR buffer) — bilkul level par nahi, wahan stops cluster hote hain.

**Zaroori insight:** bahut zyada test hua level **kamzor** ho jata hai (orders khatam ho jate hain). 2–3 test =
strong, 6–8 test = coil.

## 11. Exercise

Build a level map on a daily chart using the 8-step procedure. Count the touches per level. Then rank the levels.
Which level would you use for a stop, and which for a target? Write down the ATR buffer you would use and why.

---
*See also: [`ranges-and-trends.md`](ranges-and-trends.md) · [`../price-action/retest.md`](../price-action/retest.md) ·
[`../indicators/volume-profile.md`](../indicators/volume-profile.md)*
