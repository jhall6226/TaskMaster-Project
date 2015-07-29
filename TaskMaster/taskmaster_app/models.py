from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from shutil import rmtree
import os
from TaskMaster import settings

def get_project_file_storage_path(project_file_instance, filename):
    return 'project_files/%s/%s' % (project_file_instance.project.slug, filename)

def get_task_file_storage_path(task_file_instance, filename):
    return 'project_files/%s/task_files/%s/%s' % (task_file_instance.project.slug, task_file_instance.task.slug, filename)
    
def get_abs_project_file_storage_directory(project_instance):
    return os.path.join(settings.MEDIA_ROOT, 'project_files/%s' % (project_instance.slug))

def get_abs_task_file_storage_directory(task_instance):
    return os.path.join(settings.MEDIA_ROOT, 'project_files/%s/task_files/%s' % (task_instance.project.slug, task_instance.slug))

class Project(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200,default='slug_placeholder')
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, default=timezone.now())
    resources = models.ManyToManyField('Resource', related_name='projects')
    
    def delete_media_files(self):
        project_media_directory = get_abs_project_file_storage_directory(self)
        rmtree(project_media_directory)
    
    def __unicode__(self):
        return self.title
        
class Task(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,default='slug_placeholder')
    task_instructions = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, default=timezone.now())
    deadline = models.DateTimeField()
    
    # Complexity field and choice creation
    
    LOW='L'
    MEDIUM_LOW='ML'
    MEDIUM='M'
    MEDIUM_HIGH='MH'
    HIGH='H'   
    
    complexity_choices = (
        (LOW, 'Low - 1'),
        (MEDIUM_LOW, 'Medium-Low - 2'),
        (MEDIUM, 'Medium - 3'),
        (MEDIUM_HIGH, 'Medium-High - 4'),
        (HIGH, 'High - 5'),
    )
    
    complexity = models.CharField(max_length=2,blank=True,choices=complexity_choices)
    
    # -----
    
    estimated_time = models.FloatField(default=1.0) #Time to complete in hours
    
    # Status field and choice creation
    
    NOT_YET_STARTED = 'NS'
    IN_PROGRESS = 'IP'
    READY_FOR_REVIEW = 'RR'
    COMPLETE = 'CP'
    
    status_choices= (
        (NOT_YET_STARTED, 'Not yet started'),
        (IN_PROGRESS, 'In progress'),
        (READY_FOR_REVIEW, 'Ready for review'),
        (COMPLETE, 'Complete'),
        )
    
    status = models.CharField(max_length=2,default=NOT_YET_STARTED,choices=status_choices)
    
    # -----
    
    project = models.ForeignKey('Project', related_name='tasks')
    resources = models.ManyToManyField('Resource', related_name='tasks')
    
    def delete_media_files(self):
        task_media_directory = get_abs_task_file_storage_directory(self)
        rmtree(task_media_directory)
    
    def __unicode__(self):
        return (self.title)
    
    
class Resource(models.Model):
    user = models.OneToOneField(User, null=True)
    slug = models.SlugField(max_length=200,default='slug_placeholder')
    
    def __unicode__(self):
        return self.user.get_full_name()

class ProjectFile(models.Model):
    project = models.ForeignKey('Project', related_name='files', related_query_name='file')
    f = models.FileField(upload_to=get_project_file_storage_path)
    def get_full_file_name(self):
        url_text_list = self.f.url.split('/')
        full_file_name = url_text_list[-1]
        return full_file_name
        
    def get_file_name(self):
        full_file_name = self.get_full_file_name()
        return full_file_name.split('.')[0]
        
    def get_doc_type(self):
        full_file_name = self.get_full_file_name()
        return full_file_name.split('.')[-1].upper()
    
class TaskFile(models.Model):
    task = models.ForeignKey('Task', related_name='files', related_query_name='file')
    project = models.ForeignKey('Project', related_name='task_files')
    f = models.FileField(upload_to=get_task_file_storage_path)
    def get_full_file_name(self):
        url_text_list = self.f.url.split('/')
        full_file_name = url_text_list[-1]
        return full_file_name
        
    def get_file_name(self):
        full_file_name = self.get_full_file_name()
        return full_file_name.split('.')[0]
        
    def get_doc_type(self):
        full_file_name = self.get_full_file_name()
        return full_file_name.split('.')[1].upper()