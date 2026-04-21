from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0023_userinvite'),
    ]

    operations = [
        migrations.DeleteModel(name='UserInvite'),
    ]
