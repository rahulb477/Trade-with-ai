# Workflow — Trap Detection

A trap is a break that fails. Detecting one is the difference between a stopped-out trade and a profitable one in
the opposite direction — but **do not cry trap without evidence.**

## Step 1 — Nine trap types

| Trap | Definition | Evidence needed |
|------|-----------|-----------------|
| **Bull trap** | Upside break, then close back below | Prior resistance, break, then close inside |
| **Bear trap** | Downside break, then close back above | Prior support, break, then close inside |
| **Fake breakout** | Any break that reverses quickly | Break + reversal within 1–3 bars |
| **Fake breakdown** | Mirror | |
| **Liquidity sweep** | Wick beyond a level, close back inside | Prior identifiable level + close back inside + reaction |
| **Failed retest** | Break holds initially, then the retest fails | Break, retest, then close back through |
| **Stop-hunt hypothesis** | Obvious stop cluster just beyond a level, briefly taken | Cluster identifiable + wick + reclaim |
| **False reversal** | Structure break that immediately negates | Break + reclaim + new extreme in the old direction |
| **Volume divergence** | Price breaks, volume does not confirm | Break with below-average volume |

## Step 2 — Evidence checklist (all must hold for a confirmed trap)

- [ ] **A prior identifiable level** (≥2 touches). Without it, there is nothing to trap.
- [ ] **A break occurred** (a trade beyond the level).
- [ ] **A close back inside** — on the break bar or within 1–3 bars. A wick alone is insufficient.
- [ ] **A visible reaction** away from the level.
- [ ] **No immediate re-break** in the original direction.
- [ ] Volume evidence: either a spike on the sweep, or a collapse on the break.

Score it: 6/6 = confirmed trap; 4–5 = possible (label `POSSIBLE`); ≤3 = not a trap, probably noise.

## Step 3 — Distinguish trap from retest

| | Trap | Retest |
|---|------|--------|
| Close after the break | Back **inside** the prior range | Stays **outside**, at/above the level |
| Follow-through | Fails | Holds |
| Volume on the return | Often high (aggressive rejection) | Typically lower |
| Structure | Breaks down | Holds |

This is the single most common misclassification in retail analysis: calling a normal retest a "trap", or calling a
trap a "retest".

## Step 4 — What to do with a confirmed trap

```
1. Do not enter in the breakout direction. Cancel that scenario.
2. The trap creates the opposite setup: entry on the close back inside (or its retest),
   invalidation beyond the trap's extreme.
3. Recompute R:R. Traps often give excellent R:R because the invalidation is close.
4. Note that a trap is only "confirmed" after the close back inside — before that it is a hypothesis.
```

## Step 5 — Language discipline

| ✅ | ❌ |
|----|----|
| "Price closed back below 1,240 within two bars of the break — that is a failed breakout (bull trap)." | "Smart money trapped the retailers above 1,240." |
| "There is a stop cluster just below 1,196 (three equal lows); a sweep is plausible." | "They will definitely hunt stops at 1,196." |
| "Volume was 0.6× average on the break, which is consistent with a fakeout." | "This is a fakeout." |

## Step 6 — Log it
Record trap hypotheses **before** the outcome in the prediction record, with the evidence score. Later, evaluate how
often the hypothesis was right. That is how you learn whether your trap detection has any skill or is just
narrative.

## Beginner summary (Hinglish)

**Trap = jhootha break.** Price level todta hai, phir wapas andar aa jata hai.

**Confirm karne ke liye 4 cheezein:**
1. Pehle se level ho (2+ touches).
2. Price us level ke bahar jaye.
3. **Close wapas andar** aaye (wick nahi — close).
4. Wahan se reaction dikhe.

**Trap aur retest mein farq:** retest mein price level ke **bahar** rehta hai aur hold karta hai. Trap mein wapas
**andar** close ho jata hai. Yeh farq pehchan-na sabse zaroori hai.

**Kya karo:** breakout direction ki trade cancel karo. Trap ke close ke saath **opposite** direction ka setup banao,
stop trap ki extreme ke bahar.

**Kya mat likho:** "smart money ne trap kiya". Yeh verify nahi ho sakta — sirf behaviour likho.
