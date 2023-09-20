from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from wordcloud import WordCloud
import os
from django.conf import settings
from django.apps import AppConfig

# Create your models here.


class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.localtime)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.last_updated = timezone.localtime()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# Utility function to generate word cloud for a user
def generate_word_cloud_for_user(user):
    # Generate the word cloud only for the specified user
    notes = Note.objects.filter(user=user)
    note_content = ' '.join(note.content for note in notes)

    # Generate the word cloud
    wordcloud = WordCloud(width=1920, height=1080,
                          background_color='#374151', colormap='viridis')
    wordcloud.generate(note_content)

    # Get the path to the static folder inside the 'analytics' app
    static_folder = os.path.join(
        settings.BASE_DIR, 'dashboard', 'static', 'dashboard')

    # Save the word cloud image to the static folder with the user's username
    wordcloud_image_path = os.path.join(
        static_folder, f'wordcloud_{user.username}.png')
    wordcloud.to_file(wordcloud_image_path)


# Signal handler to generate word cloud when a new note is saved
@receiver(post_save, sender=Note)
def generate_word_cloud(sender, instance, **kwargs):
    # Call the utility function to generate the word cloud for the user
    generate_word_cloud_for_user(instance.user)
