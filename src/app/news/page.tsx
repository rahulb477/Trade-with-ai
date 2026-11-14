'use client';

import React, { useEffect, useState } from 'react';
import { Newspaper, Search, ShieldAlert } from 'lucide-react';
import { AppShell } from '@/components/AppShell';
import { MarketNewsCard } from '@/components/DataTables';
import {
  EducationalDisclaimer,
  ErrorState,
  LoadingState,
} from '@/components/StateViews';
import { apiFetch } from '@/lib/api';
import type { NewsArticle } from '@/lib/types';

interface EventChecklistItem {
  category: string;
  market: string;
  rule: string;
}

export default function NewsPage() {
  const [query, setQuery] = useState<string>('');
  const [instrument, setInstrument] = useState<string>('');
  const [market, setMarket] = useState<string>('all');
  const [available, setAvailable] = useState<boolean>(false);
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [statusMessage, setStatusMessage] = useState<string>('');
  const [checklist, setChecklist] = useState<EventChecklistItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadNews = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      if (query.trim()) params.set('q', query.trim());
      if (instrument.trim()) params.set('instrument', instrument.trim());
      if (market !== 'all') params.set('market', market);
      const res = await apiFetch<{
        available: boolean;
        articles: NewsArticle[];
        message: string;
        event_risk_checklist?: EventChecklistItem[];
      }>(`/api/news?${params.toString()}`);
      setAvailable(res.available);
      setArticles(res.articles || []);
      setStatusMessage(res.message || '');
      setChecklist(res.event_risk_checklist || []);
    } catch (err: any) {
      setError(err?.message || 'Failed to check financial news adapter.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadNews();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [market]);

  return (
    <AppShell>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight flex items-center gap-2.5">
            <Newspaper className="h-7 w-7 text-[#667AFF]" />
            <span>Financial Research News &amp; Event Risk</span>
          </h1>
          <p className="text-sm ti-text-muted mt-1">
            Cited market news and Gate G2 binary event-risk verification. Unverified or synthetic headlines are never fabricated.
          </p>
        </div>

        {/* Search & Filter Controls */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            void loadNews();
          }}
          className="ti-surface rounded-2xl p-4 sm:p-5 grid grid-cols-1 sm:grid-cols-12 gap-3 items-end"
        >
          <div className="sm:col-span-5">
            <label htmlFor="news-q" className="block text-xs font-semibold ti-text-muted mb-1">
              Keyword Search
            </label>
            <div className="relative">
              <Search className="h-4 w-4 ti-text-muted absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                id="news-q"
                type="search"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Central bank, earnings, CPI…"
                className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] pl-9 pr-3 py-2 text-sm"
              />
            </div>
          </div>
          <div className="sm:col-span-3">
            <label htmlFor="news-inst" className="block text-xs font-semibold ti-text-muted mb-1">
              Instrument Filter
            </label>
            <input
              id="news-inst"
              type="text"
              value={instrument}
              onChange={(e) => setInstrument(e.target.value)}
              placeholder="e.g. NIFTY, BTC, AAPL"
              className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3 py-2 text-sm"
            />
          </div>
          <div className="sm:col-span-2">
            <label htmlFor="news-mkt" className="block text-xs font-semibold ti-text-muted mb-1">
              Market
            </label>
            <select
              id="news-mkt"
              value={market}
              onChange={(e) => setMarket(e.target.value)}
              className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3 py-2 text-sm"
            >
              <option value="all">All Markets</option>
              <option value="india">India</option>
              <option value="us">US</option>
              <option value="crypto">Crypto</option>
              <option value="forex">Forex</option>
              <option value="commodities">Commodities</option>
            </select>
          </div>
          <div className="sm:col-span-2">
            <button
              type="submit"
              className="w-full py-2 px-4 rounded-xl bg-[#667AFF] hover:bg-[#5267F5] text-white text-sm font-semibold"
            >
              Search
            </button>
          </div>
        </form>

        {error && <ErrorState message={error} onRetry={loadNews} />}
        {loading ? (
          <LoadingState label="Checking authorized financial news adapter…" rows={3} />
        ) : available && articles.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {articles.map((art, idx) => (
              <MarketNewsCard key={`${art.url}-${idx}`} article={art} />
            ))}
          </div>
        ) : (
          <div className="space-y-5">
            <div className="rounded-2xl border border-[#F5B841]/35 bg-[#F5B841]/10 p-5 text-sm space-y-2">
              <div className="flex items-center gap-2 font-semibold text-[#F5B841]">
                <ShieldAlert className="h-5 w-5" />
                <span>Authorized Live News Feed Not Connected</span>
              </div>
              <p className="text-[#E8EDF7]/90 leading-relaxed">{statusMessage}</p>
              <p className="text-xs ti-text-muted">
                Per SKILL.md Rule 3 &amp; 4, AI Trading Intelligence never invents news headlines or displays stale cached articles as current.
              </p>
            </div>

            {checklist.length > 0 && (
              <div className="space-y-3">
                <h2 className="text-base font-bold">
                  Mandatory Gate G2 Event-Risk Verification Checklist (<code className="font-mono text-xs">data-sources/news-data.md</code>)
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {checklist.map((item) => (
                    <div key={item.category} className="ti-surface rounded-xl p-5 space-y-2">
                      <div className="flex items-center justify-between gap-2">
                        <h3 className="font-semibold text-sm">{item.category}</h3>
                        <span className="text-[11px] font-mono uppercase px-2 py-0.5 rounded bg-[#101827] border border-[#1F2E47] ti-text-muted">
                          {item.market}
                        </span>
                      </div>
                      <p className="text-xs sm:text-sm ti-text-muted leading-relaxed">
                        {item.rule}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        <EducationalDisclaimer />
      </div>
    </AppShell>
  );
}
