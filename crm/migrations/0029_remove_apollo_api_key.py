from django.db import migrations


def _drop_column(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        # IF EXISTS makes this idempotent in case column is already gone
        schema_editor.execute(
            "ALTER TABLE crm_heatsettings DROP COLUMN IF EXISTS apollo_api_key"
        )
    else:
        # SQLite: check first, then drop (requires SQLite 3.35+, shipped with Python 3.12+)
        with schema_editor.connection.cursor() as cursor:
            cursor.execute("PRAGMA table_info(crm_heatsettings)")
            cols = {row[1] for row in cursor.fetchall()}
            if 'apollo_api_key' in cols:
                cursor.execute(
                    "ALTER TABLE crm_heatsettings DROP COLUMN apollo_api_key"
                )


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0028_alter_contact_drip_followups_sent_and_more'),
    ]

    operations = [
        # RunPython handles the actual DB column drop for both Postgres and SQLite.
        # RemoveField is moved into state_operations so it only updates Django's
        # internal migration state — it does NOT issue a second DROP COLUMN.
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(_drop_column, migrations.RunPython.noop),
            ],
            state_operations=[
                migrations.RemoveField(
                    model_name='heatsettings',
                    name='apollo_api_key',
                ),
            ],
        ),
    ]
