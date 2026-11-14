'use client';

import React from 'react';
import { AlertCircle, CheckCircle2, Clock, Inbox } from 'lucide-react';
import type { VerdictType } from '@/lib/types';

export function VerdictBadge({
  verdict,
  size = 'md',
}: {
  verdict: VerdictType | string;
  size?: 'sm' | 'md' | 'lg';
}) {
  const normalized = (verdict || 'WAIT').toUpperCase();

  let colorClasses =
    'bg-[#F5B841]/15 text-[#F5B841] border-[#F5B841]/40';
  let Icon = Clock;

  if (normalized === 'PAPER-TRADING SETUP READY') {
    colorClasses =
      'bg-[#16B995]/15 text-[#16B995] border-[#16B995]/40';
    Icon = CheckCircle2;
  } else if (normalized === 'NO TRADE' || normalized === 'NO-TRADE') {
    colorClasses =
      'bg-[#F16F83]/15 text-[#F16F83] border-[#F16F83]/40';
    Icon = AlertCircle;
  }

  const sizeClasses =
    size === 'lg'
      ? 'px-4 py-2 text-sm sm:text-base font-bold tracking-wide'
      : size === 'sm'
      ? 'px-2.5 py-0.5 text-xs font-semibold'
      : 'px-3 py-1 text-xs sm:text-sm font-semibold';

  return (
    <span
      data-testid="verdict-badge"
      className={`inline-flex items-center gap-1.5 rounded-lg border ${colorClasses} ${sizeClasses}`}
    >
      <Icon className={size === 'lg' ? 'h-4 w-4 shrink-0' : 'h-3.5 w-3.5 shrink-0'} />
      <span>VERDICT: {normalized}</span>
    </span>
  );
}

export function LoadingState({
  label = 'Loading research data…',
  rows = 3,
}: {
  label?: string;
  rows?: number;
}) {
  return (
    <div
      role="status"
      aria-live="polite"
      className="ti-surface rounded-xl p-5 sm:p-6 space-y-4"
    >
      <div className="flex items-center gap-3">
        <div className="h-4 w-4 rounded-full border-2 border-[#667AFF] border-t-transparent animate-spin" />
        <span className="text-sm ti-text-muted">{label}</span>
      </div>
      <div className="space-y-2.5">
        {Array.from({ length: rows }).map((_, i) => (
          <div
            key={i}
            className="h-9 rounded-lg bg-[#1A273D]/60 animate-pulse"
          />
        ))}
      </div>
    </div>
  );
}

export function EmptyState({
  title,
  description,
  action,
}: {
  title: string;
  description: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="ti-surface rounded-xl p-8 text-center flex flex-col items-center justify-center">
      <div className="h-11 w-11 rounded-xl bg-[#667AFF]/15 border border-[#667AFF]/30 flex items-center justify-center text-[#667AFF] mb-3">
        <Inbox className="h-5 w-5" />
      </div>
      <h3 className="text-base font-semibold mb-1">{title}</h3>
      <p className="text-sm ti-text-muted max-w-md mb-4">{description}</p>
      {action && <div>{action}</div>}
    </div>
  );
}

export function ErrorState({
  title = 'Unable to complete request',
  message,
  onRetry,
}: {
  title?: string;
  message: string;
  onRetry?: () => void;
}) {
  return (
    <div
      role="alert"
      className="rounded-xl border border-[#F16F83]/40 bg-[#F16F83]/10 p-4 sm:p-5 text-sm"
    >
      <div className="flex items-start gap-3">
        <AlertCircle className="h-5 w-5 text-[#F16F83] shrink-0 mt-0.5" />
        <div className="flex-1 min-w-0">
          <p className="font-semibold text-[#F16F83]">{title}</p>
          <p className="mt-1 text-[#E8EDF7]/90 break-words">{message}</p>
          {onRetry && (
            <button
              type="button"
              onClick={onRetry}
              className="mt-3 inline-flex items-center px-3 py-1.5 rounded-lg bg-[#F16F83]/20 hover:bg-[#F16F83]/30 text-[#F16F83] font-medium text-xs transition-colors"
            >
              Retry
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export function EducationalDisclaimer() {
  return (
    <div className="rounded-xl border border-[#1F2E47] bg-[#101827]/80 px-4 py-3 text-xs ti-text-muted leading-relaxed">
      <strong className="text-[#E8EDF7] font-medium">Educational Research &amp; Paper-Trading Only:</strong>{' '}
      AI Trading Intelligence does not provide personalized investment advice, broker connectivity, or real-money order execution.
      All setups are hypothetical scenarios derived from visible chart structure and documented technical rules. Never trade with capital you cannot afford to lose.
    </div>
  );
}
