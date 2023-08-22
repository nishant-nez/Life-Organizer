from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Goal
from django import forms
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin



@login_required
def home(request):
    user_goals = Goal.objects.filter(user=request.user)
    context = {
        'goals': user_goals,
    }

    return render(request, 'goal/index.html', context)


class GoalCreateView(LoginRequiredMixin, CreateView):
    model = Goal
    template_name = 'goal/goal_form.html'
    fields = ['title', 'amount', 'description', 'start_date', 'end_date', 'notification_mode', 'category']
    success_url = reverse_lazy('goal-home')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['start_date'].widget = forms.TextInput(attrs={'type': 'datetime-local'})
        form.fields['end_date'].widget = forms.TextInput(attrs={'type': 'datetime-local'})
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    


class GoalUpdateView(LoginRequiredMixin, UpdateView):
    model = Goal
    template_name = 'goal/goal_form.html'
    fields = ['title', 'amount', 'description', 'start_date', 'end_date', 'notification_mode', 'category']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['start_date'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
        form.fields['end_date'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
        return form


class GoalAmountUpdateView(LoginRequiredMixin, UpdateView):
    model = Goal
    template_name = 'goal/goal_amount.html'
    fields = ['complete_amount']
    success_url = reverse_lazy('goal-home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        goal = self.object
        context['goal'] = goal
        return context


class GoalDeleteView(LoginRequiredMixin, DeleteView):
    model = Goal
    success_url = '/goal'

    # def test_func(self):
    #     goal = self.get_object()
    #     if self.request.user == goal.user:
    #         return True
    #     return False



class GoalActionView(View):
    def post(self, request, goal_id):
        goal = get_object_or_404(Goal, id=goal_id)
        amount = int(request.POST.get('amount', 0))
        
        action = request.POST.get('action')
        if action == 'deposit':
            goal.complete_amount += amount
        elif action == 'withdraw':
            goal.complete_amount -= amount
        
        goal.save()
        return redirect(f'/goal/{goal.id}/amount/')