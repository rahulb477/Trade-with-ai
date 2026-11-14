'use client';

import React, { Suspense, useState } from 'react';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { Activity, KeyRound, LogIn } from 'lucide-react';
import { ErrorState } from '@/components/StateViews';
import { useApp } from '@/context/AppContext';
import { apiFetch } from '@/lib/api';
import type { User, UserSettings } from '@/lib/types';

function SignInForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { signInWithToken } = useApp();

  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Password reset modal/mode
  const [resetMode, setResetMode] = useState<boolean>(false);
  const [resetStep, setResetStep] = useState<'request' | 'confirm'>('request');
  const [resetCode, setResetCode] = useState<string>('');
  const [newPassword, setNewPassword] = useState<string>('');
  const [resetBanner, setResetBanner] = useState<string | null>(null);

  const nextPath = searchParams.get('next') || '/dashboard';

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const res = await apiFetch<{
        ok: boolean;
        token: string;
        user: User;
        settings: UserSettings;
      }>('/api/auth/signin', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      });
      signInWithToken(res.token, res.user, res.settings);
      router.push(nextPath);
    } catch (err: any) {
      setError(err?.message || 'Sign in failed.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleRequestReset = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    setResetBanner(null);
    try {
      const res = await apiFetch<{
        ok: boolean;
        message: string;
        local_verification_code?: string;
      }>('/api/auth/reset-request', {
        method: 'POST',
        body: JSON.stringify({ email }),
      });
      if (res.local_verification_code) {
        setResetCode(res.local_verification_code);
        setResetBanner(
          `${res.message} Local sandbox verification code: ${res.local_verification_code}`
        );
      } else {
        setResetBanner(res.message);
      }
      setResetStep('confirm');
    } catch (err: any) {
      setError(err?.message || 'Could not initiate password reset.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleConfirmReset = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const res = await apiFetch<{ ok: boolean; message: string }>(
        '/api/auth/reset-confirm',
        {
          method: 'POST',
          body: JSON.stringify({
            email,
            code: resetCode,
            new_password: newPassword,
          }),
        }
      );
      setResetBanner(res.message);
      setResetMode(false);
      setResetStep('request');
      setPassword('');
    } catch (err: any) {
      setError(err?.message || 'Password reset failed.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center space-y-2">
          <Link href="/" className="inline-flex items-center gap-2.5">
            <div className="h-10 w-10 rounded-xl bg-[#667AFF] flex items-center justify-center text-white">
              <Activity className="h-5 w-5" />
            </div>
            <span className="font-bold text-lg">AI Trading Intelligence</span>
          </Link>
          <h1 className="text-2xl font-bold pt-2">
            {resetMode ? 'Reset Your Password' : 'Sign In to Research Workspace'}
          </h1>
          <p className="text-xs sm:text-sm ti-text-muted">
            {resetMode
              ? 'Generate a 6-digit verification code to set a new password.'
              : 'Deep Market Intelligence. Simple Trading Insights.'}
          </p>
        </div>

        {error && <ErrorState message={error} />}
        {resetBanner && (
          <div className="rounded-xl border border-[#16B995]/40 bg-[#16B995]/10 p-3.5 text-xs text-[#16B995]">
            {resetBanner}
          </div>
        )}

        {!resetMode ? (
          <form onSubmit={handleSignIn} className="ti-surface rounded-2xl p-6 space-y-4 shadow-card">
            <div>
              <label htmlFor="signin-email" className="block text-xs font-semibold ti-text-muted mb-1.5">
                Email Address
              </label>
              <input
                id="signin-email"
                type="email"
                required
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3.5 py-2.5 text-sm"
              />
            </div>

            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label htmlFor="signin-password" className="text-xs font-semibold ti-text-muted">
                  Password
                </label>
                <button
                  type="button"
                  onClick={() => {
                    setResetMode(true);
                    setError(null);
                  }}
                  className="text-xs text-[#667AFF] hover:underline"
                >
                  Forgot password?
                </button>
              </div>
              <input
                id="signin-password"
                type="password"
                required
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3.5 py-2.5 text-sm"
              />
            </div>

            <button
              type="submit"
              disabled={submitting}
              data-testid="signin-submit"
              className="w-full py-3 rounded-xl bg-[#667AFF] hover:bg-[#5267F5] text-white font-semibold text-sm flex items-center justify-center gap-2"
            >
              <LogIn className="h-4 w-4" />
              <span>{submitting ? 'Signing In…' : 'Sign In'}</span>
            </button>
          </form>
        ) : resetStep === 'request' ? (
          <form onSubmit={handleRequestReset} className="ti-surface rounded-2xl p-6 space-y-4">
            <div>
              <label htmlFor="reset-email" className="block text-xs font-semibold ti-text-muted mb-1.5">
                Account Email
              </label>
              <input
                id="reset-email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3.5 py-2.5 text-sm"
              />
            </div>
            <button
              type="submit"
              disabled={submitting}
              className="w-full py-3 rounded-xl bg-[#667AFF] hover:bg-[#5267F5] text-white font-semibold text-sm flex items-center justify-center gap-2"
            >
              <KeyRound className="h-4 w-4" />
              <span>{submitting ? 'Generating Code…' : 'Send Reset Code'}</span>
            </button>
            <button
              type="button"
              onClick={() => setResetMode(false)}
              className="w-full text-xs ti-text-muted hover:text-[#E8EDF7]"
            >
              Back to Sign In
            </button>
          </form>
        ) : (
          <form onSubmit={handleConfirmReset} className="ti-surface rounded-2xl p-6 space-y-4">
            <div>
              <label htmlFor="reset-code" className="block text-xs font-semibold ti-text-muted mb-1.5">
                6-Digit Reset Code
              </label>
              <input
                id="reset-code"
                type="text"
                required
                value={resetCode}
                onChange={(e) => setResetCode(e.target.value)}
                placeholder="123456"
                className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3.5 py-2.5 text-sm font-mono"
              />
            </div>
            <div>
              <label htmlFor="reset-new-pw" className="block text-xs font-semibold ti-text-muted mb-1.5">
                New Password (min 8 characters)
              </label>
              <input
                id="reset-new-pw"
                type="password"
                required
                minLength={8}
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                placeholder="New secure password"
                className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3.5 py-2.5 text-sm"
              />
            </div>
            <button
              type="submit"
              disabled={submitting}
              className="w-full py-3 rounded-xl bg-[#16B995] hover:opacity-90 text-white font-semibold text-sm"
            >
              {submitting ? 'Updating…' : 'Confirm New Password'}
            </button>
          </form>
        )}

        <p className="text-center text-xs sm:text-sm ti-text-muted">
          Don&apos;t have an account?{' '}
          <Link
            href={`/signup?next=${encodeURIComponent(nextPath)}`}
            className="text-[#667AFF] font-semibold hover:underline"
          >
            Create Account
          </Link>
        </p>
      </div>
    </div>
  );
}

export default function SignInPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center text-sm">Loading…</div>}>
      <SignInForm />
    </Suspense>
  );
}
