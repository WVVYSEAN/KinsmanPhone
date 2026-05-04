from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0036_heatsettings_outreach_enabled_default_false'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='drip_paused',
            field=models.BooleanField(default=True, help_text='Drip sequence temporarily paused'),
        ),
    ]
