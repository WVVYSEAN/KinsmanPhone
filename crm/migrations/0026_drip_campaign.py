from django.db import migrations, models
import django.db.models.deletion


# ── helpers for idempotent column additions ───────────────────────────────────

def _pg_add(table, col, col_type):
    return f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {col} {col_type};"


def _sqlite_add(cursor, table, col, col_type):
    cols = {row[1] for row in cursor.execute(f"PRAGMA table_info({table})")}
    if col not in cols:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col} {col_type}")


# ── HeatSettings new drip fields ──────────────────────────────────────────────

def _add_drip_settings(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute(_pg_add('crm_heatsettings', 'drip_interval_days', 'integer NOT NULL DEFAULT 3'))
        schema_editor.execute(_pg_add('crm_heatsettings', 'drip_max_followups', 'integer NOT NULL DEFAULT 5'))
    else:
        with schema_editor.connection.cursor() as cursor:
            _sqlite_add(cursor, 'crm_heatsettings', 'drip_interval_days', 'integer NOT NULL DEFAULT 3')
            _sqlite_add(cursor, 'crm_heatsettings', 'drip_max_followups', 'integer NOT NULL DEFAULT 5')


def _drop_drip_settings(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute("ALTER TABLE crm_heatsettings DROP COLUMN IF EXISTS drip_interval_days;")
        schema_editor.execute("ALTER TABLE crm_heatsettings DROP COLUMN IF EXISTS drip_max_followups;")


# ── Contact new drip fields ───────────────────────────────────────────────────

def _add_drip_contact_fields(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute(_pg_add('crm_contact', 'drip_followups_sent',    'integer NOT NULL DEFAULT 0'))
        schema_editor.execute(_pg_add('crm_contact', 'drip_sequence_stopped',  'boolean NOT NULL DEFAULT false'))
        schema_editor.execute(_pg_add('crm_contact', 'drip_paused',            'boolean NOT NULL DEFAULT false'))
    else:
        with schema_editor.connection.cursor() as cursor:
            _sqlite_add(cursor, 'crm_contact', 'drip_followups_sent',   'integer NOT NULL DEFAULT 0')
            _sqlite_add(cursor, 'crm_contact', 'drip_sequence_stopped', 'boolean NOT NULL DEFAULT 0')
            _sqlite_add(cursor, 'crm_contact', 'drip_paused',           'boolean NOT NULL DEFAULT 0')


def _drop_drip_contact_fields(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute("ALTER TABLE crm_contact DROP COLUMN IF EXISTS drip_followups_sent;")
        schema_editor.execute("ALTER TABLE crm_contact DROP COLUMN IF EXISTS drip_sequence_stopped;")
        schema_editor.execute("ALTER TABLE crm_contact DROP COLUMN IF EXISTS drip_paused;")


# ── DripEmail table ───────────────────────────────────────────────────────────

def _create_drip_email(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute("""
            CREATE TABLE IF NOT EXISTS crm_dripemail (
                id              serial PRIMARY KEY,
                contact_id      integer NOT NULL REFERENCES crm_contact(id) ON DELETE CASCADE,
                sequence_number integer NOT NULL DEFAULT 1,
                subject         varchar(500) NOT NULL DEFAULT '',
                body            text NOT NULL DEFAULT '',
                status          varchar(20) NOT NULL DEFAULT 'pending',
                scheduled_for   timestamp with time zone,
                sent_at         timestamp with time zone,
                ai_call_log_id  integer REFERENCES crm_aicalllog(id) ON DELETE SET NULL,
                created_at      timestamp with time zone NOT NULL DEFAULT now()
            );
        """)
    else:
        schema_editor.execute("""
            CREATE TABLE IF NOT EXISTS crm_dripemail (
                id              integer PRIMARY KEY AUTOINCREMENT,
                contact_id      integer NOT NULL REFERENCES crm_contact(id) ON DELETE CASCADE,
                sequence_number integer NOT NULL DEFAULT 1,
                subject         varchar(500) NOT NULL DEFAULT '',
                body            text NOT NULL DEFAULT '',
                status          varchar(20) NOT NULL DEFAULT 'pending',
                scheduled_for   datetime,
                sent_at         datetime,
                ai_call_log_id  integer REFERENCES crm_aicalllog(id) ON DELETE SET NULL,
                created_at      datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)


def _drop_drip_email(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute("DROP TABLE IF EXISTS crm_dripemail;")


# ── DripEditExample table ─────────────────────────────────────────────────────

def _create_drip_edit_example(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute("""
            CREATE TABLE IF NOT EXISTS crm_dripeditexample (
                id            serial PRIMARY KEY,
                workspace_id  integer NOT NULL REFERENCES crm_workspace(id) ON DELETE CASCADE,
                original_body text NOT NULL DEFAULT '',
                edited_body   text NOT NULL DEFAULT '',
                created_at    timestamp with time zone NOT NULL DEFAULT now()
            );
        """)
    else:
        schema_editor.execute("""
            CREATE TABLE IF NOT EXISTS crm_dripeditexample (
                id            integer PRIMARY KEY AUTOINCREMENT,
                workspace_id  integer NOT NULL REFERENCES crm_workspace(id) ON DELETE CASCADE,
                original_body text NOT NULL DEFAULT '',
                edited_body   text NOT NULL DEFAULT '',
                created_at    datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)


def _drop_drip_edit_example(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute("DROP TABLE IF EXISTS crm_dripeditexample;")


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0025_invitedemail_workspace_role'),
    ]

    operations = [
        # HeatSettings drip config
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(_add_drip_settings, _drop_drip_settings),
            ],
            state_operations=[
                migrations.AddField(
                    model_name='heatsettings',
                    name='drip_interval_days',
                    field=models.IntegerField(default=3),
                ),
                migrations.AddField(
                    model_name='heatsettings',
                    name='drip_max_followups',
                    field=models.IntegerField(default=5),
                ),
            ],
        ),
        # Contact drip tracking
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(_add_drip_contact_fields, _drop_drip_contact_fields),
            ],
            state_operations=[
                migrations.AddField(
                    model_name='contact',
                    name='drip_followups_sent',
                    field=models.IntegerField(default=0),
                ),
                migrations.AddField(
                    model_name='contact',
                    name='drip_sequence_stopped',
                    field=models.BooleanField(default=False),
                ),
                migrations.AddField(
                    model_name='contact',
                    name='drip_paused',
                    field=models.BooleanField(default=False),
                ),
            ],
        ),
        # DripEmail model
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(_create_drip_email, _drop_drip_email),
            ],
            state_operations=[
                migrations.CreateModel(
                    name='DripEmail',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('sequence_number', models.IntegerField(default=1)),
                        ('subject', models.CharField(max_length=500)),
                        ('body', models.TextField()),
                        ('status', models.CharField(
                            choices=[
                                ('pending',  'Pending Review'),
                                ('approved', 'Approved'),
                                ('sent',     'Sent'),
                                ('rejected', 'Rejected'),
                            ],
                            default='pending', max_length=20,
                        )),
                        ('scheduled_for', models.DateTimeField(blank=True, null=True)),
                        ('sent_at',       models.DateTimeField(blank=True, null=True)),
                        ('created_at',    models.DateTimeField(auto_now_add=True)),
                        ('contact', models.ForeignKey(
                            on_delete=django.db.models.deletion.CASCADE,
                            related_name='drip_emails', to='crm.contact',
                        )),
                        ('ai_call_log', models.ForeignKey(
                            blank=True, null=True,
                            on_delete=django.db.models.deletion.SET_NULL,
                            related_name='drip_emails', to='crm.aicalllog',
                        )),
                    ],
                    options={'ordering': ['sequence_number', 'created_at']},
                ),
            ],
        ),
        # DripEditExample model
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(_create_drip_edit_example, _drop_drip_edit_example),
            ],
            state_operations=[
                migrations.CreateModel(
                    name='DripEditExample',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('original_body', models.TextField()),
                        ('edited_body',   models.TextField()),
                        ('created_at',    models.DateTimeField(auto_now_add=True)),
                        ('workspace', models.ForeignKey(
                            on_delete=django.db.models.deletion.CASCADE,
                            related_name='drip_edit_examples', to='crm.workspace',
                        )),
                    ],
                    options={'ordering': ['-created_at']},
                ),
            ],
        ),
    ]
