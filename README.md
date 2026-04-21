# WVVYReach

AI-powered outbound CRM for sending personalised cold email campaigns. Built on Django, deployed on Railway at [wvvy.pro](https://wvvy.pro).

## What it does

- **Lead generation** — search LinkedIn via Apify and import contacts directly into the CRM
- **Automated outreach** — send personalised email sequences to imported leads via Resend
- **AI email replies** — inbound replies are handled by an AI pipeline that drafts or sends responses
- **Multi-workspace** — each team gets an isolated workspace with its own contacts, settings, and API keys
- **Invite-only access** — Google OAuth login, restricted to invited email addresses

## Stack

| Layer | Technology |
|---|---|
| Backend | Django 6, Python |
| Database | PostgreSQL (Railway) / SQLite (local) |
| Email | Resend API |
| Lead import | Apify (LinkedIn scraper) |
| Background tasks | Python threads (within gunicorn) |
| Static files | WhiteNoise |
| Deployment | Railway |

## Local setup

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/Scripts/activate   # Windows
# source .venv/bin/activate     # Mac/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create a .env file
cp .env.example .env            # then fill in values (see Environment variables below)

# 4. Run migrations and start the dev server
python manage.py migrate
python manage.py runserver
```

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | Yes | Django secret key — generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | No | Set to `true` for local dev (default: `false`) |
| `MASTER_EMAIL` | Yes | Email address with implicit admin rights across all workspaces |
| `GOOGLE_LOGIN_CLIENT_ID` | Yes | Google OAuth client ID |
| `GOOGLE_LOGIN_CLIENT_SECRET` | Yes | Google OAuth client secret |
| `REDIS_URL` | No | Redis connection URL (only needed if Celery worker is running) |
| `APIFY_API_TOKEN` | Yes | Apify API token for LinkedIn scraping |
| `APIFY_WEBHOOK_SECRET` | Yes | Secret for validating Apify webhook payloads |

Per-workspace settings (Resend API key, outreach templates, AI config) are stored in the database via the Settings page.

## Deployment

Deployed as a single Railway service. The `web` process in the Procfile runs migrations, collects static files, and starts gunicorn:

```
web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn config.wsgi
```

A scheduled cron job handles periodic email checks (see `railway.cron.toml`).

## Key concepts

**Workspaces** — all CRM data is scoped to a workspace. Users belong to workspaces with roles (`owner`, `admin`, `member`). The active workspace is tracked in the session.

**Lead import flow** — user fills in the Advanced Search form → Apify runs the LinkedIn scrape → webhook fires on completion → contacts are imported and outreach emails sent, all tracked by a `TaskJob` record with a live progress bar in the UI.

**Settings** — each workspace configures its own Resend API key, email templates, scoring thresholds, and AI behaviour via the Settings page (`/settings/`).
