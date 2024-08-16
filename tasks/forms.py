from django.forms import ModelForm

from tasks.models import Tasks


class TaskForm(ModelForm):
    class Meta:
        model = Tasks
        fields = ('title', 'description', 'important')