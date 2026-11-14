"""Trading Knowledge Loader & Market Rules Service.

Reads directly from the existing V1+V2+V3 repository Markdown modules:
- knowledge/ (candlesticks, indicators, chart-patterns, price-action,
  market-structure, smart-money, derivatives, fundamental-analysis,
  quantitative-analysis, risk-management, trading-psychology, education)
- markets/ (india, united-states, forex, commodities, crypto)
- strategies/ & workflows/ & core/

Never fabricates module contents; loads and indexes real Markdown files on disk.
"""

from __future__ import annotations

import os
import re
from typing import Any, Dict, List, Optional


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _read_md(rel_path: str) -> str:
    full = os.path.join(REPO_ROOT, rel_path)
    if not os.path.isfile(full):
        return ""
    with open(full, "r", encoding="utf-8") as handle:
        return handle.read()


def _extract_title_and_summary(markdown_text: str) -> Dict[str, str]:
    lines = [ln.strip() for ln in markdown_text.splitlines()]
    title = ""
    summary_parts: List[str] = []
    for ln in lines:
        if not title and ln.startswith("# "):
            title = ln[2:].strip()
            continue
        if title and ln and not ln.startswith(("#", "|", "-", "*", ">", "`", "---")):
            summary_parts.append(ln)
            if len(" ".join(summary_parts)) > 240:
                break
    return {
        "title": title or "Module",
        "summary": " ".join(summary_parts)[:320],
    }


class KnowledgeLoader:
    """Indexes and serves the 119+ knowledge and market modules in the skill repo."""

    DOMAINS = [
        ("candlesticks", "Candlestick Formations", "knowledge/candlesticks"),
        ("chart-patterns", "Chart Patterns", "knowledge/chart-patterns"),
        ("indicators", "Technical Indicators", "knowledge/indicators"),
        ("price-action", "Price Action", "knowledge/price-action"),
        ("market-structure", "Market Structure", "knowledge/market-structure"),
        ("smart-money", "Smart Money Concepts", "knowledge/smart-money"),
        ("risk-management", "Risk Management", "knowledge/risk-management"),
        ("quantitative-analysis", "Quantitative Analysis", "knowledge/quantitative-analysis"),
        ("derivatives", "Options & Derivatives", "knowledge/derivatives"),
        ("fundamental-analysis", "Fundamental Context", "knowledge/fundamental-analysis"),
        ("trading-psychology", "Trading Psychology", "knowledge/trading-psychology"),
        ("education", "Beginner & Hinglish Education", "knowledge/education"),
    ]

    MARKET_GUIDES = [
        {
            "id": "india",
            "name": "Indian Markets (NSE / BSE)",
            "venues": ["NSE", "BSE"],
            "session": "09:15–15:30 IST (Pre-open 09:00–09:08 IST)",
            "settlement": "T+1 rolling settlement",
            "key_instruments": ["NIFTY 50", "BANK NIFTY", "FINNIFTY", "SENSEX", "F&O Equities"],
            "structural_rules": [
                "Never confuse NSE and BSE tickers; verify exchange header.",
                "Circuit bands (2%, 5%, 10%, 20%) can lock illiquid scrips so stops cannot fill.",
                "Intraday cash equity shorts must be squared off before 15:30 IST close.",
                "Weekly/monthly index derivative expiries create elevated gamma and pin risk.",
            ],
            "doc_path": "markets/india/README.md",
        },
        {
            "id": "us",
            "name": "United States Markets (NYSE / NASDAQ / CME)",
            "venues": ["NYSE", "NASDAQ", "Cboe", "CME"],
            "session": "09:30–16:00 ET regular (04:00–09:30 pre, 16:00–20:00 post)",
            "settlement": "T+1 equities",
            "key_instruments": ["S&P 500 (SPX/SPY)", "Nasdaq 100 (NDX/QQQ)", "DJIA", "Russell 2000", "NVDA", "AAPL"],
            "structural_rules": [
                "Extended hours have thin liquidity; do not equate pre-market wicks with regular-session volume.",
                "Single-stock LULD volatility halts and market-wide circuit breakers apply instead of fixed daily bands.",
                "FOMC, CPI, NFP, and quarterly earnings create binary gap risk across sessions.",
            ],
            "doc_path": "markets/united-states/README.md",
        },
        {
            "id": "crypto",
            "name": "Crypto Markets (Spot & Perpetuals)",
            "venues": ["Bitstamp", "Binance", "Coinbase", "Kraken"],
            "session": "24/7/365 continuous trading (UTC daily close convention)",
            "settlement": "Instant spot / periodic funding on perpetuals",
            "key_instruments": ["BTCUSD", "BTCUSDT", "ETHUSD", "ETHUSDT", "SOLUSDT"],
            "structural_rules": [
                "No overnight session gaps exist on 24/7 venues; anchor VWAP explicitly.",
                "Always state exact pair and venue (BTCUSD on Bitstamp differs from BTCUSDT perpetuals).",
                "Weekend liquidity thins out and stop sweeps around obvious highs/lows are more frequent.",
                "Extreme positive/negative perpetual funding indicates crowding, not guaranteed reversal.",
            ],
            "doc_path": "markets/crypto/README.md",
        },
        {
            "id": "forex",
            "name": "Global Forex (FX Spot)",
            "venues": ["Interbank FX", "NSE Currency"],
            "session": "24/5 (Sydney → Tokyo → London → New York overlap)",
            "settlement": "T+2 standard spot",
            "key_instruments": ["EURUSD", "GBPUSD", "USDJPY", "GBPUSD", "USDINR"],
            "structural_rules": [
                "Peak liquidity occurs during the London–New York session overlap.",
                "Tick volume on spot FX feeds represents quote updates rather than centralised exchange volume.",
                "Central bank rate decisions (Fed, ECB, BoJ, RBI) are binary event-risk gates.",
            ],
            "doc_path": "markets/forex/README.md",
        },
        {
            "id": "commodities",
            "name": "Commodities (Metals & Energy)",
            "venues": ["COMEX", "NYMEX", "MCX"],
            "session": "Near-24h Globex / MCX 09:00–23:30 IST",
            "settlement": "Contract-specific futures expiry & rollover",
            "key_instruments": ["XAUUSD (Gold)", "XAGUSD (Silver)", "WTI Crude Oil", "Natural Gas"],
            "structural_rules": [
                "Futures contract rollovers create price steps on unadjusted continuous charts.",
                "Inventory releases (EIA Crude) and US real yields / DXY strongly drive intraday volatility.",
            ],
            "doc_path": "markets/commodities/README.md",
        },
    ]

    def list_catalog(self) -> List[Dict[str, Any]]:
        catalog: List[Dict[str, Any]] = []
        for slug, label, rel_dir in self.DOMAINS:
            abs_dir = os.path.join(REPO_ROOT, rel_dir)
            if not os.path.isdir(abs_dir):
                continue
            topics: List[Dict[str, str]] = []
            for fname in sorted(os.listdir(abs_dir)):
                if not fname.endswith(".md") or fname == "README.md":
                    continue
                topic_slug = fname[:-3]
                md = _read_md(f"{rel_dir}/{fname}")
                meta = _extract_title_and_summary(md)
                topics.append(
                    {
                        "slug": topic_slug,
                        "title": meta["title"],
                        "summary": meta["summary"],
                        "path": f"{rel_dir}/{fname}",
                    }
                )
            readme_meta = _extract_title_and_summary(_read_md(f"{rel_dir}/README.md"))
            catalog.append(
                {
                    "domain": slug,
                    "label": label,
                    "description": readme_meta["summary"],
                    "count": len(topics),
                    "topics": topics,
                }
            )
        return catalog

    def get_article(self, domain: str, slug: str) -> Optional[Dict[str, Any]]:
        safe_domain = re.sub(r"[^a-z0-9\-]", "", (domain or "").lower())
        safe_slug = re.sub(r"[^a-z0-9\-]", "", (slug or "").lower())
        valid_domains = {d[0]: d[2] for d in self.DOMAINS}
        if safe_domain not in valid_domains:
            return None
        rel_path = (
            f"{valid_domains[safe_domain]}/README.md"
            if safe_slug in ("", "readme")
            else f"{valid_domains[safe_domain]}/{safe_slug}.md"
        )
        content = _read_md(rel_path)
        if not content:
            return None
        meta = _extract_title_and_summary(content)
        return {
            "domain": safe_domain,
            "slug": safe_slug or "readme",
            "title": meta["title"],
            "summary": meta["summary"],
            "path": rel_path,
            "markdown": content,
        }

    def get_markets_overview(self) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        for item in self.MARKET_GUIDES:
            doc = _read_md(item["doc_path"])
            enriched = dict(item)
            enriched["documented"] = bool(doc)
            enriched["word_count"] = len(doc.split()) if doc else 0
            out.append(enriched)
        return out

    def select_relevant_modules(
        self,
        market: str = "auto",
        candle_patterns: Optional[List[str]] = None,
        indicators_used: Optional[List[str]] = None,
    ) -> List[Dict[str, str]]:
        """Follow AGENTS.md §3.1 module-loading budget (<= 8 modules per request)."""
        loaded: List[Dict[str, str]] = [
            {"module": "core/quick-output-engine.md", "role": "Quick Signal Output contract"},
            {"module": "core/verdict-rules.md", "role": "3-verdict gate ladder (WAIT / NO TRADE / READY)"},
            {"module": "core/decision-engine.md", "role": "Gates G1–G8 & evidence classes"},
            {"module": "workflows/entry-validation.md", "role": "Entry validation hierarchy"},
            {"module": "workflows/target-calculation.md", "role": "Structural Stop Loss & TP1–TP3 rules"},
        ]

        mkt_map = {
            "india": "markets/india/README.md",
            "us": "markets/united-states/README.md",
            "crypto": "markets/crypto/README.md",
            "forex": "markets/forex/README.md",
            "commodities": "markets/commodities/README.md",
        }
        if market in mkt_map and os.path.isfile(os.path.join(REPO_ROOT, mkt_map[market])):
            loaded.append({"module": mkt_map[market], "role": f"Market microstructure ({market.upper()})"})

        for pat in (candle_patterns or [])[:1]:
            slug = pat.lower().replace("_", "-")
            candidate = f"knowledge/candlesticks/{slug}.md"
            if os.path.isfile(os.path.join(REPO_ROOT, candidate)) and len(loaded) < 8:
                loaded.append({"module": candidate, "role": f"Candlestick specification ({pat})"})

        for ind_name in (indicators_used or [])[:1]:
            slug = ind_name.lower().replace("_", "-")
            candidate = f"knowledge/indicators/{slug}.md"
            if os.path.isfile(os.path.join(REPO_ROOT, candidate)) and len(loaded) < 8:
                loaded.append({"module": candidate, "role": f"Indicator methodology ({ind_name})"})

        return loaded[:8]
