from django.shortcuts import render, redirect
# from .forms import ReminderCreateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Reminder
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse


# @login_required
# def home(request):
#     # return HttpResponse('<h1>Reminder Home</h1>')
#     context = {
#         # 'reminders': reminder_list,
#         'reminders': Reminder.objects.all(),
#     }

#     return render(request, 'reminder/index.html', context)


@login_required
def home(request):
    user_reminders = Reminder.objects.filter(user=request.user)

    # if request.method == "POST":
    #     r_form = ReminderCreateForm(request.POST)

    #     if r_form.is_valid():
    #         reminder = r_form.save(commit=False)
    #         reminder.user = request.user
    #         reminder.save()
    #         r_title = r_form.cleaned_data.get('title')
    #         messages.success(request, f'{r_title} has been created!')
    #         return redirect('reminder-home')
    # else:
    #     r_form = ReminderCreateForm()

    context = {
        'reminders': user_reminders,
        # 'r_form': r_form,
    }
    return render(request, 'reminder/index.html', context)


class ReminderListView(LoginRequiredMixin, ListView):
    model = Reminder
    template_name = 'reminder/index.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'reminders'
    ordering = ['due_date']

    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user)

    # provide necessary context data for forms
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(*kwargs)
    #     context['r_form'] = ReminderCreateForm()
    #     return context


class ReminderDetailView(LoginRequiredMixin, DetailView):
    model = Reminder
    template_name = 'reminder/reminder_details.html'  # <app>/<model>_<viewtype>.html


class ReminderCreateView(LoginRequiredMixin, CreateView):
    model = Reminder
    template_name = 'reminder/reminder_form.html'  # <app>/<model>_<viewtype>.html
    fields = ['title', 'description', 'due_date', 'notification_mode']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['due_date'].widget = forms.TextInput(
            attrs={'type': 'datetime-local'})
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReminderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Reminder
    template_name = 'reminder/reminder_form.html'  # <app>/<model>_<viewtype>.html
    fields = ['title', 'description', 'due_date',
              'is_completed', 'notification_mode']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # form.fields['due_date'].widget = forms.TextInput(attrs={'type': 'datetime-local'})
        # return form

        # Format the due_date value for datetime-local input
        if form.instance.due_date:
            formatted_due_date = form.instance.due_date.strftime(
                '%Y-%m-%dT%H:%M')
            form.fields['due_date'].widget = forms.TextInput(
                attrs={'type': 'datetime-local', 'value': formatted_due_date})

        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        reminder = self.get_object()
        if self.request.user == reminder.user:
            return True
        return False


class ReminderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Reminder
    # success_url = '/reminder/'
    # template name automatically added without specifying
    # template_name = 'reminder/reminder_confirm_delete.html'

    def get_success_url(self):
        return reverse('reminder-home')

    def test_func(self):
        reminder = self.get_object()
        if self.request.user == reminder.user:
            return True
        return False


@login_required
def mark_as_completed(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk)

    if request.method == 'POST':
        reminder.is_completed = True
        reminder.save()

    return redirect('reminder-home')
