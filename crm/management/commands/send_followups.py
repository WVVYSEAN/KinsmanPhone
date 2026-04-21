"""
Management command: send AI follow-up emails to leads who haven't replied.

Scheduling rules:
  - Only between 13:00 and 15:00 in the contact's local timezone
  - Not on weekends (Saturday / Sunday)
  - At least 48 hours since the last AI email was sent
  - Contact must have ai_managed=True, an email address, and sequence_stopped=False
  - Maximum 9 AI emails per contact; after that the sequence stops
  - Contacts whose sequence is stopped and who never replied are deleted

Run this command every 30–60 minutes via a Railway Cron Job:
  python manage.py send_followups
"""

import logging
from datetime import timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from django.core.management.base import BaseCommand
from django.utils import timezone as _tz

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Send proactive AI follow-up emails to eligible leads.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Skip time-of-day, weekend, and 48h gap checks (for testing).',
        )

    def handle(self, *args, **options):
        # Import here to avoid circular issues at startup
        from crm.models import Contact, EmailThread
        from crm.views import _send_ai_followup

        force = options['force']
        now_utc = _tz.now()

        # ── Step 1: delete leads whose sequence finished with no reply ─────────
        from django.db.models import OuterRef, Subquery
        last_dir_qs = (
            EmailThread.objects
            .filter(contact=OuterRef('pk'))
            .order_by('-sent_at')
            .values('direction')[:1]
        )
        stale_cutoff = now_utc - timedelta(hours=48)
        to_delete = (
            Contact.objects
            .annotate(last_thread_dir=Subquery(last_dir_qs))
            .filter(
                ai_managed=True,
                sequence_stopped=True,
                last_thread_dir='outbound',      # no reply after our last message
                last_follow_up_at__lt=stale_cutoff,
            )
        )
        deleted_count = 0
        for c in to_delete:
            logger.info('Deleting lead %s (pk=%s) — sequence complete, no reply.', c.name, c.pk)
            c.delete()
            deleted_count += 1

        # ── Step 2: find contacts eligible for a follow-up ────────────────────
        cutoff_48h = now_utc - timedelta(hours=48)
        candidates = Contact.objects.filter(
            ai_managed=True,
            sequence_stopped=False,
            email__gt='',           # must have an email address
        ).exclude(follow_up_count__gte=9)

        sent_count = 0
        for contact in candidates:
            # Must have at least one outbound email already (initial outreach)
            if not contact.email_thread.filter(direction='outbound').exists():
                continue

            # Must not have a recent inbound (they replied — let _send_ai_reply handle it)
            if contact.email_thread.filter(
                direction='inbound',
                sent_at__gt=cutoff_48h,
            ).exists():
                continue

            # 48-hour gap since last AI email
            if not force and contact.last_follow_up_at and contact.last_follow_up_at > cutoff_48h:
                continue

            # Time-of-day check in contact's local timezone (1pm–3pm, Mon–Fri)
            if not force:
                try:
                    tz_name = contact.timezone or 'UTC'
                    local_tz = ZoneInfo(tz_name)
                except ZoneInfoNotFoundError:
                    local_tz = ZoneInfo('UTC')

                local_now = now_utc.astimezone(local_tz)
                if local_now.weekday() >= 5:          # 5=Sat, 6=Sun
                    continue
                if not (13 <= local_now.hour < 15):   # 1pm–3pm
                    continue

            logger.info('Sending follow-up to %s (pk=%s, count=%s)', contact.name, contact.pk, contact.follow_up_count)
            try:
                _send_ai_followup(contact)
                sent_count += 1
            except Exception:
                logger.exception('Error sending follow-up to contact pk=%s', contact.pk)

        self.stdout.write(
            self.style.SUCCESS(
                f'send_followups complete: {sent_count} sent, {deleted_count} deleted.'
            )
        )
