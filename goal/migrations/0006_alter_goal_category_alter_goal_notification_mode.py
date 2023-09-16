# Generated by Django 4.2.3 on 2023-09-16 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goal', '0005_alter_goal_category_alter_goal_notification_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='category',
            field=models.CharField(choices=[('career and buisness', 'Career & Buisness'), ('educational', 'Educational'), ('health and fitness', 'Health & Fitness'), ('entertainment', 'Entertainment'), ('personal development', 'Personal Development'), ('other', 'Other'), ('spendings', 'Spendings'), ('savings', 'Savings'), ('travel and vacation', 'Travel & Vacation'), ('home and family', 'Home & Family')]),
        ),
        migrations.AlterField(
            model_name='goal',
            name='notification_mode',
            field=models.CharField(choices=[('sms', 'SMS'), ('email', 'Email'), ('both', 'Both'), ('None', 'None')], default=None, max_length=5),
        ),
    ]
