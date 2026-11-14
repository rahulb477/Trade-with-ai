'use client';

import React, { createContext, useCallback, useContext, useEffect, useState } from 'react';
import { apiFetch, getStoredToken, setStoredToken } from '@/lib/api';
import type { LanguageType, ThemeType, User, UserSettings } from '@/lib/types';

interface AppContextValue {
  user: User | null;
  settings: UserSettings;
  loadingAuth: boolean;
  refreshAuth: () => Promise<void>;
  signInWithToken: (token: string, user: User, settings?: UserSettings) => void;
  signOut: () => Promise<void>;
  updateSettings: (partial: Partial<UserSettings>) => Promise<UserSettings>;
  setLocalLanguage: (lang: LanguageType) => void;
  setLocalTheme: (theme: ThemeType) => void;
}

const DEFAULT_SETTINGS: UserSettings = {
  language: 'english',
  theme: 'dark',
  default_mode: 'quick',
  preferred_market: 'auto',
  timezone: 'Asia/Kolkata',
  save_history: true,
  share_anonymous_diagnostics: false,
};

const AppContext = createContext<AppContextValue | undefined>(undefined);

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [settings, setSettings] = useState<UserSettings>(DEFAULT_SETTINGS);
  const [loadingAuth, setLoadingAuth] = useState<boolean>(true);

  const applyThemeClass = useCallback((theme: ThemeType) => {
    if (typeof document === 'undefined') return;
    const root = document.documentElement;
    root.dataset.theme = theme;
    if (theme === 'light') {
      root.classList.remove('dark');
    } else {
      root.classList.add('dark');
    }
  }, []);

  const refreshAuth = useCallback(async () => {
    try {
      const res = await apiFetch<{
        ok: boolean;
        authenticated: boolean;
        user: User | null;
        settings?: UserSettings;
      }>('/api/auth/me');
      if (res.authenticated && res.user) {
        setUser(res.user);
        if (res.settings) {
          setSettings(res.settings);
          applyThemeClass(res.settings.theme);
        }
      } else {
        setUser(null);
      }
    } catch {
      setUser(null);
    } finally {
      setLoadingAuth(false);
    }
  }, [applyThemeClass]);

  useEffect(() => {
    // Check stored local theme/language fallback before auth finishes
    if (typeof window !== 'undefined') {
      const savedTheme = window.localStorage.getItem('ti_theme') as ThemeType | null;
      const savedLang = window.localStorage.getItem('ti_lang') as LanguageType | null;
      if (savedTheme) {
        setSettings((prev) => ({ ...prev, theme: savedTheme }));
        applyThemeClass(savedTheme);
      } else {
        applyThemeClass('dark');
      }
      if (savedLang) {
        setSettings((prev) => ({ ...prev, language: savedLang }));
      }
    }
    refreshAuth();
  }, [applyThemeClass, refreshAuth]);

  const signInWithToken = useCallback(
    (token: string, nextUser: User, nextSettings?: UserSettings) => {
      setStoredToken(token);
      setUser(nextUser);
      if (nextSettings) {
        setSettings(nextSettings);
        applyThemeClass(nextSettings.theme);
      }
      setLoadingAuth(false);
    },
    [applyThemeClass]
  );

  const signOut = useCallback(async () => {
    try {
      if (getStoredToken()) {
        await apiFetch('/api/auth/signout', { method: 'POST' });
      }
    } catch {
      // ignore signout network failure
    } finally {
      setStoredToken(null);
      setUser(null);
    }
  }, []);

  const updateSettings = useCallback(
    async (partial: Partial<UserSettings>): Promise<UserSettings> => {
      const optimistic = { ...settings, ...partial };
      setSettings(optimistic);
      if (partial.theme) {
        applyThemeClass(partial.theme);
        if (typeof window !== 'undefined') window.localStorage.setItem('ti_theme', partial.theme);
      }
      if (partial.language && typeof window !== 'undefined') {
        window.localStorage.setItem('ti_lang', partial.language);
      }
      if (user) {
        const res = await apiFetch<{ ok: boolean; settings: UserSettings }>('/api/settings', {
          method: 'PUT',
          body: JSON.stringify(partial),
        });
        setSettings(res.settings);
        applyThemeClass(res.settings.theme);
        return res.settings;
      }
      return optimistic;
    },
    [applyThemeClass, settings, user]
  );

  const setLocalLanguage = useCallback(
    (lang: LanguageType) => {
      void updateSettings({ language: lang });
    },
    [updateSettings]
  );

  const setLocalTheme = useCallback(
    (theme: ThemeType) => {
      void updateSettings({ theme });
    },
    [updateSettings]
  );

  return (
    <AppContext.Provider
      value={{
        user,
        settings,
        loadingAuth,
        refreshAuth,
        signInWithToken,
        signOut,
        updateSettings,
        setLocalLanguage,
        setLocalTheme,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) {
    throw new Error('useApp must be used within AppProvider');
  }
  return ctx;
}
