from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_google_calendar'),
    ]

    operations = [
        migrations.AddField(
            model_name='heatsettings',
            name='reply_to_domain',
            field=models.CharField(
                max_length=200, blank=True,
                help_text='Domain used for reply-to addresses, e.g. yourdomain.com',
            ),
        ),
    ]
