/**
 * Relative URL API client.
 * Browser-facing code NEVER calls localhost or 127.0.0.1 directly so live
 * preview proxying works identically on desktop, Android, iPhone, and production.
 */

const TOKEN_STORAGE_KEY = 'ti_auth_token';

export function getStoredToken(): string | null {
  if (typeof window === 'undefined') return null;
  try {
    return window.localStorage.getItem(TOKEN_STORAGE_KEY);
  } catch {
    return null;
  }
}

export function setStoredToken(token: string | null): void {
  if (typeof window === 'undefined') return;
  try {
    if (token) {
      window.localStorage.setItem(TOKEN_STORAGE_KEY, token);
    } else {
      window.localStorage.removeItem(TOKEN_STORAGE_KEY);
    }
  } catch {
    // ignore storage errors in restricted private browsing
  }
}

export class ApiError extends Error {
  status: number;
  code?: string;

  constructor(message: string, status: number, code?: string) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.code = code;
  }
}

export async function apiFetch<T = any>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getStoredToken();
  const headers = new Headers(options.headers || {});
  if (!headers.has('Content-Type') && options.body) {
    headers.set('Content-Type', 'application/json');
  }
  if (token && !headers.has('Authorization')) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 30000);

  try {
    const response = await fetch(path, {
      ...options,
      headers,
      credentials: 'include',
      signal: options.signal || controller.signal,
    });

    let data: any = null;
    const contentType = response.headers.get('content-type') || '';
    if (contentType.includes('application/json')) {
      data = await response.json();
    } else {
      const txt = await response.text();
      data = { ok: response.ok, error: txt || response.statusText };
    }

    if (!response.ok || data?.ok === false) {
      throw new ApiError(
        data?.error || `Request failed with status ${response.status}`,
        response.status,
        data?.code
      );
    }
    return data as T;
  } catch (err: any) {
    if (err?.name === 'AbortError') {
      throw new ApiError('Request timed out. Please check your connection and retry.', 408, 'TIMEOUT');
    }
    if (err instanceof ApiError) {
      throw err;
    }
    throw new ApiError(
      err?.message || 'Network error while communicating with the intelligence server.',
      0,
      'NETWORK_ERROR'
    );
  } finally {
    clearTimeout(timeoutId);
  }
}

export function buildScreenshotUrl(analysisId: string): string {
  const token = getStoredToken();
  if (token) {
    return `/api/analyses/${encodeURIComponent(analysisId)}/image?token=${encodeURIComponent(token)}`;
  }
  return `/api/analyses/${encodeURIComponent(analysisId)}/image`;
}

export function formatTimestamp(iso: string | undefined, timezone?: string): string {
  if (!iso) return 'Unknown';
  try {
    const dt = new Date(iso);
    if (Number.isNaN(dt.getTime())) return iso;
    return new Intl.DateTimeFormat('en-IN', {
      dateStyle: 'medium',
      timeStyle: 'short',
      timeZone: timezone || undefined,
    }).format(dt);
  } catch {
    return new Date(iso).toLocaleString();
  }
}

export function formatBytes(bytes: number): string {
  if (!bytes || bytes <= 0) return '0 B';
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}
