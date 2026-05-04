from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0035_contact_call_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heatsettings',
            name='outreach_enabled',
            field=models.BooleanField(default=False),
        ),
    ]
