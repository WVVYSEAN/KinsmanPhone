from django.db import migrations, models
import django.db.models.deletion


# ── idempotent helpers ─────────────────────────────────────────────────────────

def _pg_add(table, col, col_type):
    return f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {col} {col_type};"


def _sqlite_add(cursor, table, col, col_type):
    cols = {row[1] for row in cursor.execute(f"PRAGMA table_info({table})")}
    if col not in cols:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col} {col_type}")


# ── DripEditExample new columns ───────────────────────────────────────────────

def _add_drip_example_fields(apps, schema_editor):
    t = 'crm_dripeditexample'
    if schema_editor.connection.vendor == 'postgresql':
        for col, spec in [
            ('full_system_prompt',  "text NOT NULL DEFAULT ''"),
            ('full_user_prompt',    "text NOT NULL DEFAULT ''"),
            ('ai_raw_response',     "text NOT NULL DEFAULT ''"),
            ('model_used',          "varchar(100) NOT NULL DEFAULT ''"),
            ('sequence_number',     "integer NULL"),
            ('contact_industry',    "varchar(255) NOT NULL DEFAULT ''"),
            ('reply_received',      "boolean NOT NULL DEFAULT false"),
            ('reply_received_at',   "timestamp with time zone NULL"),
            ('reply_intent',        "varchar(50) NOT NULL DEFAULT ''"),
            ('outcome_score',       "real NULL"),
            ('exported_at',         "timestamp with time zone NULL"),
            ('export_batch_id',     "varchar(100) NOT NULL DEFAULT ''"),
            ('is_high_quality',     "boolean NOT NULL DEFAULT false"),
            ('drip_email_id',       "integer NULL REFERENCES crm_dripemail(id) ON DELETE SET NULL"),
            ('contact_id',          "integer NULL REFERENCES crm_contact(id) ON DELETE SET NULL"),
        ]:
            schema_editor.execute(_pg_add(t, col, spec))
    else:
        with schema_editor.connection.cursor() as cursor:
            for col, spec in [
                ('full_system_prompt',  "text NOT NULL DEFAULT ''"),
                ('full_user_prompt',    "text NOT NULL DEFAULT ''"),
                ('ai_raw_response',     "text NOT NULL DEFAULT ''"),
                ('model_used',          "varchar(100) NOT NULL DEFAULT ''"),
                ('sequence_number',     "integer NULL"),
                ('contact_industry',    "varchar(255) NOT NULL DEFAULT ''"),
                ('reply_received',      "boolean NOT NULL DEFAULT 0"),
                ('reply_received_at',   "datetime NULL"),
                ('reply_intent',        "varchar(50) NOT NULL DEFAULT ''"),
                ('outcome_score',       "real NULL"),
                ('exported_at',         "datetime NULL"),
                ('export_batch_id',     "varchar(100) NOT NULL DEFAULT ''"),
                ('is_high_quality',     "boolean NOT NULL DEFAULT 0"),
                ('drip_email_id',       "integer NULL REFERENCES crm_dripemail(id) ON DELETE SET NULL"),
                ('contact_id',          "integer NULL REFERENCES crm_contact(id) ON DELETE SET NULL"),
            ]:
                _sqlite_add(cursor, t, col, spec)


def _drop_drip_example_fields(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        for col in [
            'full_system_prompt', 'full_user_prompt', 'ai_raw_response',
            'model_used', 'sequence_number', 'contact_industry',
            'reply_received', 'reply_received_at', 'reply_intent',
            'outcome_score', 'exported_at', 'export_batch_id',
            'is_high_quality', 'drip_email_id', 'contact_id',
        ]:
            schema_editor.execute(
                f"ALTER TABLE crm_dripeditexample DROP COLUMN IF EXISTS {col};"
            )


# ── HeatSettings new columns ───────────────────────────────────────────────────

def _add_heatsettings_training_fields(apps, schema_editor):
    t = 'crm_heatsettings'
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute(_pg_add(t, 'drip_model_id', "varchar(255) NOT NULL DEFAULT ''"))
        schema_editor.execute(_pg_add(t, 'training_data_min_quality', "real NOT NULL DEFAULT 0.5"))
    else:
        with schema_editor.connection.cursor() as cursor:
            _sqlite_add(cursor, t, 'drip_model_id', "varchar(255) NOT NULL DEFAULT ''")
            _sqlite_add(cursor, t, 'training_data_min_quality', "real NOT NULL DEFAULT 0.5")


def _drop_heatsettings_training_fields(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute(
            "ALTER TABLE crm_heatsettings DROP COLUMN IF EXISTS drip_model_id;"
        )
        schema_editor.execute(
            "ALTER TABLE crm_heatsettings DROP COLUMN IF EXISTS training_data_min_quality;"
        )


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0026_drip_campaign'),
    ]

    operations = [
        # DripEditExample training data fields + FK links
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(
                    _add_drip_example_fields, _drop_drip_example_fields,
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name='dripeditexample',
                    name='full_system_prompt',
                    field=models.TextField(blank=True, default=''),
                ),
                migrations.AddField(
                    model_name='dripeditexample',
                    name='full_user_prompt',
                    field=models.TextField(blank=True, default=''),
                ),
                migrations.AddField(
                    model_name='dripeditexample',
                    name='ai_raw_response',
                    field=models.TextField(blank=True, default=''),
                ),
                migrations.AddField(
                    model_name='dripeditexample',
                    name='model_used',
                    field=models.CharField(blank=True, default='', max_length=100),
                ),
                migrations.AddField(
                    model_name='dripeditexample',
                    name='sequence_number',
                    field=models.PositiveIntegerField(null=True, blank=True),
                ),
                migrations.AddField(
                    model_name='dripeditexample',
                    name='contact_industry',
                    field=models.CharField(blank=True, default='', max_length=255),
                ),
                migrations.AddField(
                    model_name='dripeditexample',
                    name='reply_received',
                    field=models.BooleanField(default=False),
                ),
                migrations.AddField(
                    model_name='dripeditexample',
                    name='reply_received_at',
                    field=models.DateTimeField(blank=True, null=True),
                ),
                migrations.AddField(
                    model_name='dripeditexample',
                    name='reply_intent',
                    field=models.CharField(blank=True, default='', max_length=50),
                ),
                migrations.AddField(
                    model_name='dripeditexample',
                    name='outcome_score',
                    field=models.FloatField(blank=True, null=True),
                ),
                migrations.AddField(
                    model_name='dripeditexample',
                    name='exported_at',
                    field=models.DateTimeField(blank=True, null=True),
                ),
                migrations.AddField(
                    model_name='dripeditexample',
                    name='export_batch_id',
                    field=models.CharField(blank=True, default='', max_length=100),
                ),
                migrations.AddField(
                    model_name='dripeditexample',
                    name='is_high_quality',
                    field=models.BooleanField(default=False),
                ),
                migrations.AddField(
                    model_name='dripeditexample',
                    name='drip_email',
                    field=models.ForeignKey(
                        blank=True, null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='drip_edit_examples',
                        to='crm.dripemail',
                    ),
                ),
                migrations.AddField(
                    model_name='dripeditexample',
                    name='contact',
                    field=models.ForeignKey(
                        blank=True, null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='drip_edit_examples',
                        to='crm.contact',
                    ),
                ),
            ],
        ),
        # HeatSettings: fine-tuning fields
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(
                    _add_heatsettings_training_fields,
                    _drop_heatsettings_training_fields,
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name='heatsettings',
                    name='drip_model_id',
                    field=models.CharField(
                        blank=True, default='', max_length=255,
                        help_text='Fine-tuned OpenAI model ID (e.g. ft:gpt-4o-mini:org:name:id). Leave blank to use Claude.',
                    ),
                ),
                migrations.AddField(
                    model_name='heatsettings',
                    name='training_data_min_quality',
                    field=models.FloatField(
                        default=0.5,
                        help_text='Minimum outcome_score to include in JSONL exports.',
                    ),
                ),
            ],
        ),
    ]
