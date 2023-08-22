from django.contrib import admin
from django.urls import path
from . import views  
from .views import GoalCreateView, GoalUpdateView, GoalDeleteView, GoalAmountUpdateView, GoalActionView

urlpatterns = [
    path('', views.home, name='goal-home'), 
    path('new/', GoalCreateView.as_view(), name='goal-create'),
    path('<int:pk>/update/', GoalUpdateView.as_view(), name='goal-update'),
    path('<int:pk>/delete/', GoalDeleteView.as_view(), name='goal-delete'),
    path('<int:pk>/amount/', GoalAmountUpdateView.as_view(), name='goal-amount'),
    path('<int:goal_id>/action/', GoalActionView.as_view(), name='goal-action'),
]