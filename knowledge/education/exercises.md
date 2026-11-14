# Exercises — Graded Set With Guidance

Work through these in order. Guidance is given, answers are deliberately not — the point is to build your own
judgement and to notice how small your sample is.

---

## Level 1 — Observation (no trading)

### 1.1 Candle anatomy
Take 10 consecutive candles. For each, compute `body/range`, `upper_wick/range`, `lower_wick/range`, and
`close_pos`. Classify each.

*Guidance:* do not name patterns yet. Just measure. You will find most candles are unremarkable — that is the
lesson.

### 1.2 Level identification
Find every price with ≥2 touches in a 100-candle window. Record the number of touches and the size of each
reaction in ATR.

*Guidance:* most beginners over-count. Swings within 0.4 ATR of each other are the same zone.

### 1.3 Swing structure
Fix `k=3`. Mark every swing high and low. Classify the sequence.

*Guidance:* write down `k` before you start and do not change it.

---

## Level 2 — Recognition

### 2.1 Pattern audit
Find three candlestick patterns from `knowledge/candlesticks/`. For each, audit the formation rules numerically
and assign a status code (`CONFIRMED` / `DEVELOPING` / `POSSIBLE` / `UNCLEAR`).

*Guidance:* if you cannot fill in the numbers, you cannot confirm the pattern. Most "patterns" you see at first
will come out as `POSSIBLE`.

### 2.2 Trap or breakout?
Find three breakouts. For each, record: volume multiple, close vs wick, follow-through, retest. Then classify as
breakout or fakeout.

*Guidance:* do this *before* looking at what happened next. Then check.

### 2.3 Timeframe table
For one instrument, build the timeframe table for daily, 1H and 15m. Mark conflicts.

*Guidance:* include a column for "not viewed". Never fill it in by guessing.

---

## Level 3 — Arithmetic

### 3.1 R:R computation
For five historical setups, compute entry, stop, T1, T2, risk per unit, R for each target, and the R:R. Apply the
1.5R gate.

*Guidance:* at least two of the five should fail the gate. If none do, you are choosing your setups after seeing
the outcome.

### 3.2 Position sizing
Using equity 500,000 and risk 0.5%, compute size and notional for three stop distances (1 ATR, 2 ATR, 3 ATR).
Identify which breaches a 25% notional ceiling.

### 3.3 Cost conversion
For an intraday setup with a 6-point stop, estimate round-trip costs at 10 bps on a ₹1,200 stock. Convert to R.
Recompute the R:R after costs.

*Guidance:* 10 bps on 1,200 = 1.2 points one way. Round trip ≈ 2.4 + slippage. With a 6-point stop, that is
≈0.4R+ — enough to destroy a 1R target.

---

## Level 4 — Decisions

### 4.1 The WAIT case
Construct three situations where the correct verdict is `WAIT`. State the specific failing condition for each.

*Guidance:* a WAIT without a named failing condition is just indecision.

### 4.2 The insufficient-data case
Take a chart screenshot with a cropped price axis. Write the `INSUFFICIENT DATA` report — what is missing, what
you can still say, what you cannot.

*Guidance:* this is a skills test, not a cop-out. A good one describes the structure qualitatively and refuses the
numbers.

### 4.3 Scenario construction
For one chart, write Scenario A (bullish), Scenario B (bearish) and Scenario C (no trade), each with a specific
trigger, invalidation and targets.

*Guidance:* A and B should not be predictions — they are conditional plans. Both should be plausible.

---

## Level 5 — Research discipline

### 5.1 Sample size reality check
Record the outcome of 15 occurrences of one pattern. Compute the win rate and its 95% confidence interval.

*Guidance:* with n=15 the interval will be roughly ±25 percentage points. Write down what that means for your
confidence in the pattern.

### 5.2 Bias hunt
Take a backtest (yours or an example). Identify at least two potential biases and state how each would bias the
result (up or down).

### 5.3 Journal audit
Review five of your own past analyses. For each, check: did you state the invalidation? Did you state what was
missing? Did you claim anything you could not verify?

*Guidance:* most people find at least one unfalsifiable claim per analysis. That is the starting point for
improvement.

---

## Self-assessment rubric

| Skill | Novice | Competent | Strong |
|-------|--------|-----------|--------|
| Candle reading | Names patterns by shape only | Audits rules numerically | Audits rules and context, assigns status codes |
| Levels | Draws lines freely | Requires 2 touches | Zones, ranked by touches/recency/confluence |
| Breakouts | Buys any break | Checks volume | Checks volume, room, retest, and plans the failure |
| Risk | Uses a mental stop | Uses a structural stop | Structural stop + ATR buffer + notional check + gap haircut |
| Timeframes | Uses one | Checks two | Declares every unviewed timeframe as unknown |
| Honesty | States opinions as facts | Admits uncertainty | Quantifies uncertainty and lists missing data |
| Refusal | Always produces a trade | Sometimes says wait | Produces WAIT with the specific failing condition |

Work until "Strong" in Risk and Honesty. Those two protect you when everything else is wrong.
