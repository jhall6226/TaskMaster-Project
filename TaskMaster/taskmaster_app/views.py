from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

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
        if request.POST.get('control') == 'delete':
            project.delete()
            messages.add_message(request, messages.INFO, 'Project deleted!')
            return HttpResponseRedirect(reverse('taskmaster_app:dashboard'))
            
        form = ProjectForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.slug = slugify(p.title)
            p.save()
            messages.add_message(request, messages.INFO, 'Project added!')
            return HttpResponseRedirect(reverse('taskmaster_app:dashboard'))
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'taskmaster_app/addproject.html',{'form':form, 'project':project})

@login_required(login_url='/')
def add_task(request):
    id = request.GET.get('id', None)
    if id is not None:
        task = get_object_or_404(Task, id=id)
    else:
        task = None
        
    if request.method == 'POST':
        if request.POST.get('control') == 'delete':
            task.delete()
            messages.add_message(request, messages.INFO, 'Task deleted!')
            return HttpResponseRedirect(reverse('taskmaster_app:dashboard'))
            
        form = ProjectForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.slug = slugify(t.project.title + '_' + t.title)
            t.save()
            messages.add_message(request, messages.INFO, 'Task added!')
            return HttpResponseRedirect(reverse('taskmaster_app:dashboard'))
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'taskmaster_app/addtask.html',{'form':form, 'task':task})

@login_required(login_url='/')
def project_view(request, **kwargs):
    slug = kwargs['slug']
    project = get_object_or_404(Project, slug=slug)
    tasks = project.tasks.all()
    resources = project.resources.all()
    
    return render(request, 'taskmaster_app/project.html', {'project':project,'tasks':tasks, 'resources':resources})

@login_required(login_url='/')
def task_view(request, **kwargs):
    slug = kwargs['slug']
    task = get_object_or_404(Task, slug=slug)
    project = task.project
    resources = task.resources.all()
    
    return render(request, 'taskmaster_app/task.html', {'project':project,'task':task, 'resources':resources})
    
@login_required(login_url='/')
def resource_view(request, **kwargs):
    slug = kwargs['slug']
    resource = get_object_or_404(Resource, slug=slug)
    projects = resource.projects.all()
    tasks = resource.tasks.all()
    
    return render(request, 'taskmaster_app/resource.html', {'projects':projects,'tasks':tasks, 'resource':resource})