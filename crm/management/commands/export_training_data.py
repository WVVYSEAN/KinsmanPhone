"""
Management command: export drip training data as JSONL for OpenAI fine-tuning.

Usage:
  python manage.py export_training_data --workspace-id 1
  python manage.py export_training_data --workspace-id 1 --only-new --min-score 0.8
  python manage.py export_training_data --workspace-id 1 --dry-run
  python manage.py export_training_data --workspace-id 1 --output my_data.jsonl
"""

import json
import uuid
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone


class Command(BaseCommand):
    help = 'Export drip training examples as JSONL for OpenAI fine-tuning.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--workspace-id', type=int, required=True,
            help='Workspace pk to export data for.',
        )
        parser.add_argument(
            '--min-score', type=float, default=None,
            help='Minimum outcome_score to include (default: HeatSettings.training_data_min_quality).',
        )
        parser.add_argument(
            '--only-new', action='store_true',
            help='Only export records where exported_at is null.',
        )
        parser.add_argument(
            '--output', type=str, default=None,
            help='Output file path (default: training_data_<ws_id>_<timestamp>.jsonl).',
        )
        parser.add_argument(
            '--dry-run', action='store_true',
            help='Print stats without writing file or updating records.',
        )

    def handle(self, *args, **options):
        from crm.models import Workspace, HeatSettings, DripEditExample

        ws_id = options['workspace_id']
        try:
            workspace = Workspace.objects.get(pk=ws_id)
        except Workspace.DoesNotExist:
            raise CommandError(f'Workspace pk={ws_id} not found.')

        cfg       = HeatSettings.get_for_workspace(workspace)
        min_score = options['min_score']
        if min_score is None:
            min_score = cfg.training_data_min_quality

        dry_run  = options['dry_run']
        only_new = options['only_new']

        # ── Build queryset ─────────────────────────────────────────────────────
        qs = DripEditExample.objects.filter(
            workspace=workspace,
            outcome_score__isnull=False,
            outcome_score__gte=min_score,
        ).exclude(full_system_prompt='')  # skip records without captured prompts

        if only_new:
            qs = qs.filter(exported_at__isnull=True)

        examples = list(qs.order_by('created_at'))
        skipped  = DripEditExample.objects.filter(workspace=workspace).count() - len(examples)

        if dry_run:
            self.stdout.write(self.style.SUCCESS(
                f'DRY RUN — workspace={workspace.name} (pk={ws_id})\n'
                f'  Would export: {len(examples)} examples\n'
                f'  Skipped (below threshold / no prompts): {skipped}\n'
                f'  Min score: {min_score}\n'
                f'  Only new: {only_new}'
            ))
            return

        if not examples:
            self.stdout.write('No examples to export.')
            return

        # ── Generate output path ───────────────────────────────────────────────
        batch_id  = str(uuid.uuid4())
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output    = options['output'] or f'training_data_{ws_id}_{timestamp}.jsonl'

        # ── Write JSONL ────────────────────────────────────────────────────────
        now = timezone.now()
        lines_written = 0

        with open(output, 'w', encoding='utf-8') as fh:
            for ex in examples:
                was_edited = bool(ex.edited_body) and ex.original_body != ex.edited_body
                assistant_content = ex.edited_body if was_edited else ex.original_body

                record = {
                    'messages': [
                        {
                            'role':    'system',
                            'content': ex.full_system_prompt,
                        },
                        {
                            'role':    'user',
                            'content': ex.full_user_prompt,
                        },
                        {
                            'role':    'assistant',
                            'content': assistant_content,
                        },
                    ],
                    'metadata': {
                        'example_id':       ex.pk,
                        'outcome_score':    ex.outcome_score,
                        'reply_received':   ex.reply_received,
                        'reply_intent':     ex.reply_intent or '',
                        'sequence_number':  ex.sequence_number,
                        'was_edited':       was_edited,
                        'contact_industry': ex.contact_industry or '',
                        'export_batch_id':  batch_id,
                    },
                }
                fh.write(json.dumps(record, ensure_ascii=False) + '\n')
                lines_written += 1

        # ── Mark as exported ───────────────────────────────────────────────────
        ids = [ex.pk for ex in examples]
        DripEditExample.objects.filter(pk__in=ids).update(
            exported_at=now,
            export_batch_id=batch_id,
        )

        self.stdout.write(self.style.SUCCESS(
            f'Export complete — workspace={workspace.name} (pk={ws_id})\n'
            f'  Exported:   {lines_written} examples\n'
            f'  Skipped:    {skipped}\n'
            f'  Batch ID:   {batch_id}\n'
            f'  Output:     {output}'
        ))
