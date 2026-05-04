from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0037_contact_drip_paused_default_true'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='org_type',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='contact',
            name='org_founded_year',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='contact',
            name='org_revenue',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='contact',
            name='connections',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
