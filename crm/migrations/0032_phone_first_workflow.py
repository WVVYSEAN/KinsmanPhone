from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0031_taskjob'),
    ]

    operations = [
        # New Contact fields
        migrations.AddField(
            model_name='contact',
            name='called',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contact',
            name='call_outcome',
            field=models.CharField(
                blank=True, default='', max_length=20,
                choices=[
                    ('interested',     'Interested'),
                    ('not_now',        'Not Now'),
                    ('not_interested', 'Not Interested'),
                    ('booked',         'Discovery Booked'),
                    ('no_answer',      'No Answer'),
                ],
            ),
        ),
        migrations.AddField(
            model_name='contact',
            name='email_outreach_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contact',
            name='revenue',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='contact',
            name='ebitda',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='contact',
            name='company_size',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='contact',
            name='ownership_structure',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='contact',
            name='reason_for_sale',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='contact',
            name='causality_notes',
            field=models.TextField(blank=True, default=''),
        ),
        # New TouchPoint field
        migrations.AddField(
            model_name='touchpoint',
            name='outcome',
            field=models.CharField(
                blank=True, default='', max_length=20,
                choices=[
                    ('interested',     'Interested'),
                    ('not_now',        'Not Now'),
                    ('not_interested', 'Not Interested'),
                    ('booked',         'Discovery Booked'),
                    ('no_answer',      'No Answer'),
                ],
            ),
        ),
        # Update touchpoint_type to include voicemail and text
        migrations.AlterField(
            model_name='touchpoint',
            name='touchpoint_type',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('email',          'Email Sent'),
                    ('call',           'Call'),
                    ('voicemail',      'Voicemail'),
                    ('text',           'Text'),
                    ('meeting',        'Meeting'),
                    ('event',          'Event'),
                    ('linkedin',       'LinkedIn Interaction'),
                    ('proposal',       'Proposal Sent'),
                    ('product_launch', 'Product Launch'),
                    ('other',          'Other'),
                ],
            ),
        ),
    ]
