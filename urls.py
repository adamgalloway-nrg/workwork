from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'timetracker.views.home', name='home'),
    # url(r'^timetracker/', include('timetracker.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'timetracker.timetrackerapp.views.index'),
    url(r'^update/', 'timetracker.timetrackerapp.views.update'),
    url(r'^delete/', 'timetracker.timetrackerapp.views.delete'),
    url(r'^client/', 'timetracker.timetrackerapp.views.manage_clients'),
    url(r'^customer/', 'timetracker.timetrackerapp.views.manage_customers'),
    url(r'^project/', 'timetracker.timetrackerapp.views.manage_projects'),
    url(r'^task/', 'timetracker.timetrackerapp.views.manage_tasks'),
    url(r'^employee/', 'timetracker.timetrackerapp.views.manage_employees'),
)
