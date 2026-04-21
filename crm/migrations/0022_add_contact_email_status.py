from django.db import migrations, models


def _add_email_status(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        # ADD COLUMN is a no-op on production where the column already exists.
        # ALTER COLUMN adds a persistent DEFAULT so future inserts that omit
        # email_status (e.g. Apify import) no longer hit the NOT NULL constraint.
        schema_editor.execute(
            "ALTER TABLE crm_contact ADD COLUMN IF NOT EXISTS email_status varchar(100) NOT NULL DEFAULT '';"
        )
        schema_editor.execute(
            "ALTER TABLE crm_contact ALTER COLUMN email_status SET DEFAULT '';"
        )
    else:
        with schema_editor.connection.cursor() as cursor:
            cols = {row[1] for row in cursor.execute("PRAGMA table_info(crm_contact)")}
            if 'email_status' not in cols:
                cursor.execute("ALTER TABLE crm_contact ADD COLUMN email_status varchar(100) NOT NULL DEFAULT ''")


def _drop_email_status(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute("ALTER TABLE crm_contact DROP COLUMN IF EXISTS email_status;")


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0021_add_contact_company_domain'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(_add_email_status, _drop_email_status),
            ],
            state_operations=[
                migrations.AddField(
                    model_name='contact',
                    name='email_status',
                    field=models.CharField(
                        blank=True, default='', max_length=100,
                        help_text='Apollo email verification status',
                    ),
                ),
            ],
        ),
    ]
