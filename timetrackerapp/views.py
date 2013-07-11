from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView
from django.http import HttpResponse
from models import Post
from models import Client, Comment, Customer, Employee, PaidTimeOff, Project, TaskDefinition, TimeEntry, WeekEntry
from forms import TimeEntryForm
import datetime
import calendar
import math
import decimal
import json
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
import collections





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


def get_week_dates(weekId):
    week_id_str = str(weekId)
    year = int(week_id_str[:4])
    month = int(week_id_str[4:6])
    week = int(week_id_str[6:7])

    cal = calendar.Calendar(calendar.SUNDAY)

    monthcalendar = cal.monthdatescalendar(year, month)
    return  monthcalendar[week - 1]


def get_range_title(startDate, endDate):
    if startDate.year != endDate.year:
        return startDate.strftime("%b %-d, %Y") + ' - ' + endDate.strftime("%b %-d, %Y")
    elif startDate.month != endDate.month:
        return startDate.strftime("%b %-d") + ' - ' + endDate.strftime("%b %-d, %Y")
    else:
        return startDate.strftime("%b %-d") + ' - ' + endDate.strftime("%-d, %Y")



def get_employee(request):
    if 'employee' not in request.session:
        request.session['employee'] = Employee.objects.get(email=request.user.email)
    return request.session['employee']



def get_task_description(task):
    if task.customerName.strip() == task.clientName.strip():
        return task.customerName + ' - ' + task.projectName
    else:
        return task.customerName + ' - ' + task.clientName + ' - ' + task.projectName

def get_tasks_map():
    tasks_map = {}
    for task in TaskDefinition.objects.order_by('name'):
        task_group = get_task_description(task)
        if task_group not in tasks_map:
            tasks_map[task_group] = []
        tasks_map[task_group].append(task)

    # sort keys alphabetically
    return collections.OrderedDict(sorted(tasks_map.items()))

def get_projects_map():
    projects_map = {}
    for project in Project.objects.order_by('name'):
        project_group = project.customerName
        if project.customerName.strip() != project.clientName.strip():
            project_group += ' - ' + project.clientName

        if project_group not in projects_map:
            projects_map[project_group] = []
        projects_map[project_group].append(project)

    # sort keys alphabetically
    return collections.OrderedDict(sorted(projects_map.items()))

def get_projects_tasks_map():
    projects_map = {}
    for task in TaskDefinition.objects.order_by('name'):
        project_group = task.customerName
        if task.customerName.strip() != task.clientName.strip():
            project_group += ' - ' + task.clientName

        if project_group not in projects_map:
            projects_map[project_group] = {}

        if task.projectName not in projects_map[project_group]:
            projects_map[project_group][task.projectName] = []

        projects_map[project_group][task.projectName].append(task)

    # sort keys alphabetically
    return collections.OrderedDict(sorted(projects_map.items()))

def get_pto_map(year):
    pto_map = {}

    task_map = {}
    for task in TaskDefinition.objects(pto=True):
        task_map[task.id] = task

    for employee in Employee.objects.order_by('email'):
        email = employee.email
        if employee not in pto_map:
            pto_map[employee] = []

        for task_id in task_map.keys():
            pto, created = PaidTimeOff.objects.get_or_create(year=year,employee=email,taskDefinitionId=task_id,defaults={'hours': 0})
            item = {
                'pto': pto,
                'task': task_map[task_id]
            }

            pto_map[employee].append(item)

    return collections.OrderedDict(sorted(pto_map.items(), key=lambda emp: emp[0].name));


@login_required
def index(request):
    employee = get_employee(request)

    if 'weekId' not in request.REQUEST or not request.REQUEST['weekId']:
        return redirect('/?weekId=' + get_current_weekId())
    else:
        weekId = request.REQUEST['weekId']

        if math.isnan(int(weekId)):
            return redirect('/?weekId=' + get_current_weekId())

        sunDate, monDate, tueDate, wedDate, thuDate, friDate, satDate = get_week_dates(weekId)


        time_entries = TimeEntry.objects(employee=employee.email, weekId=weekId)
        comments = Comment.objects(employee=employee.email, weekId=weekId)

        tasks_map = get_tasks_map()

        time_entry_row = {}
        for time_entry in time_entries:
            task_id = str(time_entry.taskDefinitionId)
            row_id = str(time_entry.rowId)

            if row_id not in time_entry_row:
                time_entry_row[row_id] = {
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
                time_entry_row[row_id]['mondayHours'] += time_entry.durationInHours
            elif time_entry.date.weekday() == 1:
                time_entry_row[row_id]['tuesdayHours'] += time_entry.durationInHours
            elif time_entry.date.weekday() == 2:
                time_entry_row[row_id]['wednesdayHours'] += time_entry.durationInHours
            elif time_entry.date.weekday() == 3:
                time_entry_row[row_id]['thursdayHours'] += time_entry.durationInHours
            elif time_entry.date.weekday() == 4:
                time_entry_row[row_id]['fridayHours'] += time_entry.durationInHours
            elif time_entry.date.weekday() == 5:
                time_entry_row[row_id]['saturdayHours'] += time_entry.durationInHours
            elif time_entry.date.weekday() == 6:
                time_entry_row[row_id]['sundayHours'] += time_entry.durationInHours

        for comment in comments:
            row_id = str(comment.rowId)

            time_entry_row[row_id]['comment'] = comment.text


        form_data = []
        for time_entry_row_id in time_entry_row:
            # get data without keys
            form_data.append(time_entry_row[time_entry_row_id])


        TimeEntryFormSet = formset_factory(TimeEntryForm,extra=0)
        if request.method == 'POST':
            time_entry_formset = TimeEntryFormSet(request.POST, request.FILES)
            if time_entry_formset.is_valid():
                # do something with the cleaned_data on the formsets.
                #print str(time_entry_formset)


                pass
        else:
            time_entry_formset = TimeEntryFormSet(initial=form_data)


        return render_to_response('index.html', {
            'time_entry_formset': time_entry_formset,
            'weekId': weekId,
            'prev_weekId': get_prev_weekId(weekId),
            'next_weekId': get_next_weekId(weekId),
            'tasks_map': tasks_map,
            'sunTitle': sunDate.strftime("%-m/%-d"),
            'monTitle': monDate.strftime("%-m/%-d"),
            'tueTitle': tueDate.strftime("%-m/%-d"),
            'wedTitle': wedDate.strftime("%-m/%-d"),
            'thuTitle': thuDate.strftime("%-m/%-d"),
            'friTitle': friDate.strftime("%-m/%-d"),
            'satTitle': satDate.strftime("%-m/%-d"),
            'rangeTitle': get_range_title(sunDate, satDate)
        }, context_instance=RequestContext(request))



@login_required
def manage_customers(request):

    return render_to_response('customer.html', {'customers': Customer.objects}, context_instance=RequestContext(request))

@login_required
def manage_clients(request):

    return render_to_response('client.html', {'clients': Client.objects}, context_instance=RequestContext(request))

@login_required
def manage_projects(request):

    params = {
        'projects_map': get_projects_map(),
        'clients': Client.objects.order_by('name'),
        'customers': Customer.objects.order_by('name')
    }

    return render_to_response('project.html', params, context_instance=RequestContext(request))

@login_required
def manage_tasks(request):

    params = {
        'projects_map': get_projects_map(),
        'projects_tasks_map' : get_projects_tasks_map()
    }

    return render_to_response('task.html', params, context_instance=RequestContext(request))

@login_required
def manage_employees(request):

    return render_to_response('employee.html', {'employees': Employee.objects}, context_instance=RequestContext(request))

@login_required
def manage_pto(request):

    if 'year' not in request.REQUEST or not request.REQUEST['year']:
        date = datetime.datetime.now()
        return redirect('/pto/?year=' + str(date.year))
    else:
        year = request.REQUEST['year']

        if math.isnan(int(year)):
            date = datetime.datetime.now()
            return redirect('/pto/?year=' + str(date.year))

        if request.is_ajax() and request.method == 'POST':
            ptos = json.loads(request.body)
            print str(ptos)
            for pto in ptos:
                PaidTimeOff(id=pto['id'],employee=pto['employee'],hours=pto['hours'],year=year,taskDefinitionId=pto['taskDefinitionId']).save()
            return HttpResponse(status=204)


        params = {
            'employees': Employee.objects,
            'pto_map': get_pto_map(year),
            'year': int(year),
            'prev_year': int(year) - 1,
            'next_year': int(year) + 1
        }

        return render_to_response('pto.html', params, context_instance=RequestContext(request))


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
#     FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_row_id, request.user)
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
#     if not xsrfutil.validate_token(settings.SECRET_row_id, request.REQUEST['state'], request.user):
#         return  HttpResponseBadRequest()
#     credential = FLOW.step2_exchange(request.REQUEST)
#     storage = Storage(CredentialsModel, 'id', request.user, 'credential')
#     storage.put(credential)
#     return HttpResponseRedirect("/")