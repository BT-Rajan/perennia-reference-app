"""
Demo Mailer implementation for perennia-auth.

perennia-auth requires the consuming application to provide a Mailer
(see perennia_auth.mailer.Mailer). This reference app does not ship an SMTP
integration - that is a deployment concern outside the scope of a reference
app - so instead it implements the same protocol by printing the links to
the backend console.

This is a demo convenience only. It does not weaken or bypass email
verification: verification is still required, the token still expires,
and the token is still consumed exactly once by perennia-auth. Only the
*delivery channel* is replaced (console instead of SMTP) so the reference
app can be exercised end-to-end without external mail infrastructure.
"""
from urllib.parse import urlencode


class ConsoleMailer:
    def __init__(self, frontend_base_url: str):
        self._frontend_base_url = frontend_base_url.rstrip("/")

    def _print(self, heading: str, link: str) -> None:
        print("\n" + "=" * 72)
        print(f"[ConsoleMailer] {heading}")
        print(link)
        print("=" * 72 + "\n")

    def send_verification_email(self, email: str, raw_token: str) -> None:
        link = f"{self._frontend_base_url}/verify-email?{urlencode({'token': raw_token})}"
        self._print(f"Verify email for {email}", link)

    def send_email_change_verification(self, new_email: str, raw_token: str) -> None:
        link = f"{self._frontend_base_url}/verify-email?{urlencode({'token': raw_token})}"
        self._print(f"Confirm new email {new_email}", link)

    def send_password_recovery_email(self, email: str, raw_token: str) -> None:
        link = f"{self._frontend_base_url}/reset-password?{urlencode({'token': raw_token})}"
        self._print(f"Reset password for {email}", link)

    def notify_email_changed(self, old_email: str, new_email: str) -> None:
        self._print("Email address changed", f"{old_email} -> {new_email}")
