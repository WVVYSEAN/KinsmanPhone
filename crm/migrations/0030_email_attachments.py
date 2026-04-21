from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0029_remove_apollo_api_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='OutreachAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=255)),
                ('content_type', models.CharField(max_length=100)),
                ('file_size', models.IntegerField()),
                ('file_data', models.BinaryField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('workspace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                related_name='outreach_attachments',
                                                to='crm.workspace')),
            ],
            options={
                'ordering': ['filename'],
            },
        ),
        migrations.CreateModel(
            name='EmailTemplateAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=255)),
                ('content_type', models.CharField(max_length=100)),
                ('file_size', models.IntegerField()),
                ('file_data', models.BinaryField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('email_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                      related_name='attachments',
                                                      to='crm.emailtemplate')),
            ],
            options={
                'ordering': ['filename'],
            },
        ),
    ]
