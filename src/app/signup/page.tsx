'use client';

import React, { Suspense, useState } from 'react';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { Activity, UserPlus } from 'lucide-react';
import { ErrorState } from '@/components/StateViews';
import { useApp } from '@/context/AppContext';
import { apiFetch } from '@/lib/api';
import type { User, UserSettings } from '@/lib/types';

function SignUpForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { signInWithToken } = useApp();

  const [name, setName] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [confirmPassword, setConfirmPassword] = useState<string>('');
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const nextPath = searchParams.get('next') || '/dashboard';

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (password.length < 8) {
      setError('Password must be at least 8 characters long.');
      return;
    }
    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setSubmitting(true);
    try {
      const res = await apiFetch<{
        ok: boolean;
        token: string;
        user: User;
        settings: UserSettings;
      }>('/api/auth/signup', {
        method: 'POST',
        body: JSON.stringify({ name, email, password }),
      });
      signInWithToken(res.token, res.user, res.settings);
      router.push(nextPath);
    } catch (err: any) {
      setError(err?.message || 'Could not create account.');
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
          <h1 className="text-2xl font-bold pt-2">Create Research Account</h1>
          <p className="text-xs sm:text-sm ti-text-muted">
            Save chart analyses, build watchlists, and study V1–V3 market structure.
          </p>
        </div>

        {error && <ErrorState message={error} />}

        <form onSubmit={handleSignUp} className="ti-surface rounded-2xl p-6 space-y-4 shadow-card">
          <div>
            <label htmlFor="signup-name" className="block text-xs font-semibold ti-text-muted mb-1.5">
              Full Name
            </label>
            <input
              id="signup-name"
              type="text"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Aarav Sharma"
              className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3.5 py-2.5 text-sm"
            />
          </div>

          <div>
            <label htmlFor="signup-email" className="block text-xs font-semibold ti-text-muted mb-1.5">
              Email Address
            </label>
            <input
              id="signup-email"
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
            <label htmlFor="signup-password" className="block text-xs font-semibold ti-text-muted mb-1.5">
              Password (minimum 8 characters)
            </label>
            <input
              id="signup-password"
              type="password"
              required
              minLength={8}
              autoComplete="new-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3.5 py-2.5 text-sm"
            />
          </div>

          <div>
            <label htmlFor="signup-confirm" className="block text-xs font-semibold ti-text-muted mb-1.5">
              Confirm Password
            </label>
            <input
              id="signup-confirm"
              type="password"
              required
              minLength={8}
              autoComplete="new-password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3.5 py-2.5 text-sm"
            />
          </div>

          <button
            type="submit"
            disabled={submitting}
            data-testid="signup-submit"
            className="w-full py-3 rounded-xl bg-[#667AFF] hover:bg-[#5267F5] text-white font-semibold text-sm flex items-center justify-center gap-2"
          >
            <UserPlus className="h-4 w-4" />
            <span>{submitting ? 'Creating Account…' : 'Create Account'}</span>
          </button>
        </form>

        <p className="text-center text-xs sm:text-sm ti-text-muted">
          Already have an account?{' '}
          <Link
            href={`/signin?next=${encodeURIComponent(nextPath)}`}
            className="text-[#667AFF] font-semibold hover:underline"
          >
            Sign In
          </Link>
        </p>
      </div>
    </div>
  );
}

export default function SignUpPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center text-sm">Loading…</div>}>
      <SignUpForm />
    </Suspense>
  );
}
