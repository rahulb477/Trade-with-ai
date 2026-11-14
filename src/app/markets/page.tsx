'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { CheckCircle2, Compass, Info, Upload } from 'lucide-react';
import { AppShell } from '@/components/AppShell';
import {
  EducationalDisclaimer,
  ErrorState,
  LoadingState,
} from '@/components/StateViews';
import { apiFetch } from '@/lib/api';
import type { MarketGuide } from '@/lib/types';

export default function MarketsPage() {
  const [markets, setMarkets] = useState<MarketGuide[]>([]);
  const [providerStatus, setProviderStatus] = useState<{
    configured: boolean;
    provider: string | null;
    mode: string;
    note: string;
  } | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadMarkets = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch<{
        markets: MarketGuide[];
        provider_status: {
          configured: boolean;
          provider: string | null;
          mode: string;
          note: string;
        };
      }>('/api/markets');
      setMarkets(res.markets || []);
      setProviderStatus(res.provider_status || null);
    } catch (err: any) {
      setError(err?.message || 'Could not load market specifications.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadMarkets();
  }, []);

  return (
    <AppShell>
      <div className="space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight flex items-center gap-2.5">
              <Compass className="h-7 w-7 text-[#667AFF]" />
              <span>Supported Markets &amp; Venue Rules</span>
            </h1>
            <p className="text-sm ti-text-muted mt-1">
              Each asset class enforces its own session timings, circuit/halt limits, and microstructure rules from <code className="font-mono">markets/</code>.
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

        {/* Honest Market Data Adapter Banner */}
        {providerStatus && (
          <div className="rounded-2xl border border-[#1F2E47] bg-[#101827] p-4 sm:p-5 flex items-start gap-3 text-xs sm:text-sm">
            <Info className="h-5 w-5 text-[#667AFF] shrink-0 mt-0.5" />
            <div className="space-y-1">
              <p className="font-semibold">
                Data Mode: <span className="font-mono text-[#667AFF]">{providerStatus.mode}</span>
              </p>
              <p className="ti-text-muted leading-relaxed">{providerStatus.note}</p>
            </div>
          </div>
        )}

        {error && <ErrorState message={error} onRetry={loadMarkets} />}
        {loading ? (
          <LoadingState label="Loading market microstructure rules…" rows={5} />
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
            {markets.map((mkt) => (
              <section
                key={mkt.id}
                className="ti-surface rounded-2xl p-5 sm:p-6 flex flex-col justify-between gap-4"
              >
                <div className="space-y-3">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <h2 className="text-base sm:text-lg font-bold">{mkt.name}</h2>
                      <p className="text-xs ti-text-muted font-mono mt-0.5">
                        Session: {mkt.session}
                      </p>
                    </div>
                    <span className="px-2.5 py-1 rounded-lg bg-[#16B995]/15 border border-[#16B995]/30 text-[#16B995] text-xs font-mono shrink-0">
                      {mkt.venues.join(' · ')}
                    </span>
                  </div>

                  <div className="flex flex-wrap gap-1.5">
                    {mkt.key_instruments.map((inst) => (
                      <span
                        key={inst}
                        className="px-2.5 py-0.5 rounded-md bg-[#101827] border border-[#1F2E47] text-xs font-mono"
                      >
                        {inst}
                      </span>
                    ))}
                  </div>

                  <ul className="space-y-1.5 pt-1 text-xs sm:text-sm ti-text-muted">
                    {mkt.structural_rules.map((rule, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <CheckCircle2 className="h-4 w-4 text-[#667AFF] shrink-0 mt-0.5" />
                        <span>{rule}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="pt-3 border-t border-[#1F2E47] flex items-center justify-between text-xs ti-text-muted">
                  <span className="font-mono">{mkt.doc_path}</span>
                  <span>Settlement: {mkt.settlement}</span>
                </div>
              </section>
            ))}
          </div>
        )}

        <EducationalDisclaimer />
      </div>
    </AppShell>
  );
}
