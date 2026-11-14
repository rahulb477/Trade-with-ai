'use client';

import React from 'react';
import Link from 'next/link';
import {
  Activity,
  ArrowRight,
  BookOpen,
  CheckCircle2,
  Layers,
  ShieldCheck,
  Sparkles,
  Upload,
} from 'lucide-react';
import { useApp } from '@/context/AppContext';
import { EducationalDisclaimer, VerdictBadge } from '@/components/StateViews';

export default function LandingPage() {
  const { user } = useApp();

  return (
    <div className="min-h-screen flex flex-col">
      {/* Top Bar */}
      <header className="border-b ti-secondary px-4 sm:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="h-9 w-9 rounded-xl bg-[#667AFF] flex items-center justify-center text-white">
            <Activity className="h-5 w-5" />
          </div>
          <div>
            <span className="font-bold text-sm sm:text-base tracking-tight block">
              AI Trading Intelligence
            </span>
            <span className="text-[11px] ti-text-muted hidden sm:block">
              Deep Market Intelligence. Simple Trading Insights.
            </span>
          </div>
        </div>

        <nav className="flex items-center gap-2 sm:gap-4 text-xs sm:text-sm">
          <Link href="/education" className="ti-text-muted hover:text-[#E8EDF7] hidden sm:inline">
            Education
          </Link>
          <Link href="/markets" className="ti-text-muted hover:text-[#E8EDF7] hidden sm:inline">
            Markets
          </Link>
          {user ? (
            <Link
              href="/dashboard"
              className="px-4 py-2 rounded-xl bg-[#667AFF] hover:bg-[#5267F5] text-white font-semibold"
            >
              Open Dashboard
            </Link>
          ) : (
            <>
              <Link
                href="/signin"
                className="px-3 py-2 rounded-xl ti-text-muted hover:text-[#E8EDF7] font-medium"
              >
                Sign In
              </Link>
              <Link
                href="/signup"
                className="px-4 py-2 rounded-xl bg-[#667AFF] hover:bg-[#5267F5] text-white font-semibold"
              >
                Get Started
              </Link>
            </>
          )}
        </nav>
      </header>

      {/* Hero Section */}
      <main className="flex-1 max-w-6xl mx-auto w-full px-4 sm:px-8 py-12 sm:py-16 space-y-16">
        <section className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
          <div className="lg:col-span-7 space-y-6">
            <div className="inline-flex items-center gap-2 rounded-full border border-[#667AFF]/35 bg-[#667AFF]/10 px-3.5 py-1 text-xs font-medium text-[#667AFF]">
              <Sparkles className="h-3.5 w-3.5" />
              <span>V1 + V2 + V3 Intelligence Engine &middot; Quick Signal Default</span>
            </div>

            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight leading-tight">
              Deep Market Intelligence.{' '}
              <span className="text-[#667AFF]">Simple Trading Insights.</span>
            </h1>

            <p className="text-base sm:text-lg ti-text-muted leading-relaxed max-w-2xl">
              Upload any candlestick chart screenshot and receive a disciplined, five-second Quick Signal summary backed by 119 documented technical modules, deterministic Python risk mathematics, and honest uncertainty gates.
            </p>

            <div className="flex flex-wrap items-center gap-3 pt-1">
              <Link
                href={user ? '/analyze' : '/signup?next=/analyze'}
                className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-[#667AFF] hover:bg-[#5267F5] text-white font-semibold text-sm sm:text-base transition-colors"
              >
                <Upload className="h-4 w-4" />
                <span>Analyze a Chart Screenshot</span>
                <ArrowRight className="h-4 w-4" />
              </Link>
              <Link
                href={user ? '/dashboard' : '/education'}
                className="inline-flex items-center gap-2 px-5 py-3.5 rounded-xl border border-[#1F2E47] bg-[#111C2D] hover:border-[#667AFF] font-semibold text-sm sm:text-base transition-colors"
              >
                <BookOpen className="h-4 w-4 text-[#667AFF]" />
                <span>{user ? 'Go to Dashboard' : 'Explore Knowledge Base'}</span>
              </Link>
            </div>

            <div className="grid grid-cols-3 gap-4 pt-4 border-t border-[#1F2E47] text-xs sm:text-sm">
              <div>
                <p className="font-bold text-lg sm:text-xl font-mono">119+</p>
                <p className="ti-text-muted">Knowledge Modules</p>
              </div>
              <div>
                <p className="font-bold text-lg sm:text-xl font-mono">22</p>
                <p className="ti-text-muted">Full Report Sections</p>
              </div>
              <div>
                <p className="font-bold text-lg sm:text-xl font-mono">0</p>
                <p className="ti-text-muted">Fabricated Prices</p>
              </div>
            </div>
          </div>

          {/* Illustrative Quick Signal Preview Card */}
          <div className="lg:col-span-5">
            <div className="ti-surface rounded-2xl p-5 sm:p-6 shadow-card space-y-4">
              <div className="flex items-center justify-between text-xs ti-text-muted border-b border-[#1F2E47] pb-3">
                <span className="font-mono font-bold text-[#E8EDF7]">
                  BTCUSD | Bitstamp | 5m
                </span>
                <span className="px-2 py-0.5 rounded bg-[#101827] border border-[#1F2E47] text-[10px] uppercase">
                  Illustrative Preview
                </span>
              </div>

              <VerdictBadge verdict="WAIT" size="md" />

              <div className="rounded-xl border border-[#F5B841]/30 bg-[#F5B841]/10 px-3.5 py-2.5 text-xs">
                <span className="font-semibold text-[#F5B841] block uppercase">
                  WAIT UNTIL
                </span>
                <span className="text-[#E8EDF7] mt-0.5 block">
                  5-minute candle closes below identified support (67,300) with volume confirmation.
                </span>
              </div>

              <div className="grid grid-cols-2 gap-2.5 text-xs font-mono">
                <div className="rounded-lg border border-[#4C9AFF]/30 bg-[#4C9AFF]/10 p-2.5">
                  <span className="ti-text-muted block text-[10px]">ENTRY</span>
                  <span className="font-bold text-[#4C9AFF] text-sm">67,300–67,400</span>
                </div>
                <div className="rounded-lg border border-[#F16F83]/30 bg-[#F16F83]/10 p-2.5">
                  <span className="ti-text-muted block text-[10px]">STOP LOSS</span>
                  <span className="font-bold text-[#F16F83] text-sm">67,800</span>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-2 text-xs font-mono">
                <div className="rounded-lg border border-[#16B995]/30 bg-[#16B995]/10 p-2">
                  <span className="ti-text-muted block text-[10px]">TP1</span>
                  <span className="font-bold text-[#16B995]">66,950</span>
                </div>
                <div className="rounded-lg border border-[#16B995]/30 bg-[#16B995]/10 p-2">
                  <span className="ti-text-muted block text-[10px]">TP2</span>
                  <span className="font-bold text-[#16B995]">66,500</span>
                </div>
                <div className="rounded-lg border border-[#16B995]/30 bg-[#16B995]/10 p-2">
                  <span className="ti-text-muted block text-[10px]">TP3</span>
                  <span className="font-bold text-[#16B995]">66,200</span>
                </div>
              </div>

              <div className="rounded-lg bg-[#101827] border border-[#1F2E47] p-3 text-xs space-y-1">
                <p className="font-mono text-[#E8EDF7]">
                  RISK / REWARD: T1 0.89 | T2 1.89 | T3 2.56
                </p>
                <p className="ti-text-muted">
                  Hinglish: Support break abhi confirm nahi hua. Candle close ka wait karo.
                </p>
              </div>
              <p className="text-[11px] ti-text-muted italic text-center">
                Fictional demonstration values shown above for layout preview only.
              </p>
            </div>
          </div>
        </section>

        {/* Core Pillars */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {[
            {
              icon: CheckCircle2,
              title: '5-Second Quick Signal Surface',
              desc: 'Performs 20 internal checks across structure, candles, traps, and R:R arithmetic, then outputs a clean WAIT, NO TRADE, or PAPER-TRADING SETUP READY verdict.',
            },
            {
              icon: Layers,
              title: 'V1 + V2 + V3 Python Engine',
              desc: 'Directly executes the repository’s zero-dependency Python trading_intel modules for Wilder RSI, ATR stops, R-multiples, and break-even math.',
            },
            {
              icon: ShieldCheck,
              title: 'Strict Anti-Fabrication Honesty',
              desc: 'Never invents live market prices, unseen indicators, countdown timers, or win-rate percentages. Saying WAIT or NO TRADE is a core feature.',
            },
          ].map((card) => {
            const Icon = card.icon;
            return (
              <div key={card.title} className="ti-surface rounded-2xl p-6 space-y-3">
                <div className="h-10 w-10 rounded-xl bg-[#667AFF]/15 border border-[#667AFF]/30 flex items-center justify-center text-[#667AFF]">
                  <Icon className="h-5 w-5" />
                </div>
                <h2 className="font-bold text-base">{card.title}</h2>
                <p className="text-sm ti-text-muted leading-relaxed">{card.desc}</p>
              </div>
            );
          })}
        </section>

        <EducationalDisclaimer />
      </main>

      <footer className="border-t ti-secondary px-4 sm:px-8 py-6 text-xs ti-text-muted flex flex-col sm:flex-row items-center justify-between gap-3">
        <span>AI Trading Intelligence &middot; Educational Paper-Trading Research Platform</span>
        <div className="flex items-center gap-4">
          <Link href="/education" className="hover:text-[#E8EDF7]">
            Knowledge Modules
          </Link>
          <Link href="/markets" className="hover:text-[#E8EDF7]">
            Supported Markets
          </Link>
          <Link href="/analyze" className="hover:text-[#E8EDF7]">
            Analyze Chart
          </Link>
        </div>
      </footer>
    </div>
  );
}
