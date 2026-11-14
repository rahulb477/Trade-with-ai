# Workflow — Breakdown Analysis

## Step 1 — Is there a level and compression?
- [ ] Support tested ≥2 times
- [ ] Compression/distribution above it
If not → no breakdown setup.

## Step 2 — Break state
Pre-break / break (unconfirmed) / confirmed (close below + follow-through + volume) / failed (reclaim).

## Step 3 — Volume nuance
Unlike breakouts, a **very** high volume breakdown bar with a long lower wick and a close back near the level can
signal **absorption** rather than genuine selling. Check the close position:
- Close near the low → genuine.
- Close near the high with a long lower wick → suspect a trap.

## Step 4 — Room below
Same ATR test as breakouts. Support immediately beneath makes the setup untradeable.

## Step 5 — Trap audit
Breakdowns at obvious support are prime stop-hunt territory. Specifically check:
- Are stops clustered just below the level (equal lows)?
- Did price sweep below and close back inside?
- Did volume collapse after the break?
- Is a major support level directly beneath?

## Step 6 — Shortability constraints

| Constraint | Check |
|------------|-------|
| Market rules | India: intraday cash-equity shorts must be squared off by session close |
| Borrow availability | Delivery shorting needs an SLB facility |
| Event risk | Results/policy within the horizon |
| Liquidity | Borrow/exit availability |
| Circuit limits | Price can lock at the band |

State the constraint explicitly in the plan. See `markets/india/`.

## Step 7 — Entry design
Same three styles as breakout analysis (break close / follow-through / failed retest from below). The **failed
retest from below** is usually the best R:R.

## Step 8 — Output
Mirror the breakout template, with the shortability note and the event-risk gate.
