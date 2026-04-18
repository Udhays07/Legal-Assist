/**
 * Client-side auth helpers for localStorage token management.
 * All auth state is stored under the 'legal_assist_' prefix.
 */

const TOKEN_KEY = "legal_assist_token";
const ROLE_KEY = "legal_assist_role";
const NAME_KEY = "legal_assist_name";
const USER_ID_KEY = "legal_assist_user_id";

export interface AuthState {
  token: string;
  role: string;
  name: string;
  userId: string;
}

/** Persist auth state to localStorage after successful login / register. */
export function saveAuth({ token, role, name, userId }: AuthState): void {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(ROLE_KEY, role);
  localStorage.setItem(NAME_KEY, name);
  localStorage.setItem(USER_ID_KEY, userId);
}

/** Remove all auth state (logout). */
export function clearAuth(): void {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(ROLE_KEY);
  localStorage.removeItem(NAME_KEY);
  localStorage.removeItem(USER_ID_KEY);
}

export const getToken = (): string | null => localStorage.getItem(TOKEN_KEY);
export const getRole = (): string | null => localStorage.getItem(ROLE_KEY);
export const getName = (): string | null => localStorage.getItem(NAME_KEY);
export const getUserId = (): string | null => localStorage.getItem(USER_ID_KEY);

/** True if a token exists in localStorage (does NOT verify expiry). */
export const isAuthenticated = (): boolean => !!getToken();

/** True if the stored role is "admin". */
export const isAdmin = (): boolean => getRole() === "admin";

/**
 * Returns an Authorization header object for API requests.
 * Returns an empty object if no token is stored.
 */
export function authHeaders(): Record<string, string> {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}
