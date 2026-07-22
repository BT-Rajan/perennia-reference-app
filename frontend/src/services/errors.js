/**
 * Centralized error configuration for the frontend.
 *
 * The backend already returns a `{ error: { code, message } }` body with a
 * user-facing message for every application-level failure (see
 * backend/app/config/errors.py) - components should show that message
 * as-is. This file exists for the cases the backend never gets a chance
 * to describe: the request never reached it, or something failed before
 * a response existed. It also lets us apply a consistent code -> message
 * fallback for API errors, and can override tone by code if a page ever
 * disagrees with the generic message.
 *
 * No component should hardcode an error string. If a message is not
 * available on the response body, look it up here.
 */
export const FRONTEND_ERROR_MESSAGES = {
  network_error: "Could not reach the server. Check your connection and try again.",
  unexpected_error: "Something unexpected happened. Please try again.",
  session_expired: "Your session has expired. Please sign in again.",
};

/**
 * Resolve a user-facing message for an API/network failure.
 *
 * @param {{ code?: string, message?: string } | null} apiError - the parsed
 *   `error` object from a backend JSON response, if one was received.
 * @param {string} fallbackCode - a key into FRONTEND_ERROR_MESSAGES to use
 *   when no backend message is available.
 */
export function resolveErrorMessage(apiError, fallbackCode = "unexpected_error") {
  if (apiError && apiError.message) {
    return apiError.message;
  }
  return FRONTEND_ERROR_MESSAGES[fallbackCode] || FRONTEND_ERROR_MESSAGES.unexpected_error;
}
