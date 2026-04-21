from django.db import migrations, models


def _add_company_domain(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute(
            "ALTER TABLE crm_contact ADD COLUMN IF NOT EXISTS company_domain varchar(200) NOT NULL DEFAULT '';"
        )
    else:
        with schema_editor.connection.cursor() as cursor:
            cols = {row[1] for row in cursor.execute("PRAGMA table_info(crm_contact)")}
            if 'company_domain' not in cols:
                cursor.execute("ALTER TABLE crm_contact ADD COLUMN company_domain varchar(200) NOT NULL DEFAULT ''")


def _drop_company_domain(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute("ALTER TABLE crm_contact DROP COLUMN IF EXISTS company_domain;")


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0020_add_contact_phone'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(_add_company_domain, _drop_company_domain),
            ],
            state_operations=[
                migrations.AddField(
                    model_name='contact',
                    name='company_domain',
                    field=models.CharField(blank=True, default='', max_length=200),
                ),
            ],
        ),
    ]
