import { reactive } from "vue";
import { apiFetch, ApiError } from "../services/api";

const STORAGE_KEY = "abc_enterprises_tokens";

export const authState = reactive({
  subjectId: null,
  roles: [],
  permissions: [],
  ready: false, // true once an initial /me attempt (or skip) has resolved
});

export function getTokens() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function setTokens(tokens) {
  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify({
      access_token: tokens.access_token,
      refresh_token: tokens.refresh_token,
      access_token_expires_at: tokens.access_token_expires_at,
    })
  );
}

export function clearTokens() {
  localStorage.removeItem(STORAGE_KEY);
}

function resetIdentity() {
  authState.subjectId = null;
  authState.roles = [];
  authState.permissions = [];
}

export function isAuthenticated() {
  return !!getTokens();
}

export function hasPermission(code) {
  return authState.permissions.includes(code);
}

/** Populate authState from perennia-access's view of the current identity. */
export async function loadCurrentIdentity() {
  if (!getTokens()) {
    resetIdentity();
    authState.ready = true;
    return;
  }
  try {
    const me = await apiFetch("/api/auth/me");
    authState.subjectId = me.subject_id;
    authState.roles = me.roles;
    authState.permissions = me.permissions;
  } catch {
    // Token invalid/expired beyond refresh - treat as signed out.
    clearTokens();
    resetIdentity();
  } finally {
    authState.ready = true;
  }
}

export async function login(email, password) {
  const result = await apiFetch("/api/auth/login", { method: "POST", body: { email, password }, auth: false });
  setTokens(result);
  await loadCurrentIdentity();
}

export async function register(email, password, role) {
  return apiFetch("/api/auth/register", { method: "POST", body: { email, password, role }, auth: false });
}

export async function logout() {
  try {
    await apiFetch("/api/auth/logout", { method: "POST" });
  } catch {
    // Best-effort: even if the network call fails, clear local state below.
  }
  clearTokens();
  resetIdentity();
}

export { ApiError };
