from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify

class Project(models.Model):
    title = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=200,default='slug_placeholder')
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, default=timezone.now())
    
    resources = models.ManyToManyField('Resource', related_name='projects')
    
    attachments = models.FileField(upload_to='projects/',blank=True)
    
    def __unicode__(self):
        return self.title
        
class Task(models.Model):
    title = models.CharField(max_length=200,unique=True)
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
        (COMPLETE, 'CP'),
        )
    
    status = models.CharField(max_length=2,default=NOT_YET_STARTED,choices=status_choices)
    
    # -----
    
    project = models.ForeignKey('Project', related_name='tasks')
    
    resources = models.ManyToManyField('Resource', related_name='tasks')
    
    def __unicode__(self):
        return (self.title)
    
    
class Resource(models.Model):
    user = models.OneToOneField(User, null=True)
    slug = models.SlugField(max_length=200,default='slug_placeholder')
    
    def __unicode__(self):
        return self.user.get_full_name()