from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from taskmaster_app.models import Project, Task, Resource, ProjectFile
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
    # delete_file_id = request.GET.get('delete_file_id', None)
    # if delete_file_id is not None:
    #     ProjectFile.objects.get(id=delete_file_id).delete()
    #     messages.add_message(request, messages.INFO, 'File deleted!')
    #     form = ProjectForm(instance=project)
    #     return render(request, 'taskmaster_app/addproject.html',{'form':form, 'project':project, 'files':files})

        
    if request.method == 'POST':
        if request.POST.get('control') == 'cancel':
            if id is None:
                return HttpResponseRedirect(reverse('taskmaster_app:dashboard'))
            else:
                return HttpResponseRedirect(reverse('taskmaster_app:project_view', kwargs={'project':project.slug}))
        if request.POST.get('control') == 'delete':
            for f in ProjectFile.objects.filter(project=project):
                f.delete()
            project.delete()
            messages.add_message(request, messages.INFO, 'Project deleted!')
            return HttpResponseRedirect(reverse('taskmaster_app:dashboard'))
        for f in files:
            if request.POST.get('control') == 'delete_file_' + str(f.id):
                ProjectFile.objects.get(id=f.id).delete()
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
    
    # elif request.method == 'DELETE':
    #     ProjectFile.objects.get(id=request.DELETE.get('file_id')).delete()
    #     messages.add_message(request, messages.INFO, 'File deleted!')
    #     form = ProjectForm(instance=project)
    #     return redirect('add_project',{'form':form, 'project':project, 'files':files})  
        
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
    files = project.files.all()
    
    return render(request, 'taskmaster_app/project.html', {'project':project,'tasks':tasks, 'resources':resources, 'files':files})

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