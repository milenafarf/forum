__author__ = 'Milena Farfulowska'

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from forum import views, viewsAdmin

admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'home', name='home'),
    url(r'^$', views.home, name='home'),
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^signIn/$', views.signIn, name='signIn'),
    url(r'^signUp/$', views.signUp, name='signUp'),
    url(r'^logOut/$', views.logOut, name='logOut'),

    url(r'^userProfile/(?P<id>[a-z\d]{24})/$', views.userProfile, name='userProfile'),
    url(r'^editUser/$', views.editUser, name='editUser'),
    url(r'^delUser/(?P<id>[a-z\d]{24})/$', views.delUser, name='delUser'),
    url(r'^usersAdmin/$', viewsAdmin.users, name='usersAdmin'),
    url(r'^usersAdmin/editUser/(?P<id>[a-z\d]{24})/$', viewsAdmin.editUser, name='editUserAdmin'),
    url(r'^usersAdmin/delUser/(?P<id>[a-z\d]{24})/$', viewsAdmin.delUser, name='delUserAdmin'),

    url(r'^signUp/success/', views.success, name='success'),
    url(r'^found/$', views.found, name='found'),
    url(r'^error/(?P<msg>[\d]{1})/$', views.error, name='error'),
    url(r'^success/(?P<msg>[\d]{1})/$', views.success, name='success'),
    url(r'^info/(?P<msg>[\d]{1})/$', views.info, name='info'),
    url(r'^category/(?P<id>[a-z\d]{24})/', views.category, name='category'),

    # threads
    url(r'^thread/(?P<id>[a-z\d]{24})/$', views.thread, name='thread'),
    url(r'^editThread/(?P<id>[a-z\d]{24})/$', views.editThread, name='editThread'),
    url(r'^delThread/(?P<id>[a-z\d]{24})/$', views.delThread, name='delThread'),
    url(r'^reportThread/(?P<id>[a-z\d]{24})/$', views.reportThread, name='reportThread'),
    # url(r'^banThread/(?P<id>[a-z\d]{24})/$', viewsAdmin.banThread, name='banThread'),
    url(r'^setOkThread/(?P<id>[a-z\d]{24})/$', viewsAdmin.setOkThread, name='setOkThread'),
    url(r'^reportedThreads/$', viewsAdmin.reportedThreads, name='reportedThreads'),
    url(r'^newThread/', views.newThread, name='newThread'),

    #responses
    url(r'^response/(?P<id>[a-z\d]{24})/$', views.response, name='response'),
    url(r'^editResponse/(?P<id>[a-z\d]{24})/$', views.editResponse, name='editResponse'),
    url(r'^delResponse/(?P<id>[a-z\d]{24})/$', views.delResponse, name='delResponse'),
    url(r'^reportResponse/(?P<id>[a-z\d]{24})/$', views.reportResponse, name='reportResponse'),
    # url(r'^banThread/(?P<id>[a-z\d]{24})/$', viewsAdmin.banThread, name='banThread'),
    url(r'^setOkResponse/(?P<id>[a-z\d]{24})/$', viewsAdmin.setOkResponse, name='setOkResponse'),
    url(r'^reportedResponses/$', viewsAdmin.reportedResponses, name='reportedResponses'),

    # url(r'^response/(?P<id>[a-z\d]+)/$', views.response, name='response'),
   # url(r'^thread/$', views.thread, name='thread'),
    # url(r'^project/', include('project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
