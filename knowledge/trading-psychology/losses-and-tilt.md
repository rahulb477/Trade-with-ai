# Losses, Streaks and Tilt

## 1. Losing streaks are arithmetic, not bad luck

With win rate `p`, the probability of at least one run of `k` losses in `n` trades is high even for good methods.
A useful approximation for the expected longest streak in `n` trades with loss probability `q = 1 − p`:

```
expected_longest_streak ≈ ln(n) / ln(1/q)
```

| Win rate | Loss prob q | n = 100 | n = 300 | n = 1000 |
|----------|-------------|---------|---------|----------|
| 60% | 0.40 | ~5 | ~6 | ~8 |
| 50% | 0.50 | ~7 | ~8 | ~10 |
| 40% | 0.60 | ~9 | ~11 | ~14 |
| 30% | 0.70 | ~13 | ~16 | ~19 |

**Implication:** if your method wins 40% of the time, you should *expect* ~11 losses in a row within 300 trades.
If your risk per trade is 2%, that streak is a 20% drawdown — and it is normal, not a signal that the method broke.

This is the single most valuable table in this directory. Most people abandon working methods because they never
computed it.

## 2. Tilt: what it looks like

| Symptom | Behaviour |
|---------|-----------|
| Revenge trading | Immediate re-entry after a loss, often larger |
| Size escalation | Increasing size to "get it back" |
| Rule erosion | Skipping the checklist "just this once" |
| Timeframe compression | Moving to 1-minute charts to have more action |
| Rationalisation | Finding a new indicator that "confirms" the desired direction |
| Selective memory | Recalling wins, forgetting losses |

## 3. Circuit breakers (define them in advance, in writing)

| Breaker | Example (educational, not advice) | Purpose |
|---------|-----------------------------------|---------|
| Per-trade risk | 0.25–1.0% of equity | Bounds any single error |
| Daily loss limit | Stop after −2% | Prevents a bad day becoming a bad month |
| Weekly loss limit | Halve size after −4% | Detects regime mismatch |
| Consecutive losses | After 4, halve size until 2 wins | Handles streak clustering |
| Max drawdown | Stop and review at −15% | Preserves the account |
| Time-based | No trades in the first 15 minutes | Avoids the noisiest period |
| Event-based | No new positions into scheduled binary events | Avoids gaps |

The critical detail: they are written **before** the losing streak, because during it you will not want them.

## 4. What to do during a drawdown

```
1. Halve size. Not double. The instinct is exactly backwards.
2. Check the regime: did the market change character (ADX, volatility, trend structure)?
3. Check execution: is the rule-breach rate rising?
4. Check the sample: is this drawdown inside the historical distribution for your method?
5. Pause if the breaker triggers. Review the journal before resuming.
6. Change one thing at a time, and only after the review.
```

## 5. The two things that end accounts

1. **Size** — a single oversized position, or size escalation during a drawdown.
2. **Refusal to accept a loss** — widening stops, averaging down, holding through events.

Neither is an analytical failure. Both are psychological. That is why this directory exists.

## 6. Loss classification (do this, weekly)

| Class | Definition | Action |
|-------|-----------|--------|
| A | Rule followed, thesis wrong | None — this is the cost of a positive-expectancy method |
| B | Rule broken | Fix the process rule that allowed it |
| C | Exogenous (gap, halt, news) | Reduce event exposure; size for gaps |
| D | Execution (slippage, error) | Improve instrument choice and order handling |

Only B is a discipline problem. Only D is an infrastructure problem. A and C are business costs.

## 7. Beginner summary (Hinglish)

**Lagatar losses normal hain — ganit hai, badkismati nahi.**

Agar win rate 40% hai, to 300 trades mein **~11 lagatar losses** aana expected hai. Agar risk 2% hai, woh 20%
drawdown hai — aur woh normal hai.

**Isliye:** drawdown dekh kar method chhodna sabse aam galti hai. Pehle compute karo ki streak expected hai ya nahi.

**Tilt ke symptoms:** loss ke turant baad wapas entry, size badhana, checklist skip karna, 1-minute chart par
switch karna.

**Circuit breakers pehle se likho:** daily loss limit, consecutive-loss rule, max drawdown. Streak ke **dauraan**
aap yeh nahi likh paoge.

**Drawdown mein kya karo:** size **aadha** karo — double nahi. Phir regime check karo, journal padho.

**Account do cheezon se khatam hota hai:** size, aur loss accept na karna.

## 8. Exercise

Using your own win rate, compute the expected longest losing streak over 300 trades. Then compute the drawdown
that streak would cause at 1% and at 3% risk. Write down the risk level you could survive both financially and
psychologically — and set your per-trade risk accordingly.

---
*See also: [`cognitive-biases.md`](cognitive-biases.md) · [`../risk-management/drawdown-and-survival.md`](../risk-management/drawdown-and-survival.md)*
