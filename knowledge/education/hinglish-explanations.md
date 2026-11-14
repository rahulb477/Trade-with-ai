# Hinglish Explanation Templates

Reusable patterns for explaining charts simply. Every analysis report must contain one such section.

## 1. Rules for good Hinglish explanation

1. **Short sentences.** One idea per sentence.
2. **Keep English trading terms in English** (breakout, stop loss, support) — that is how Indian traders speak. Do
   not translate "support" into something unrecognisable.
3. **Numbers stay identical** to the English section.
4. **No new claims** in the Hinglish section. It is a translation, not an addition.
5. **Explain the *why***, not just the what. "Price upar gaya" is a fact; "kyunki sellers thak gaye" is the
   explanation.
6. **Name the thing that would prove it wrong.** Every scenario needs its invalidation stated in both languages.
7. **Never use Hinglish to be vague or to avoid a commitment.** "Thoda upar ja sakta hai" is useless.

---

## 2. Template — overall market condition

```
Market ka haal: <bullish / bearish / sideways / confusion>
Kyun: price <pichhle high se upar> hai, <EMA ke upar> hai, aur <volume> bhi support kar raha hai.
Matlab: <ek line mein simple translation>.
Lekin: <ek cheez jo against hai>.
```

Example:

> Market ka haal: bullish. Price pichhle high 1,240 ke upar hai, 50-EMA ke upar hai, aur last 3 upar wali
> candles par volume average se zyada tha. Matlab: buyers abhi control mein hain. Lekin: 1,275 par ek bada
> resistance hai, isliye upar ki jagah seemit hai.

---

## 3. Template — candlestick pattern

```
Candle pattern: <naam>
Dikhne mein kaisa: <body chhoti / wick lambi / pichhli candle ko nigal liya>
Kahan bana: <support / resistance / level ke paas>
Matlab: <ek line>
Confirm hone ke liye: <agli candle ko kya karna hai>
Agar fail ho jaye: <kya hoga>
```

Example:

> Candle pattern: hammer. Dikhne mein: body chhoti hai aur neeche ki wick lambi hai. Kahan bana: 1,196 ke support
> par, jo pehle do baar hold hua tha. Matlab: sellers ne price ko neeche giraya, par buyers ne wapas khareed
> liya. Confirm hone ke liye: agli candle ko 1,206 ke upar close karna hoga. Agar fail ho jaye (candle ki low ke
> neeche close), to matlab rejection jhoothi thi.

---

## 4. Template — the trade plan

```
Setup: <long ya short> — sirf tab jab <condition>
Entry: <price ya zone>
Stop loss: <price> — kyunki <reason>
Target 1: <price> (<R>R) · Target 2: <price> (<R>R)
Risk vs reward: <agar target 1 tak jaye to risk se kitna zyada>
Kya wait karna hai: <confirmation>
Kab setup cancel: <invalidation>
```

Example:

> Setup: long — sirf tab jab 15m candle 1,206 ke upar close kare. Entry: 1,206.5. Stop loss: 1,193 (hammer ki low
> 1,194 ke thoda neeche) — kyunki wahan se neeche close hone ka matlab hai rejection fail ho gayi. Target 1:
> 1,215 (0.6R) · Target 2: 1,232 (1.9R). Risk vs reward: T1 bahut kam hai, isliye T2 hi asli target hai. Kya wait
> karna hai: 1,206 ke upar close. Kab cancel: 1,193 ke neeche close.

---

## 5. Template — the honest WAIT

```
Abhi trade nahi.
Kyun: <teen specific reasons>
Kya chahiye: <ek specific confirmation>
Jab tak woh nahi milta, <kya karein — observe, ya kuch nahi>
```

Example:

> Abhi trade nahi. Kyun: (1) price range ke **beech** mein hai, na support par na resistance par; (2) ADX 13 hai,
> matlab trend nahi hai; (3) entry se target tak sirf 0.9R hai — risk se kam reward. Kya chahiye: ya to 1,196
> support par rejection candle, ya 1,245 resistance ke upar volume ke saath close. Jab tak woh nahi milta, sirf
> observe karo.

---

## 6. Template — explaining a trap

```
Yeh trap ho sakta hai.
Kaise pata chalega: <behaviour>
Kyun: <reason>
Kya karein: <action>
```

Example:

> Yeh bull trap ho sakta hai. Kaise pata chalega: price 1,240 ke upar gaya, par agli do candles wapas 1,240 ke
> neeche close ho gayi. Kyun: breakout accept nahi hua — jo log upar khareede the, woh loss mein hain. Kya karein:
> long mat lo. Neeche ki trade tabhi socho jab 1,220 (pre-breakout low) ke neeche close ho.

---

## 7. Template — explaining indicators simply

```
<Indicator> kya bata raha hai: <value aur position>
Iska matlab: <simple>
Iska matlab NAHI hai: <common misconception>
Isliye: <how much weight to give it>
```

Example:

> RSI 61.3 par hai. Iska matlab: momentum bullish hai, par overbought nahi. Iska matlab **nahi** hai ki price
> girne wala hai — strong trend mein RSI 80 par hafton reh sakta hai. Isliye: isse sirf confirmation maano, entry
> trigger nahi.

---

## 8. Template — volatility and size

```
Volatility: ATR <value> hai, matlab ek din mein price average <x>% hilta hai.
Isliye stop: <distance> rakha hai.
Position size: <units> (risk 1% maankar) — kyunki agar stop hit ho to loss ek fixed amount ho.
Dhyan: agar result aane wala hai, to size aadha karo — kyunki gap mein stop kaam nahi karta.
```

---

## 9. Things never to say in Hinglish

| Don't | Why |
|-------|-----|
| "Pakka upar jayega" | No such certainty exists |
| "Sure shot setup" | Same |
| "Smart money aa gaya" | Unverifiable |
| "Isme 90% win rate hai" without a source | Fabricated statistic |
| "Aap sab kuch lagao" | Real-money advice |
| "Thoda dekh lena" | Vague; give a specific level |

---

## 10. Checklist before finishing the Hinglish section

- [ ] Every price level matches the English section exactly
- [ ] Every scenario has an invalidation
- [ ] No new claims were introduced
- [ ] A beginner could repeat the plan back correctly
- [ ] No certainty language, no unfalsifiable claims
- [ ] It is short enough to actually be read
