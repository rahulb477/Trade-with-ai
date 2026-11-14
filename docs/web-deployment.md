# Web Application Architecture, Local Development & Deployment Guide

This guide documents how the **AI Trading Intelligence** web application integrates with the existing **V1 + V2 + V3** skill repository (`SKILL.md`, `AGENTS.md`, `knowledge/`, `markets/`, and `integrations/python/trading_intel/`).

---

## 1. System Architecture

```
Browser (Desktop / Android / iPhone)
   │  Relative HTTP requests (`/api/*` + Next.js App Router pages)
   ▼
Next.js 14 Frontend (`src/app/`, `src/components/`, Port 3000)
   │  Server-side rewrite proxy (`next.config.mjs` -> PYTHON_BACKEND_URL)
   ▼
Python Intelligence API (`backend/server.py`, Port 8000, zero external packages)
   ├── ScreenshotService (`backend/screenshot_service.py`) — PNG/JPEG/WEBP binary parser, size/HEIC gate, optional Tesseract OCR
   ├── VisionProviderAdapter (`backend/providers_service.py`) — Gemini / OpenAI-compatible multimodal JSON extractor
   ├── MarketDataAdapter & NewsResearchAdapter — Authorized external feeds (or explicit screenshot-only mode)
   ├── KnowledgeLoader (`backend/knowledge_service.py`) — Indexes 119+ Markdown modules in `knowledge/` & `markets/`
   ├── AnalysisOrchestrator (`backend/analysis_service.py`) — Calls `integrations/python/trading_intel/` directly:
   │      • `quick_signal.py` (WAIT / NO TRADE / PAPER-TRADING SETUP READY, Hinglish, anti-fabrication checks)
   │      • `indicators.py` (Wilder RSI, EMA, SMA, MACD, ATR, VWAP)
   │      • `patterns.py` (23 candlestick pattern detectors)
   │      • `risk.py` & `sizing.py` (R-multiples, break-even win rate, paper position sizing)
   │      • `observation.py` & `validation.py` (0–10 chart quality rubric, OHLC integrity, freshness)
   └── SQLite WAL Persistence (`backend/database.py`) — Users, PBKDF2 passwords, sessions, immutable analyses, watchlists, settings, logs
```

### Core Honesty & Safety Guarantees
1. **Zero rewritten math:** All technical indicators, R:R calculations, stop-loss buffers, target derivations, and verdict gates execute directly inside `integrations/python/trading_intel/`.
2. **No fabricated data:** When external Vision, Market Data, or News API keys are not configured, the backend reports their exact status (`OFFLINE DETERMINISTIC ENGINE`, `SCREENSHOT_ONLY`, `UNAVAILABLE`) and never invents live prices, RSI readings, or news headlines.
3. **Educational scope only:** No broker connectivity, no order execution, and mandatory disclaimers on every screen.

---

## 2. Prerequisites

- **Python:** 3.9+ (uses Python standard library only; zero `pip` packages required)
- **Node.js:** 18.17+ (tested on Node 22) and `npm`

---

## 3. Installation & Local Development

### Step 1: Clone and configure environment
```bash
cp .env.example .env
npm install
```

### Step 2: Start the Python Intelligence Backend (Terminal 1)
```bash
npm run backend
# Or directly: python3 backend/server.py
# Listens on http://0.0.0.0:8000
```

### Step 3: Start the Next.js Frontend (Terminal 2)
```bash
npm run dev
# Listens on http://0.0.0.0:3000 and proxies /api/* -> http://127.0.0.1:8000/api/*
```

Open `http://localhost:3000` in your browser.

---

## 4. Running the Test Suite

Run all Python unit tests, link integrity checks, repository audits, HTTP end-to-end tests, and Frontend Vitest component tests with a single command:

```bash
npm test
```

Or run individual suites:

```bash
# 1. Python V1-V3 + Quick Signal + Backend API E2E + Link Check + Repo Audit (402 tests)
./scripts/run_all_tests.sh

# 2. Frontend React/TypeScript Component & Upload Validation Tests (Vitest)
npm run test:web

# 3. Verify Production Next.js Build
npm run build
```

### Tests Requiring External Credentials
All **402 Python tests** and **9 Frontend Vitest tests** run **100% offline** with zero API keys. Live external calls in `VisionProviderAdapter` (`GEMINI_API_KEY` / `OPENAI_API_KEY`), `MarketDataAdapter` (`TI_MARKET_DATA_KEY`), and `NewsResearchAdapter` (`TI_NEWS_KEY`) are optional runtime integrations and are only invoked when their respective environment variables are populated.

---

## 5. Production Deployment Guide

### Frontend Deployment (Vercel or Node Server)
1. Import the repository into **Vercel** (`vercel.json` is preconfigured for Next.js).
2. Set the environment variable `PYTHON_BACKEND_URL` in Vercel to the HTTPS URL of your hosted Python Intelligence API (e.g., `https://api.your-domain.example`).
3. Alternatively, self-host with `npm run build && npm run start`.

### Python Backend Deployment (Render / Railway / Fly.io / Systemd VPS)
1. Deploy the repository root (so `backend/` can read `integrations/python/trading_intel/`, `knowledge/`, `markets/`, and `core/`).
2. Start command:
   ```bash
   python3 backend/server.py
   ```
3. Mount a persistent volume at `/app/data` (or configure `TI_DB_PATH` and `TI_UPLOAD_DIR`) so SQLite WAL records and uploaded chart screenshots persist across container restarts.
4. Set optional server-side secrets (`GEMINI_API_KEY`, `OPENAI_API_KEY`, `TI_MARKET_DATA_PROVIDER`, `TI_MARKET_DATA_KEY`, `TI_NEWS_PROVIDER`, `TI_NEWS_KEY`) in the host secret manager — **never** in client-exposed `NEXT_PUBLIC_*` variables.

---

## 6. Environment Variables Reference

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `PYTHON_BACKEND_URL` | No | `http://127.0.0.1:8000` | Next.js server-side proxy target for `/api/*` |
| `TI_API_HOST` | No | `0.0.0.0` | Python backend bind address |
| `TI_API_PORT` | No | `8000` | Python backend bind port |
| `TI_DB_PATH` | No | `./data/trading_intel.db` | SQLite database path |
| `TI_UPLOAD_DIR` | No | `./data/uploads` | Uploaded chart screenshot storage directory |
| `TI_MAX_UPLOAD_MB` | No | `10` | Maximum allowed chart upload size in megabytes |
| `GEMINI_API_KEY` | Optional | empty | Enables Google Gemini multimodal chart OCR/extraction |
| `GEMINI_MODEL` | Optional | `gemini-2.0-flash` | Gemini vision model identifier |
| `OPENAI_API_KEY` | Optional | empty | Enables OpenAI-compatible vision extraction |
| `OPENAI_BASE_URL` | Optional | `https://api.openai.com/v1` | Custom OpenAI-compatible endpoint URL |
| `OPENAI_VISION_MODEL` | Optional | `gpt-4o-mini` | OpenAI-compatible multimodal model name |
| `TI_MARKET_DATA_PROVIDER` | Optional | empty | Authorized market quote provider (`alphavantage`) |
| `TI_MARKET_DATA_KEY` | Optional | empty | API key for authorized market quote provider |
| `TI_NEWS_PROVIDER` | Optional | empty | Authorized news wire provider (`newsapi`) |
| `TI_NEWS_KEY` | Optional | empty | API key for authorized news provider |
