# Triple Top

**Type:** Reversal (topping) · **Bars:** typically 25–80

## 1. Shape
Three peaks at roughly the same price, with two troughs between them. The neckline is drawn at the **lower of
the two troughs** (the conservative choice) or a line through both.

## 2. Formation rules
| # | Rule |
|---|------|
| 1 | Prior **uptrend** |
| 2 | Three peaks at approximately equal prices (1–3% tolerance) |
| 3 | Two distinct troughs between them, at comparable depths |
| 4 | Each peak/trough is a real swing |
| 5 | Volume generally declining across the three peaks |
| 6 | Confirmation: a **close below the neckline** |

**Triple top vs H&S:** in an H&S the middle peak is *clearly* higher. In a triple top all three are comparable.
If the middle is only marginally higher, the distinction is a judgement call — say so.

## 3. Volume
Declining volume across the three attempts is the classic signature: the market repeatedly tries the same
level and each attempt is weaker. A volume *increase* on the third peak changes the read — the level may be
about to be absorbed.

## 4. Confirmation, entry, measurement
```
Confirmation : close below the neckline, volume ≥ 1.3× average
Entry        : neckline break, or a failed retest of the neckline
height       = |peak − neckline|
target       = neckline − height
```
Worked: peaks ~860, neckline 838 (lower trough) → height 22 → target 816.

Because the three peaks create a wide topping structure, the stop (above the peaks) is often far, which
frequently makes the R:R poor. **Check the arithmetic before presenting a scenario.**

## 5. Invalidation
Close above the peaks (the level was finally absorbed — a breakout, not a reversal); close back above the
neckline after a break; the third peak meaningfully higher than the first two (that is a continuation).

## 6. Common false signals
| False signal | Guard |
|--------------|-------|
| Three touches of resistance that keep getting rejected but never break | Requires the neckline break |
| Patterns on very short timeframes | Noise |
| Peaks spread over years | Not a single pattern; use long-term structure |
| Wide tolerance | Enforce 1–3% |
| Break into major support | Room check |
| Ignoring the *rise* in volume on the third peak | Re-read the volume profile |

## 7. Why triple tops are rarer than they look
Price often breaks a double-top level on the third attempt — which converts the "triple top" into a breakout.
So the pattern you *think* you see at the time frequently resolves upward. This is a documented reason to wait
for confirmation rather than pre-empting.

## 8. Worked example (fictional)
```
Instrument MNO · Daily · uptrend 780 → 862
Peak 1: 858 · trough 840 · Peak 2: 861 · trough 838 · Peak 3: 859
Tolerance ≤ 0.4% ✔ · neckline = 838
Breakout: close 834 on 1.4× volume → CONFIRMED
height = 858 − 838 = 20 → measured target 818
Invalidation: close above 864
Retest entry 836 · stop 864 · risk 28 · T1 818 = 0.64R FAIL
Verdict: WAIT — the stop is wide relative to the measured move. The tradeable version would need a
tighter invalidation (e.g. above the third peak's minor lower high at 852 → risk 16 → 1.13R, still marginal).
Being explicit about this is the correct output.
```

## 9. Beginner summary (Hinglish)
**Triple top:** teen barabar highs, beech mein do troughs. Neeche wale trough ki line = neckline.

**Matlab:** market teen baar same level try karta hai aur har baar fail hota hai, volume bhi girta jata hai.

**Signal:** neckline ke neeche close.

**Target:** neckline − height. **Stop:** peaks ke upar.

**Important:** triple top aksar "double top" jaisa dikhta hai aur teesri koshish mein toot jata hai (upar ki
taraf). Isliye confirmation ke bina pre-empt mat karo.

## 10. Exercise
Find one triple top that reversed and one that broke upward on the third attempt. Compare the volume on the
third peak in each. Write the single check that would have distinguished them — and whether it was visible in
real time or only in hindsight.

---
*See also: [`triple-bottom.md`](triple-bottom.md) · [`head-and-shoulders.md`](head-and-shoulders.md) · [`rectangle.md`](rectangle.md)*
