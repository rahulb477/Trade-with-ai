# API Configuration

**The core skill must work with zero configuration.** Everything here is optional.

## 1. Philosophy

| Requirement | Status |
|-------------|--------|
| API key to use the skill | **Not required** |
| Network access to use the skill | **Not required** |
| Configuration wizard | **Not provided and not needed** |
| Credentials stored in the repository | **Never** |

Without any credentials the repository runs in **offline knowledge mode**: education, methodology, chart reading
from an image, manual arithmetic. That is the default and it is fully functional.

## 2. Environment variables (the only supported mechanism)

```bash
# Example names only — the actual names depend on the provider's documentation.
export TI_MARKET_DATA_PROVIDER="your-provider-name"
export TI_MARKET_DATA_KEY="..."
export TI_NEWS_PROVIDER="your-news-provider"
export TI_NEWS_KEY="..."
export TI_CACHE_DIR="./cache"          # gitignored
export TI_LOG_LEVEL="INFO"
```

Rules:
1. Read from `os.environ` at runtime; never from a committed file.
2. Never log a key, and never include a key in an exception message or URL.
3. Fail loudly if a key is *required* by the chosen provider and absent — and fall back to offline mode with a
   clear message.
4. `.env` is gitignored; `.env.example` may be committed with placeholders only.

## 3. Fallback ladder

```
providers configured and healthy     -> FULL RESEARCH MODE
providers configured but erroring    -> retry x2, then cache, then OFFLINE MODE (marked STALE)
no providers, web tool available     -> WEB RESEARCH MODE (context only)
no providers, no web                 -> OFFLINE KNOWLEDGE MODE
```

The mode is always declared in report section 10.

## 4. Rate-limit and retry policy

```python
RETRY = 2                      # total attempts = 3
BACKOFF = [1, 3]               # seconds; exponential with jitter
TIMEOUT = 10                   # seconds per request
ON_RATE_LIMIT = respect the reset header if provided, else abort and degrade
```

Never hammer a provider. Never rotate keys to evade limits. Never scrape around an authentication wall.

## 5. Secret hygiene checklist

- [ ] No keys in code, tests, fixtures, notebooks, or docs
- [ ] No keys in logs or error messages
- [ ] No keys in committed notebooks (output cells often leak them)
- [ ] `.gitignore` covers `.env*` (except `.env.example`), `*.pem`, `*.key`, `secrets.json`
- [ ] CI uses repository secrets, not files
- [ ] If a key is ever committed, treat it as compromised: rotate it, then purge history

## 6. Verifying a configuration without a wizard

```
1. Set the environment variables.
2. Run: python3 -c "from trading_intel.providers import describe; print(describe())"
   -> prints which providers are detected, WITHOUT printing keys
3. Run: python3 -m trading_intel.providers.health
   -> prints status/latency per provider
```

If a provider is misconfigured, the health check reports which variable is missing — never its value.

## 7. Terms of service

- Respect the provider's terms and licensing.
- Do not redistribute licensed data.
- Do not store licensed data in a public repository.
- Cite the provider in any report that uses its data.

## 8. What to tell a user who asks "how do I set this up?"

> "You do not need to. The skill works without any API. If you want live data, set the provider's key as an
> environment variable — never paste it into chat, and never commit it. The repository will detect it and switch
> to full research mode automatically; otherwise it stays in offline mode and tells you so in every report."
