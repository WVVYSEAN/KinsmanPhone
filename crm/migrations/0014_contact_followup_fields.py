from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0013_email_templates'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='timezone',
            field=models.CharField(blank=True, default='UTC', help_text='IANA timezone for scheduling follow-ups (e.g. America/New_York)', max_length=100),
        ),
        migrations.AddField(
            model_name='contact',
            name='follow_up_count',
            field=models.IntegerField(default=0, help_text='Number of AI emails sent to this contact'),
        ),
        migrations.AddField(
            model_name='contact',
            name='last_follow_up_at',
            field=models.DateTimeField(blank=True, help_text='When the last AI email was sent', null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='needs_attention',
            field=models.BooleanField(default=False, help_text='Lead expressed interest — needs a human response'),
        ),
        migrations.AddField(
            model_name='contact',
            name='sequence_stopped',
            field=models.BooleanField(default=False, help_text='AI follow-up sequence is stopped for this contact'),
        ),
    ]
