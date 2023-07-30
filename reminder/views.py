from django.shortcuts import render
from .models import Reminder
from django.http import HttpResponse


def home(request):
    # return HttpResponse('<h1>Reminder Home</h1>')
    context = {
        # 'reminders': reminder_list,
        'reminders': Reminder.objects.all(),
    }

    return render(request, 'reminder/index.html', context)

