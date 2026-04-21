from django.db import migrations


def delete_pending_runs(apps, schema_editor):
    ApifyRun = apps.get_model('crm', 'ApifyRun')
    ApifyRun.objects.filter(apify_run_id='pending').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0018_apify_models'),
    ]

    operations = [
        migrations.RunPython(delete_pending_runs, migrations.RunPython.noop),
    ]
