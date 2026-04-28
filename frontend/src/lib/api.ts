import { get } from 'svelte/store';
import { token } from './stores/auth';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:4443/api/v1';

async function request(path: string, options: RequestInit = {}) {
  const current = get(token);
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  };
  if (current) headers['Authorization'] = `Bearer ${current}`;

  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.message || 'Request failed');
  }
  return response.json();
}

export const login = (username: string, password: string) => request('/auth/login', { method: 'POST', body: JSON.stringify({ username, password }) });
export const authStatus = () => request('/auth/status', { method: 'GET' });

export type RegisterPayload = { email?: string; username?: string; password: string; display_name?: string; country?: string; profile_type?: string; accept_terms?: boolean; accept_privacy?: boolean; marketing_opt_in?: boolean; };

export function register(username: string, password: string, extra?: Record<string, unknown>): Promise<unknown>;
export function register(payload: RegisterPayload): Promise<unknown>;
export function register(usernameOrPayload: string | RegisterPayload, password?: string, extra: Record<string, unknown> = {}): Promise<unknown> {
  if (typeof usernameOrPayload === 'string') {
    return request('/auth/register', { method: 'POST', body: JSON.stringify({ username: usernameOrPayload, password, accept_terms: true, accept_privacy: true, ...extra }) });
  }
  const payload = usernameOrPayload;
  const username = payload.username ?? payload.email ?? '';
  return request('/auth/register', { method: 'POST', body: JSON.stringify({ ...payload, username, accept_terms: payload.accept_terms ?? true, accept_privacy: payload.accept_privacy ?? true }) });
}

export const saveOnboarding = (payload: { primary_goal: string; platforms: string[]; categories: string[]; regions: string[] }) => request('/me/preferences', { method: 'POST', body: JSON.stringify(payload) });
export const fetchVideos = () => request('/videos');
export const fetchDailyRadar = () => request('/radar/daily');
export const fetchPlans = () => request('/plans');
export const fetchBillingStatus = () => request('/billing/status');
export const createCheckout = (plan: 'pro' | 'studio') => request('/billing/checkout', { method: 'POST', body: JSON.stringify({ plan }) });
export const openBillingPortal = () => request('/billing/portal', { method: 'POST' });
export const scanVideos = () => request('/videos/scan', { method: 'POST' });
export const saveNote = (video_id: string, notes: string) => request('/notes', { method: 'POST', body: JSON.stringify({ video_id, notes }) });

export const fetchFavorites = () => request('/favorites');
export const addFavorite = (platform: string, trend_id: string) => request('/favorites', { method: 'POST', body: JSON.stringify({ platform, trend_id }) });
export const deleteFavorite = (platform: string, trend_id: string) => request(`/favorites/${platform}/${trend_id}`, { method: 'DELETE' });

export const fetchConsents = () => request('/me/consents');
export const saveConsent = (payload: { consent_type: string; granted: boolean; version: string }) => request('/me/consents', { method: 'POST', body: JSON.stringify(payload) });
export const requestDataExport = () => request('/me/data-export', { method: 'POST' });
export const requestDeleteAccount = () => request('/me/delete-request', { method: 'POST' });
