# Volume Profile

**Family:** Volume/levels · **No standard period** (session, composite, or anchored)
**Implementation:** `indicators.volume_profile(highs, lows, closes, volumes, bins=50)`

## 1. What it is

Instead of plotting volume against **time**, Volume Profile plots volume against **price**. For each price
bin, it sums the volume traded there. The result is a horizontal histogram that shows where the market spent
its effort.

Standard derived values:

| Term | Definition |
|------|-----------|
| **POC** (Point of Control) | The price bin with the highest traded volume |
| **Value Area** | The contiguous price band containing ~70% of total volume |
| **VAH / VAL** | Value Area High / Low — the boundaries of that band |
| **HVN** (High Volume Node) | A local volume peak — an area of acceptance |
| **LVN** (Low Volume Node) | A local volume trough — an area price moves through quickly |

## 2. Calculation (practical algorithm)

```
1. Determine the price range [min_low, max_high] over the chosen window.
2. Divide into N bins (commonly 50–100).
3. For each bar, distribute its volume across the bins its [low, high] spans.
   Simple approach: assign all volume to the bin containing the close.
   Better approach: proportional distribution across spanned bins.
4. POC = argmax(bin volume).
5. Value area: start at the POC and repeatedly add the adjacent bin with more volume until
   the cumulative volume reaches 70% of the total.
```

This repository's implementation uses the proportional-distribution method and a 70% value area, and
returns `(poc, vah, val, bins)`.

## 3. Interpretation

| Reading | Meaning |
|---------|---------|
| Price at the POC | Fair value; the market agrees here — often a magnet, often chop |
| Price above the value area | Accepted higher; the old VAH becomes support |
| Price below the value area | Accepted lower; the old VAL becomes resistance |
| Price in an LVN | Fast movement expected — little volume to absorb |
| Price returning to a prior POC | Common magnet behaviour |
| Naked POC (untested since forming) | Often cited as a target |

**The key concept is acceptance vs rejection.** High-volume nodes are places where the market agreed to
trade; low-volume nodes are places it refused to linger. Price tends to move quickly through LVNs and stall
in HVNs.

## 4. Limitations

- **Requires accurate volume with price granularity.** Bar OHLC volume is an approximation: you do not know
  where inside the bar the volume actually occurred. Assigning it to the close is a crude proxy.
- **Window dependence.** Session vs weekly vs composite gives different profiles. A result is only
  meaningful with the window stated.
- **No time dimension.** You cannot tell whether the volume at a price is old or recent.
- **Heavy computation** and platform-dependent implementations; bin count changes the shape.
- **Useless on low-volume instruments.**
- **Not available on most free chart screenshots** — do not pretend to read a profile that is not displayed.

## 5. Combining

- **Profile + structure**: a POC at a horizontal support is a strong confluence.
- **Profile + Fib**: a 0.618 retracement into an HVN is high quality.
- **Profile + VWAP**: session VWAP often coincides with the developing POC.
- **Profile + volume**: the raw panel tells you *when*, the profile tells you *where*.

## 6. Reading from a screenshot

Extractable: if a profile is drawn, the POC line position, the value-area band, and where price sits relative
to them; whether nodes are visible as dark/light bands.

Not extractable: exact prices without labels; the bin count; whether the profile is session or composite.

## 7. Worked example (illustrative)

```
Bins (simplified, 5 bins) with total volume 10 000:
  1_200–1_210 : 1 000
  1_210–1_220 : 3 500   <- POC
  1_220–1_230 : 2 500
  1_230–1_240 : 2 000
  1_240–1_250 : 1 000
Value area (70% = 7 000): start at POC 3 500 (+2 500 above = 6 000, +2 000 below = 8 000)
  -> include the 1_220–1_230 bin (6 000) then either neighbour; proportional rule picks the larger
  -> VAH ≈ 1_230, VAL ≈ 1_210 (approximately, depending on tie-breaking)
Price at 1_245 is above the value area -> accepted higher; VAH 1_230 is now a support reference.
See tests/indicators/test_volume_profile.py.
```

## 8. Beginner summary (Hinglish)

**Volume Profile kya hai?** Volume ko **time** ki jagah **price** par plot karna — matlab kis price par kitna
business hua.

**POC:** sabse zyada volume wala price — market ka "fair value".

**Value Area:** woh price band jahan 70% volume hua.

**Kaise padhein:**
- Price POC par = market agree karta hai, aksar chop.
- Price value area ke **upar** = naya higher value accept hua, purana VAH support ban sakta hai.
- Price **low volume node** mein = wahan volume nahi hai, isliye price jaldi bhaagta hai.

**Dhyan:** yeh volume data par depend karta hai — agar volume galat hai to profile bekaar hai.

## 9. Exercise

Build two profiles for the same stock: one for a single session, one for a month. Compare their POCs. Then
check how price behaved when it returned to each POC. Write one sentence about which window was more useful
and why the answer might differ by trading style.

---
*See also: [`vwap.md`](vwap.md) · [`obv.md`](obv.md) · [`../engines/order-flow/README.md`](../../engines/order-flow/README.md)*
