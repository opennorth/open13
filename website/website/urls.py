from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include('billy.web.admin.urls')),
    (r'^djadmin/', include(admin.site.urls)),
    (r'^login/$', 'django.contrib.auth.views.login',
     #{'template_name': 'django/login.html'}
    ),
)
