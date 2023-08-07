from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Note
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy





class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'note/index.html'
    context_object_name = 'notes'

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)



class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    template_name = 'note/note_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('note-home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'note/note_details.html'



class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    template_name = 'note/note_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        reminder = self.get_object()
        if self.request.user == reminder.user:
            return True
        return False



class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    success_url = '/note'

    def test_func(self):
        reminder = self.get_object()
        if self.request.user == reminder.user:
            return True
        return False