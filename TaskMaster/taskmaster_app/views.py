from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from taskmaster_app.models import Project, Task, Resource
from taskmaster_app.forms import ProjectForm, TaskForm


@login_required(login_url='/')
def dashboard(request):
    
    resource = Resource.objects.get(user=request.user)
    projects = resource.projects.all()
    tasks = resource.tasks.all()
    return render(request, 'taskmaster_app/dashboard.html',{'resource':resource,'projects':projects, 'tasks':tasks})

@login_required(login_url='/')
def add_project(request):
    id = request.GET.get('id', None)
    if id is not None:
        project = get_object_or_404(Project, id=id)
    else:
        project = None
        
    if request.method == 'POST':
        if request.POST.get('control') == 'cancel':
            if id is None:
                return HttpResponseRedirect(reverse('taskmaster_app:dashboard'))
            else:
                return HttpResponseRedirect(reverse('taskmaster_app:project_view', kwargs={'project':project.slug}))
        if request.POST.get('control') == 'delete':
            project.delete()
            messages.add_message(request, messages.INFO, 'Project deleted!')
            return HttpResponseRedirect(reverse('taskmaster_app:dashboard'))
            
        form = ProjectForm(request.POST)
        if form.is_valid():
            p = form.save()
            p.slug = slugify(p.title)
            p.save()
            if id is None:
                messages.add_message(request, messages.INFO, 'Project added!')
            else:
                messages.add_message(request, messages.INFO, 'Project saved!')
            return HttpResponseRedirect(reverse('taskmaster_app:dashboard'))
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'taskmaster_app/addproject.html',{'form':form, 'project':project})

@login_required(login_url='/')
def add_task(request, **kwargs):
    slug = kwargs['project']
    project = get_object_or_404(Project, slug=slug)
    
    id = request.GET.get('id', None)
    if id is not None:
        task = get_object_or_404(Task, id=id)
    else:
        task = Task(title='',task_instructions='',project=project,deadline=timezone.now())
        
    if request.method == 'POST':
        if request.POST.get('control') == 'cancel':
            return HttpResponseRedirect(reverse('taskmaster_app:project_view', kwargs={'project':project.slug}))
        if request.POST.get('control') == 'delete':
            task.delete()
            messages.add_message(request, messages.INFO, 'Task deleted!')
            return HttpResponseRedirect(reverse('taskmaster_app:project_view', kwargs={'project':project.slug}))
            
        form = TaskForm(request.POST)
        if form.is_valid():
            t = form.save()
            t.slug = slugify(t.title)
            t.save()            
            if id is None:
                messages.add_message(request, messages.INFO, 'Task added!')
            else:
                messages.add_message(request, messages.INFO, 'Task saved!')
            return HttpResponseRedirect(reverse('taskmaster_app:project_view', kwargs={'project':project.slug}))
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'taskmaster_app/addtask.html',{'form':form, 'task':task, 'Tasks':Task.objects.all()})

@login_required(login_url='/')
def project_view(request, **kwargs):
    slug = kwargs['project']
    project = get_object_or_404(Project, slug=slug)
    tasks = project.tasks.all()
    resources = project.resources.all()
    
    return render(request, 'taskmaster_app/project.html', {'project':project,'tasks':tasks, 'resources':resources})

@login_required(login_url='/')
def task_view(request, **kwargs):
    slug = kwargs['task']
    task = get_object_or_404(Task, slug=slug)
    project = task.project
    resources = task.resources.all()
    
    return render(request, 'taskmaster_app/task.html', {'project':project,'task':task, 'resources':resources})
    
@login_required(login_url='/')
def resource_view(request, **kwargs):
    slug = kwargs['resource']
    resource = get_object_or_404(Resource, slug=slug)
    projects = resource.projects.all()
    tasks = resource.tasks.all()
    
    return render(request, 'taskmaster_app/resource.html', {'projects':projects,'tasks':tasks, 'resource':resource})