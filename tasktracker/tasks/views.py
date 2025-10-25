from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm
from datetime import date
from django.contrib.auth.models import User

class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        default_user = User.objects.first() 
        form.instance.author = default_user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = date.today().strftime("%Y-%m-%d")
        return context

def form_valid(self, form):
    form.instance.author_id = 1
    return super().form_valid(form)

