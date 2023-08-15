# Generated by Django 4.2.3 on 2023-08-11 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0010_alter_reminder_notification_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminder',
            name='notification_mode',
            field=models.CharField(choices=[('sms', 'SMS'), ('both', 'Both'), ('None', 'None'), ('email', 'Email')], default=None, max_length=5),
        ),
    ]