'use client';

import React, { useEffect, useState } from 'react';
import { Check, KeyRound, User as UserIcon } from 'lucide-react';
import { AppShell } from '@/components/AppShell';
import { EducationalDisclaimer, ErrorState } from '@/components/StateViews';
import { useApp } from '@/context/AppContext';
import { apiFetch, formatTimestamp } from '@/lib/api';
import type { User } from '@/lib/types';

export default function UserProfilePage() {
  const { user, refreshAuth, settings } = useApp();

  const [name, setName] = useState<string>(user?.name || '');
  const [bio, setBio] = useState<string>(user?.bio || '');
  const [currentPassword, setCurrentPassword] = useState<string>('');
  const [newPassword, setNewPassword] = useState<string>('');
  const [saving, setSaving] = useState<boolean>(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (user) {
      setName(user.name);
      setBio(user.bio || '');
    }
  }, [user]);

  const handleSaveProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    setSuccessMsg(null);
    try {
      await apiFetch<{ ok: boolean; user: User }>('/api/auth/profile', {
        method: 'PUT',
        body: JSON.stringify({
          name,
          bio,
          current_password: currentPassword || undefined,
          new_password: newPassword || undefined,
        }),
      });
      await refreshAuth();
      setCurrentPassword('');
      setNewPassword('');
      setSuccessMsg('Account profile updated.');
    } catch (err: any) {
      setError(err?.message || 'Failed to update profile.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <AppShell requireAuth>
      <div className="max-w-3xl mx-auto space-y-6">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight flex items-center gap-2.5">
            <UserIcon className="h-7 w-7 text-[#667AFF]" />
            <span>User Profile</span>
          </h1>
          <p className="text-sm ti-text-muted mt-1">
            Manage your researcher identity and account security credentials.
          </p>
        </div>

        {user && (
          <div className="ti-surface rounded-2xl p-5 flex flex-wrap items-center justify-between gap-4 text-xs sm:text-sm">
            <div>
              <p className="font-bold text-base">{user.name}</p>
              <p className="ti-text-muted font-mono">{user.email}</p>
            </div>
            <div className="text-right space-y-1">
              <span className="px-2.5 py-1 rounded-lg bg-[#667AFF]/15 border border-[#667AFF]/30 text-[#667AFF] font-mono text-xs uppercase">
                Role: {user.role}
              </span>
              <p className="text-xs ti-text-muted">
                Joined {formatTimestamp(user.created_at, settings.timezone)}
              </p>
            </div>
          </div>
        )}

        {error && <ErrorState message={error} />}
        {successMsg && (
          <div className="rounded-xl border border-[#16B995]/40 bg-[#16B995]/10 px-4 py-3 text-xs sm:text-sm text-[#16B995] flex items-center gap-2">
            <Check className="h-4 w-4" />
            <span>{successMsg}</span>
          </div>
        )}

        <form onSubmit={handleSaveProfile} className="ti-surface rounded-2xl p-5 sm:p-7 space-y-5">
          <div>
            <label htmlFor="prof-name" className="block text-xs font-semibold ti-text-muted mb-1.5">
              Display Name
            </label>
            <input
              id="prof-name"
              type="text"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3.5 py-2.5 text-sm"
            />
          </div>

          <div>
            <label htmlFor="prof-bio" className="block text-xs font-semibold ti-text-muted mb-1.5">
              Research Focus / Notes (Optional)
            </label>
            <textarea
              id="prof-bio"
              rows={3}
              value={bio}
              onChange={(e) => setBio(e.target.value)}
              placeholder="e.g. Studying NSE NIFTY 15m structure and candlestick invalidation rules."
              className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3.5 py-2.5 text-sm"
            />
          </div>

          <div className="border-t border-[#1F2E47] pt-5 space-y-4">
            <h2 className="text-sm font-bold flex items-center gap-2">
              <KeyRound className="h-4 w-4 text-[#667AFF]" />
              <span>Change Password (Optional)</span>
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label htmlFor="prof-cur-pw" className="block text-xs font-semibold ti-text-muted mb-1.5">
                  Current Password
                </label>
                <input
                  id="prof-cur-pw"
                  type="password"
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  placeholder="Leave blank to keep unchanged"
                  className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3.5 py-2.5 text-sm"
                />
              </div>
              <div>
                <label htmlFor="prof-new-pw" className="block text-xs font-semibold ti-text-muted mb-1.5">
                  New Password (min 8 chars)
                </label>
                <input
                  id="prof-new-pw"
                  type="password"
                  minLength={8}
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  placeholder="New password"
                  className="w-full rounded-xl border border-[#1F2E47] bg-[#080D19] px-3.5 py-2.5 text-sm"
                />
              </div>
            </div>
          </div>

          <div className="flex justify-end pt-2">
            <button
              type="submit"
              disabled={saving}
              className="px-6 py-2.5 rounded-xl bg-[#667AFF] hover:bg-[#5267F5] text-white text-sm font-semibold"
            >
              {saving ? 'Saving…' : 'Update Profile'}
            </button>
          </div>
        </form>

        <EducationalDisclaimer />
      </div>
    </AppShell>
  );
}
