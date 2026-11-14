# Swing Trading

**Horizon:** days to weeks. **Holding:** 3–20 sessions. **Trades per month:** 2–10.

**Status:** `DOCUMENTED` — method described, not validated. This is also the most beginner-appropriate style in this
repository because cost/R ratios are far better than intraday.

## 1. Characteristics

| Attribute | Typical |
|-----------|---------|
| Analysis timeframe | Daily |
| Entry timeframe | Daily or 1H |
| Target | 2–6 ATR / 5–15% |
| Stop | 1.5–2.5 ATR, beyond structure |
| Win rate needed at 1:2 | ~33% + costs |
| Key risks | Overnight gaps, event risk, longer exposure to regime change |

## 2. The interaction that matters: swing entries vs regime

| Regime | Swing approach |
|--------|----------------|
| Trending up | Buy pullbacks to structure/20-EMA; hold with a trail |
| Ranging | Fade boundaries only; expect smaller targets |
| Trending down | Short rallies into resistance (subject to shortability) or stand aside |
| Transitional | Reduce size; wait for a resolution |
| High volatility | Wider stops, smaller size, fewer trades |
| Event-heavy week | Avoid, or halve size |

## 3. Playbook

| Play | Condition | Entry | Invalidation |
|------|-----------|-------|--------------|
| Pullback to structure | Uptrend, price retraces to a tested support / 20–50 EMA | Bullish reaction close | Below the pullback low |
| Breakout + retest | Range/triangle breakout | Retest that holds | Back inside the range |
| Reversal after structure break | CHoCH + failed retest | Close back in the new direction | Beyond the pattern extreme |
| Base breakout | Long consolidation, volume contraction → expansion | Close above the base | Back inside the base |

## 4. Weekly process

```
Weekend
  1. Scan for regime: which indices/sectors are trending?
  2. Build a watchlist (5-10 names max) with a level map for each.
  3. For each: write the trigger, invalidation, T1/T2, and R:R.
  4. Discard anything failing the 1.5R gate.
  5. Note the week's event calendar.

Daily (10 minutes)
  1. Check if any trigger fired.
  2. If yes: execute per the plan, log it.
  3. If a position's invalidation is hit: exit. No renegotiation.
  4. Update trailing levels per the pre-written rule.
```

## 5. Failure modes

| Failure | Guard |
|---------|-------|
| Holding through results | Event-risk gate |
| Moving the stop "because it's a swing trade" | Never |
| Too many positions | Cap at 3–6 |
| Correlated positions counted separately | Aggregate sector risk |
| Chasing an extended move | Require a pullback or a retest |
| Ignoring the weekly timeframe | Always check one timeframe up |

## 6. A worked plan skeleton (fictional, illustrative)

```
Instrument   : ABC (NSE), daily
Regime       : trending up (ADX 27, price above rising 50-EMA)
Structure    : HH/HL x4; last HL 1_198; resistance 1_310
Play         : pullback to structure
Trigger      : daily close above 1_212 after a touch of 1_198-1_204
Entry zone   : 1_212-1_216
Invalidation : 1_192 (below the HL + 0.3 ATR)
Risk         : ~22
T1 1_248 (1.6R) · T2 1_276 (2.9R) · T3 1_310 (4.5R)
Trail        : after T2, below each new higher low
Gap risk     : results 2026-11-18 inside the horizon -> half size or exit before
```

## 7. Beginner summary (Hinglish)

**Swing trading** = kuch din se kuch hafte ka holding. **Beginner ke liye sabse theek style** — kyunki costs ka
asar intraday se bahut kam hota hai.

**Kaam ka tareeka:** uptrend mein **pullback** par kharido (support / 20-50 EMA), stop pullback low ke neeche,
targets structure se.

**Hafte mein ek baar** watchlist banao aur har stock ke liye trigger + stop + targets **pehle se** likho.

**Sabse bada risk:** result/overnight gap. Event se pehle **size aadha** karo ya exit kar do.

**Kabhi na karo:** stop ko "swing hai, thoda time do" bol kar neeche karna.

## 8. Validation notes

Daily data, 5 years minimum, costs 10–15 bps round trip, gaps filled at the open. Report per-year results and
per-regime breakdown.
