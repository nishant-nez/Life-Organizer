import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from reminder.models import Reminder
from goal.models import Goal
from note.models import Note
from mycalendar.models import Events
from django.db.models import Count
from wordcloud import WordCloud
import base64
import os
import matplotlib.pyplot as plt
from django.conf import settings


@login_required
def home(request):
    reminders = Reminder.objects.filter(user=request.user)
    goals = Goal.objects.filter(user=request.user)
    calendars = Events.objects.filter(user=request.user)

    total_reminders = reminders.count()
    completed_reminders = reminders.filter(is_completed=True).count()

    total_calendars = calendars.count()

    total_goals = goals.count()
    print("\n\ntotal cals: ", total_calendars)
    completed_goals = sum(1 for goal in goals if goal.percentage() == 100.0)

    # Count goals by category
    goal_category_counts = goals.values('category').annotate(count=Count('id'))

    # Serialize the goal_category_counts dictionary to JSON
    goal_category_json = json.dumps(list(goal_category_counts))

    notes = Note.objects.filter(user=request.user)
    total_notes = notes.count()

    # note_content = ' '.join(note.content for note in notes)
    # # Generate the word cloud
    # wordcloud = WordCloud(width=800, height=400, background_color='white')
    # # Generate the word cloud from the note content
    # wordcloud.generate(note_content)
    # # Get the path to the static folder inside the 'analytics' app
    # static_folder = os.path.join(settings.BASE_DIR, 'analytics', 'static')

    # # Save the word cloud image to the static folder
    # wordcloud.to_file(os.path.join(static_folder, 'wordcloud.png'))

    wordcloud_image_path = f'/static/wordcloud_{request.user.username}.png'

    context = {
        'total_reminders': total_reminders,
        'completed_reminders': completed_reminders,
        'total_goals': total_goals,
        'completed_goals': completed_goals,
        'goal_category_json': goal_category_json,  # Pass as JSON string
        'total_notes': total_notes,
        # Convert the image to base64 and decode
        # 'wordcloud_image_url': '/s',
        'total_cals': total_calendars,
        'wordcloud_image_path': wordcloud_image_path,
    }

    return render(request, 'analytics/index.html', context)
