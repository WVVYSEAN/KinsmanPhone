from django.db import migrations, models


def _clear_old_file_paths(apps, schema_editor):
    # Existing logo values are filesystem paths (e.g. "workspace_logos/x.png")
    # which are no longer valid after moving to base64 storage.
    # Clear them so logos show as missing rather than broken.
    Workspace = apps.get_model('crm', 'Workspace')
    Workspace.objects.exclude(logo='').exclude(logo__isnull=True).update(logo='')


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0038_contact_apify_company_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workspace',
            name='logo',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.RunPython(_clear_old_file_paths, migrations.RunPython.noop),
    ]
