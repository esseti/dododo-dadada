from django.views.generic.base import TemplateView

__author__ = 'stefanotranquillini'
from django.conf.urls import patterns, include, url
from do import views
urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.ToDo.as_view(), name='todo'),
    url(r'^(?P<list>\w+)/$', views.ToDo.as_view(), name='list'),

    # url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),
    # url(r'^addtask/', views.AddTask, name="create" ),
    # url(r'^tasks/', views.TaskList.as_view(), name="list" ),
    # url(r'^percorso/$', views.percorso, name='percorso'),
    # url(r'^stazione/$', views.stazione, name='stazione'),
    # url(r'^trenitalia/', include('trenitalia.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)