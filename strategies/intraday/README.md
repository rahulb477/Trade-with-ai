# Intraday Trading

**Horizon:** minutes to hours. **Holding:** within one session (closed before the close). **Trades per day:** 1–5.

**Status:** `DOCUMENTED` — method described, not validated.

## 1. Characteristics

| Attribute | Typical |
|-----------|---------|
| Analysis timeframe | 15m or 1H |
| Entry timeframe | 5m or 15m |
| Target | 1–3 ATR |
| Stop | 0.75–1.5 ATR, beyond structure |
| Win rate needed at 1:1.5 | ~40% (plus costs) |
| Key risk | Session-end square-off, gap-free by design, but cost-heavy |

## 2. India-specific constraints (non-negotiable in any plan)

| Constraint | Statement to include |
|------------|---------------------|
| Session | 09:15–15:30 IST |
| Cash-equity shorts | Must be squared off before the close |
| Circuit limits | Small caps can lock; stops may not fill |
| Expiry days | Index behaviour can be erratic |
| Costs | Delivery vs intraday STT differ — verify with the broker |

## 3. Documented plays

| Play | Setup | Trigger | Invalidation |
|------|-------|---------|--------------|
| Opening range breakout | First 15/30 min range defined | Close beyond the range with volume | Back inside the range |
| VWAP trend day | Price above VWAP, pullbacks holding VWAP | Reclaim close after a VWAP touch | Close below VWAP |
| Failed breakout (trap) | Sweep of a level, close back inside | Close back inside | Beyond the sweep extreme |
| Range fade | Range with ≥2 boundary touches, ADX < 20 | Rejection candle at the boundary | Close beyond the boundary |
| Continuation after pullback | 1H trend, 15m pullback to structure | 15m close back in trend direction | Below the pullback low |

## 4. Daily process

```
Pre-market (before 09:15)
  - note the prior day's high/low/close, and the pivot levels
  - note the index/sector context (if available)
  - note any scheduled event
  - write the two conditional plans (long trigger, short trigger) BEFORE the open

During the session
  - check the regime (opening range, VWAP relationship, ADX)
  - execute only pre-written triggers
  - no new ideas invented mid-session without the full checklist

Post-session
  - log every trade in R
  - note whether the plan was followed
```

## 5. Failure modes

| Failure | Guard |
|---------|-------|
| Overtrading | Maximum 2–3 trades/day rule |
| Holding a cash short past the close | Session-end rule |
| Trading the first 5 minutes | Wait for the opening range |
| Ignoring costs | Convert to R before taking the trade |
| Scaling into a losing intraday position | Never |

## 6. Beginner summary (Hinglish)

**Intraday** = ek hi session mein entry aur exit, market band hone se pehle.

**India mein:** 09:15–15:30. Cash equity short **close se pehle** band karna padta hai.

**Best practice:** subah **pehle se** do plans likho (long trigger, short trigger). Session ke beech mein naye ideas
mat banao.

**Pehle 5–15 minute avoid karo** — opening noise hota hai.

**Costs yaad rakho:** intraday mein costs R ka bada hissa hote hain.

## 7. Validation notes

Backtest with 5-minute bars, realistic slippage (5–10 bps for liquid names), and intraday cost assumptions.
Report per-year results to expose regime dependence.
