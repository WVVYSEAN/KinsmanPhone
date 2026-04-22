from django.db import migrations, models


def _add_contact_updated_at(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute(
            "ALTER TABLE crm_contact ADD COLUMN IF NOT EXISTS"
            " updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL"
        )
    else:
        with schema_editor.connection.cursor() as cursor:
            cols = {row[1] for row in cursor.execute("PRAGMA table_info(crm_contact)")}
            if 'updated_at' not in cols:
                cursor.execute(
                    "ALTER TABLE crm_contact"
                    " ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL"
                )


def _add_savedfilter_emoji(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute(
            "ALTER TABLE crm_savedfilter ADD COLUMN IF NOT EXISTS emoji VARCHAR(8) DEFAULT '' NOT NULL"
        )
    else:
        with schema_editor.connection.cursor() as cursor:
            cols = {row[1] for row in cursor.execute("PRAGMA table_info(crm_savedfilter)")}
            if 'emoji' not in cols:
                cursor.execute(
                    "ALTER TABLE crm_savedfilter ADD COLUMN emoji VARCHAR(8) DEFAULT '' NOT NULL"
                )


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0033_savedfilter'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name='contact',
                    name='updated_at',
                    field=models.DateTimeField(auto_now=True),
                ),
                migrations.AddField(
                    model_name='savedfilter',
                    name='emoji',
                    field=models.CharField(blank=True, default='', max_length=8),
                ),
            ],
            database_operations=[
                migrations.RunPython(_add_contact_updated_at, migrations.RunPython.noop),
                migrations.RunPython(_add_savedfilter_emoji, migrations.RunPython.noop),
            ],
        ),
    ]
