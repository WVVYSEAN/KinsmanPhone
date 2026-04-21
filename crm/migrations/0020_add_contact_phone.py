from django.db import migrations, models


def _add_phone(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute(
            "ALTER TABLE crm_contact ADD COLUMN IF NOT EXISTS phone varchar(50) NOT NULL DEFAULT '';"
        )
    else:
        with schema_editor.connection.cursor() as cursor:
            cols = {row[1] for row in cursor.execute("PRAGMA table_info(crm_contact)")}
            if 'phone' not in cols:
                cursor.execute("ALTER TABLE crm_contact ADD COLUMN phone varchar(50) NOT NULL DEFAULT ''")


def _drop_phone(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute("ALTER TABLE crm_contact DROP COLUMN IF EXISTS phone;")


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0019_cleanup_pending_apify_runs'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(_add_phone, _drop_phone),
            ],
            state_operations=[
                migrations.AddField(
                    model_name='contact',
                    name='phone',
                    field=models.CharField(blank=True, default='', max_length=50),
                ),
            ],
        ),
    ]
