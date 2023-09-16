# Generated by Django 4.2.3 on 2023-09-16 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goal', '0006_alter_goal_category_alter_goal_notification_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='category',
            field=models.CharField(choices=[('other', 'Other'), ('educational', 'Educational'), ('health and fitness', 'Health & Fitness'), ('entertainment', 'Entertainment'), ('personal development', 'Personal Development'), ('savings', 'Savings'), ('career and buisness', 'Career & Buisness'), ('home and family', 'Home & Family'), ('travel and vacation', 'Travel & Vacation'), ('spendings', 'Spendings')]),
        ),
        migrations.AlterField(
            model_name='goal',
            name='notification_mode',
            field=models.CharField(choices=[('both', 'Both'), ('sms', 'SMS'), ('email', 'Email'), ('None', 'None')], default=None, max_length=5),
        ),
    ]