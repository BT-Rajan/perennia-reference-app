# ABC Enterprises — Perennia Reference Application

A small, compact reference application showing how a real Perennia
application is expected to consume the two core Perennia packages:

- [`perennia-auth`](https://github.com/BT-Rajan/perennia-auth) — who is this user?
- [`perennia-access`](https://github.com/BT-Rajan/perennia-access) — what may this user do?

This repository contains **only the application layer**. Neither package's
source code is vendored, copied, or forked here — both are installed as Git
dependencies (pinned to their `v1.0.0` tags) and used through their public
APIs, exactly as any other Perennia application would.

```
Browser
  │
  ▼
ABC Enterprises (this repo)      — routes, permission vocabulary, UI
  │
  ▼
perennia-access                  — roles, permissions, ALLOW / DENY
  │
  ▼
perennia-auth                    — registration, sign-in, sessions, identity
```

There is no second token exchange between the two packages. Every protected
route authenticates once (`perennia-auth.verify_access_token`) to get an
`AuthenticatedIdentity`, then passes that identity into `perennia-access` to
check a permission. See `backend/app/deps.py`.

## What this demonstrates

- Registration, sign-in, session refresh, logout, forgot/reset password —
  all via `perennia-auth`, none of it reimplemented here.
- Permission-based authorization via `perennia-access` — routes check
  permission codes (`profile.view`, `reports.view`, `admin.access`), never
  role names. Nothing in this codebase does `if role == "Administrator"`.
- A single, centralized error catalog (`backend/app/config/errors.py`) that
  is the one place every HTTP status and user-facing message is declared,
  for both this app's own errors and every `perennia-auth` / `perennia-access`
  exception.
- A clear, deliberate distinction between **authentication failure** (401,
  redirected to `/login`) and **authorization failure** (403, redirected to
  `/access-denied`) — an authenticated-but-unauthorized user is never sent
  back to the login page.

This is **not** a CRM, ERP, dashboard, or analytics product. `/reports` and
`/administration` contain no real business data — they exist purely to
demonstrate a permission-gated route.

## Two things worth knowing before you start

**1. Demo role picker at registration.** In a real deployment, roles are
assigned by an administrator, not chosen by the person signing up. This
reference app's registration form *does* let you pick Employee / Manager /
Administrator, purely so you can explore all three permission levels without
needing separate admin tooling. This is a demo convenience, not a pattern to
copy into a production application.

**2. Email verification has no SMTP integration.** `perennia-auth`
requires the consuming application to supply a `Mailer`, and — this is a
real quirk of the current package, not something invented for this demo —
`perennia-auth`'s `require_email_verification` config flag exists but isn't
actually enforced in its own logic: every new account starts `pending` and
must call `/api/auth/verify-email` regardless of that setting. Rather than
require a real SMTP server for a reference app, `backend/app/mailer.py`
implements a `ConsoleMailer` that prints verification and password-reset
links to the **backend console** instead of sending email. Verification is
still fully required and each token is still single-use and expiring — only
the delivery channel changed. Swap in a real `Mailer` implementation for
production use.

## Repository structure

```
abc-enterprises-reference/
├── .env.example              # shared DB / perennia-auth config
├── backend/
│   ├── pyproject.toml        # declares perennia-auth & perennia-access as Git deps
│   ├── scripts/init_db.py    # applies both packages' schema.sql to one shared DB
│   └── app/
│       ├── main.py           # FastAPI app, CORS, startup seeding, error handlers
│       ├── deps.py           # the auth+access integration seam
│       ├── mailer.py         # ConsoleMailer (see above)
│       ├── config/
│       │   ├── settings.py   # env-based configuration
│       │   └── errors.py     # the centralized error catalog
│       ├── permissions/
│       │   └── definitions.py# the app's permission vocabulary + demo roles
│       └── api/               # auth, home, profile, reports, administration
└── frontend/
    ├── .env.example           # VITE_API_BASE_URL
    └── src/
        ├── router/            # route guards: auth failure vs. authz failure
        ├── state/auth.js      # token storage + reactive identity state
        ├── services/
        │   ├── api.js         # fetch wrapper w/ auto refresh-on-401
        │   └── errors.js      # centralized frontend error-message config
        ├── components/        # NavBar, AlertBanner, PermissionChip
        ├── pages/              # the 9 pages below
        └── styles/             # tokens.css / theme.css / components.css
```

## Pages

| Path | Purpose |
|---|---|
| `/` | Public landing page |
| `/login`, `/register`, `/forgot-password`, `/reset-password`, `/verify-email` | Auth flows (perennia-auth) |
| `/home` | Authenticated landing page — areas shown/hidden by permission |
| `/profile` | Requires `profile.view` |
| `/reports` | Requires `reports.view` |
| `/administration` | Requires `admin.access` |
| `/access-denied` | Authenticated but missing a permission (distinct from a 401) |

## Roles and permissions (demo data)

| Role | Permissions |
|---|---|
| Employee | `profile.view` |
| Manager | `profile.view`, `reports.view` |
| Administrator | `profile.view`, `reports.view`, `admin.access` |

Defined once in `backend/app/permissions/definitions.py` and seeded into
`perennia-access` idempotently on every backend startup.

## Database files

- `backend/sql/schema.sql` — a **generated** snapshot: the actual `schema.sql`
  files shipped inside the installed `perennia-auth` and `perennia-access`
  packages, exported verbatim and concatenated. Produced by
  `backend/scripts/generate_schema_sql.py`; re-run that script after
  upgrading either dependency rather than hand-editing the output. Equivalent
  to what `backend/scripts/init_db.py` applies at setup time - this file
  exists so the schema can also be applied with a plain SQL client.
- `backend/sql/test_data.sql` — seeds the application's permission
  vocabulary and the three demo roles into `perennia-access` (mirrors
  `backend/app/permissions/definitions.py`, which seeds the same data
  automatically on every backend startup). It intentionally contains no
  `perennia-auth` data - see below.
- `backend/scripts/seed_demo_data.py` — creates three **login-ready** demo
  accounts, one per role. A real account needs a password hash produced by
  perennia-auth's own hashing code, which can't be hand-written as SQL
  without reimplementing authentication, so this goes through the real
  `perennia-auth` / `perennia-access` APIs instead (the same ones the
  backend itself uses) and auto-verifies each account in-process. Safe to
  re-run - existing accounts are skipped.

  | Role | Email | Password |
  |---|---|---|
  | Employee | `employee.demo@abc-enterprises.example` | `DemoPass123` |
  | Manager | `manager.demo@abc-enterprises.example` | `DemoPass123` |
  | Administrator | `administrator.demo@abc-enterprises.example` | `DemoPass123` |

## Setup

Prerequisites: Python 3.10+, Node.js 18+, a running MySQL-compatible server
(MySQL or MariaDB).

```bash
git clone https://github.com/BT-Rajan/perennia-reference-app.git
cd perennia-reference-app

# 1. Backend — installs perennia-auth and perennia-access from Git
python3 -m venv .venv
source .venv/bin/activate
pip install -e backend/

# 2. Configure
cp .env.example .env
# edit .env: set AUTH_SIGNING_SECRET and your DB credentials
cp frontend/.env.example frontend/.env

# 3. Initialize the database (applies both packages' schema.sql)
python backend/scripts/init_db.py

# 3b. Optional: create login-ready demo accounts (see Database files below)
python backend/scripts/seed_demo_data.py

# 4. Run the backend
uvicorn app.main:app --reload --port 8000 --app-dir backend

# 5. Run the frontend (separate terminal)
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173`, register an account, then check the
**backend terminal** for the verification link (see the mailer note above).

No Docker, no test suite, by design — see the project brief this reference
app was built from for the reasoning.

## Security notes

- Every protected backend route independently re-checks authentication and
  authorization; the frontend hiding a link is a UX nicety, never the
  security boundary.
- Passwords, tokens, SQL, tracebacks, and internal file paths are never
  returned to a client — the global exception handler in `app/main.py`
  logs unexpected failures server-side and returns only the generic message
  from the error catalog.
- Forgot-password and registration responses are intentionally identical
  whether or not an email address exists, to avoid account enumeration.
