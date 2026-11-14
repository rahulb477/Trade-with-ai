'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import {
  ArrowRight,
  Clock,
  Compass,
  History,
  ShieldCheck,
  Star,
  Upload,
} from 'lucide-react';
import { AppShell } from '@/components/AppShell';
import {
  EducationalDisclaimer,
  EmptyState,
  ErrorState,
  LoadingState,
  VerdictBadge,
} from '@/components/StateViews';
import { useApp } from '@/context/AppContext';
import { apiFetch, formatTimestamp } from '@/lib/api';
import type { AnalysisRecord, MarketGuide, WatchlistItem } from '@/lib/types';

export default function DashboardPage() {
  const { user, settings } = useApp();
  const [recentAnalyses, setRecentAnalyses] = useState<AnalysisRecord[]>([]);
  const [watchlist, setWatchlist] = useState<WatchlistItem[]>([]);
  const [markets, setMarkets] = useState<MarketGuide[]>([]);
  const [marketProviderNote, setMarketProviderNote] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadDashboardData = async () => {
    if (!user) {
      setLoading(false);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const [analysesRes, watchlistRes, marketsRes] = await Promise.all([
        apiFetch<{ analyses: AnalysisRecord[] }>('/api/analyses?limit=5'),
        apiFetch<{ watchlist: WatchlistItem[]; market_data_status: { note: string } }>('/api/watchlist'),
        apiFetch<{ markets: MarketGuide[]; provider_status: { note: string } }>('/api/markets'),
      ]);
      setRecentAnalyses(analysesRes.analyses || []);
      setWatchlist(watchlistRes.watchlist || []);
      setMarkets(marketsRes.markets || []);
      setMarketProviderNote(marketsRes.provider_status?.note || '');
    } catch (err: any) {
      setError(err?.message || 'Could not load dashboard data.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadDashboardData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user?.id]);

  return (
    <AppShell requireAuth>
      <div className="space-y-6">
        {/* A. Welcome Section */}
        <section className="ti-surface rounded-2xl p-6 sm:p-7 flex flex-col md:flex-row md:items-center justify-between gap-5">
          <div className="space-y-1.5">
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight">
              Welcome to AI Trading Intelligence
            </h1>
            <p className="text-sm sm:text-base ti-text-muted">
              Upload a chart and let AI analyze its market structure.
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <Link
              href="/analyze"
              className="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-[#667AFF] hover:bg-[#5267F5] text-white text-sm font-semibold transition-colors"
            >
              <Upload className="h-4 w-4" />
              <span>Analyze New Chart</span>
            </Link>
            <Link
              href="/history"
              className="inline-flex items-center gap-2 px-4 py-3 rounded-xl border border-[#1F2E47] hover:border-[#667AFF] text-sm font-semibold transition-colors"
            >
              <History className="h-4 w-4 text-[#667AFF]" />
              <span>View Previous Analysis</span>
            </Link>
          </div>
        </section>

        {/* B. Quick Analysis Action Cards */}
        <section className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <Link
            href="/analyze"
            className="ti-surface rounded-2xl p-5 hover:border-[#667AFF] transition-colors flex flex-col justify-between gap-3"
          >
            <div className="h-10 w-10 rounded-xl bg-[#667AFF]/15 border border-[#667AFF]/30 flex items-center justify-center text-[#667AFF]">
              <Upload className="h-5 w-5" />
            </div>
            <div>
              <h2 className="font-semibold text-base">Upload Chart</h2>
              <p className="text-xs ti-text-muted mt-1">
                Drop PNG, JPG, JPEG, or WEBP screenshots up to 10 MB.
              </p>
            </div>
            <span className="inline-flex items-center gap-1 text-xs font-semibold text-[#667AFF]">
              Start Upload <ArrowRight className="h-3.5 w-3.5" />
            </span>
          </Link>

          <Link
            href="/analyze?preset=btcusd_5m_wait"
            className="ti-surface rounded-2xl p-5 hover:border-[#667AFF] transition-colors flex flex-col justify-between gap-3"
          >
            <div className="h-10 w-10 rounded-xl bg-[#16B995]/15 border border-[#16B995]/30 flex items-center justify-center text-[#16B995]">
              <ShieldCheck className="h-5 w-5" />
            </div>
            <div>
              <h2 className="font-semibold text-base">Analyze Sample Setup</h2>
              <p className="text-xs ti-text-muted mt-1">
                Test the V1–V3 Quick Signal engine on a verified educational fixture.
              </p>
            </div>
            <span className="inline-flex items-center gap-1 text-xs font-semibold text-[#16B995]">
              Run Quick Demo <ArrowRight className="h-3.5 w-3.5" />
            </span>
          </Link>

          <Link
            href={recentAnalyses[0] ? `/results/${recentAnalyses[0].id}` : '/history'}
            className="ti-surface rounded-2xl p-5 hover:border-[#667AFF] transition-colors flex flex-col justify-between gap-3"
          >
            <div className="h-10 w-10 rounded-xl bg-[#F5B841]/15 border border-[#F5B841]/30 flex items-center justify-center text-[#F5B841]">
              <Clock className="h-5 w-5" />
            </div>
            <div>
              <h2 className="font-semibold text-base">View Previous Analysis</h2>
              <p className="text-xs ti-text-muted mt-1">
                {recentAnalyses[0]
                  ? `Latest: ${recentAnalyses[0].instrument} (${recentAnalyses[0].timeframe})`
                  : 'Reopen saved immutable research reports.'}
              </p>
            </div>
            <span className="inline-flex items-center gap-1 text-xs font-semibold text-[#F5B841]">
              Open Report <ArrowRight className="h-3.5 w-3.5" />
            </span>
          </Link>
        </section>

        {error && <ErrorState message={error} onRetry={loadDashboardData} />}
        {loading ? (
          <LoadingState label="Loading recent analyses and watchlist…" rows={4} />
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* D. Recent Analyses */}
            <section className="lg:col-span-7 space-y-3">
              <div className="flex items-center justify-between">
                <h2 className="text-base font-bold">Recent Analyses</h2>
                <Link href="/history" className="text-xs font-semibold text-[#667AFF] hover:underline">
                  View All
                </Link>
              </div>

              {recentAnalyses.length === 0 ? (
                <EmptyState
                  title="No chart analyses yet"
                  description="Upload your first candlestick chart screenshot to generate a Quick Signal report."
                  action={
                    <Link
                      href="/analyze"
                      className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-[#667AFF] text-white text-xs font-semibold"
                    >
                      <Upload className="h-3.5 w-3.5" />
                      <span>Upload Chart</span>
                    </Link>
                  }
                />
              ) : (
                <div className="ti-surface rounded-2xl overflow-hidden">
                  <div className="overflow-x-auto">
                    <table className="w-full text-left text-xs sm:text-sm">
                      <thead className="bg-[#101827] border-b border-[#1F2E47] text-xs uppercase ti-text-muted">
                        <tr>
                          <th className="px-4 py-3">Instrument</th>
                          <th className="px-4 py-3">Timeframe</th>
                          <th className="px-4 py-3">Verdict</th>
                          <th className="px-4 py-3">Timestamp</th>
                          <th className="px-4 py-3 text-right">Report</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-[#1F2E47]">
                        {recentAnalyses.map((a) => (
                          <tr key={a.id} className="hover:bg-[#1A273D]/30">
                            <td className="px-4 py-3 font-mono font-semibold">
                              {a.instrument}
                              <span className="block text-[11px] font-sans font-normal ti-text-muted">
                                {a.exchange}
                              </span>
                            </td>
                            <td className="px-4 py-3 font-mono">{a.timeframe}</td>
                            <td className="px-4 py-3">
                              <VerdictBadge verdict={a.verdict} size="sm" />
                            </td>
                            <td className="px-4 py-3 text-xs ti-text-muted">
                              {formatTimestamp(a.analysis_timestamp, settings.timezone)}
                            </td>
                            <td className="px-4 py-3 text-right">
                              <Link
                                href={`/results/${a.id}`}
                                className="px-2.5 py-1.5 rounded-lg border border-[#1F2E47] hover:border-[#667AFF] text-xs font-semibold inline-block"
                              >
                                View Report
                              </Link>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </section>

            {/* E. Watchlist Preview + C. Market Overview */}
            <div className="lg:col-span-5 space-y-6">
              <section className="space-y-3">
                <div className="flex items-center justify-between">
                  <h2 className="text-base font-bold flex items-center gap-2">
                    <Star className="h-4 w-4 text-[#F5B841]" />
                    <span>Watchlist Preview</span>
                  </h2>
                  <Link href="/watchlist" className="text-xs font-semibold text-[#667AFF] hover:underline">
                    Manage Watchlist
                  </Link>
                </div>

                {watchlist.length === 0 ? (
                  <div className="ti-surface rounded-2xl p-5 text-xs ti-text-muted space-y-2">
                    <p>No saved instruments yet.</p>
                    <Link
                      href="/watchlist"
                      className="inline-flex items-center gap-1 text-[#667AFF] font-semibold hover:underline"
                    >
                      Add instruments to track <ArrowRight className="h-3 w-3" />
                    </Link>
                  </div>
                ) : (
                  <div className="ti-surface rounded-2xl divide-y divide-[#1F2E47]">
                    {watchlist.slice(0, 4).map((w) => (
                      <div key={w.id} className="p-3.5 flex items-center justify-between gap-2 text-xs">
                        <div>
                          <p className="font-mono font-bold text-sm">{w.symbol}</p>
                          <p className="ti-text-muted">{w.exchange || w.market.toUpperCase()}</p>
                        </div>
                        {w.last_analysis ? (
                          <Link href={`/results/${w.last_analysis.id}`}>
                            <VerdictBadge verdict={w.last_analysis.verdict} size="sm" />
                          </Link>
                        ) : (
                          <Link
                            href={`/analyze?symbol=${encodeURIComponent(w.symbol)}`}
                            className="text-[#667AFF] font-semibold hover:underline"
                          >
                            Analyze →
                          </Link>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </section>

              <section className="space-y-3">
                <div className="flex items-center justify-between">
                  <h2 className="text-base font-bold flex items-center gap-2">
                    <Compass className="h-4 w-4 text-[#667AFF]" />
                    <span>Market Coverage &amp; Feed Status</span>
                  </h2>
                  <Link href="/markets" className="text-xs font-semibold text-[#667AFF] hover:underline">
                    Details
                  </Link>
                </div>
                <div className="ti-surface rounded-2xl p-4 space-y-3 text-xs">
                  <p className="ti-text-muted leading-relaxed">{marketProviderNote}</p>
                  <div className="grid grid-cols-1 gap-2">
                    {markets.slice(0, 4).map((m) => (
                      <div
                        key={m.id}
                        className="rounded-lg border border-[#1F2E47] bg-[#080D19]/50 px-3 py-2 flex items-center justify-between gap-2"
                      >
                        <span className="font-semibold">{m.name}</span>
                        <span className="ti-text-muted font-mono text-[11px] truncate max-w-[150px]">
                          {m.session.split('(')[0].trim()}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </section>
            </div>
          </div>
        )}

        <EducationalDisclaimer />
      </div>
    </AppShell>
  );
}
