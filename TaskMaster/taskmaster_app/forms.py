# /TaskMaster/taskmaster_app/forms.py

from django import forms
from taskmaster_app.models import Project, Task

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            'title',
            'description',
            'resources',
        )
        
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            'title',
            'task_instructions',
            'project',
            'resources',
            'status',
            'complexity',
            'estimated_time',
            'deadline',
        )