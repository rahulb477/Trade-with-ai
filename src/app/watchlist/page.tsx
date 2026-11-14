'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { Plus, Search, Star, Upload } from 'lucide-react';
import { AppShell } from '@/components/AppShell';
import { WatchlistTable } from '@/components/DataTables';
import {
  EducationalDisclaimer,
  EmptyState,
  ErrorState,
  LoadingState,
} from '@/components/StateViews';
import { useApp } from '@/context/AppContext';
import { apiFetch } from '@/lib/api';
import type { MarketType, WatchlistItem } from '@/lib/types';

export default function WatchlistPage() {
  const { user, settings } = useApp();
  const [items, setItems] = useState<WatchlistItem[]>([]);
  const [liveQuotesEnabled, setLiveQuotesEnabled] = useState<boolean>(false);
  const [providerNote, setProviderNote] = useState<string>('');
  const [filterText, setFilterText] = useState<string>('');
  const [symbol, setSymbol] = useState<string>('');
  const [exchange, setExchange] = useState<string>('');
  const [market, setMarket] = useState<MarketType>('auto');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState<boolean>(false);

  const loadWatchlist = async () => {
    if (!user) {
      setLoading(false);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch<{
        watchlist: WatchlistItem[];
        market_data_status: { configured: boolean; note: string };
      }>('/api/watchlist');
      setItems(res.watchlist || []);
      setLiveQuotesEnabled(Boolean(res.market_data_status?.configured));
      setProviderNote(res.market_data_status?.note || '');
    } catch (err: any) {
      setError(err?.message || 'Could not load watchlist.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadWatchlist();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user?.id]);

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!symbol.trim()) return;
    setSubmitting(true);
    setError(null);
    try {
      const res = await apiFetch<{ item: WatchlistItem }>('/api/watchlist', {
        method: 'POST',
        body: JSON.stringify({
          symbol: symbol.trim().toUpperCase(),
          exchange: exchange.trim().toUpperCase(),
          market,
        }),
      });
      setItems((prev) => [res.item, ...prev]);
      setSymbol('');
      setExchange('');
    } catch (err: any) {
      setError(err?.message || 'Could not add instrument.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleRemove = async (id: string) => {
    try {
      await apiFetch(`/api/watchlist/${encodeURIComponent(id)}`, { method: 'DELETE' });
      setItems((prev) => prev.filter((it) => it.id !== id));
    } catch (err: any) {
      setError(err?.message || 'Could not remove watchlist item.');
    }
  };

  const filtered = items.filter((it) => {
    const q = filterText.trim().toLowerCase();
    if (!q) return true;
    return (
      it.symbol.toLowerCase().includes(q) ||
      it.exchange.toLowerCase().includes(q) ||
      it.market.toLowerCase().includes(q)
    );
  });

  return (
    <AppShell requireAuth>
      <div className="space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight flex items-center gap-2.5">
              <Star className="h-7 w-7 text-[#F5B841]" />
              <span>Research Watchlist</span>
            </h1>
            <p className="text-sm ti-text-muted mt-1">
              Track instruments alongside their most recent verified Quick Signal verdict and timestamp.
            </p>
          </div>
          <Link
            href="/analyze"
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-[#667AFF] hover:bg-[#5267F5] text-white text-xs sm:text-sm font-semibold"
          >
            <Upload className="h-4 w-4" />
            <span>Analyze Chart</span>
          </Link>
        </div>

        {/* Add Instrument Form */}
        <form
          onSubmit={handleAdd}
          className="ti-surface rounded-2xl p-4 sm:p-5 grid grid-cols-1 sm:grid-cols-12 gap-3 items-end"
        >
          <div className="sm:col-span-4">
            <label htmlFor="wl-symbol" className="block text-xs font-semibold ti-text-muted mb-1">
              Instrument Symbol
            </label>
            <input
              id="wl-symbol"
              type="text"
              required
              value={symbol}
              onChange={(e) => setSymbol(e.target.value)}
              placeholder="e.g. BTCUSD, NIFTY 50, NVDA"
              className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3 py-2 text-sm"
            />
          </div>
          <div className="sm:col-span-3">
            <label htmlFor="wl-exchange" className="block text-xs font-semibold ti-text-muted mb-1">
              Exchange (Optional)
            </label>
            <input
              id="wl-exchange"
              type="text"
              value={exchange}
              onChange={(e) => setExchange(e.target.value)}
              placeholder="e.g. NSE, NASDAQ, Bitstamp"
              className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3 py-2 text-sm"
            />
          </div>
          <div className="sm:col-span-3">
            <label htmlFor="wl-market" className="block text-xs font-semibold ti-text-muted mb-1">
              Market
            </label>
            <select
              id="wl-market"
              value={market}
              onChange={(e) => setMarket(e.target.value as MarketType)}
              className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3 py-2 text-sm"
            >
              <option value="auto">Auto</option>
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
              disabled={submitting}
              className="w-full py-2 px-4 rounded-xl bg-[#667AFF] hover:bg-[#5267F5] text-white text-sm font-semibold inline-flex items-center justify-center gap-1.5"
            >
              <Plus className="h-4 w-4" />
              <span>Add</span>
            </button>
          </div>
        </form>

        {/* Search + Live Quote Disclosure */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="relative flex-1 max-w-sm">
            <Search className="h-4 w-4 ti-text-muted absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="search"
              value={filterText}
              onChange={(e) => setFilterText(e.target.value)}
              placeholder="Filter saved watchlist…"
              aria-label="Filter watchlist"
              className="w-full rounded-xl border border-[#1F2E47] bg-[#111C2D] pl-9 pr-3 py-2 text-xs sm:text-sm"
            />
          </div>
          {providerNote && (
            <p className="text-xs ti-text-muted max-w-xl">{providerNote}</p>
          )}
        </div>

        {error && <ErrorState message={error} onRetry={loadWatchlist} />}
        {loading ? (
          <LoadingState label="Loading your watchlist…" rows={3} />
        ) : filtered.length === 0 ? (
          <EmptyState
            title="Your watchlist is empty"
            description="Add instruments above (such as NIFTY 50, BTCUSD, AAPL, or EURUSD) to link them with your latest chart analyses."
          />
        ) : (
          <WatchlistTable
            items={filtered}
            liveQuotesEnabled={liveQuotesEnabled}
            timezone={settings.timezone}
            onRemove={handleRemove}
          />
        )}

        <EducationalDisclaimer />
      </div>
    </AppShell>
  );
}
