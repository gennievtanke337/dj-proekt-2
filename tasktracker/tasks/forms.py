from django import forms
from .models import Task
from django import forms
from .models import Comment
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),  
        }



class TaskFilterForm(forms.Form):
    status = forms.ChoiceField(
        choices=[('', 'All')] + list(Task._meta.get_field('status').choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    priority = forms.ChoiceField(
        choices=[('', 'All')] + list(Task._meta.get_field('priority').choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']