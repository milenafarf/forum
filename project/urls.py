__author__ = 'Milena Farfulowska'

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from forum import views

admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'home', name='home'),
    url(r'^$', views.home, name='home'),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^newThread/', views.newThread, name='newThread'),
    url(r'^signIn/$', views.signIn, name='signIn'),
    url(r'^signUp/$', views.signUp, name='signUp'),
    url(r'^signUp/success/', views.success, name='success'),
    url(r'^found/$', views.found, name='found'),
    url(r'^category/(?P<id>[a-z\d]{24})/$', views.category, name='category'),
    url(r'^thread/(?P<id>[a-z\d]{24})/$', views.thread, name='thread'),
    # url(r'^response/(?P<id>[a-z\d]+)/$', views.response, name='response'),
   # url(r'^thread/$', views.thread, name='thread'),
    # url(r'^project/', include('project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
