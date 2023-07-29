from django.shortcuts import render
from django.http import HttpResponse

# database returns

reminder_list = [
    {
        'title': 'First reminder',
        'description':'This is the first reminder',
        'date_added': '29 Jul 2023',
        'due_date' : '5 August 2023',
        'is_completed': 'False',
        'notification_mode': 'email',
    },
    {
        'title': 'Second reminder',
        'description':'This is the second reminder',
        'date_added': '20 Jul 2023',
        'due_date' : '9 August 2023',
        'is_completed': 'False',
        'notification_mode': 'SMS',
    },
    {
        'title': 'Third reminder',
        'description':'This is the third reminder',
        'date_added': '1 Jul 2023',
        'due_date' : '5 November 2023',
        'is_completed': 'False',
        'notification_mode': 'email',
    }
]

def home(request):
    # return HttpResponse('<h1>Reminder Home</h1>')
    context = {
        'reminders': reminder_list,
    }

    return render(request, 'reminder/index.html', context)

