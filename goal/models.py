from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Goal(models.Model):
    notification_choices = {
        ('email', 'Email'),
        ('None', 'None'),
        # ('sms', 'SMS'),
        # ('both', 'Both'),
    }
    category_choices = {
        ('savings', 'Savings'),
        ('spendings', 'Spendings'),
        ('entertainment', 'Entertainment'),
        ('educational', 'Educational'),
        ('home and family', 'Home & Family'),
        ('health and fitness', 'Health & Fitness'),
        ('career and buisness', 'Career & Buisness'),
        ('travel and vacation', 'Travel & Vacation'),
        ('personal development', 'Personal Development'),
        ('other', 'Other'),
    }

    title = models.CharField(max_length=70)
    amount = models.IntegerField()
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    notification_mode = models.CharField(
        max_length=5, choices=notification_choices, default=None)
    category = models.CharField(choices=category_choices)
    complete_amount = models.IntegerField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def progress(self):
        return int(self.complete_amount / self.amount * 100)

    def theme_color(self):
        colors = {
            'savings': 'bg-green-300',
            'spendings': 'bg-red-300',
            'entertainment': 'bg-blue-300',
            'educational': 'bg-yellow-300',
            'home and family': 'bg-indigo-300',
            'health and fitness': 'bg-red-300',
            'career and buisness': 'bg-blue-300',
            'travel and vacation': 'bg-purple-300',
            'personal development': 'bg-pink-300',
            'other': 'bg-gray-300',
        }
        return colors.get(self.category, 'bg-pink-300')

    def icon(self):
        return self.category.replace(' ', '_') + '.png'

    def remaining_days(self):
        today = datetime.now().replace(tzinfo=None)
        end_date_naive = self.end_date.replace(tzinfo=None)
        remaining = (end_date_naive - today).days
        return remaining

    def percentage(self):
        return round((self.complete_amount / self.amount * 100), 1)

    def amount_difference(self):
        if self.complete_amount is not None:
            return self.amount - self.complete_amount
        return None

    def change_amount(self, change_value):
        print(self.complete_amount + change_value)
        return self.complete_amount + change_value
