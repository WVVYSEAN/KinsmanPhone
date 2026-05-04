from django.db import migrations, models


def _add_call_notes(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute(
            "ALTER TABLE crm_contact ADD COLUMN IF NOT EXISTS call_notes TEXT DEFAULT '' NOT NULL"
        )
    else:
        with schema_editor.connection.cursor() as cursor:
            cols = {row[1] for row in cursor.execute("PRAGMA table_info(crm_contact)")}
            if 'call_notes' not in cols:
                cursor.execute(
                    "ALTER TABLE crm_contact ADD COLUMN call_notes TEXT DEFAULT '' NOT NULL"
                )


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0034_contact_updated_at_savedfilter_emoji'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name='contact',
                    name='call_notes',
                    field=models.TextField(blank=True, default=''),
                ),
            ],
            database_operations=[
                migrations.RunPython(_add_call_notes, migrations.RunPython.noop),
            ],
        ),
    ]
