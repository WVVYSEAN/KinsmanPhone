from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_outreach_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='heatsettings',
            name='google_client_id',
            field=models.CharField(max_length=500, blank=True),
        ),
        migrations.AddField(
            model_name='heatsettings',
            name='google_client_secret',
            field=models.CharField(max_length=500, blank=True),
        ),
        migrations.AddField(
            model_name='heatsettings',
            name='google_tokens',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='heatsettings',
            name='google_calendar_id',
            field=models.CharField(max_length=200, blank=True, default='primary'),
        ),
        migrations.AddField(
            model_name='heatsettings',
            name='google_account_email',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='heatsettings',
            name='calendar_booking_url',
            field=models.CharField(max_length=1000, blank=True),
        ),
    ]
