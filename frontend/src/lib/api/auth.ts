/**
 * API call wrappers for authentication endpoints.
 * All functions throw on non-2xx responses with the backend error detail.
 */

import { API_BASE_URL, API_ENDPOINTS } from "@/features/admin/api/api.constants";

export interface TokenResponse {
  access_token: string;
  token_type: string;
  role: string;
  name: string;
  user_id: string;
}

export interface MeResponse {
  user_id: string;
  name: string;
  role: string;
  email: string | null;
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(body.detail ?? `HTTP ${res.status}`);
  }
  return res.json();
}

/** POST /auth/login — returns TokenResponse or throws with error message. */
export async function apiLogin(email: string, password: string): Promise<TokenResponse> {
  const res = await fetch(`${API_BASE_URL}${API_ENDPOINTS.auth.login}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  return handleResponse<TokenResponse>(res);
}

/** POST /auth/register — returns TokenResponse or throws with error message. */
export async function apiRegister(
  name: string,
  email: string,
  password: string
): Promise<TokenResponse> {
  const res = await fetch(`${API_BASE_URL}${API_ENDPOINTS.auth.register}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password }),
  });
  return handleResponse<TokenResponse>(res);
}

/** GET /auth/me — returns MeResponse or throws (requires valid token). */
export async function apiGetMe(token: string): Promise<MeResponse> {
  const res = await fetch(`${API_BASE_URL}${API_ENDPOINTS.auth.me}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return handleResponse<MeResponse>(res);
}
