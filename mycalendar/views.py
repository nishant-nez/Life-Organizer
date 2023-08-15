from django.shortcuts import render, redirect
from django.http import JsonResponse 
from .models import Events 
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import pytz
from dateutil import parser
from django.utils.timezone import make_aware
import re

import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials




@login_required
def authenticate_google(request):
    """authenticate google with google calendar and read all events!."""

    redirect_uri = "http://localhost:8000"  # Update this with your redirect URI

    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
                "project_id": os.environ.get("GOOGLE_PROJECT_ID"),
                "auth_uri": os.environ.get("GOOGLE_AUTH_URI"),
                "token_uri": os.environ.get("GOOGLE_TOKEN_URI"),
                "auth_provider_x509_cert_url": os.environ.get("GOOGLE_AUTH_PROVIDER_CERT_URL"),
                "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
                "redirect_uris": [os.environ.get("GOOGLE_REDIRECT_URIS")],
            }
        },
        scopes=["https://www.googleapis.com/auth/calendar.events"],
    )

    credentials = flow.run_local_server(port=0)
    time_min = datetime(2023, 1, 1).isoformat() + 'Z'

    service = build('calendar', 'v3', credentials=credentials)
    events_result = service.events().list(calendarId='primary', timeMin=time_min).execute()
    events = events_result.get('items', [])

    if events:
        for event in events:
            print(f"\n\nnew event: {event}")
            event_id = event['id']
            summary = event.get('summary', '')
            start = event.get('start', {})
            end = event.get('end', {})

            start_datetime_str = start.get('dateTime', None)
            end_datetime_str = end.get('dateTime', None)

            start_datetime = None  # Initialize start_datetime

            if start_datetime_str:
                start_datetime_str = start_datetime_str.split('+', 1)[0]
                start_datetime = timezone.datetime.strptime(start_datetime_str, "%Y-%m-%dT%H:%M:%S")
                start_datetime = timezone.make_aware(start_datetime, pytz.timezone(settings.TIME_ZONE))

            if end_datetime_str:
                end_datetime_str = end_datetime_str.split('+', 1)[0]
                end_datetime = timezone.datetime.strptime(end_datetime_str, "%Y-%m-%dT%H:%M:%S")
                end_datetime = timezone.make_aware(end_datetime, pytz.timezone(settings.TIME_ZONE))
            elif start_datetime:
                end_datetime = start_datetime + timedelta(hours=1)  # Default to 1 hour duration

            if start_datetime:
                if not Events.objects.filter(name=summary, start=start_datetime):
                    Events.objects.create(
                        user=request.user,
                        event_id=event_id,
                        name=summary,
                        start=start_datetime,
                        end=end_datetime,
                    )

    return redirect('/calendar/')

##############################################

@login_required
def index(request):  
    all_events = Events.objects.filter(user=request.user) 
    context = {
        "events":all_events,
    }
    return render(request,'mycalendar/index.html',context)

@login_required
def all_events(request):                                                                                                 
    all_events = Events.objects.filter(user=request.user)                                                                           
    out = []                                                                                                             
    for event in all_events:                                                                                             
        out.append({                                                                                                     
            'title': event.name,                                                                                         
            'id': event.id,                                                                                              
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),                                                         
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),                         
        })                                                                                                                                                                                                                      
    return JsonResponse(out, safe=False)

# to fix the runtimewarning : received a naive datetime while time zone support is active.

def parse_datetime(datetime_str):
    print("\n\n" + datetime_str + "\n\n")
    tz = timezone.get_current_timezone()  # Use the timezone from settings
    try:
        naive_datetime = timezone.datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M")
        aware_datetime = timezone.make_aware(naive_datetime, tz)
    except ValueError:
        try:
            input_datetime_str = re.sub(r'[AT]', '_', datetime_str)
            input_format = '%Y-%m-%d_P%I:%M:%S'
            output_format = '%Y-%m-%dT%H:%M'

            # Parse the input datetime string
            parsed_datetime = datetime.strptime(input_datetime_str, input_format)

            # Convert the parsed datetime to the desired format
            formatted_datetime = parsed_datetime.strftime(output_format)

            # Convert to timezone-aware datetime (adjust 'your_timezone_here')
            aware_datetime = tz.localize(parsed_datetime)
        except ValueError:
            # Handle other cases if needed
            raise ValueError("\nnk: Invalid datetime format: %s" % datetime_str)

    return aware_datetime



def parse_update_datetime(datetime_str):
    tz = timezone.get_current_timezone()  # Use the timezone from settings
    
    datetime_formats = [
        r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})P?(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})',
        # Add more regex patterns as needed
    ]
    
    for format_pattern in datetime_formats:
        match = re.match(format_pattern, datetime_str)
        if match:
            datetime_dict = match.groupdict()
            print("Extracted components:", datetime_dict)  # Debug print
            # Handle AM/PM format
            if datetime_str[-2:] in ('AM', 'PM'):
                datetime_dict['hour'] = datetime_dict['hour'].rjust(2, '0')
            # Construct the datetime object
            parsed_datetime = timezone.datetime(**{k: int(v) for k, v in datetime_dict.items()})
            aware_datetime = timezone.make_aware(parsed_datetime, tz)
            return aware_datetime
    
    raise ValueError("\nnk: Invalid datetime format: %s" % datetime_str)



@login_required
def add_event(request):
    start = parse_datetime(request.GET.get("start", None))
    end = parse_datetime(request.GET.get("end", None))
    title = request.GET.get("title", None)
    user = request.user
    event = Events(name=str(title), start=start, end=end, user=user)
    event.save()
    data = {}
    return JsonResponse(data)

@login_required
def update(request):
    start = parse_update_datetime(request.GET.get("start", None))
    end = parse_update_datetime(request.GET.get("end", None))
    print(start)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)



@login_required
def remove(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)