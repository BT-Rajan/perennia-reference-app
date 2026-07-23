import { resolveErrorMessage } from "./errors";
import { getTokens, setTokens, clearTokens } from "../state/auth";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export class ApiError extends Error {
  constructor(code, message, status) {
    super(message);
    this.code = code;
    this.status = status;
  }
}

async function parseErrorBody(response) {
  try {
    const body = await response.json();
    return body && body.error ? body.error : null;
  } catch {
    return null;
  }
}

async function doFetch(path, options, { auth: withAuth } = { auth: true }) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (withAuth) {
    const tokens = getTokens();
    if (tokens && tokens.access_token) {
      headers["Authorization"] = `Bearer ${tokens.access_token}`;
    }
  }

  let response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });
  } catch {
    throw new ApiError("network_error", resolveErrorMessage(null, "network_error"), 0);
  }

  return response;
}

async function refreshAccessToken() {
  const tokens = getTokens();
  if (!tokens || !tokens.refresh_token) return false;

  const response = await doFetch(
    "/api/auth/refresh",
    { method: "POST", body: JSON.stringify({ refresh_token: tokens.refresh_token }) },
    { auth: false }
  );

  if (!response.ok) {
    clearTokens();
    return false;
  }

  const data = await response.json();
  setTokens(data);
  return true;
}

/**
 * Perform an authenticated (or public) API call. On a 401 with a live
 * refresh token, transparently refreshes the access token once and
 * retries - callers never see the intermediate 401.
 */
export async function apiFetch(path, { method = "GET", body, auth: withAuth = true } = {}) {
  const options = { method, body: body !== undefined ? JSON.stringify(body) : undefined };

  let response = await doFetch(path, options, { auth: withAuth });

  if (response.status === 401 && withAuth) {
    const refreshed = await refreshAccessToken();
    if (refreshed) {
      response = await doFetch(path, options, { auth: withAuth });
    }
  }

  if (!response.ok) {
    const errorBody = await parseErrorBody(response);
    const code = errorBody ? errorBody.code : "unexpected_error";
    const message = resolveErrorMessage(errorBody, "unexpected_error");
    throw new ApiError(code, message, response.status);
  }

  if (response.status === 204) return null;
  return response.json();
}

/**
 * Perform an authenticated multipart/form-data request (file uploads and
 * new file versions). Mirrors apiFetch's auth/refresh/error handling, but
 * never sets a JSON Content-Type - the browser sets the multipart boundary
 * itself when the body is a FormData instance.
 */
async function doUpload(path, formData) {
  const headers = {};
  const tokens = getTokens();
  if (tokens && tokens.access_token) {
    headers["Authorization"] = `Bearer ${tokens.access_token}`;
  }

  try {
    return await fetch(`${API_BASE_URL}${path}`, { method: "POST", headers, body: formData });
  } catch {
    throw new ApiError("network_error", resolveErrorMessage(null, "network_error"), 0);
  }
}

export async function apiUpload(path, formData) {
  let response = await doUpload(path, formData);

  if (response.status === 401) {
    const refreshed = await refreshAccessToken();
    if (refreshed) {
      response = await doUpload(path, formData);
    }
  }

  if (!response.ok) {
    const errorBody = await parseErrorBody(response);
    const code = errorBody ? errorBody.code : "unexpected_error";
    const message = resolveErrorMessage(errorBody, "unexpected_error");
    throw new ApiError(code, message, response.status);
  }

  return response.json();
}
