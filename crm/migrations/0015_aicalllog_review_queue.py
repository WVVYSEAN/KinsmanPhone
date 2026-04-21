from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0014_contact_followup_fields'),
    ]

    operations = [
        # HeatSettings
        migrations.AddField(
            model_name='heatsettings',
            name='ai_review_mode',
            field=models.BooleanField(default=False, help_text='Hold AI replies for human review before sending'),
        ),
        # AICallLog draft/status fields
        migrations.AddField(
            model_name='aicalllog',
            name='status',
            field=models.CharField(
                choices=[('auto_sent','Auto Sent'),('pending','Pending Review'),
                         ('approved','Approved'),('edited','Edited & Sent'),('rejected','Rejected')],
                default='auto_sent', max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='aicalllog',
            name='edited_response',
            field=models.TextField(blank=True, help_text='What was actually sent, if edited before approval'),
        ),
        migrations.AddField(
            model_name='aicalllog',
            name='draft_subject',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='aicalllog',
            name='draft_inbound_msg_id',
            field=models.CharField(blank=True, help_text='Lead Message-ID for threading', max_length=500),
        ),
        migrations.AddField(
            model_name='aicalllog',
            name='draft_in_reply_to',
            field=models.CharField(blank=True, help_text='In-Reply-To header value', max_length=500),
        ),
        migrations.AddField(
            model_name='aicalllog',
            name='draft_is_followup',
            field=models.BooleanField(default=False),
        ),
    ]
