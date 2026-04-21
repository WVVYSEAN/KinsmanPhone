"""
Service layer for Apify Advanced Search integration.

- trigger_apify_run(search, user, triggered_by, workspace) — POSTs to Apify actor
- fetch_and_import_leads(run) — GETs dataset items and creates Contact records
"""
import base64
import json
import logging

import requests
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

ACTOR_ID = 'T1XDXWc1L92AfIJtd'

# Normalize old compact format → Apify's required spaced format
_EMPLOYEE_SIZE_MAP = {
    '0-1':       '0 - 1',
    '2-10':      '2 - 10',
    '11-50':     '11 - 50',
    '51-200':    '51 - 200',
    '201-500':   '201 - 500',
    '501-1000':  '501 - 1000',
    '1001-5000': '1001 - 5000',
    '5001-10000':'5001 - 10000',
}


def _normalize_filters(filters):
    """Fix any stored filter values that don't match Apify's expected format."""
    f = dict(filters)
    if f.get('companyEmployeeSize'):
        f['companyEmployeeSize'] = [
            _EMPLOYEE_SIZE_MAP.get(v, v) for v in f['companyEmployeeSize']
        ]
    # Migrate old saved searches that used the strict `industry` enum field:
    # move those values to `industryKeywords` (free-text) so they don't cause 400s.
    if f.get('industry'):
        existing_kw = f.get('industryKeywords') or []
        merged = existing_kw + [v for v in f.pop('industry') if v not in existing_kw]
        f['industryKeywords'] = merged
    return f


def _encode_webhooks(webhooks):
    return base64.b64encode(json.dumps(webhooks).encode()).decode()


def trigger_apify_run(search, user, triggered_by, workspace):
    import uuid
    from crm.models import ApifyRun

    token          = getattr(settings, 'APIFY_API_TOKEN', '')
    webhook_secret = getattr(settings, 'APIFY_WEBHOOK_SECRET', '')
    site_url       = getattr(settings, 'SITE_URL', '').rstrip('/')

    webhook_url = f"{site_url}/apify/webhook/"
    if webhook_secret:
        webhook_url += f"?secret={webhook_secret}"

    ad_hoc_webhooks = [
        {
            "eventTypes": [
                "ACTOR.RUN.SUCCEEDED",
                "ACTOR.RUN.FAILED",
                "ACTOR.RUN.ABORTED",
            ],
            "requestUrl": webhook_url,
        }
    ]

    try:
        resp = requests.post(
            f'https://api.apify.com/v2/acts/{ACTOR_ID}/runs',
            json=_normalize_filters(search.filters),
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
            },
            params={'webhooks': _encode_webhooks(ad_hoc_webhooks)},
            timeout=30,
        )
        if not resp.ok:
            raise Exception(f"Apify {resp.status_code}: {resp.text[:500]}")
        data = resp.json().get('data', {})
        run_obj = ApifyRun.objects.create(
            search=search,
            user=user,
            workspace=workspace,
            apify_run_id=data['id'],
            status='RUNNING',
            triggered_by=triggered_by,
        )
    except Exception as exc:
        run_obj = ApifyRun.objects.create(
            search=search,
            user=user,
            workspace=workspace,
            apify_run_id=f'failed-{uuid.uuid4().hex[:12]}',
            status='FAILED',
            triggered_by=triggered_by,
            error_message=str(exc),
            completed_at=timezone.now(),
        )
        raise

    return run_obj


def fetch_and_import_leads(run):
    """Fetch dataset items from Apify and import as Contact (cold_lead) records."""
    from crm.models import Contact, HeatSettings
    from crm.views import _maybe_send_outreach

    token      = getattr(settings, 'APIFY_API_TOKEN', '')
    dataset_id = run.apify_dataset_id
    workspace  = run.workspace
    user       = run.user

    # Fetch config once — used for outreach sends inside the loop
    cfg = HeatSettings.get_for_workspace(workspace)

    existing_emails = set(
        Contact.objects
        .filter(workspace=workspace, email__gt='')
        .values_list('email', flat=True)
    )

    offset   = 0
    limit    = 1000
    imported = 0

    while True:
        try:
            resp = requests.get(
                f'https://api.apify.com/v2/datasets/{dataset_id}/items',
                params={'format': 'json', 'clean': 'true', 'offset': offset, 'limit': limit},
                headers={'Authorization': f'Bearer {token}'},
                timeout=60,
            )
            resp.raise_for_status()
            items = resp.json()
        except Exception as exc:
            logger.error('Error fetching Apify dataset %s: %s', dataset_id, exc)
            break

        if not items:
            break

        for item in items:
            # Actor uses firstName/lastName or fullName
            first   = (item.get('firstName') or '').strip()
            last    = (item.get('lastName')  or '').strip()
            name    = (f"{first} {last}".strip()
                       or (item.get('fullName')  or '').strip()
                       or (item.get('name')      or '').strip())
            email   = (item.get('email') or '').strip().lower()
            # Actor uses organizationName, not companyName
            company = (item.get('organizationName') or item.get('companyName') or '').strip()

            if not name:
                continue
            if email and email in existing_emails:
                continue
            if not email and name and Contact.objects.filter(
                workspace=workspace, name=name, company=company
            ).exists():
                continue

            location_str = ', '.join(filter(None, [
                (item.get('city')    or '').strip(),
                (item.get('state')   or '').strip(),
                (item.get('country') or '').strip(),
            ]))

            # phone_numbers may be a list of strings or dicts; extract a plain number
            _phone_raw = item.get('phone_numbers') or item.get('phone') or ''
            if isinstance(_phone_raw, list):
                _first = _phone_raw[0] if _phone_raw else ''
                if isinstance(_first, dict):
                    _phone_raw = _first.get('sanitizedNumber') or _first.get('number') or ''
                else:
                    _phone_raw = _first
            # If it's still a dict/non-string (unexpected shape), discard it
            if not isinstance(_phone_raw, str):
                _phone_raw = ''
            phone_val = _phone_raw.strip()[:50]  # model max_length=50

            contact = Contact.objects.create(
                workspace = workspace,
                name      = name[:200],
                email     = email[:254],
                phone     = phone_val,
                # Actor uses 'position', fallback to 'title'
                role      = (item.get('position') or item.get('title') or '').strip()[:200],
                company   = company[:200],
                linkedin  = (item.get('linkedinUrl') or '').strip()[:200],
                location  = location_str[:200],
                # Actor uses organizationIndustry, fallback to industry
                industry  = (item.get('organizationIndustry') or item.get('industry') or '').strip()[:200],
                source    = 'apify_advanced_search',
                stage     = 'cold_lead',
            )
            if email:
                existing_emails.add(email)
                try:
                    _maybe_send_outreach(contact, workspace, user, cfg)
                except Exception as exc:
                    logger.warning('Outreach send failed for contact %s: %s', contact.pk, exc)
            imported += 1

        if len(items) < limit:
            break
        offset += limit

    run.leads_imported = imported
    run.status         = 'SUCCEEDED'
    run.completed_at   = timezone.now()
    run.save(update_fields=['leads_imported', 'status', 'completed_at'])
    return imported
