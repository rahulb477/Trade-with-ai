# Stop-Loss Design

A stop is **the price at which your thesis is proven wrong.** Not a comfort threshold, not a round number you can
afford.

## 1. Types

| Type | Rule | Use when |
|------|------|----------|
| **Structural** | Just beyond the swing/pattern boundary that defines the setup | Default |
| **Volatility** | `entry ± k × ATR` (k = 1.5–2.5 swing) | No clean swing, or noisy instrument |
| **Hybrid** | Structural level + 0.25–0.5 × ATR buffer | Recommended default |
| **Percentage** | Fixed % from entry | Only when nothing structural exists — flag as crude |
| **Time** | Exit after N bars without resolution | Stagnant setups, event plays |
| **Trailing** | Chandelier (`highest_high − 3 × ATR`), Supertrend line, or below each new higher low | Locking trend profit |

## 2. What makes a *good* stop

1. **Causally linked to the thesis.** "If this fails, this is where I am wrong" — not "this is what I can afford".
2. **Outside the noise band.** At least ~0.25 ATR beyond the obvious level.
3. **Not exactly at a cluster.** Stops at obvious levels get swept.
4. **Defined before entry**, and unchanged after (except to move in your favour).
5. **Close enough that the position size is meaningful**, and far enough that normal noise does not trigger it.

## 3. The two failure modes

| Failure | Consequence |
|---------|-------------|
| **Too tight** | Stopped out by noise on correct theses; a high loss rate with high R:R that never materialises |
| **Too wide** | Large losses when wrong; position size becomes trivial; R:R fails |

The calibration: `stop_distance ≈ 1.5–2.5 × ATR` for swing setups, placed *behind* structure. If the structural
level is further than ~3 ATR away, the setup is probably not a good entry — find a closer one rather than
stretching the stop.

## 4. Buffers

```
buffer = 0.25 × ATR   (typical)
stop   = structural_level − buffer   (for a long)
```

Rationale: intraday wicks and spread noise around obvious levels. Without a buffer, a correct thesis is frequently
stopped by a spike.

## 5. Gap risk: the stop is not a floor

| Situation | Behaviour |
|-----------|-----------|
| Overnight gap through the stop | Fill at the open, often far worse than the stop price |
| Results announcement | Typical single-stock gaps of 5–20% |
| Circuit limits (India) | Price can lock at the band; you cannot exit |
| Halt/suspension | Position frozen |
| Illiquid market | No bid to fill at |

**Implication:** the stop limits planned loss, not maximum loss. For event-exposed positions, reduce size rather
than relying on the stop.

## 6. Never do these

| Don't | Why |
|-------|-----|
| Widen a stop after entry | Converts a controlled loss into an uncontrolled one |
| Move the stop to break-even too early | Guarantees getting scratched on correct trades |
| Place the stop at the exact level | That is where resting orders cluster |
| Use a percentage stop on a volatile instrument "because it worked on a calm one" | Volatility regimes differ |
| Average down a losing leveraged position | The classic ruin path |
| Trade without a stop "just this once" | The one time it hurts is the time it ends the account |

## 7. Trailing methods (comparison)

| Method | Character |
|--------|-----------|
| Below each new higher low | Structural, slower, gives back more |
| `highest_high − 3 × ATR` (chandelier) | Volatility-scaled, mechanical |
| Supertrend line | ATR-based, mechanical, whipsaws in ranges |
| MA-based (e.g. below 20-EMA) | Simple, lags in fast moves |
| Partial scale-out + trail remainder | Reduces giveback but caps upside |

No trailing method is optimal in all regimes; state which you use and why.

## 8. Report template

```
Invalidation   : 1,186
Basis          : below the 12 Nov swing low 1,188, minus a 0.11 ATR buffer (ATR 18 -> ~2 points)
Distance       : 18 points = 1.0 ATR = 1.5% of price
Why it voids   : a close below 1,186 breaks the higher-low structure that defines the setup
Gap risk       : results on 18 Nov are inside the intended horizon -> size reduced by half
```

## 9. Beginner summary (Hinglish)

**Stop loss ka matlab:** woh price jahan aapka **idea galat sabit ho jata hai** — woh price jo aap afford kar
sakte ho, woh nahi.

**Kaise choose karein:**
1. Structure dekho (swing low / pattern boundary).
2. Uske **thoda bahar** jao (0.25 ATR buffer), taaki normal wick se stop na hate.
3. Distance check karo: agar 3 ATR se zyada hai, to setup hi galat hai — stop ko stretch mat karo.

**Do galtiyan:**
- **Bahut tight** → noise se stop hit, sahi idea bhi fail.
- **Bahut wide** → loss bada, size chhota.

**Sabse zaroori:** gap risk. Stop "floor" nahi hai — result ke din price stop se bahut neeche open ho sakta hai.
Isliye event se pehle **size kam** karo.

**Kabhi na karo:** stop widen karna, ya bina stop trade lena.

## 10. Exercise

Take a completed trade idea. Identify three candidate stops: the tight structural one, the structural + ATR buffer
one, and a 2-ATR volatility stop. For each compute the position size at 1% risk and the R:R to the first target.
Then decide which you would use — and write one sentence on what you are trading off.

---
*See also: [`position-sizing.md`](position-sizing.md) · [`drawdown-and-survival.md`](drawdown-and-survival.md)*
