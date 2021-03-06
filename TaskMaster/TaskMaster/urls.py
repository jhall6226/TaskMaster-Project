from django.conf.urls import patterns, include, url
from django.contrib import admin
from TaskMaster.views import home_view, register_view

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TaskMaster.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home_view, name='home'),   
    url(r'^register/', register_view, name='register'),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page':'home'}, name='logout'),
    url(r'^/', include('taskmaster_app.urls', namespace='taskmaster_app')),
)
