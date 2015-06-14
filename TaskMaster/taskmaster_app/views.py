from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from taskmaster_app.models import Project, Task, Resource, ProjectFile, TaskFile
from taskmaster_app.forms import ProjectForm, TaskForm


@login_required(login_url='/')
def dashboard(request):
    
    resource = Resource.objects.get(user=request.user)
    projects = resource.projects.all()
    tasks = resource.tasks.all()
    return render(request, 'taskmaster_app/dashboard.html',{'resource':resource,'projects':projects, 'tasks':tasks})

@login_required(login_url='/')
def add_project(request, **kwargs):
    
    id = request.GET.get('id', None)
    if id is not None:
        project = get_object_or_404(Project, id=id)
        date_created = project.date_created
        files = project.files.all()
    else:
        project = None
        files=[]
        
    if request.method == 'POST':
        if request.POST.get('control') == 'cancel':
            if id is None:
                return HttpResponseRedirect(reverse('taskmaster_app:dashboard'))
            else:
                return HttpResponseRedirect(reverse('taskmaster_app:project_view', kwargs={'project':project.slug}))
        if request.POST.get('control') == 'delete':
            for f in ProjectFile.objects.filter(project=project):
                f.delete()
            project.delete_media_files()
            project.delete()
            messages.add_message(request, messages.INFO, 'Project deleted!')
            return HttpResponseRedirect(reverse('taskmaster_app:dashboard'))
        for f in files:
            if request.POST.get('control') == 'delete_file_' + str(f.id):
                pf = ProjectFile.objects.get(id=f.id)
                pf.f.delete()
                pf.delete()
                messages.add_message(request, messages.INFO, 'File deleted!')
                project = get_object_or_404(Project, id=id)
                files = project.files.all()
                form = ProjectForm(instance=project)
                return render(request, 'taskmaster_app/addproject.html',{'form':form, 'project':project, 'files':files})
                    
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.slug = slugify(project.title)
            if id:
                project.date_created = date_created
                project.id = id
                messages.add_message(request, messages.INFO, 'Project saved!')
            else:
                messages.add_message(request, messages.INFO, 'Project added!')
            project.save()
            form.save_m2m() 
            for f in request.FILES.getlist('files'):
                ProjectFile(f=f,project=project).save()
            return HttpResponseRedirect(reverse('taskmaster_app:project_view', kwargs={'project':project.slug})) 
        
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'taskmaster_app/addproject.html',{'form':form, 'project':project, 'files':files})

@login_required(login_url='/')
def add_task(request, **kwargs):
    slug = kwargs['project']
    project = get_object_or_404(Project, slug=slug)
    
    id = request.GET.get('id', None)
    if id is not None:
        task = get_object_or_404(Task, id=id)
        date_created = task.date_created
        files = task.files.all()
    else:
        task = Task(title='',task_instructions='',project=project,deadline=timezone.now())
        files = []
        
    if request.method == 'POST':
        if request.POST.get('control') == 'cancel':
            return HttpResponseRedirect(reverse('taskmaster_app:task_view', kwargs={'project':project.slug, 'task':task.slug}))
        if request.POST.get('control') == 'delete':
            task.delete_media_files()
            task.delete()
            messages.add_message(request, messages.INFO, 'Task deleted!')
            return HttpResponseRedirect(reverse('taskmaster_app:project_view', kwargs={'project':project.slug}))
        for f in files:
            if request.POST.get('control') == 'delete_file_' + str(f.id):
                tf = TaskFile.objects.get(id=f.id)
                tf.f.delete()
                tf.delete()
                messages.add_message(request, messages.INFO, 'File deleted!')
                task = get_object_or_404(Task, id=id)
                files = task.files.all()
                form = TaskForm(instance=task)
                return render(request, 'taskmaster_app/addtask.html',{'form':form, 'task':task, 'files':files})        
            
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.slug = slugify(task.title)
            if id:
                task.date_created = date_created
                task.id = id
                messages.add_message(request, messages.INFO, 'Task saved!')
            else:
                messages.add_message(request, messages.INFO, 'Task added!')
            task.save()
            form.save_m2m() 
            for f in request.FILES.getlist('files'):
                TaskFile(f=f,task=task,project=project).save()
            return HttpResponseRedirect(reverse('taskmaster_app:task_view', kwargs={'project':project.slug, 'task':task.slug})) 
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'taskmaster_app/addtask.html',{'form':form, 'task':task, 'files':files})

@login_required(login_url='/')
def project_view(request, **kwargs):
    slug = kwargs['project']
    project = get_object_or_404(Project, slug=slug)
    tasks = project.tasks.all()
    resources = project.resources.all()
    files = project.files.all()
    
    return render(request, 'taskmaster_app/project.html', {'project':project,'tasks':tasks, 'resources':resources, 'files':files})

@login_required(login_url='/')
def task_view(request, **kwargs):
    slug = kwargs['task']
    task = get_object_or_404(Task, slug=slug)
    project = task.project
    resources = task.resources.all()
    files = task.files.all()
    
    return render(request, 'taskmaster_app/task.html', {'project':project,'task':task, 'resources':resources, 'files':files})
    
@login_required(login_url='/')
def resource_view(request, **kwargs):
    slug = kwargs['resource']
    resource = get_object_or_404(Resource, slug=slug)
    projects = resource.projects.all()
    tasks = resource.tasks.all()
    
    return render(request, 'taskmaster_app/resource.html', {'projects':projects,'tasks':tasks, 'resource':resource})