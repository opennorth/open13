from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include('billy.web.admin.urls')),
    (r'^api/', include('billy.web.api.urls')),
    (r'^', include('billy.web.public.urls')),
    #(r'^djadmin/', include(admin.site.urls)),
    #(r'^login/$', 'django.contrib.auth.views.login',
    # {'template_name': 'django/login.html'}
    #),
)
