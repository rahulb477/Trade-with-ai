'use client';

import React from 'react';
import Link from 'next/link';
import { ArrowUpRight, ExternalLink, Trash2 } from 'lucide-react';
import { VerdictBadge } from '@/components/StateViews';
import { formatTimestamp } from '@/lib/api';
import type { AnalysisRecord, NewsArticle, WatchlistItem } from '@/lib/types';

export function MarketNewsCard({ article }: { article: NewsArticle }) {
  return (
    <article className="ti-surface rounded-xl p-4 sm:p-5 flex flex-col justify-between gap-3">
      <div className="space-y-2">
        <div className="flex flex-wrap items-center justify-between gap-2 text-xs">
          <span className="font-semibold text-[#667AFF]">{article.source}</span>
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded bg-[#101827] border border-[#1F2E47] font-mono text-[11px] ti-text-muted">
              {article.relevance}
            </span>
            <span className="ti-text-muted">
              {formatTimestamp(article.published_at)}
            </span>
          </div>
        </div>
        <h3 className="font-semibold text-sm sm:text-base leading-snug">
          {article.title}
        </h3>
        {article.summary && (
          <p className="text-xs sm:text-sm ti-text-muted leading-relaxed">
            {article.summary}
          </p>
        )}
      </div>

      {article.url && (
        <div className="pt-2 border-t border-[#1F2E47]/60 flex justify-end">
          <a
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-xs font-medium text-[#667AFF] hover:underline"
          >
            <span>Original Source</span>
            <ExternalLink className="h-3.5 w-3.5" />
          </a>
        </div>
      )}
    </article>
  );
}

export function WatchlistTable({
  items,
  liveQuotesEnabled,
  timezone,
  onRemove,
}: {
  items: WatchlistItem[];
  liveQuotesEnabled: boolean;
  timezone?: string;
  onRemove: (id: string) => void;
}) {
  return (
    <div className="ti-surface rounded-2xl overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-[#1F2E47] bg-[#101827] text-xs uppercase ti-text-muted">
            <tr>
              <th className="px-4 py-3 font-semibold">Instrument</th>
              <th className="px-4 py-3 font-semibold">Market</th>
              {liveQuotesEnabled && (
                <th className="px-4 py-3 font-semibold">Authorized Quote</th>
              )}
              <th className="px-4 py-3 font-semibold">Last Analysis Verdict</th>
              <th className="px-4 py-3 font-semibold">Last Analyzed</th>
              <th className="px-4 py-3 font-semibold text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#1F2E47]">
            {items.map((item) => (
              <tr key={item.id} className="hover:bg-[#1A273D]/30">
                <td className="px-4 py-3.5">
                  <p className="font-bold font-mono">{item.symbol}</p>
                  {item.exchange && (
                    <p className="text-xs ti-text-muted">{item.exchange}</p>
                  )}
                </td>
                <td className="px-4 py-3.5 uppercase text-xs font-mono ti-text-muted">
                  {item.market}
                </td>
                {liveQuotesEnabled && (
                  <td className="px-4 py-3.5 font-mono text-xs">
                    {item.live_quote?.available ? (
                      <div>
                        <span className="font-semibold">{item.live_quote.last}</span>
                        <span className="block text-[11px] ti-text-muted">
                          {item.live_quote.source} ({item.live_quote.freshness})
                        </span>
                      </div>
                    ) : (
                      <span className="ti-text-muted">Unavailable</span>
                    )}
                  </td>
                )}
                <td className="px-4 py-3.5">
                  {item.last_analysis ? (
                    <div className="space-y-1">
                      <VerdictBadge verdict={item.last_analysis.verdict} size="sm" />
                      <p className="text-xs ti-text-muted font-mono">
                        TF: {item.last_analysis.timeframe} &middot; Entry: {item.last_analysis.entry_display}
                      </p>
                    </div>
                  ) : (
                    <span className="text-xs ti-text-muted">No chart analyzed yet</span>
                  )}
                </td>
                <td className="px-4 py-3.5 text-xs ti-text-muted">
                  {item.last_analysis
                    ? formatTimestamp(item.last_analysis.analysis_timestamp, timezone)
                    : '—'}
                </td>
                <td className="px-4 py-3.5 text-right">
                  <div className="inline-flex items-center gap-2">
                    {item.last_analysis ? (
                      <Link
                        href={`/results/${item.last_analysis.id}`}
                        className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg border border-[#1F2E47] hover:border-[#667AFF] text-xs font-medium"
                      >
                        <span>Report</span>
                        <ArrowUpRight className="h-3.5 w-3.5" />
                      </Link>
                    ) : (
                      <Link
                        href={`/analyze?symbol=${encodeURIComponent(item.symbol)}`}
                        className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg border border-[#667AFF]/40 text-[#667AFF] hover:bg-[#667AFF]/15 text-xs font-medium"
                      >
                        <span>Analyze</span>
                      </Link>
                    )}
                    <button
                      type="button"
                      onClick={() => onRemove(item.id)}
                      aria-label={`Remove ${item.symbol} from watchlist`}
                      className="p-1.5 rounded-lg border border-[#1F2E47] hover:border-[#F16F83] text-[#8D9AB0] hover:text-[#F16F83]"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export function AnalysisHistoryList({
  analyses,
  timezone,
  onDelete,
}: {
  analyses: AnalysisRecord[];
  timezone?: string;
  onDelete?: (id: string) => void;
}) {
  return (
    <div className="space-y-3" data-testid="analysis-history-list">
      {analyses.map((item) => (
        <div
          key={item.id}
          className="ti-surface rounded-xl p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4"
        >
          <div className="space-y-1.5 min-w-0">
            <div className="flex flex-wrap items-center gap-2.5">
              <span className="font-bold font-mono text-sm sm:text-base">
                {item.instrument} | {item.exchange} | {item.timeframe}
              </span>
              <VerdictBadge verdict={item.verdict} size="sm" />
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-[#101827] border border-[#1F2E47] ti-text-muted">
                v{item.immutable_version || 1} immutable
              </span>
            </div>
            <p className="text-xs sm:text-sm ti-text-muted line-clamp-2">
              {item.short_explanation}
            </p>
            <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs font-mono ti-text-muted">
              <span>Entry: {item.entry_display}</span>
              <span>SL: {item.stop_loss}</span>
              <span>TP1: {item.tp1}</span>
              <span>Analyzed: {formatTimestamp(item.analysis_timestamp, timezone)}</span>
            </div>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <Link
              href={`/results/${item.id}`}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-[#667AFF] hover:bg-[#5267F5] text-white text-xs font-semibold"
            >
              <span>View Report</span>
              <ArrowUpRight className="h-3.5 w-3.5" />
            </Link>
            {onDelete && (
              <button
                type="button"
                onClick={() => onDelete(item.id)}
                aria-label={`Delete analysis ${item.instrument}`}
                className="p-2 rounded-xl border border-[#1F2E47] hover:border-[#F16F83] ti-text-muted hover:text-[#F16F83]"
              >
                <Trash2 className="h-4 w-4" />
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
