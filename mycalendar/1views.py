from django.shortcuts import render, redirect
# from .forms import ReminderCreateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.http import HttpResponse

from django.conf import settings
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


from django.shortcuts import render, redirect
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.utils.decorators import method_decorator
# from .models import Event
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .models import Event

import json
import os

from .forms import EventForm
from datetime import datetime


from django.shortcuts import render, redirect
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import json
from datetime import datetime
from .models import Event

import pytz

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


from django.http import JsonResponse

from dateutil import parser, tz

import string
import random

@login_required
def home(request):
    # user_reminders = Reminder.objects.filter(user=request.user)
    user_calendars = []

    context = {
        'calendars': user_calendars,
    }
    return render(request, 'mycalendar/index.html', context)


# Authentication
# def authenticate_google(request):
#     credentials_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.json')

#     flow = InstalledAppFlow.from_client_secrets_file(
#         credentials_path,
#         scopes=['https://www.googleapis.com/auth/calendar.events']
#     )

#     credentials = flow.run_local_server(port=0)

#     request.session['google_credentials'] = credentials.to_json()

#     return redirect('/calendar/calendar-events')

def authenticate_google(request):
    print('inside authenticate google')
    flow = InstalledAppFlow.from_client_secrets_file(
        './credentials.json',
        scopes=['https://www.googleapis.com/auth/calendar.events']
    )

    credentials = flow.run_local_server(port=0)

    # Build the service
    service = build('calendar', 'v3', credentials=credentials)

    # Get events from the user's primary calendar
    events_result = service.events().list(calendarId='primary', maxResults=10).execute()
    print(f"\n\nEvents result {events_result}\n\n")
    events = events_result.get('items', [])
    print(f"\n\nEvents {events}\n\n")

    if events:
        for event in events:
            event_id = event['id']
            summary = event.get('summary', '')
            description = event.get('description', 'No description available')
            start = event.get('start', {})
            end = event.get('end', {})
            print(f"\nnew: {event}")

            if 'start' in event and 'dateTime' in event['start']:
                start_datetime_str = event['start']['dateTime']
                try:
                    start_datetime = parser.parse(start_datetime_str)
                except ValueError:
                    start_datetime = None
            else:
                start_datetime = None

            # Check if the event already exists in the database
            if not Event.objects.filter(event_id=event_id).exists():
                Event.objects.create(
                    user=request.user,
                    event_id=event_id,
                    summary=summary,
                    description=description,
                    start_datetime=start_datetime,
                )

    return redirect('/calendar/calendar-events')









def calendar_events(request):
    credentials_json = request.session.get('google_credentials')
    if credentials_json:
        credentials_dict = json.loads(credentials_json)
        credentials = Credentials.from_authorized_user_info(
            credentials_dict,
            scopes=['https://www.googleapis.com/auth/calendar.events']
        )
        service = build('calendar', 'v3', credentials=credentials)
        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        events = events_result.get('items', [])

        context = {'events': events}
        return render(request, 'mycalendar/calendar_events.html', context)

    return redirect('/calendar/authenticate-google')




class CalendarEventsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        credentials_json = request.session.get('google_credentials')
        if credentials_json:
            credentials = Credentials.from_authorized_user_info(
                json.loads(credentials_json),
                scopes=['https://www.googleapis.com/auth/calendar.events']
            )
            service = build('calendar', 'v3', credentials=credentials)
            events_result = service.events().list(calendarId='primary', maxResults=10).execute()
            events = events_result.get('items', [])

            context = {'events': events}
            return render(request, 'mycalendar/calendar_events.html', context)

        return redirect('/calendar/authenticate-google')



def add_event_to_calendar_and_model(user, event_data):
    credentials_json = user.profile.google_credentials
    if credentials_json:
        credentials_dict = json.loads(credentials_json)
        credentials = Credentials.from_authorized_user_info(
            credentials_dict,
            scopes=['https://www.googleapis.com/auth/calendar.events']
        )
        service = build('calendar', 'v3', credentials=credentials)

        event = service.events().insert(calendarId='primary', body=event_data).execute()

        # Save event to Event model
        event_instance = Event.objects.create(
            user=user,
            event_id=event['id'],
            summary=event['summary'],
            description=event.get('description', ''),
            start_datetime=event['start']['dateTime'],
            end_datetime=event['end']['dateTime'],
            location=event.get('location', ''),
            # Add other fields as needed
        )

        return event_instance



def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event_data = {
                'summary': form.cleaned_data['summary'],
                'description': form.cleaned_data['description'],
                'start': {
                    'dateTime': form.cleaned_data['start_datetime'],
                    'timeZone': 'NPT',
                },
                'end': {
                    'dateTime': form.cleaned_data['end_datetime'],
                    'timeZone': 'NPT',
                },
                # Add other fields as needed
            }
            user = request.user
            event_instance = add_event_to_calendar_and_model(user, event_data)

            return redirect('/calendar/calendar-events')

    else:
        form = EventForm()

    context = {'form': form}
    return render(request, 'mycalendar/create_event.html', context)



class CalendarListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'mycalendar/index.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)
    




# ajax full calendar
def test_cal(request):
    all_events = Event.objects.filter(user=request.user)
    context = {
        "events": all_events,
    }
    return render(request, 'mycalendar/test_cal.html', context)


def all_events(request):
    all_events = Event.objects.filter(user=request.user)                                                                                  
    out = []                                                                                                             
    for event in all_events:
        out.append({
            'title': event.summary,                                                                                         
            'id': event.event_id,                                                                                              
            'start': event.start_datetime.strftime("%m/%d/%Y, %H:%M:%S"),                                                         
            'end': event.end_datetime.strftime("%m/%d/%Y, %H:%M:%S"),                                                             
        })
    return JsonResponse(out, safe=False)

def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    # event = Event(name=str(title), start=start, end=end)
    event = Event(summary=str(title), start_datetime=start, end_datetime=end, user=request.user, event_id=''.join(random.choices(string.ascii_lowercase, k=7)))
    event.save()
    data = {}
    return JsonResponse(data)
