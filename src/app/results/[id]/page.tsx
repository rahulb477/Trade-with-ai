'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { useParams, useSearchParams } from 'next/navigation';
import {
  ArrowLeft,
  Check,
  ExternalLink,
  Maximize2,
  Plus,
  Upload,
  X,
} from 'lucide-react';
import { AppShell } from '@/components/AppShell';
import {
  FullAnalysisAccordion,
  QuickSignalCard,
} from '@/components/SignalComponents';
import {
  EducationalDisclaimer,
  ErrorState,
  LoadingState,
} from '@/components/StateViews';
import { useApp } from '@/context/AppContext';
import { apiFetch, buildScreenshotUrl, formatBytes, formatTimestamp } from '@/lib/api';
import type { AnalysisRecord } from '@/lib/types';

export default function AnalysisResultsPage() {
  const params = useParams<{ id: string }>();
  const searchParams = useSearchParams();
  const { settings } = useApp();

  const [analysis, setAnalysis] = useState<AnalysisRecord | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [showFull, setShowFull] = useState<boolean>(false);
  const [lightboxOpen, setLightboxOpen] = useState<boolean>(false);
  const [addedWatchlist, setAddedWatchlist] = useState<boolean>(false);
  const [watchlistMsg, setWatchlistMsg] = useState<string | null>(null);

  const analysisId = params?.id;

  const loadAnalysis = async () => {
    if (!analysisId) return;
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch<{ analysis: AnalysisRecord }>(
        `/api/analyses/${encodeURIComponent(analysisId)}`
      );
      setAnalysis(res.analysis);
      if (searchParams.get('view') === 'full' || res.analysis.mode === 'full') {
        setShowFull(true);
      }
    } catch (err: any) {
      setError(err?.message || 'Could not load analysis report.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadAnalysis();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [analysisId]);

  const handleAddWatchlist = async () => {
    if (!analysis || analysis.instrument === 'UNVERIFIED') return;
    try {
      await apiFetch('/api/watchlist', {
        method: 'POST',
        body: JSON.stringify({
          symbol: analysis.instrument,
          exchange: analysis.exchange === 'UNVERIFIED' ? '' : analysis.exchange,
          market: analysis.market || 'auto',
        }),
      });
      setAddedWatchlist(true);
      setWatchlistMsg(`${analysis.instrument} saved to your Watchlist.`);
    } catch (err: any) {
      setWatchlistMsg(err?.message || 'Already in Watchlist.');
    }
  };

  return (
    <AppShell requireAuth>
      <div className="space-y-6">
        {/* Top Action Bar */}
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <Link
              href="/history"
              className="inline-flex items-center gap-1.5 text-xs sm:text-sm font-medium ti-text-muted hover:text-[#E8EDF7]"
            >
              <ArrowLeft className="h-4 w-4" />
              <span>History</span>
            </Link>
            <span className="ti-text-muted">/</span>
            <span className="text-xs sm:text-sm font-mono ti-text-muted">
              {analysisId}
            </span>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            {analysis && analysis.instrument !== 'UNVERIFIED' && (
              <button
                type="button"
                onClick={handleAddWatchlist}
                disabled={addedWatchlist}
                className="inline-flex items-center gap-1.5 px-3 py-2 rounded-xl border border-[#1F2E47] bg-[#111C2D] hover:border-[#667AFF] text-xs font-semibold"
              >
                {addedWatchlist ? (
                  <>
                    <Check className="h-3.5 w-3.5 text-[#16B995]" />
                    <span>In Watchlist</span>
                  </>
                ) : (
                  <>
                    <Plus className="h-3.5 w-3.5 text-[#667AFF]" />
                    <span>Add to Watchlist</span>
                  </>
                )}
              </button>
            )}
            <Link
              href="/analyze"
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-[#667AFF] hover:bg-[#5267F5] text-white text-xs font-semibold"
            >
              <Upload className="h-3.5 w-3.5" />
              <span>Analyze Another Chart</span>
            </Link>
          </div>
        </div>

        {watchlistMsg && (
          <div className="rounded-xl border border-[#16B995]/40 bg-[#16B995]/10 px-4 py-2.5 text-xs text-[#16B995]">
            {watchlistMsg}
          </div>
        )}

        {error && <ErrorState message={error} onRetry={loadAnalysis} />}
        {loading ? (
          <LoadingState label="Loading Quick Signal & V1–V3 report…" rows={5} />
        ) : analysis ? (
          <>
            {/* Desktop side-by-side; Mobile: 1. Quick Result first -> 2. Chart Preview below */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
              <div className="lg:col-span-7 order-1">
                <QuickSignalCard
                  analysis={analysis}
                  timezone={settings.timezone}
                  fullOpen={showFull}
                  onToggleFullAnalysis={() => setShowFull((v) => !v)}
                />
              </div>

              <aside className="lg:col-span-5 order-2 space-y-4">
                <div className="ti-surface rounded-2xl p-4 sm:p-5 space-y-3">
                  <div className="flex items-center justify-between">
                    <h2 className="text-sm font-bold">Uploaded Chart Screenshot</h2>
                    <button
                      type="button"
                      onClick={() => setLightboxOpen(true)}
                      className="inline-flex items-center gap-1 text-xs font-medium text-[#667AFF] hover:underline"
                    >
                      <Maximize2 className="h-3.5 w-3.5" />
                      <span>Open Original</span>
                    </button>
                  </div>

                  <div className="rounded-xl overflow-hidden border border-[#1F2E47] bg-[#080D19] flex items-center justify-center min-h-[220px]">
                    <img
                      src={buildScreenshotUrl(analysis.id)}
                      alt={`Analyzed chart for ${analysis.instrument}`}
                      className="max-h-[360px] w-auto object-contain cursor-zoom-in"
                      onClick={() => setLightboxOpen(true)}
                    />
                  </div>

                  <div className="text-xs ti-text-muted space-y-1 pt-1">
                    <div className="flex justify-between">
                      <span>File:</span>
                      <span className="font-mono text-[#E8EDF7] truncate max-w-[200px]">
                        {analysis.screenshot_filename}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span>Dimensions:</span>
                      <span className="font-mono text-[#E8EDF7]">
                        {analysis.screenshot_width} &times; {analysis.screenshot_height}px ({formatBytes(analysis.screenshot_size_bytes)})
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span>Analyzed At:</span>
                      <span className="text-[#E8EDF7]">
                        {formatTimestamp(analysis.analysis_timestamp, settings.timezone)}
                      </span>
                    </div>
                    {analysis.snapshot_sha256 && (
                      <div className="flex justify-between">
                        <span>Immutable Hash:</span>
                        <span className="font-mono text-[#E8EDF7]">
                          {analysis.snapshot_sha256.slice(0, 14)}…
                        </span>
                      </div>
                    )}
                  </div>

                  <a
                    href={buildScreenshotUrl(analysis.id)}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-full py-2 px-3 rounded-lg border border-[#1F2E47] hover:border-[#667AFF] text-xs font-medium inline-flex items-center justify-center gap-1.5"
                  >
                    <span>View Raw Image in New Tab</span>
                    <ExternalLink className="h-3.5 w-3.5" />
                  </a>
                </div>
              </aside>
            </div>

            {/* 3. Expandable Full V1–V3 Analysis Mode */}
            {showFull && analysis.full_report?.sections && (
              <FullAnalysisAccordion
                sections={analysis.full_report.sections}
                legacyVerdict={analysis.legacy_verdict}
              />
            )}

            {/* Original Screenshot Lightbox Modal */}
            {lightboxOpen && (
              <div
                role="dialog"
                aria-modal="true"
                aria-label="Original Chart Screenshot"
                className="fixed inset-0 z-50 bg-black/85 p-4 sm:p-8 flex flex-col items-center justify-center"
              >
                <div className="w-full max-w-5xl flex items-center justify-between mb-3 text-white">
                  <span className="font-mono text-sm">
                    {analysis.screenshot_filename} ({analysis.screenshot_width}&times;{analysis.screenshot_height}px)
                  </span>
                  <button
                    type="button"
                    onClick={() => setLightboxOpen(false)}
                    aria-label="Close full screen image"
                    className="p-2 rounded-lg bg-white/10 hover:bg-white/20"
                  >
                    <X className="h-5 w-5" />
                  </button>
                </div>
                <img
                  src={buildScreenshotUrl(analysis.id)}
                  alt={`Original screenshot ${analysis.screenshot_filename}`}
                  className="max-h-[82vh] max-w-full object-contain rounded-lg border border-[#1F2E47]"
                />
              </div>
            )}
          </>
        ) : null}

        <EducationalDisclaimer />
      </div>
    </AppShell>
  );
}
