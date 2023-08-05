from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Reminder(models.Model):
    notification_choices = {
        ('None', 'None'),
        ('email', 'Email'),
        ('sms','SMS'),
        ('both','Both'),
    }

    title = models.CharField(max_length=50)
    description = models.TextField()
    date_added = models.DateTimeField(default=timezone.localtime)
    due_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    notification_mode = models.CharField(max_length=5, choices=notification_choices, default=None)
    #
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    # returns ful url as string
    def get_absolute_url(self):
        return reverse('reminder-detail', kwargs={'pk':self.pk})