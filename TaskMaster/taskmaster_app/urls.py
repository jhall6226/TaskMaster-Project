from django.conf.urls import patterns, include, url
from django.contrib import admin
from taskmaster_app.views import dashboard, project_view, task_view, add_project, add_task, resource_view


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TaskMaster.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^dashboard/', dashboard, name='dashboard'),
    url(r'^projects/(?P<slug>[-\w]+)/$', project_view, name='project_view'),
    url(r'^tasks/(?P<slug>[-\w]+)/$', task_view, name='task_view'),
    url(r'^addproject/', add_project, name='add_project'),
    url(r'^addtask/', add_task, name='add_task'),
    url(r'^resources/(?P<slug>[-\w]+)/$', resource_view, name='resource_view'),
)