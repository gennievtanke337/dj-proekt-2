from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'Нова'),
        ('in_progress', 'В процесі'),
        ('done', 'Виконана'),
    ]


    PRIORITY_CHOICES = [
        ('low', 'Низький'),
        ('medium', 'Середній'),
        ('high', 'Високий'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Коментар від {self.author.username}'