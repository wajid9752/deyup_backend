# Generated by Django 4.2.5 on 2023-10-03 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0002_user_active_user_admin_user_staff'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='user_name',
            new_name='username',
        ),
    ]