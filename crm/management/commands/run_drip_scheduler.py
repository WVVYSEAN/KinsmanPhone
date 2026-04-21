"""
Management command: run the drip campaign cycle for all workspaces.

Run this every hour via a Railway Cron Job:
  python manage.py run_drip_scheduler

Or run once on demand (e.g. during testing):
  python manage.py run_drip_scheduler --once
"""

import logging
import time

from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

SLEEP_SECONDS = 3600  # 1 hour


class Command(BaseCommand):
    help = 'Run the drip campaign scheduler (infinite loop or single pass).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--once',
            action='store_true',
            help='Run a single cycle and exit (instead of looping indefinitely).',
        )

    def handle(self, *args, **options):
        run_once = options['once']

        self.stdout.write(
            self.style.SUCCESS(
                f'Drip scheduler starting ({"single pass" if run_once else "infinite loop, interval=1h"}).'
            )
        )

        while True:
            self._run_cycle()
            if run_once:
                break
            logger.info('Drip cycle complete. Sleeping %ds.', SLEEP_SECONDS)
            time.sleep(SLEEP_SECONDS)

    def _run_cycle(self):
        from crm.models import Workspace
        from crm.drip import run_drip_cycle

        workspaces = Workspace.objects.all()
        self.stdout.write(f'Running drip cycle for {workspaces.count()} workspace(s).')

        for workspace in workspaces:
            try:
                run_drip_cycle(workspace)
            except Exception:
                logger.exception('Drip cycle error for workspace pk=%s', workspace.pk)
