"""
Management command: trigger scheduled Apify Advanced Search runs.

Set in Railway cron service:
  */5 * * * * python manage.py run_apify_schedules
"""
import logging
from datetime import datetime, timezone as dt_tz

from django.core.management.base import BaseCommand
from django.utils import timezone

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Trigger due Apify scheduled searches.'

    def handle(self, *args, **options):
        from crm.models import ApifySchedule
        from crm.services.apify import trigger_apify_run

        try:
            from croniter import croniter
        except ImportError:
            self.stderr.write('croniter not installed — run: pip install croniter')
            return

        now       = timezone.now()
        schedules = (
            ApifySchedule.objects
            .filter(is_active=True)
            .select_related('search', 'search__workspace', 'user')
        )
        triggered = 0

        for schedule in schedules:
            try:
                base_time = schedule.last_run_at or schedule.created_at
                cron      = croniter(schedule.cron_expression, base_time)
                next_run  = datetime.fromtimestamp(cron.get_next(float), tz=dt_tz.utc)
            except Exception:
                logger.exception('Invalid cron expression for schedule pk=%s', schedule.pk)
                continue

            if next_run > now:
                if not schedule.next_run_at or schedule.next_run_at != next_run:
                    schedule.next_run_at = next_run
                    schedule.save(update_fields=['next_run_at'])
                continue

            try:
                workspace = schedule.search.workspace
                trigger_apify_run(schedule.search, schedule.user, 'schedule', workspace)
                schedule.last_run_at = now
                try:
                    nxt = datetime.fromtimestamp(
                        croniter(schedule.cron_expression, now).get_next(float), tz=dt_tz.utc
                    )
                    schedule.next_run_at = nxt
                except Exception:
                    schedule.next_run_at = None
                schedule.save(update_fields=['last_run_at', 'next_run_at'])
                triggered += 1
                logger.info('Triggered Apify run for schedule pk=%s', schedule.pk)
            except Exception:
                logger.exception('Error triggering Apify run for schedule pk=%s', schedule.pk)

        self.stdout.write(
            self.style.SUCCESS(f'run_apify_schedules: {triggered} run(s) triggered.')
        )
