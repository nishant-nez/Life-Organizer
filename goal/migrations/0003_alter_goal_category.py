# Generated by Django 4.2.3 on 2023-09-16 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goal', '0002_alter_goal_category_alter_goal_notification_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='category',
            field=models.CharField(choices=[('home and family', 'Home & Family'), ('savings', 'Savings'), ('entertainment', 'Entertainment'), ('spendings', 'Spendings'), ('personal development', 'Personal Development'), ('other', 'Other'), ('career and buisness', 'Career & Buisness'), ('educational', 'Educational'), ('travel and vacation', 'Travel & Vacation'), ('health and fitness', 'Health & Fitness')]),
        ),
    ]