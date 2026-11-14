'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import {
  Activity,
  BarChart3,
  BookOpen,
  Compass,
  History,
  LayoutDashboard,
  LogOut,
  Menu,
  Moon,
  Newspaper,
  Search,
  Settings,
  ShieldCheck,
  Star,
  Sun,
  Upload,
  User as UserIcon,
  X,
} from 'lucide-react';
import { useApp } from '@/context/AppContext';
import type { LanguageType, ThemeType } from '@/lib/types';

export interface NavItem {
  href: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
}

export const SIDEBAR_ITEMS: NavItem[] = [
  { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/analyze', label: 'Analyze Chart', icon: Upload },
  { href: '/markets', label: 'Markets', icon: Compass },
  { href: '/watchlist', label: 'Watchlist', icon: Star },
  { href: '/news', label: 'Market News', icon: Newspaper },
  { href: '/history', label: 'Analysis History', icon: History },
  { href: '/education', label: 'Trading Education', icon: BookOpen },
  { href: '/settings', label: 'Settings', icon: Settings },
];

export function BrandLogo({ compact = false }: { compact?: boolean }) {
  return (
    <Link href="/" className="inline-flex items-center gap-2.5 group">
      <div className="h-9 w-9 rounded-xl bg-[#667AFF] flex items-center justify-center text-white shadow-sm shrink-0">
        <Activity className="h-5 w-5" />
      </div>
      {!compact && (
        <div className="leading-tight">
          <span className="block font-bold text-sm sm:text-base tracking-tight">
            AI Trading Intelligence
          </span>
          <span className="hidden sm:block text-[11px] ti-text-muted">
            V1–V3 Research Platform
          </span>
        </div>
      )}
    </Link>
  );
}

export function Sidebar({
  mobileOpen,
  onCloseMobile,
}: {
  mobileOpen: boolean;
  onCloseMobile: () => void;
}) {
  const pathname = usePathname();
  const { user } = useApp();

  const renderLinks = () => (
    <nav aria-label="Main Sidebar Navigation" className="space-y-1 px-3 py-4">
      {SIDEBAR_ITEMS.map((item) => {
        const active =
          pathname === item.href ||
          (item.href !== '/dashboard' && pathname?.startsWith(item.href));
        const Icon = item.icon;
        return (
          <Link
            key={item.href}
            href={item.href}
            onClick={onCloseMobile}
            className={`flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-sm font-medium transition-colors ${
              active
                ? 'bg-[#667AFF] text-white'
                : 'ti-text-muted hover:bg-[#1A273D]/60 hover:text-[#E8EDF7]'
            }`}
          >
            <Icon className="h-4 w-4 shrink-0" />
            <span>{item.label}</span>
          </Link>
        );
      })}

      {user && (
        <Link
          href="/admin"
          onClick={onCloseMobile}
          className={`flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-sm font-medium transition-colors ${
            pathname === '/admin'
              ? 'bg-[#667AFF] text-white'
              : 'ti-text-muted hover:bg-[#1A273D]/60 hover:text-[#E8EDF7]'
          }`}
        >
          <ShieldCheck className="h-4 w-4 shrink-0" />
          <span>System Status</span>
        </Link>
      )}
    </nav>
  );

  return (
    <>
      {/* Desktop sidebar */}
      <aside className="hidden lg:flex lg:flex-col lg:w-64 lg:shrink-0 border-r ti-secondary min-h-[calc(100vh-4rem)] justify-between">
        {renderLinks()}
        <div className="p-4 m-3 rounded-xl border border-[#1F2E47] bg-[#080D19]/60 text-xs ti-text-muted space-y-1.5">
          <div className="flex items-center gap-1.5 font-semibold text-[#E8EDF7]">
            <BarChart3 className="h-3.5 w-3.5 text-[#16B995]" />
            <span>Paper-Trading Research</span>
          </div>
          <p className="leading-relaxed">
            Evidence-gated Quick Signals powered by the V1–V3 Python trading_intel engine.
          </p>
        </div>
      </aside>

      {/* Mobile slide-over drawer */}
      {mobileOpen && (
        <div className="fixed inset-0 z-50 lg:hidden flex">
          <div
            className="fixed inset-0 bg-black/65"
            onClick={onCloseMobile}
            aria-hidden="true"
          />
          <div className="relative z-10 w-72 max-w-[85vw] ti-secondary border-r h-full flex flex-col justify-between overflow-y-auto">
            <div>
              <div className="flex items-center justify-between px-4 h-16 border-b border-[#1F2E47]">
                <BrandLogo />
                <button
                  type="button"
                  onClick={onCloseMobile}
                  aria-label="Close navigation menu"
                  className="p-2 rounded-lg ti-text-muted hover:text-[#E8EDF7]"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
              {renderLinks()}
            </div>
            <div className="p-4 border-t border-[#1F2E47] text-xs ti-text-muted">
              Deep Market Intelligence. Simple Trading Insights.
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export function Navbar({ onOpenMobileMenu }: { onOpenMobileMenu: () => void }) {
  const router = useRouter();
  const { user, settings, setLocalLanguage, setLocalTheme, signOut } = useApp();
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = searchQuery.trim();
    if (!trimmed) {
      router.push('/education');
      return;
    }
    router.push(`/education?q=${encodeURIComponent(trimmed)}`);
  };

  const cycleTheme = () => {
    const order: ThemeType[] = ['dark', 'midnight', 'light'];
    const next = order[(order.indexOf(settings.theme) + 1) % order.length];
    setLocalTheme(next);
  };

  return (
    <header className="sticky top-0 z-40 h-16 border-b ti-secondary px-3 sm:px-6 flex items-center justify-between gap-3">
      <div className="flex items-center gap-2 sm:gap-3">
        <button
          type="button"
          onClick={onOpenMobileMenu}
          aria-label="Open navigation menu"
          className="lg:hidden p-2 rounded-lg border border-[#1F2E47] ti-text-muted hover:text-[#E8EDF7]"
        >
          <Menu className="h-5 w-5" />
        </button>
        <BrandLogo />
      </div>

      {/* Global Search */}
      <form
        onSubmit={handleSearch}
        className="hidden md:flex items-center flex-1 max-w-md mx-4"
      >
        <div className="relative w-full">
          <Search className="h-4 w-4 ti-text-muted absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="search"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search candlesticks, RSI, BOS, NSE rules…"
            aria-label="Search trading intelligence modules"
            className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19]/70 pl-9 pr-3 py-1.5 text-sm placeholder:text-[#8D9AB0] focus:border-[#667AFF]"
          />
        </div>
      </form>

      {/* Controls */}
      <div className="flex items-center gap-2">
        <label className="sr-only" htmlFor="navbar-language-select">
          Output Language
        </label>
        <select
          id="navbar-language-select"
          aria-label="Select analysis language"
          value={settings.language}
          onChange={(e) => setLocalLanguage(e.target.value as LanguageType)}
          className="rounded-lg border border-[#1F2E47] bg-[#111C2D] px-2.5 py-1.5 text-xs font-medium cursor-pointer"
        >
          <option value="english">EN</option>
          <option value="hinglish">Hinglish</option>
          <option value="hindi">हिंदी</option>
        </select>

        <button
          type="button"
          onClick={cycleTheme}
          title={`Theme: ${settings.theme}`}
          aria-label={`Switch theme (current: ${settings.theme})`}
          className="p-2 rounded-lg border border-[#1F2E47] bg-[#111C2D] ti-text-muted hover:text-[#E8EDF7]"
        >
          {settings.theme === 'light' ? (
            <Sun className="h-4 w-4 text-[#F5B841]" />
          ) : (
            <Moon className="h-4 w-4 text-[#667AFF]" />
          )}
        </button>

        {user ? (
          <div className="flex items-center gap-1.5">
            <Link
              href="/profile"
              className="inline-flex items-center gap-2 rounded-lg border border-[#1F2E47] bg-[#111C2D] px-2.5 py-1.5 text-xs font-medium hover:border-[#667AFF]"
            >
              <UserIcon className="h-3.5 w-3.5 text-[#667AFF]" />
              <span className="hidden sm:inline max-w-[110px] truncate">
                {user.name}
              </span>
            </Link>
            <button
              type="button"
              onClick={async () => {
                await signOut();
                router.push('/signin');
              }}
              title="Sign out"
              aria-label="Sign out"
              className="p-2 rounded-lg border border-[#1F2E47] bg-[#111C2D] ti-text-muted hover:text-[#F16F83]"
            >
              <LogOut className="h-4 w-4" />
            </button>
          </div>
        ) : (
          <div className="flex items-center gap-2">
            <Link
              href="/signin"
              className="px-3 py-1.5 rounded-lg text-xs font-medium ti-text-muted hover:text-[#E8EDF7]"
            >
              Sign In
            </Link>
            <Link
              href="/signup"
              className="px-3 py-1.5 rounded-lg bg-[#667AFF] hover:bg-[#5267F5] text-white text-xs font-semibold"
            >
              Get Started
            </Link>
          </div>
        )}
      </div>
    </header>
  );
}

export function AppShell({
  children,
  requireAuth = false,
}: {
  children: React.ReactNode;
  requireAuth?: boolean;
}) {
  const [mobileOpen, setMobileOpen] = useState(false);
  const { user, loadingAuth } = useApp();
  const pathname = usePathname();

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar onOpenMobileMenu={() => setMobileOpen(true)} />
      <div className="flex-1 flex">
        <Sidebar
          mobileOpen={mobileOpen}
          onCloseMobile={() => setMobileOpen(false)}
        />
        <main className="flex-1 min-w-0 p-4 sm:p-6 lg:p-8 pb-24 lg:pb-10 max-w-7xl mx-auto w-full">
          {requireAuth && !loadingAuth && !user ? (
            <div className="ti-surface rounded-2xl p-6 sm:p-10 max-w-lg mx-auto my-8 text-center space-y-4">
              <div className="h-12 w-12 rounded-2xl bg-[#667AFF]/15 border border-[#667AFF]/30 flex items-center justify-center text-[#667AFF] mx-auto">
                <UserIcon className="h-6 w-6" />
              </div>
              <h1 className="text-xl font-bold">Sign in to access your workspace</h1>
              <p className="text-sm ti-text-muted">
                Create a free research account or sign in to upload chart screenshots, save immutable analysis history, and manage your watchlist.
              </p>
              <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
                <Link
                  href={`/signin?next=${encodeURIComponent(pathname || '/analyze')}`}
                  className="px-5 py-2.5 rounded-xl bg-[#667AFF] hover:bg-[#5267F5] text-white text-sm font-semibold"
                >
                  Sign In
                </Link>
                <Link
                  href={`/signup?next=${encodeURIComponent(pathname || '/analyze')}`}
                  className="px-5 py-2.5 rounded-xl border border-[#1F2E47] hover:border-[#667AFF] text-sm font-semibold"
                >
                  Create Account
                </Link>
              </div>
            </div>
          ) : (
            children
          )}
        </main>
      </div>

      {/* Mobile bottom quick navigation for Android / iPhone */}
      <nav
        aria-label="Mobile Bottom Navigation"
        className="lg:hidden fixed bottom-0 inset-x-0 z-30 border-t ti-secondary px-2 py-1.5 grid grid-cols-5 gap-1"
      >
        {[
          { href: '/dashboard', label: 'Home', icon: LayoutDashboard },
          { href: '/analyze', label: 'Analyze', icon: Upload },
          { href: '/watchlist', label: 'Watchlist', icon: Star },
          { href: '/history', label: 'History', icon: History },
          { href: '/settings', label: 'Settings', icon: Settings },
        ].map((item) => {
          const active = pathname === item.href;
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex flex-col items-center justify-center py-1 rounded-lg text-[11px] font-medium ${
                active ? 'text-[#667AFF]' : 'ti-text-muted'
              }`}
            >
              <Icon className="h-4 w-4 mb-0.5" />
              <span className="truncate">{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </div>
  );
}
