# Rejection

## 1. Definition
**Rejection** is a visible refusal by the market to accept a price: price trades at a level, fails to hold
beyond it, and closes back on the other side. It is seen most clearly as a **long wick** or as a candle that
closes away from its extreme.

## 2. Forms of rejection

| Form | Appearance | Reading |
|------|-----------|---------|
| Wick rejection | Long upper/lower wick, close away from the extreme | Intraday refusal of a price |
| Close rejection | Price trades beyond a level but closes back inside | Failed break |
| Multiple-bar rejection | Several attempts at a level, each closing back | A well-tested level |
| Volume rejection | Huge volume with no price progress | Absorption |
| Gap rejection | Gap up that closes back in the prior range | Failed enthusiasm |

## 3. What makes rejection meaningful

Rejection alone is weak. It matters when:

1. It occurs **at a level** (support, resistance, round number, prior swing).
2. The candle that shows it is **large relative to recent range** (≥1.2× average).
3. **Volume** supports it — either expansion (a real battle) or a distinct spike (capitulation).
4. The **close** is decisively on the rejection side (not mid-range).
5. The **next candle** confirms (continues away from the rejected price).
6. The **higher timeframe** context is consistent with the rejection.

## 4. Common rejection candles

| Candle | Location | Reading |
|--------|----------|---------|
| Hammer | Support after a decline | Bullish rejection of lower prices |
| Shooting star | Resistance after an advance | Bearish rejection of higher prices |
| Hanging man | Resistance after an advance | Weak bearish rejection |
| Inverted hammer | Support after a decline | Weak bullish rejection |
| Long-legged doji | Any level | Two-sided rejection — indecision |
| High wave | Any level | Violent two-sided rejection |

Details in `knowledge/candlesticks/`.

## 5. Absorption vs rejection

A subtle but important distinction:

- **Rejection**: price goes to a level, fails, and moves away. Visible as a wick and a close back.
- **Absorption**: heavy volume at a level with little price movement — someone is taking the other side of
  every order. Visible as high volume with a small range.

Absorption often *precedes* a reversal by several bars; rejection *is* the reversal attempt. Distinguishing them
requires volume data. Without a volume panel, state that the distinction cannot be made.

## 6. Confirmation and entry

```
Bullish rejection at support:
  trigger      : next candle closes above the rejection candle's high (or the body's high)
  entry        : trigger level ± 0.1 ATR
  invalidation : below the rejection candle's low
  targets      : nearest swing high, then measured move

Bearish rejection at resistance: mirror.
```

Entering *on* the rejection candle's close is possible but weaker — the confirmation candle is what converts
"attempt" into "result".

## 7. Failure modes

| Failure | Meaning |
|---------|---------|
| Price returns and breaks the rejected extreme | The rejection was momentary; continuation in the original direction |
| Repeated rejections at the same level | The level is strong — but eventually it breaks; the *last* rejection is always the losing one |
| Rejection with no volume | Possibly illiquidity, not intent |
| Rejection in the middle of nowhere | No information |

## 8. Common errors

| Error | Guard |
|-------|-------|
| Trading every long wick | Require a level and a confirmation close |
| Reading wicks on a Heikin-Ashi chart | HA synthesises OHLC — refuse |
| Assuming rejection = reversal | It is an attempt; the confirmation candle decides |
| Ignoring the higher timeframe | A rejection against a strong trend fails often |
| Counting five rejection candles at one level as five signals | It is one level being tested repeatedly |

## 9. Beginner summary (Hinglish)

**Rejection kya hai?** Market ne ek price ko **accept nahi kiya** — wahan gaya, fail hua, aur wapas aa gaya.
Dikhne mein lambi wick jaisa.

**Kab matlab rakhta hai?**
1. Kisi **level** par ho (support/resistance).
2. Candle **badi** ho (average se).
3. **Volume** support kare.
4. Close rejection side par ho.
5. Agli candle confirm kare.

**Entry:** rejection candle ki high todne par (bullish case), stop uski low ke neeche.

**Galti:** har lambi wick ko rejection samajhna. Level ke bina wick sirf noise hai.

## 10. Exercise

Find five long-wick candles. For each, note: was there a level? Volume? Did the next candle confirm? Then compute
how many would have passed all three checks. Write down whether the filter changed your view of "rejection
candles" as a category.

---
*See also: [`retest.md`](retest.md) · [`../candlesticks/hammer.md`](../candlesticks/hammer.md) ·
[`../candlesticks/shooting-star.md`](../candlesticks/shooting-star.md)*
