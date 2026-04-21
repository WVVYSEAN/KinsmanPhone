from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0024_drop_userinvite'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitedemail',
            name='workspace',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='pending_invites',
                to='crm.workspace',
            ),
        ),
        migrations.AddField(
            model_name='invitedemail',
            name='role',
            field=models.CharField(default='member', max_length=20),
        ),
    ]
