import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0012_ai_email_thread'),
    ]

    operations = [
        migrations.AddField(
            model_name='heatsettings',
            name='signature',
            field=models.TextField(blank=True),
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('subject', models.CharField(blank=True, max_length=500)),
                ('body', models.TextField(blank=True)),
                ('is_default', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('workspace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                related_name='email_templates', to='crm.workspace')),
            ],
            options={
                'verbose_name': 'Email Template',
                'ordering': ['-is_default', 'name'],
            },
        ),
        migrations.CreateModel(
            name='EmailImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('image', models.ImageField(upload_to='email_images/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('workspace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                related_name='email_images', to='crm.workspace')),
            ],
        ),
    ]
