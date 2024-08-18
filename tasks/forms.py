from django import forms
from django.forms import ModelForm

from tasks.models import Tasks


class TaskForm(ModelForm):
    class Meta:
        model = Tasks
        fields = ('title', 'description', 'important')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'important': forms.CheckboxInput(attrs={}),
        }