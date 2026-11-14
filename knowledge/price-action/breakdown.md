# Breakdown

## 1. Definition
A **close below a defined support level** after compression above it. The mirror of a breakout, with important
asymmetries (§6).

## 2. Anatomy of a high-quality breakdown

| Component | Requirement |
|-----------|-------------|
| Compression before | Range, triangle, distribution, or a failed base |
| Level quality | ≥2 prior touches |
| Close below | Decisive, not a wick |
| Volume | ≥1.3–1.5× average on the breakdown bar |
| Follow-through | Next bar remains below the level |
| Retest | The broken level is retested from below and rejects |
| Room below | No major support immediately beneath |
| Context | Higher timeframe not strongly up |

## 3. Outcomes

```
1. Breakdown -> follow-through
2. Breakdown -> retest from below fails -> run
3. Breakdown -> immediate reclaim   (bear trap; a bullish signal)
4. Breakdown -> chop around the level (no trade)
```

Outcome 3 is common: breakdowns at obvious support are prime stop-hunt territory, because stops cluster just
below. See [`../workflows/trap-detection.md`](../../workflows/trap-detection.md).

## 4. Entry approaches

| Approach | Entry | Stop | Notes |
|----------|-------|------|-------|
| Breakdown close | On the close below | Back above the level | Most false signals |
| Breakdown + follow-through | Next bar staying below | Back above | Fewer traps |
| Failed retest from below | On the rejection at the level | Above the level | Best R:R, best quality |
| Pre-empt intraday | Before the close | Tight | Highest failure rate |

## 5. Volume
Same rules as a breakout: expansion required. One nuance — a breakdown on **very** high volume sometimes marks
capitulation and is followed by a sharp reversal. Distinguish:

- High volume + close near the low + follow-through → genuine breakdown.
- High volume + long lower wick + close back near the level → absorption, possible trap.

## 6. Asymmetries that matter

| Feature | Breakdown vs breakout |
|---------|----------------------|
| Speed | Breakdowns tend to be faster (panic, margin calls) |
| Reversals | Recoveries from breakdowns can be violent (short covering) |
| Volume signature | Breakdowns are more likely to show a capitulation spike |
| Shorting constraints | In India, cash-equity intraday shorts must be squared off by session close; delivery shorting needs an SLB facility. See `markets/india/` |
| Event risk | Results/policy announcements gapping a short position against you can be severe |

## 7. Invalidation
Close back above the broken support (a reclaim — often a strong bullish signal); two closes back above; the
breakdown bar's high taken out.

## 8. Common errors

| Error | Guard |
|-------|-------|
| Shorting the breakdown at the low, directly above support | Wait for a retest from below |
| Ignoring volume | Volume filter |
| No room below (support immediately beneath) | Room check |
| Shorting into an event | Event-risk gate |
| Confusing a wick with a close | Require a close |
| Assuming a breakdown must continue because "it looks weak" | Structure describes the past |
| Ignoring the higher timeframe's uptrend | Context check |

## 9. Beginner summary (Hinglish)

**Breakdown kya hai?** Price support ke **neeche close** kar de.

**Achha breakdown:** pehle compression, level 2+ baar test, breakdown par **volume**, aur neeche target tak
**jagah**.

**Sabse achha entry:** broken level ka **retest from below** — price wapas level par aaye aur reject ho jaye.

**Sabse bada trap:** support ke **theek neeche** short karna. Wahan stops cluster hote hain, price ek wick
maar kar wapas upar aa jata hai (bear trap).

**India specific:** intraday cash-equity short session end se pehle band karna hota hai — plan mein likho.

## 10. Exercise

Find three breakdowns. For each: note whether the breakdown was at an obvious "obvious support" (where stops
would cluster), the volume multiple, and whether price reclaimed the level. Then compare "short the breakdown"
versus "short the failed retest" outcomes. Report the difference and your sample size honestly.

---
*See also: [`breakout.md`](breakout.md) · [`retest.md`](retest.md) · [`../../workflows/breakdown-analysis.md`](../../workflows/breakdown-analysis.md)*
