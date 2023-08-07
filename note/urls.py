from django.urls import path
from .views import NoteListView, NoteCreateView, NoteDetailView, NoteUpdateView, NoteDeleteView
from . import views

urlpatterns = [
    path('', NoteListView.as_view(), name='note-home'),
    path('new/', NoteCreateView.as_view(), name='note-create'),
    path('<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
    path('<int:pk>/update/', NoteUpdateView.as_view(), name='note-update'),
    path('<int:pk>/delete/', NoteDeleteView.as_view(), name='note-delete'),
]