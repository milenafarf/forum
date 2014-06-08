from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from forum import views

admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'home', name='home'),
    url(r'^$', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^project/', include('project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
