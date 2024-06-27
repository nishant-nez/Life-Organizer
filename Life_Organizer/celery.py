

from celery.schedules import crontab
from celery import Celery
from django.conf import settings
import os
from django.core.mail import send_mail
from django.utils import timezone
import pytz


kathmandu_tz = pytz.timezone("Asia/Kathmandu")

# import django
# django.setup()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Life_Organizer.settings')
# t


# from reminder.models import Reminder

app = Celery('Life_Organizer')
# Set the default Django settings module for the 'celery' program.


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print("Celery says hello")


@app.task
def print_hello():
    from reminder.models import Reminder
    from django.contrib.auth.models import User

    subject = "account not verified"
    message = "Your account is not verified"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['khadkanishant1@gmail.com',
                      'nishant.khadka@deerwalk.edu.np']
    send_mail(subject, message, email_from, recipient_list)
    print("Hello world! from Celery, print_hello() function")

    current_directory = os.getcwd()  # Get the current directory
    # Create a file path in the current directory
    file_name = os.path.join(current_directory, "test.txt")

    with open(file_name, 'w') as file:
        file.write("This is something written to the file.")

    print(f"Successfully wrote to {file_name}")


@app.task
def check_reminder():
    from reminder.models import Reminder

    current_datetime = timezone.now()
    one_hour_later = current_datetime + timezone.timedelta(hours=1)

    # Truncate seconds and microseconds from both timestamps
    current_datetime = current_datetime.replace(second=0, microsecond=0)
    one_hour_later = one_hour_later.replace(second=0, microsecond=0)

    email_reminders = Reminder.objects.filter(
        notification_mode='email',
        due_date=one_hour_later,
        sent=False
    )

    if email_reminders:
        for reminder in email_reminders:
            user = reminder.user
            from_email = settings.EMAIL_HOST_USER
            subject = f"Reminder {reminder.title} due in 1 hour"
            formatted_due_date = reminder.due_date.astimezone(
                kathmandu_tz).strftime('%d/%m/%Y %H:%M')
            message = f"Hello {user.get_full_name()},\n\nYou have a reminder titled '{reminder.title}' due at {formatted_due_date}.\n\nRegards,\nLife Organizer"
            recipient_list = [user.email, 'nishant.khadka@deerwalk.edu.np']

            try:
                send_mail(subject,
                          message,
                          from_email,
                          recipient_list,
                          fail_silently=False)
                reminder.sent = True
                reminder.save()
            except Exception as e:
                print(
                    f"Failed to send email for reminder '{reminder.title}': {str(e)}")
    else:
        pass

# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')


# Load task modules from all registered Django apps.
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS + ['Life_Organizer'])
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'check-reminder-every-minute': {
#         'task': 'check_reminder',
#         # Every minute at 00 seconds
#         'schedule': crontab(minute='*/1'),
#     }
# }
