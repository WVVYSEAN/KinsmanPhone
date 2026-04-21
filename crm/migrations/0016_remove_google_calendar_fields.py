from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0015_aicalllog_review_queue'),
    ]

    operations = [
        migrations.RemoveField(model_name='heatsettings', name='google_client_id'),
        migrations.RemoveField(model_name='heatsettings', name='google_client_secret'),
        migrations.RemoveField(model_name='heatsettings', name='google_tokens'),
        migrations.RemoveField(model_name='heatsettings', name='google_calendar_id'),
        migrations.RemoveField(model_name='heatsettings', name='google_account_email'),
    ]
