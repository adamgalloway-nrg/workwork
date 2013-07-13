from django.conf.urls import patterns, include, url
from tastypie.api import Api
from timetrackerapp.resources import ClientResource, CustomerResource, ProjectResource, EmployeeResource, TaskDefinitionResource, PaidTimeOffResource, CommentResource, TimeEntryResource, WeekEntryResource
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()
from timetrackerapp.mongo_auth_views import GoogleLoginView
from mongo_auth.views import GoogleCallbackView

service_api = Api(api_name='service')
service_api.register(ClientResource())
service_api.register(CustomerResource())
service_api.register(ProjectResource())
service_api.register(EmployeeResource())
service_api.register(TaskDefinitionResource())
service_api.register(PaidTimeOffResource())
service_api.register(CommentResource())
service_api.register(TimeEntryResource())
service_api.register(WeekEntryResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'timetracker.views.home', name='home'),
    # url(r'^timetracker/', include('timetracker.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #url(r'^', include('mongo_auth.contrib.urls')),

    url(r'^google/login/$', GoogleLoginView.as_view(), name='google_login'),
    url(r'^google/callback/$', GoogleCallbackView.as_view(), name='google_callback'),
    url(r'^logout/$', 'mongo_auth.views.logout', name='logout'),

    url(r'^$', 'timetracker.timetrackerapp.views.index'),
    url(r'^dashboard/', 'timetracker.timetrackerapp.views.dashboard'),
    
    url(r'^client/', 'timetracker.timetrackerapp.views.manage_clients'),
    url(r'^customer/', 'timetracker.timetrackerapp.views.manage_customers'),
    url(r'^project/', 'timetracker.timetrackerapp.views.manage_projects'),
    url(r'^task/', 'timetracker.timetrackerapp.views.manage_tasks'),
    url(r'^employee/', 'timetracker.timetrackerapp.views.manage_employees'),
    url(r'^pto/', 'timetracker.timetrackerapp.views.manage_pto'),
    url(r'^time/', 'timetracker.timetrackerapp.views.manage_time'),

    #url(r'^oauth2callback', 'timetracker.timetrackerapp.views.auth_return'),
    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'plus/login.html'}),
    
    url(r'', include(service_api.urls)),
)

