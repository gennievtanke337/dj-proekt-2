from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Task, Comment
from .forms import TaskForm, TaskFilterForm, CommentForm
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect

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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if "add_comment" in request.POST:
            form = CommentForm(request.POST, request.FILES)
            if form.is_valid():
                c = form.save(commit=False)
                c.task = self.object
                c.author = request.user
                c.save()
            return redirect('task_detail', pk=self.object.pk)

        if "edit_comment" in request.POST:
            comment = Comment.objects.get(pk=request.POST.get("comment_id"))
            if comment.author != request.user:
                raise PermissionDenied
            form = CommentForm(request.POST, request.FILES, instance=comment)
            if form.is_valid():
                form.save()
            return redirect('task_detail', pk=self.object.pk)

        if "delete_comment" in request.POST:
            comment = Comment.objects.get(pk=request.POST.get("comment_id"))
            if comment.author != request.user:
                raise PermissionDenied
            comment.delete()
            return redirect('task_detail', pk=self.object.pk)

        return redirect('task_detail', pk=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all().order_by('-created_at')
        return context


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
