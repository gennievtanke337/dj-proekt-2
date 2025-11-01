from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm, TaskFilterForm
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class UserIsOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class TaskListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        qs = Task.objects.filter(author=self.request.user)
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')

        if status:
            qs = qs.filter(status=status)
        if priority:
            qs = qs.filter(priority=priority)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TaskFilterForm(self.request.GET)
        return context


class TaskDetailView(LoginRequiredMixin, UserIsOwnerMixin, DetailView):
    login_url = 'login'
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'


class TaskCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = date.today().strftime("%Y-%m-%d")
        return context

class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    login_url = 'login'
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')


class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    login_url = 'login'
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')


