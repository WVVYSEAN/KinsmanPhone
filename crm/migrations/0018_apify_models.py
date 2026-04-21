from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0017_alter_heatsettings_calendar_booking_url_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='source',
            field=models.CharField(
                blank=True, max_length=25,
                choices=[
                    ('referral',              'Referral'),
                    ('inbound',               'Inbound'),
                    ('event',                 'Event'),
                    ('cold_research',         'Cold Research'),
                    ('apify_advanced_search', 'Apify Advanced Search'),
                ],
            ),
        ),
        migrations.CreateModel(
            name='ApifySearch',
            fields=[
                ('id',         models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name',       models.CharField(blank=True, max_length=200)),
                ('filters',    models.JSONField(default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user',       models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apify_searches', to=settings.AUTH_USER_MODEL)),
                ('workspace',  models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='apify_searches', to='crm.workspace')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ApifyRun',
            fields=[
                ('id',               models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apify_run_id',     models.CharField(max_length=200, unique=True)),
                ('apify_dataset_id', models.CharField(blank=True, max_length=200)),
                ('status',           models.CharField(choices=[('PENDING', 'Pending'), ('RUNNING', 'Running'), ('SUCCEEDED', 'Succeeded'), ('FAILED', 'Failed'), ('ABORTED', 'Aborted')], default='PENDING', max_length=20)),
                ('leads_imported',   models.IntegerField(default=0)),
                ('triggered_by',     models.CharField(default='manual', max_length=20)),
                ('started_at',       models.DateTimeField(auto_now_add=True)),
                ('completed_at',     models.DateTimeField(blank=True, null=True)),
                ('error_message',    models.TextField(blank=True)),
                ('search',    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='runs', to='crm.apifysearch')),
                ('user',      models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apify_runs', to=settings.AUTH_USER_MODEL)),
                ('workspace', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='apify_runs', to='crm.workspace')),
            ],
            options={
                'ordering': ['-started_at'],
            },
        ),
        migrations.CreateModel(
            name='ApifySchedule',
            fields=[
                ('id',              models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cron_expression', models.CharField(default='0 9 * * 1', max_length=100)),
                ('is_active',       models.BooleanField(default=True)),
                ('last_run_at',     models.DateTimeField(blank=True, null=True)),
                ('next_run_at',     models.DateTimeField(blank=True, null=True)),
                ('created_at',      models.DateTimeField(auto_now_add=True)),
                ('search', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='schedule', to='crm.apifysearch')),
                ('user',   models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apify_schedules', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
