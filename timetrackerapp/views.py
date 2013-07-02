from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView
from models import Post
from models import Client, Comment, Customer, Employee, PaidTimeOff, Project, TaskDefinition, TimeEntry, WeekEntry
from forms import TimeEntryForm
import datetime
import calendar
import math
import decimal
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory





def get_weekId(today):
    calendar.setfirstweekday(calendar.SUNDAY)
    monthcalendar = calendar.monthcalendar(today.year, today.month)

    day_of_week = today.weekday()
    if day_of_week == 6:
        day_of_week == 0
    else:
        day_of_week += 1

    weeks = monthcalendar

    weekCount = 0
    for week in weeks:
        weekCount += 1
        if week[day_of_week] == today.day:
            if week[0] == 0:
                #get week number of prev month, year
                date = datetime.datetime(today.year,today.month, 1) - datetime.timedelta(days=1)
                prev_monthcalendar = calendar.monthcalendar(date.year, date.month)
                weekVal = len(prev_monthcalendar)
                return "%04d%02d%d" % (date.year,date.month,weekVal)
            else:
                return "%04d%02d%d" % (today.year,today.month,weekCount)


def get_current_weekId():
    return get_weekId(datetime.datetime.now())


def get_prev_weekId(weekId):
    week_id_str = str(weekId)
    year = int(week_id_str[:4])
    month = int(week_id_str[4:6])
    prev_week = int(week_id_str[6:7]) - 1

    calendar.setfirstweekday(calendar.SUNDAY)

    monthcalendar = calendar.monthcalendar(year, month)
    if prev_week == 0 or monthcalendar[prev_week - 1][0] == 0:
        #get week number of prev month, year
        date = datetime.datetime(year,month,1) - datetime.timedelta(days=1)
        prev_monthcalendar = calendar.monthcalendar(date.year, date.month)
        weekVal = len(prev_monthcalendar)
        return "%04d%02d%d" % (date.year,date.month,weekVal)
    else:
        return "%04d%02d%d" % (year,month,prev_week)


def get_next_weekId(weekId):
    week_id_str = str(weekId)
    year = int(week_id_str[:4])
    month = int(week_id_str[4:6])
    next_week = int(week_id_str[6:7]) + 1

    calendar.setfirstweekday(calendar.SUNDAY)

    monthcalendar = calendar.monthcalendar(year, month)
    if next_week > len(monthcalendar):
        #get week number of prev month, year
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1

        next_monthcalendar = calendar.monthcalendar(year, month)
        if next_monthcalendar[0][0] != 0:
            return "%04d%02d%d" % (year,month,1)
        else:
             return "%04d%02d%d" % (year,month,2)
    else:
        return "%04d%02d%d" % (year,month,next_week)


def get_employee(request):
    if 'employee' not in request.session:
        request.session['employee'] = Employee.objects.get(email=request.user.email)
    return request.session['employee']



@login_required
def index(request):
    employee = get_employee(request)

    if 'weekId' not in request.REQUEST or not request.REQUEST['weekId']:
        return redirect('/?weekId=' + get_current_weekId())
    else:
        weekId = request.REQUEST['weekId']

        if math.isnan(float(weekId)):
            return redirect('/?weekId=' + get_current_weekId())

        time_entries = TimeEntry.objects(employee=employee.email, weekId=weekId)

        time_entry_tasks = {}
        for time_entry in time_entries:
            task_id = str(time_entry.taskDefinitionId)
            row_id = str(time_entry.rowId)

            key = task_id + '-' + row_id
            print key
            if key not in time_entry_tasks:
                time_entry_tasks[key] = {
                    'taskDefinitionId': task_id,
                    'rowId': row_id,
                    'sundayHours': decimal.Decimal('0'),
                    'mondayHours': decimal.Decimal('0'),
                    'tuesdayHours': decimal.Decimal('0'),
                    'wednesdayHours': decimal.Decimal('0'),
                    'thursdayHours': decimal.Decimal('0'),
                    'fridayHours': decimal.Decimal('0'),
                    'saturdayHours': decimal.Decimal('0')
                }

            if time_entry.date.weekday() == 0:
                time_entry_tasks[key]['mondayHours'] += time_entry.durationInHours
            elif time_entry.date.weekday() == 1:
                time_entry_tasks[key]['tuesdayHours'] += time_entry.durationInHours
            elif time_entry.date.weekday() == 2:
                time_entry_tasks[key]['wednesdayHours'] += time_entry.durationInHours
            elif time_entry.date.weekday() == 3:
                time_entry_tasks[key]['thursdayHours'] += time_entry.durationInHours
            elif time_entry.date.weekday() == 4:
                time_entry_tasks[key]['fridayHours'] += time_entry.durationInHours
            elif time_entry.date.weekday() == 5:
                time_entry_tasks[key]['saturdayHours'] += time_entry.durationInHours
            elif time_entry.date.weekday() == 6:
                time_entry_tasks[key]['sundayHours'] += time_entry.durationInHours

        form_data = []
        for time_entry_key in time_entry_tasks:
            print time_entry_tasks[time_entry_key]
            form_data.append(time_entry_tasks[time_entry_key])


        TimeEntryFormSet = formset_factory(TimeEntryForm,extra=0)
        if request.method == 'POST':
            time_entry_formset = TimeEntryFormSet(request.POST, request.FILES)
            if time_entry_formset.is_valid():
                # do something with the cleaned_data on the formsets.

                pass
        else:
            time_entry_formset = TimeEntryFormSet(initial=form_data)


        return render_to_response('index.html', {
            'time_entry_formset': time_entry_formset,
            'prev_weekId': get_prev_weekId(weekId),
            'next_weekId': get_next_weekId(weekId),
            'tasks': TaskDefinition.objects
        }, context_instance=RequestContext(request))



@login_required
def manage_customers(request):

    return render_to_response('customer.html', {'customers': Customer.objects}, context_instance=RequestContext(request))

@login_required
def manage_clients(request):

    return render_to_response('client.html', {'clients': Client.objects}, context_instance=RequestContext(request))

@login_required
def manage_projects(request):

    return render_to_response('project.html', {'projects': Project.objects}, context_instance=RequestContext(request))

@login_required
def manage_tasks(request):

    return render_to_response('task.html', {'tasks': TaskDefinition.objects}, context_instance=RequestContext(request))

@login_required
def manage_employees(request):

    return render_to_response('employee.html', {'employees': Employee.objects}, context_instance=RequestContext(request))


# REQUIRES SQLITE
# import os
# import logging
# import httplib2

# from apiclient.discovery import build
# from django.contrib.auth.decorators import login_required
# from django.core.urlresolvers import reverse
# from django.http import HttpResponse
# from django.http import HttpResponseBadRequest
# from django.http import HttpResponseRedirect
# from models import CredentialsModel
# from timetracker import settings
# from oauth2client import xsrfutil
# from oauth2client.client import flow_from_clientsecrets
# from oauth2client.django_orm import Storage

# # CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# # application, including client_id and client_secret, which are found
# # on the API Access tab on the Google APIs
# # Console <http://code.google.com/apis/console>
# CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '..', 'client_secrets.json')

# FLOW = flow_from_clientsecrets(CLIENT_SECRETS, scope='https://www.googleapis.com/auth/plus.me', redirect_uri='http://localhost:8000/oauth2callback')


# @login_required
# def index(request):
#   storage = Storage(CredentialsModel, 'id', request.user, 'credential')
#   credential = storage.get()
#   if credential is None or credential.invalid == True:
#     FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
#     authorize_url = FLOW.step1_get_authorize_url()
#     print authorize_url
#     return HttpResponseRedirect(authorize_url)
#   else:
#     http = httplib2.Http()
#     http = credential.authorize(http)
#     service = build("plus", "v1", http=http)
#     activities = service.activities()
#     activitylist = activities.list(collection='public', userId='me').execute()
#     logging.info(activitylist)
#     print "headed to welcome"
#     return render_to_response('plus/welcome.html', { 'activitylist': activitylist, })


# @login_required
# def auth_return(request):
#     print "auth return"
#     if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'], request.user):
#         return  HttpResponseBadRequest()
#     credential = FLOW.step2_exchange(request.REQUEST)
#     storage = Storage(CredentialsModel, 'id', request.user, 'credential')
#     storage.put(credential)
#     return HttpResponseRedirect("/")