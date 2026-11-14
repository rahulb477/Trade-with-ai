# Inverse Head and Shoulders

**Type:** Reversal (bottoming) · **Bars:** typically 20–100

## 1. Shape

Three troughs: left shoulder, a **lower head**, and a higher right shoulder, with a **neckline** across the two
intervening peaks. It is the mirror of the H&S and is often the more reliable of the two, because market
bottoms tend to be formed with visible capitulation and recovery rather than the gradual decay of tops.

```
     R      neckline      neckline   L
      ╲    ╱        ╲    ╱
       ╲  ╱          ╲  ╱
        ╲╱            ╲╱
         ╲            ╱
          ╲          ╱
           ╲        ╱
            ╲      ╱
              ╲  ╱
              head (lowest)
```

## 2. Formation rules

| # | Rule |
|---|------|
| 1 | Prior **downtrend** exists |
| 2 | Three troughs; the middle (head) is the lowest |
| 3 | Shoulders roughly comparable and higher than the head |
| 4 | Neckline through the two peaks between the troughs |
| 5 | Each trough is a real swing low (multiple bars) |
| 6 | Confirmation: a **close above the neckline** |

## 3. Volume expectations

| Stage | Expected |
|-------|----------|
| Left shoulder | High volume (panic selling) |
| Head | Often the highest volume of all — capitulation spike |
| Recovery to neckline | Rising volume |
| Right shoulder | Lower volume than the head (sellers exhausted) |
| Neckline break | **Strong expansion** — the confirmation |

The head-is-the-volume-climax profile is what distinguishes a genuine bottom from a pause in a downtrend.

## 4. Confirmation and entry

```
Standard     : close above the neckline
Conservative : close above the neckline + retest of the neckline that holds
Aggressive   : break of the right shoulder's minor high (earlier, weaker)
Volume filter: breakout ≥ 1.3–1.5 × 20-bar average
```

## 5. Measurement

```
height = |neckline − head|
target = neckline + height
```

Worked: head 480, neckline 520 → height 40 → target 560.

Also check the target against overhead structure: the pattern often stalls at the **prior breakdown level**
or a major MA. Note both.

## 6. Invalidation

| Event | Meaning |
|-------|---------|
| Close back below the neckline after the break | Failed pattern; a bull trap |
| Close below the head | Structure destroyed; downtrend resumed |
| Neckline steeply sloped | Measured move unreliable |
| Right shoulder below the head | Not an inverse H&S |

## 7. Common false signals

| False signal | Guard |
|--------------|-------|
| No prior downtrend | Rule 1 |
| "Head" is only marginally lower than the shoulders | Require a clear head |
| Neckline through the wrong peaks | Use the two reaction highs |
| Break on a wick | Require a close |
| Break with no volume | Volume filter |
| Pattern forms at heavy overhead resistance | Room check |
| Very short timeframe | Noise |

## 8. Why bottoms often look different from tops

Two documented asymmetries worth knowing:

1. **Volatility is higher at bottoms.** Declines are faster and more panicked; bottoms have wider ranges and
   longer wicks.
2. **Volume behaves differently.** Tops often show *declining* volume into the peak (distribution is quiet),
   while bottoms often show a *spike* (capitulation). This is why the volume profile across the pattern differs
   between H&S and inverse H&S.

These are tendencies, not rules; state them as such.

## 9. Worked example (fictional)

```
Instrument DEF · Daily · downtrend 620 → 470
Left shoulder 492 (vol 3.2M) · head 470 (vol 5.8M — climax) · right shoulder 486 (vol 2.1M)
Neckline through peaks 508 and 512 → ~512 at the break
Breakout: close 516 on 4.4M (1.9× average) → CONFIRMED
height = 512 − 470 = 42 → measured target 554
Structural target: prior breakdown level 545 (nearer); 200-EMA at 548
Invalidation: close below 502 (neckline − buffer)
Retest entry 513 · stop 501 · risk 12 · T1 545 = 2.7R · T2 554 = 3.4R
```

## 10. Beginner summary (Hinglish)

**Inverse head and shoulders:** downtrend ke end mein teen troughs — beech wala sabse neeche (head), dono side
wale upar (shoulders). Dono peaks ko jodne wali line neckline.

**Matlab:** head par sabse zyada volume (panic selling / capitulation), phir selling thak jati hai, aur price
neckline ke upar close karke confirm karta hai.

**Target:** neckline + pattern ki height.

**Stop:** neckline ke neeche (retest entry par sabse tight).

**Yaad rakho:** bottoms mein volume spike hota hai, tops mein volume girta hai — dono symmetric nahi hote.

## 11. Exercise

Compare one genuine inverse H&S with one pattern that failed. For each, record: head volume vs left-shoulder
volume, breakout volume multiple, and whether the neckline was retested. Write down which two checks would have
eliminated the failed one — and whether they would also have eliminated the good one.

---
*See also: [`head-and-shoulders.md`](head-and-shoulders.md) · [`double-bottom.md`](double-bottom.md) ·
[`../engines/market-intelligence/`](../../engines/market-intelligence/)*
