from django.urls import path
from .views import ReminderListView, ReminderDetailView, ReminderCreateView, ReminderUpdateView, ReminderDeleteView
from . import views

urlpatterns = [
    # path('', views.home, name='reminder-home'),
    path('', ReminderListView.as_view(), name='reminder-home'),
    # url that contains variable:
    path('<int:pk>/', ReminderDetailView.as_view(), name='reminder-detail'),
    path('new/', ReminderCreateView.as_view(), name='reminder-create'),
    path('<int:pk>/update/', ReminderUpdateView.as_view(), name='reminder-update'),
    path('<int:pk>/delete/', ReminderDeleteView.as_view(), name='reminder-delete'),
]
