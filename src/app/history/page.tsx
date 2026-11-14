'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { History, Search, Trash2, Upload } from 'lucide-react';
import { AppShell } from '@/components/AppShell';
import { AnalysisHistoryList } from '@/components/DataTables';
import {
  EducationalDisclaimer,
  EmptyState,
  ErrorState,
  LoadingState,
} from '@/components/StateViews';
import { useApp } from '@/context/AppContext';
import { apiFetch } from '@/lib/api';
import type { AnalysisRecord } from '@/lib/types';

export default function AnalysisHistoryPage() {
  const { user, settings } = useApp();
  const [analyses, setAnalyses] = useState<AnalysisRecord[]>([]);
  const [filterQuery, setFilterQuery] = useState<string>('');
  const [verdictFilter, setVerdictFilter] = useState<string>('ALL');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadHistory = async () => {
    if (!user) {
      setLoading(false);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch<{ analyses: AnalysisRecord[] }>('/api/analyses?limit=100');
      setAnalyses(res.analyses || []);
    } catch (err: any) {
      setError(err?.message || 'Could not load analysis history.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadHistory();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user?.id]);

  const handleDeleteOne = async (id: string) => {
    try {
      await apiFetch(`/api/analyses/${encodeURIComponent(id)}`, { method: 'DELETE' });
      setAnalyses((prev) => prev.filter((a) => a.id !== id));
    } catch (err: any) {
      setError(err?.message || 'Failed to delete analysis record.');
    }
  };

  const handleClearAll = async () => {
    if (!window.confirm('Delete all of your saved analysis history? This cannot be undone.')) {
      return;
    }
    try {
      await apiFetch('/api/analyses', { method: 'DELETE' });
      setAnalyses([]);
    } catch (err: any) {
      setError(err?.message || 'Failed to clear analysis history.');
    }
  };

  const visible = analyses.filter((item) => {
    if (verdictFilter !== 'ALL' && item.verdict !== verdictFilter) return false;
    const q = filterQuery.trim().toLowerCase();
    if (!q) return true;
    return (
      item.instrument.toLowerCase().includes(q) ||
      item.exchange.toLowerCase().includes(q) ||
      item.timeframe.toLowerCase().includes(q)
    );
  });

  return (
    <AppShell requireAuth>
      <div className="space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight flex items-center gap-2.5">
              <History className="h-7 w-7 text-[#667AFF]" />
              <span>Analysis History</span>
            </h1>
            <p className="text-sm ti-text-muted mt-1">
              Immutable snapshot records of your past chart analyses. Old reports are never silently overwritten when market conditions change.
            </p>
          </div>
          <div className="flex items-center gap-2">
            {analyses.length > 0 && (
              <button
                type="button"
                onClick={handleClearAll}
                className="inline-flex items-center gap-1.5 px-3.5 py-2.5 rounded-xl border border-[#F16F83]/40 text-[#F16F83] hover:bg-[#F16F83]/15 text-xs font-semibold"
              >
                <Trash2 className="h-4 w-4" />
                <span>Clear All</span>
              </button>
            )}
            <Link
              href="/analyze"
              className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-[#667AFF] hover:bg-[#5267F5] text-white text-xs sm:text-sm font-semibold"
            >
              <Upload className="h-4 w-4" />
              <span>New Analysis</span>
            </Link>
          </div>
        </div>

        {/* Filters */}
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="h-4 w-4 ti-text-muted absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="search"
              value={filterQuery}
              onChange={(e) => setFilterQuery(e.target.value)}
              placeholder="Filter by instrument, exchange, or timeframe…"
              aria-label="Filter analysis history"
              className="w-full rounded-xl border border-[#1F2E47] bg-[#111C2D] pl-9 pr-3 py-2 text-sm"
            />
          </div>
          <select
            aria-label="Filter by verdict"
            value={verdictFilter}
            onChange={(e) => setVerdictFilter(e.target.value)}
            className="rounded-xl border border-[#1F2E47] bg-[#111C2D] px-3 py-2 text-sm"
          >
            <option value="ALL">All Verdicts</option>
            <option value="WAIT">WAIT</option>
            <option value="PAPER-TRADING SETUP READY">PAPER-TRADING SETUP READY</option>
            <option value="NO TRADE">NO TRADE</option>
          </select>
        </div>

        {error && <ErrorState message={error} onRetry={loadHistory} />}
        {loading ? (
          <LoadingState label="Loading immutable analysis history…" rows={4} />
        ) : visible.length === 0 ? (
          <EmptyState
            title="No saved analysis reports found"
            description="Analyze a chart screenshot to record an immutable Quick Signal and V1–V3 report."
            action={
              <Link
                href="/analyze"
                className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-[#667AFF] text-white text-xs font-semibold"
              >
                <Upload className="h-4 w-4" />
                <span>Analyze Chart</span>
              </Link>
            }
          />
        ) : (
          <AnalysisHistoryList
            analyses={visible}
            timezone={settings.timezone}
            onDelete={handleDeleteOne}
          />
        )}

        <EducationalDisclaimer />
      </div>
    </AppShell>
  );
}
