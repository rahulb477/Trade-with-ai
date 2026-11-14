'use client';

import React, { useState } from 'react';
import {
  ChevronDown,
  ChevronRight,
  Clock,
  FileCheck2,
  ShieldAlert,
  Target,
  TrendingUp,
} from 'lucide-react';
import { VerdictBadge } from '@/components/StateViews';
import { formatTimestamp } from '@/lib/api';
import type { AnalysisRecord, FullReportSection } from '@/lib/types';

export function EntryCard({
  entryDisplay,
  entryStatus,
  direction,
}: {
  entryDisplay: string;
  entryStatus: string;
  direction?: string;
}) {
  return (
    <div className="rounded-xl border border-[#4C9AFF]/35 bg-[#4C9AFF]/10 p-3.5 sm:p-4">
      <div className="flex items-center justify-between gap-2 text-xs uppercase tracking-wider text-[#8D9AB0]">
        <span>ENTRY {direction ? `(${direction.toUpperCase()})` : ''}</span>
        <span className="font-mono text-[11px] px-2 py-0.5 rounded bg-[#080D19]/60 text-[#4C9AFF]">
          {entryStatus}
        </span>
      </div>
      <p
        data-testid="signal-entry"
        className="mt-1.5 text-base sm:text-lg font-bold font-mono text-[#4C9AFF] break-words"
      >
        {entryDisplay}
      </p>
    </div>
  );
}

export function StopLossCard({
  stopLoss,
  basis,
}: {
  stopLoss: string;
  basis?: string;
}) {
  return (
    <div className="rounded-xl border border-[#F16F83]/35 bg-[#F16F83]/10 p-3.5 sm:p-4">
      <div className="flex items-center justify-between gap-2 text-xs uppercase tracking-wider text-[#8D9AB0]">
        <span>STOP LOSS (INVALIDATION)</span>
        <ShieldAlert className="h-3.5 w-3.5 text-[#F16F83]" />
      </div>
      <p
        data-testid="signal-stoploss"
        className="mt-1.5 text-base sm:text-lg font-bold font-mono text-[#F16F83] break-words"
      >
        {stopLoss}
      </p>
      {basis && (
        <p className="mt-1 text-[11px] ti-text-muted truncate" title={basis}>
          Basis: {basis}
        </p>
      )}
    </div>
  );
}

export function TargetCard({
  index,
  value,
  rr,
  basis,
}: {
  index: 1 | 2 | 3;
  value: string;
  rr?: number | null;
  basis?: string;
}) {
  return (
    <div className="rounded-xl border border-[#16B995]/35 bg-[#16B995]/10 p-3.5">
      <div className="flex items-center justify-between gap-1.5 text-xs uppercase tracking-wider text-[#8D9AB0]">
        <span>TAKE PROFIT {index}</span>
        {rr !== null && rr !== undefined ? (
          <span className="font-mono text-[11px] text-[#16B995] font-semibold">
            {rr.toFixed(2)}R
          </span>
        ) : (
          <Target className="h-3.5 w-3.5 text-[#16B995]" />
        )}
      </div>
      <p
        data-testid={`signal-tp${index}`}
        className="mt-1.5 text-sm sm:text-base font-bold font-mono text-[#16B995] break-words"
      >
        {value}
      </p>
      {basis && (
        <p className="mt-1 text-[11px] ti-text-muted truncate" title={basis}>
          {basis}
        </p>
      )}
    </div>
  );
}

export function RiskRewardCard({ riskReward }: { riskReward: string }) {
  return (
    <div className="rounded-xl border border-[#1F2E47] bg-[#101827] px-4 py-3 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1.5">
      <div className="flex items-center gap-2 text-xs uppercase tracking-wider ti-text-muted">
        <TrendingUp className="h-4 w-4 text-[#667AFF]" />
        <span>RISK / REWARD</span>
      </div>
      <p
        data-testid="signal-rr"
        className="font-mono text-sm font-semibold text-[#E8EDF7] break-words"
      >
        {riskReward}
      </p>
    </div>
  );
}

export function QuickSignalCard({
  analysis,
  timezone,
  onToggleFullAnalysis,
  fullOpen,
}: {
  analysis: AnalysisRecord;
  timezone?: string;
  onToggleFullAnalysis?: () => void;
  fullOpen?: boolean;
}) {
  const qp = analysis.quick_payload;

  return (
    <section
      aria-label="Quick Signal Summary"
      data-testid="quick-signal-card"
      className="ti-surface rounded-2xl p-5 sm:p-6 shadow-card space-y-5"
    >
      {/* Fictional Demo Banner when applicable */}
      {analysis.is_fictional_demo && (
        <div className="rounded-lg border border-[#667AFF]/40 bg-[#667AFF]/10 px-3 py-2 text-xs text-[#E8EDF7]">
          <strong>Fictional Educational Demo Fixture:</strong> Prices below come from the repository&apos;s illustrative paper-trading fixture to demonstrate the Quick Signal Engine.
        </div>
      )}

      {/* Header row: Instrument | Exchange | Timeframe */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-[#1F2E47] pb-4">
        <div>
          <p
            data-testid="signal-header"
            className="text-sm sm:text-base font-bold tracking-wide font-mono text-[#E8EDF7]"
          >
            {analysis.instrument} &nbsp;|&nbsp; {analysis.exchange} &nbsp;|&nbsp; {analysis.timeframe}
          </p>
          <p className="text-xs ti-text-muted mt-0.5">
            Source: {analysis.data_quality?.source_type?.replace(/_/g, ' ') || 'Screenshot Observation'} &middot; Quality {analysis.data_quality?.quality_score ?? 8}/10
          </p>
        </div>
        <VerdictBadge verdict={analysis.verdict} size="lg" />
      </div>

      {/* WAIT UNTIL block */}
      <div className="rounded-xl border border-[#F5B841]/30 bg-[#F5B841]/10 px-4 py-3">
        <div className="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wider text-[#F5B841]">
          <Clock className="h-3.5 w-3.5" />
          <span>WAIT UNTIL</span>
        </div>
        <p data-testid="signal-wait" className="mt-1 text-sm text-[#E8EDF7] leading-relaxed">
          {analysis.wait_condition || 'Clear confirmation appears.'}
        </p>
      </div>

      {/* Entry + Stop Loss */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <EntryCard
          entryDisplay={analysis.entry_display}
          entryStatus={analysis.entry_status}
          direction={analysis.direction}
        />
        <StopLossCard
          stopLoss={analysis.stop_loss}
          basis={analysis.stop_basis || qp?.stop_basis}
        />
      </div>

      {/* Take Profit 1 / 2 / 3 */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <TargetCard
          index={1}
          value={analysis.tp1}
          rr={qp?.rr_t1}
          basis={qp?.tp1_basis}
        />
        <TargetCard
          index={2}
          value={analysis.tp2}
          rr={qp?.rr_t2}
          basis={qp?.tp2_basis}
        />
        <TargetCard
          index={3}
          value={analysis.tp3}
          rr={qp?.rr_t3}
          basis={qp?.tp3_basis}
        />
      </div>

      {/* Risk / Reward */}
      <RiskRewardCard riskReward={analysis.risk_reward} />

      {/* Compact Reason + Hinglish */}
      <div className="rounded-xl border border-[#1F2E47] bg-[#101827] p-4 space-y-2 text-sm">
        <div>
          <span className="text-xs font-semibold uppercase tracking-wider ti-text-muted block">
            REASON
          </span>
          <p data-testid="signal-reason" className="mt-0.5 text-[#E8EDF7] leading-relaxed">
            {analysis.short_explanation}
          </p>
        </div>
        {analysis.hinglish_explanation && analysis.language !== 'hinglish' && (
          <div className="pt-2 border-t border-[#1F2E47]/70">
            <span className="text-xs font-semibold uppercase tracking-wider text-[#667AFF] block">
              HINGLISH SUMMARY
            </span>
            <p className="mt-0.5 ti-text-muted text-xs sm:text-sm leading-relaxed">
              {analysis.hinglish_explanation}
            </p>
          </div>
        )}
      </div>

      {/* Metadata footer */}
      <div className="flex flex-wrap items-center justify-between gap-2 text-[11px] ti-text-muted pt-1">
        <span className="inline-flex items-center gap-1.5">
          <FileCheck2 className="h-3.5 w-3.5 text-[#16B995]" />
          Ref: {analysis.screenshot_filename || analysis.screenshot_ref}
        </span>
        <span>
          Data: {formatTimestamp(analysis.data_timestamp, timezone)} &middot; Freshness:{' '}
          {analysis.data_quality?.freshness || 'SCREENSHOT_BASED'}
        </span>
      </div>

      {/* VIEW FULL ANALYSIS CTA */}
      {onToggleFullAnalysis && (
        <button
          type="button"
          onClick={onToggleFullAnalysis}
          data-testid="view-full-analysis-btn"
          className="w-full py-3 px-4 rounded-xl border border-[#667AFF]/50 bg-[#667AFF]/15 hover:bg-[#667AFF]/25 text-[#E8EDF7] font-semibold text-sm flex items-center justify-center gap-2 transition-colors"
        >
          <span>{fullOpen ? 'HIDE FULL ANALYSIS' : 'VIEW FULL ANALYSIS (22-SECTION V1–V3 REPORT)'}</span>
          <ChevronDown
            className={`h-4 w-4 transition-transform ${fullOpen ? 'rotate-180' : ''}`}
          />
        </button>
      )}
    </section>
  );
}

export function FullAnalysisAccordion({
  sections,
  legacyVerdict,
}: {
  sections: FullReportSection[];
  legacyVerdict?: string;
}) {
  const [expandedIds, setExpandedIds] = useState<Record<string, boolean>>(() => {
    const initial: Record<string, boolean> = {};
    sections.slice(0, 4).forEach((s) => {
      initial[s.id] = true;
    });
    return initial;
  });

  const toggle = (id: string) => {
    setExpandedIds((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const expandAll = (open: boolean) => {
    const next: Record<string, boolean> = {};
    sections.forEach((s) => {
      next[s.id] = open;
    });
    setExpandedIds(next);
  };

  return (
    <section
      aria-label="Full V1-V3 Research Report"
      data-testid="full-analysis-accordion"
      className="ti-surface rounded-2xl p-5 sm:p-6 space-y-4"
    >
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-[#1F2E47] pb-3">
        <div>
          <h2 className="text-base sm:text-lg font-bold">
            Complete V1–V3 Research Report (22 Sections)
          </h2>
          {legacyVerdict && (
            <p className="text-xs ti-text-muted mt-0.5">
              Normative Full-Mode Verdict: <span className="font-mono text-[#E8EDF7]">{legacyVerdict}</span>
            </p>
          )}
        </div>
        <div className="flex items-center gap-2 text-xs">
          <button
            type="button"
            onClick={() => expandAll(true)}
            className="px-2.5 py-1 rounded-lg border border-[#1F2E47] hover:border-[#667AFF]"
          >
            Expand All
          </button>
          <button
            type="button"
            onClick={() => expandAll(false)}
            className="px-2.5 py-1 rounded-lg border border-[#1F2E47] hover:border-[#667AFF]"
          >
            Collapse All
          </button>
        </div>
      </div>

      <div className="divide-y divide-[#1F2E47] border border-[#1F2E47] rounded-xl overflow-hidden">
        {sections.map((sec) => {
          const isOpen = !!expandedIds[sec.id];
          return (
            <div key={sec.id} className="bg-[#080D19]/40">
              <button
                type="button"
                onClick={() => toggle(sec.id)}
                aria-expanded={isOpen}
                className="w-full px-4 py-3 text-left flex items-center justify-between gap-3 hover:bg-[#1A273D]/40 transition-colors"
              >
                <div className="flex items-center gap-3 min-w-0">
                  <span className="text-xs font-mono px-2 py-0.5 rounded bg-[#101827] border border-[#1F2E47] ti-text-muted shrink-0">
                    {String(sec.number).padStart(2, '0')}
                  </span>
                  <span className="font-semibold text-sm truncate">{sec.title}</span>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  <span className="hidden sm:inline-block text-[11px] font-mono px-2 py-0.5 rounded bg-[#101827] ti-text-muted">
                    {sec.status}
                  </span>
                  {isOpen ? (
                    <ChevronDown className="h-4 w-4 ti-text-muted" />
                  ) : (
                    <ChevronRight className="h-4 w-4 ti-text-muted" />
                  )}
                </div>
              </button>
              {isOpen && (
                <div className="px-4 pb-4 pt-1 text-xs sm:text-sm space-y-2 bg-[#101827]/60">
                  <p className="text-[#E8EDF7] font-medium leading-relaxed">
                    {sec.summary}
                  </p>
                  {sec.details?.length > 0 && (
                    <ul className="list-disc pl-5 space-y-1 ti-text-muted">
                      {sec.details.map((d, i) => (
                        <li key={i} className="leading-relaxed break-words">
                          {d}
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
