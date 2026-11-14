'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { Check, Settings as SettingsIcon, User as UserIcon } from 'lucide-react';
import { AppShell } from '@/components/AppShell';
import { EducationalDisclaimer, ErrorState } from '@/components/StateViews';
import { useApp } from '@/context/AppContext';
import type {
  AnalysisModeType,
  LanguageType,
  MarketType,
  ThemeType,
} from '@/lib/types';

export default function SettingsPage() {
  const { settings, updateSettings, user } = useApp();

  const [language, setLanguage] = useState<LanguageType>(settings.language);
  const [theme, setTheme] = useState<ThemeType>(settings.theme);
  const [defaultMode, setDefaultMode] = useState<AnalysisModeType>(settings.default_mode);
  const [preferredMarket, setPreferredMarket] = useState<MarketType>(settings.preferred_market);
  const [timezone, setTimezone] = useState<string>(settings.timezone);
  const [saveHistory, setSaveHistory] = useState<boolean>(settings.save_history);
  const [shareDiag, setShareDiag] = useState<boolean>(settings.share_anonymous_diagnostics);

  const [saving, setSaving] = useState<boolean>(false);
  const [savedBanner, setSavedBanner] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLanguage(settings.language);
    setTheme(settings.theme);
    setDefaultMode(settings.default_mode);
    setPreferredMarket(settings.preferred_market);
    setTimezone(settings.timezone);
    setSaveHistory(settings.save_history);
    setShareDiag(settings.share_anonymous_diagnostics);
  }, [settings]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setSavedBanner(false);
    setError(null);
    try {
      await updateSettings({
        language,
        theme,
        default_mode: defaultMode,
        preferred_market: preferredMarket,
        timezone,
        save_history: saveHistory,
        share_anonymous_diagnostics: shareDiag,
      });
      setSavedBanner(true);
      setTimeout(() => setSavedBanner(false), 3500);
    } catch (err: any) {
      setError(err?.message || 'Failed to save preferences.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <AppShell requireAuth>
      <div className="max-w-3xl mx-auto space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight flex items-center gap-2.5">
              <SettingsIcon className="h-7 w-7 text-[#667AFF]" />
              <span>Preferences &amp; Privacy Settings</span>
            </h1>
            <p className="text-sm ti-text-muted mt-1">
              Configure your default Quick Signal language, visual theme, market defaults, and data privacy controls.
            </p>
          </div>
          {user && (
            <Link
              href="/profile"
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl border border-[#1F2E47] hover:border-[#667AFF] text-xs font-semibold"
            >
              <UserIcon className="h-4 w-4 text-[#667AFF]" />
              <span>Account Profile</span>
            </Link>
          )}
        </div>

        {error && <ErrorState message={error} />}
        {savedBanner && (
          <div className="rounded-xl border border-[#16B995]/40 bg-[#16B995]/10 px-4 py-3 text-xs sm:text-sm text-[#16B995] flex items-center gap-2">
            <Check className="h-4 w-4" />
            <span>Settings saved successfully.</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="ti-surface rounded-2xl p-5 sm:p-7 space-y-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label htmlFor="set-lang" className="block text-xs font-semibold ti-text-muted mb-1.5">
                Explanation Language (Default: English)
              </label>
              <select
                id="set-lang"
                value={language}
                onChange={(e) => setLanguage(e.target.value as LanguageType)}
                className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3 py-2.5 text-sm"
              >
                <option value="english">English (+ Hinglish summary)</option>
                <option value="hinglish">Hinglish Primary</option>
                <option value="hindi">Hindi (हिंदी)</option>
              </select>
            </div>

            <div>
              <label htmlFor="set-theme" className="block text-xs font-semibold ti-text-muted mb-1.5">
                Interface Theme
              </label>
              <select
                id="set-theme"
                value={theme}
                onChange={(e) => setTheme(e.target.value as ThemeType)}
                className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3 py-2.5 text-sm"
              >
                <option value="dark">Deep Navy Dark (#080D19)</option>
                <option value="midnight">Midnight OLED</option>
                <option value="light">Clean Daylight</option>
              </select>
            </div>

            <div>
              <label htmlFor="set-mode" className="block text-xs font-semibold ti-text-muted mb-1.5">
                Default Analysis Mode
              </label>
              <select
                id="set-mode"
                value={defaultMode}
                onChange={(e) => setDefaultMode(e.target.value as AnalysisModeType)}
                className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3 py-2.5 text-sm"
              >
                <option value="quick">Quick Signal (Recommended)</option>
                <option value="full">Full 22-Section Research Report</option>
              </select>
            </div>

            <div>
              <label htmlFor="set-market" className="block text-xs font-semibold ti-text-muted mb-1.5">
                Preferred Market
              </label>
              <select
                id="set-market"
                value={preferredMarket}
                onChange={(e) => setPreferredMarket(e.target.value as MarketType)}
                className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3 py-2.5 text-sm"
              >
                <option value="auto">Auto Detect</option>
                <option value="india">Indian (NSE / BSE)</option>
                <option value="us">United States (NYSE / NASDAQ)</option>
                <option value="crypto">Crypto</option>
                <option value="forex">Forex</option>
                <option value="commodities">Commodities</option>
              </select>
            </div>

            <div className="sm:col-span-2">
              <label htmlFor="set-tz" className="block text-xs font-semibold ti-text-muted mb-1.5">
                Display Timezone
              </label>
              <select
                id="set-tz"
                value={timezone}
                onChange={(e) => setTimezone(e.target.value)}
                className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3 py-2.5 text-sm"
              >
                <option value="Asia/Kolkata">Asia/Kolkata (IST, UTC+05:30)</option>
                <option value="UTC">UTC (Coordinated Universal Time)</option>
                <option value="America/New_York">America/New_York (ET)</option>
                <option value="Europe/London">Europe/London (GMT/BST)</option>
                <option value="Asia/Singapore">Asia/Singapore (SGT)</option>
              </select>
            </div>
          </div>

          <div className="border-t border-[#1F2E47] pt-5 space-y-3">
            <h2 className="text-sm font-bold">Data Privacy Controls</h2>
            <label className="flex items-start gap-3 cursor-pointer text-xs sm:text-sm">
              <input
                type="checkbox"
                checked={saveHistory}
                onChange={(e) => setSaveHistory(e.target.checked)}
                className="mt-1"
              />
              <div>
                <span className="font-medium block">Persist Immutable Analysis History</span>
                <span className="ti-text-muted text-xs">
                  When enabled, chart analyses are stored privately under your account so you can reopen past reports. Disable for transient session-only reports.
                </span>
              </div>
            </label>

            <label className="flex items-start gap-3 cursor-pointer text-xs sm:text-sm">
              <input
                type="checkbox"
                checked={shareDiag}
                onChange={(e) => setShareDiag(e.target.checked)}
                className="mt-1"
              />
              <div>
                <span className="font-medium block">Record Local Quality Gate Diagnostics</span>
                <span className="ti-text-muted text-xs">
                  Logs non-sensitive stage timing and quality scores in local system logs. Zero external telemetry is ever sent.
                </span>
              </div>
            </label>
          </div>

          <div className="pt-2 flex justify-end">
            <button
              type="submit"
              disabled={saving}
              className="px-6 py-2.5 rounded-xl bg-[#667AFF] hover:bg-[#5267F5] text-white text-sm font-semibold"
            >
              {saving ? 'Saving…' : 'Save Settings'}
            </button>
          </div>
        </form>

        <EducationalDisclaimer />
      </div>
    </AppShell>
  );
}
