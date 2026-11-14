'use client';

import React, { useEffect, useState } from 'react';
import { CheckCircle2, RefreshCw, ShieldCheck, XCircle } from 'lucide-react';
import { AppShell } from '@/components/AppShell';
import {
  EducationalDisclaimer,
  ErrorState,
  LoadingState,
} from '@/components/StateViews';
import { useApp } from '@/context/AppContext';
import { apiFetch, formatTimestamp } from '@/lib/api';

export default function AdminDiagnosticsPage() {
  const { settings } = useApp();
  const [diag, setDiag] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadDiagnostics = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch<{ diagnostics: any }>('/api/admin/diagnostics');
      setDiag(res.diagnostics);
    } catch (err: any) {
      setError(err?.message || 'Could not load system diagnostics.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadDiagnostics();
  }, []);

  return (
    <AppShell requireAuth>
      <div className="space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight flex items-center gap-2.5">
              <ShieldCheck className="h-7 w-7 text-[#667AFF]" />
              <span>System Status &amp; Capability Matrix</span>
            </h1>
            <p className="text-sm ti-text-muted mt-1">
              Live verification of AGENTS.md §2 capability detection, provider adapters, and audit logs. Never exposes API secret values.
            </p>
          </div>
          <button
            type="button"
            onClick={loadDiagnostics}
            className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl border border-[#1F2E47] hover:border-[#667AFF] text-xs font-semibold"
          >
            <RefreshCw className="h-3.5 w-3.5" />
            <span>Refresh</span>
          </button>
        </div>

        {error && <ErrorState message={error} onRetry={loadDiagnostics} />}
        {loading ? (
          <LoadingState label="Inspecting runtime capabilities…" rows={4} />
        ) : diag ? (
          <>
            {/* Metrics */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="ti-surface rounded-2xl p-4">
                <span className="text-xs ti-text-muted block">Access Role</span>
                <span className="text-lg font-bold font-mono uppercase text-[#667AFF]">
                  {diag.role}
                </span>
              </div>
              <div className="ti-surface rounded-2xl p-4">
                <span className="text-xs ti-text-muted block">Your Analyses</span>
                <span className="text-lg font-bold font-mono">
                  {diag.totals?.analyses_personal ?? 0}
                </span>
              </div>
              <div className="ti-surface rounded-2xl p-4">
                <span className="text-xs ti-text-muted block">Platform Analyses</span>
                <span className="text-lg font-bold font-mono">
                  {diag.totals?.analyses_global ?? 0}
                </span>
              </div>
              <div className="ti-surface rounded-2xl p-4">
                <span className="text-xs ti-text-muted block">Python Engine</span>
                <span className="text-lg font-bold font-mono text-[#16B995]">
                  trading_intel v1.1
                </span>
              </div>
            </div>

            {/* Adapter Capability Matrix */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {[
                {
                  title: 'Vision Multimodal Adapter',
                  configured: diag.capabilities?.vision?.configured,
                  detail: diag.capabilities?.vision?.mode_label,
                },
                {
                  title: 'Market Data Adapter',
                  configured: diag.capabilities?.market_data?.configured,
                  detail: diag.capabilities?.market_data?.note,
                },
                {
                  title: 'Financial News Adapter',
                  configured: diag.capabilities?.news?.configured,
                  detail: diag.capabilities?.news?.note,
                },
              ].map((cap) => (
                <div key={cap.title} className="ti-surface rounded-2xl p-5 space-y-2">
                  <div className="flex items-center justify-between">
                    <h2 className="font-semibold text-sm">{cap.title}</h2>
                    {cap.configured ? (
                      <span className="inline-flex items-center gap-1 text-xs text-[#16B995] font-mono">
                        <CheckCircle2 className="h-4 w-4" /> LIVE KEY
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 text-xs text-[#F5B841] font-mono">
                        <XCircle className="h-4 w-4" /> OFFLINE MODE
                      </span>
                    )}
                  </div>
                  <p className="text-xs ti-text-muted leading-relaxed">{cap.detail}</p>
                </div>
              ))}
            </div>

            {/* Audit Logs */}
            <div className="ti-surface rounded-2xl p-5 space-y-3">
              <h2 className="text-sm font-bold">Recent Audit Logs</h2>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="border-b border-[#1F2E47] ti-text-muted uppercase">
                    <tr>
                      <th className="py-2 pr-4">Timestamp</th>
                      <th className="py-2 pr-4">Level</th>
                      <th className="py-2 pr-4">Event</th>
                      <th className="py-2">Detail</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#1F2E47]/60 font-mono">
                    {(diag.recent_logs || []).map((lg: any) => (
                      <tr key={lg.id}>
                        <td className="py-2 pr-4 ti-text-muted">
                          {formatTimestamp(lg.created_at, settings.timezone)}
                        </td>
                        <td className="py-2 pr-4">{lg.level}</td>
                        <td className="py-2 pr-4 text-[#667AFF]">{lg.event}</td>
                        <td className="py-2 ti-text-muted">
                          {JSON.stringify(lg.detail)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        ) : null}

        <EducationalDisclaimer />
      </div>
    </AppShell>
  );
}
