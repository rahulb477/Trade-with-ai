# Capability Detection

Agents differ wildly. This module defines how to probe what the current host can do, and — more
importantly — how to behave when something is missing.

**Core rule:** a missing capability narrows the claims you make. It never licenses invention.

---

## 1. The capability block

Produce it once per session, keep it, and paste a summary into report section 10.

```yaml
capabilities:
  vision_input:      yes | no | unverified
  filesystem_read:   yes | no
  web_search:        yes | no | untested
  web_fetch:         yes | no | untested
  code_execution:    yes | no
  persistence_write: yes | no
  ocr_available:     yes | no | via-host
  notes: >
    Anything unusual: image is downscaled, tool returns 403, python available but no numpy, etc.
```

---

## 2. Probes

Run the cheapest probe first. Never assume; never over-probe (it wastes the user's time).

### 2.1 Vision

| Probe | Result |
|-------|--------|
| An image is present in context and you can describe non-text visual detail (colours, shapes, layout) | `yes` |
| Only a filename or a text placeholder is present | `no` |
| An image exists but is low-resolution such that text is unreadable | `yes` with `quality: poor` |

Test question to yourself: *"Can I state the colour of the last candle without guessing?"* If no,
vision is not usable — even if an image is technically attached.

### 2.2 Filesystem read

Try to read `SKILL.md`. Success → `yes`. Failure → `no`, and continue from the summaries embedded
in the conversation.

### 2.3 Web search / fetch

Single cheap query. Outcomes:

| Outcome | Classify |
|---------|----------|
| Returns dated results with URLs | `web_search: yes` |
| Returns results but fetch of a URL fails | `web_search: yes`, `web_fetch: no` |
| Returns nothing / errors / not offered | `web_search: no` |
| Works but all results are undated | `web_search: yes, quality: low` — never cite without a date |

Do not retry more than twice. Do not attempt to work around a blocked host.

### 2.4 Code execution

Try a trivial computation (`python3 -c "print(2+2)"`) or check whether a shell/exec tool exists.
Note available libraries: numpy/pandas presence changes what you can compute. This repository's own
library is **stdlib-only**, so absence of numpy is never blocking.

### 2.5 Persistence

Attempt a write to `journal/`. Success → `yes`. Read-only or absent → `no`; print records inline.

---

## 3. Behaviour matrix

| Missing | What you must not do | What you must do |
|---------|---------------------|------------------|
| Vision | Describe a chart you cannot see; infer from the filename | Request a transcription using the template in §4 |
| Filesystem | Invent content of knowledge modules | Use `SKILL.md` summaries; state reduced depth |
| Web | State news, flows, or macro as fact | Write the standard "web research unavailable" paragraph |
| Fetch | Summarise a page you could not open | Cite only the headline/snippet you actually saw, labelled as such |
| Code | Present hand arithmetic as tool output | Show the arithmetic; label it "manual calculation"; double-check |
| Persistence | Claim a record was saved | Print the record with `NOT SAVED` in the header |

---

## 4. Transcription request template (vision unavailable)

> I can't see the image itself — only that a file is attached. To analyse this properly, paste:
> 1. Instrument and exchange
> 2. Timeframe
> 3. Last traded price
> 4. The last 5 candles, e.g. `bull, small body, long lower wick`
> 5. Nearest visible support and resistance
> 6. Whether volume is rising, falling, or spikes on certain bars
> 7. Any indicator values printed as numbers (RSI, MACD, etc.)
>
> With those I can do a full structural and pattern analysis. Without them, I can only explain
> concepts.

---

## 5. Degraded-mode output templates

### 5.1 No web research

> **Web research unavailable in this environment.** No news, flow, sector or macro context was
> retrieved. The analysis is technical and structural only. Event risk — results, policy
> decisions, expiry — is unquantified and must be checked independently before acting on any
> scenario.

### 5.2 No vision

> **Chart image not readable by this agent.** The analysis below is based on the values you
> supplied in text, not on the image. Structure and levels are therefore as reliable as your
> transcription.

### 5.3 No code execution

> **Calculations performed manually.** Arithmetic is shown step by step. Rounding is to two
> decimals. Verify before relying on it.

### 5.4 No knowledge files

> **Knowledge modules not loaded** (no filesystem access). The answer uses the entry-point summary
> of `SKILL.md`. Deeper pattern rules and worked examples are unavailable in this session.

### 5.5 Partial vision (quality 2–4)

> **Screenshot quality is poor** (score N/10: <reasons>). I can describe the apparent structure but
> not quantify levels. Re-capture with the price axis visible and 100+ candles to get a full report.

---

## 6. Anti-patterns

| Anti-pattern | Consequence |
|--------------|-------------|
| Claiming browsing when the tool returned nothing | Fabricated news — the single worst failure in this domain |
| "Analysing" an image you cannot see | Fabricated chart reading |
| Producing a precise RSI value from a line's pixel height | Fabricated indicator reading |
| Saying "I've verified this with live data" without a provider | Fabricated authority |
| Silently switching to a different instrument because the ticker was unclear | Wrong analysis presented as confident |
| Hiding the degraded mode from the user | User over-trusts the output |

---

## 7. Recovery

If a capability later becomes available mid-session (the user enables browsing, supplies a second
screenshot, or provides a data file):

1. Re-run the affected stages.
2. State which conclusions changed and which held.
3. If a capability disappeared, re-state the new limitation rather than continuing as if it were
   still present.

---

*See also: [`../integrations/agent-adapters/generic.md`](../integrations/agent-adapters/generic.md) ·
[`../docs/limitations.md`](../docs/limitations.md)*
