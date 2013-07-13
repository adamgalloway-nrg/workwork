from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView
from django.http import HttpResponse
from models import Post
from models import Client, Comment, Customer, Employee, PaidTimeOff, Project, TaskDefinition, TimeEntry, WeekEntry
from forms import BaseTimeEntryFormSet, TimeEntryForm, EmployeeForm, ClientForm, CustomerForm, ProjectForm, TaskForm
import datetime
import calendar
import math
import decimal
import json
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
import collections
from django.forms.util import ErrorList





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
        return redirect('/?weekId=%s' % get_current_weekId())
    else:
        weekId = request.REQUEST['weekId']

        if math.isnan(int(weekId)):
            return redirect('/?weekId=%s' % get_current_weekId())

        saved_message = None

        sunDate, monDate, tueDate, wedDate, thuDate, friDate, satDate = get_week_dates(weekId)


        TimeEntryFormSet = formset_factory(TimeEntryForm,formset=BaseTimeEntryFormSet,extra=0)
        if request.method == 'POST':
            if 'open' in request.POST:
                week_entry, created = WeekEntry.objects.get_or_create(employee=employee.email,weekId=weekId,defaults={'complete':False})
                week_entry.complete = False
                week_entry.save()

                # redirect after post
                return redirect('/?weekId=%s&saved=%s' % (weekId, 'open'))


            time_entry_formset = TimeEntryFormSet(request.POST, request.FILES)
            if time_entry_formset.is_valid():
                # do something with the cleaned_data on the formsets.

                new_time_entries = []
                new_comments = []
                i = 0
                for form in time_entry_formset:

                    save_row = False

                    if form.cleaned_data['sundayHours'] > decimal.Decimal('0'):
                        save_row = True
                        new_time_entries.append(
                            TimeEntry(
                                date=sunDate,
                                taskDefinitionId=form.cleaned_data['taskDefinitionId'],
                                durationInHours=form.cleaned_data['sundayHours'],
                                rowId=i,
                                weekId=weekId,
                                employee=employee.email
                            )
                        )
                    if form.cleaned_data['mondayHours'] > decimal.Decimal('0'):
                        save_row = True
                        new_time_entries.append(
                            TimeEntry(
                                date=monDate,
                                taskDefinitionId=form.cleaned_data['taskDefinitionId'],
                                durationInHours=form.cleaned_data['mondayHours'],
                                rowId=i,
                                weekId=weekId,
                                employee=employee.email
                            )
                        )
                    if form.cleaned_data['tuesdayHours'] > decimal.Decimal('0'):
                        save_row = True
                        new_time_entries.append(
                            TimeEntry(
                                date=tueDate,
                                taskDefinitionId=form.cleaned_data['taskDefinitionId'],
                                durationInHours=form.cleaned_data['tuesdayHours'],
                                rowId=i,
                                weekId=weekId,
                                employee=employee.email
                            )
                        )
                    if form.cleaned_data['wednesdayHours'] > decimal.Decimal('0'):
                        save_row = True
                        new_time_entries.append(
                            TimeEntry(
                                date=wedDate,
                                taskDefinitionId=form.cleaned_data['taskDefinitionId'],
                                durationInHours=form.cleaned_data['wednesdayHours'],
                                rowId=i,
                                weekId=weekId,
                                employee=employee.email
                            )
                        )
                    if form.cleaned_data['thursdayHours'] > decimal.Decimal('0'):
                        save_row = True
                        new_time_entries.append(
                            TimeEntry(
                                date=thuDate,
                                taskDefinitionId=form.cleaned_data['taskDefinitionId'],
                                durationInHours=form.cleaned_data['thursdayHours'],
                                rowId=i,
                                weekId=weekId,
                                employee=employee.email
                            )
                        )
                    if form.cleaned_data['fridayHours'] > decimal.Decimal('0'):
                        save_row = True
                        new_time_entries.append(
                            TimeEntry(
                                date=friDate,
                                taskDefinitionId=form.cleaned_data['taskDefinitionId'],
                                durationInHours=form.cleaned_data['fridayHours'],
                                rowId=i,
                                weekId=weekId,
                                employee=employee.email
                            )
                        )
                    if form.cleaned_data['saturdayHours'] > decimal.Decimal('0'):
                        save_row = True
                        new_time_entries.append(
                            TimeEntry(
                                date=satDate,
                                taskDefinitionId=form.cleaned_data['taskDefinitionId'],
                                durationInHours=form.cleaned_data['saturdayHours'],
                                rowId=i,
                                weekId=weekId,
                                employee=employee.email
                            )
                        )

                    if save_row:
                        if form.cleaned_data['comment']:
                            new_comments.append(
                                Comment(employee=employee.email, weekId=weekId, rowId=i, text=form.cleaned_data['comment'])
                            )

                        i += 1

                print new_time_entries

                # remove time entries for this employee and weekId
                TimeEntry.objects(employee=employee.email, weekId=weekId).delete()
                # save new_time_entries
                if len(new_time_entries) > 0:
                    TimeEntry.objects.insert(new_time_entries)

                # remove comments for this employee and weekId
                Comment.objects(employee=employee.email, weekId=weekId).delete()
                # save new_comments
                if len(new_comments) > 0:
                    Comment.objects.insert(new_comments)

                # check if we are completing the week
                if 'complete' in request.POST:
                    week_entry, created = WeekEntry.objects.get_or_create(employee=employee.email,weekId=weekId,defaults={'complete':True})
                    week_entry.complete = True
                    week_entry.save()

                # redirect after post
                return redirect('/?weekId=%s&saved=%s' % (weekId, 'saved'))
        else:
            time_entries = TimeEntry.objects(employee=employee.email, weekId=weekId)
            comments = Comment.objects(employee=employee.email, weekId=weekId)

            tasks_map = get_tasks_map()

            time_entry_rows = {}
            for time_entry in time_entries:
                task_id = str(time_entry.taskDefinitionId)
                row_id = str(time_entry.rowId)

                if row_id not in time_entry_rows:
                    time_entry_rows[row_id] = {
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
                    time_entry_rows[row_id]['mondayHours'] += time_entry.durationInHours
                elif time_entry.date.weekday() == 1:
                    time_entry_rows[row_id]['tuesdayHours'] += time_entry.durationInHours
                elif time_entry.date.weekday() == 2:
                    time_entry_rows[row_id]['wednesdayHours'] += time_entry.durationInHours
                elif time_entry.date.weekday() == 3:
                    time_entry_rows[row_id]['thursdayHours'] += time_entry.durationInHours
                elif time_entry.date.weekday() == 4:
                    time_entry_rows[row_id]['fridayHours'] += time_entry.durationInHours
                elif time_entry.date.weekday() == 5:
                    time_entry_rows[row_id]['saturdayHours'] += time_entry.durationInHours
                elif time_entry.date.weekday() == 6:
                    time_entry_rows[row_id]['sundayHours'] += time_entry.durationInHours

            for comment in comments:
                row_id = str(comment.rowId)

                time_entry_rows[row_id]['comment'] = comment.text


            form_data = sorted(time_entry_rows.values(), key=lambda row: row['rowId'])

            time_entry_formset = TimeEntryFormSet(initial=form_data)


        is_complete = len(WeekEntry.objects(employee=employee.email,weekId=weekId,complete=True))


        return render_to_response('index.html', {
            'time_entry_formset': time_entry_formset,
            'weekId': weekId,
            'prev_weekId': get_prev_weekId(weekId),
            'next_weekId': get_next_weekId(weekId),
            'tasks_map': tasks_map,
            'is_complete': is_complete,
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
    employee = get_employee(request)
    if employee.admin != True:
        return redirect('/')

    if request.method == 'DELETE':
        customer_id = request.REQUEST['id']
        if len(Project.objects(customerId=customer_id)) > 0:
            return HttpResponse(status=400)
        else:
            Customer.objects.get(id=customer_id).delete()
            return HttpResponse(status=204)

    if request.method == 'PUT':
        try:
            request.method = "POST"
            request._load_post_and_files()
            request.method = "PUT"
        except AttributeError:
            request.META['REQUEST_METHOD'] = 'POST'
            request._load_post_and_files()
            request.META['REQUEST_METHOD'] = 'PUT'
            
        request.PUT = request.POST

        form = CustomerForm(request.PUT)
        if form.is_valid() and request.REQUEST['id']:
            # update item

            Customer.objects(id=request.REQUEST['id']).update_one(
                set__name=form.cleaned_data['name'],
                set__invoicingId=form.cleaned_data['invoicingId']
            )

            # update name on projects and tasks
            Project.objects(customerId=request.REQUEST['id']).update(set__customerName=form.cleaned_data['name'])
            TaskDefinition.objects(customerId=request.REQUEST['id']).update(set__customerName=form.cleaned_data['name'])

            # Always redirect after a POST
            return HttpResponse(status=204)
        else:
            print form.errors
            return HttpResponse(status=400)


    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            # create a new item
            Customer(
                name=form.cleaned_data['name'],
                invoicingId=form.cleaned_data['invoicingId']
            ).save()
            # Always redirect after a POST
            return redirect('/customer')

    else:
        # This the the first page load, display a blank form
        form = CustomerForm()

    params = {
        'customers': Customer.objects,
        'form': form
    }

    return render_to_response('customer.html', params, context_instance=RequestContext(request))

@login_required
def manage_clients(request):
    employee = get_employee(request)
    if employee.admin != True:
        return redirect('/')

    if request.method == 'DELETE':
        client_id = request.REQUEST['id']
        if len(Project.objects(clientId=client_id)) > 0:
            return HttpResponse(status=400)
        else:
            Client.objects.get(id=client_id).delete()
            return HttpResponse(status=204)

    if request.method == 'PUT':
        try:
            request.method = "POST"
            request._load_post_and_files()
            request.method = "PUT"
        except AttributeError:
            request.META['REQUEST_METHOD'] = 'POST'
            request._load_post_and_files()
            request.META['REQUEST_METHOD'] = 'PUT'
            
        request.PUT = request.POST

        form = ClientForm(request.PUT)
        if form.is_valid() and request.REQUEST['id']:
            # update item

            Client.objects(id=request.REQUEST['id']).update_one(set__name=form.cleaned_data['name'])

            # update name on projects and tasks
            Project.objects(clientId=request.REQUEST['id']).update(set__clientName=form.cleaned_data['name'])
            TaskDefinition.objects(clientId=request.REQUEST['id']).update(set__clientName=form.cleaned_data['name'])

            # Always redirect after a POST
            return HttpResponse(status=204)
        else:
            print form.errors
            return HttpResponse(status=400)


    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            # create a new item
            Client(name=form.cleaned_data['name']).save()
            # Always redirect after a POST
            return redirect('/client')

    else:
        # This the the first page load, display a blank form
        form = ClientForm()

    params = {
        'clients': Client.objects,
        'form': form
    }

    return render_to_response('client.html', params, context_instance=RequestContext(request))

@login_required
def manage_projects(request):
    employee = get_employee(request)
    if employee.admin != True:
        return redirect('/')

    if request.method == 'DELETE':
        project_id = request.REQUEST['id']
        if len(TaskDefinition.objects(projectId=project_id)) > 0:
            return HttpResponse(status=400)
        else:
            Project.objects.get(id=project_id).delete()
            return HttpResponse(status=204)

    if request.method == 'PUT':
        try:
            request.method = "POST"
            request._load_post_and_files()
            request.method = "PUT"
        except AttributeError:
            request.META['REQUEST_METHOD'] = 'POST'
            request._load_post_and_files()
            request.META['REQUEST_METHOD'] = 'PUT'
            
        request.PUT = request.POST

        form = ProjectForm(request.PUT)
        if form.is_valid() and request.REQUEST['id']:
            # update item
            customer_name = Customer.objects.get(id=form.cleaned_data['customerId']).name
            client_name = Client.objects.get(id=form.cleaned_data['clientId']).name

            Project.objects(id=request.REQUEST['id']).update_one(
                set__name=form.cleaned_data['name'],
                set__contract=form.cleaned_data['contract'],
                set__customerId=form.cleaned_data['customerId'],
                set__customerName=customer_name,
                set__clientId=form.cleaned_data['clientId'],
                set__clientName=client_name
            )

            # update project name, customer id/name, client id/name on task
            TaskDefinition.objects(projectId=request.REQUEST['id']).update(
                set__projectName=form.cleaned_data['name'],
                set__customerId=form.cleaned_data['customerId'],
                set__customerName=customer_name,
                set__clientId=form.cleaned_data['clientId'],
                set__clientName=client_name
            )


            # Always redirect after a POST
            return HttpResponse(status=204)
        else:
            print form.errors
            return HttpResponse(status=400)


    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            # create a new item
            customer_name = Customer.objects.get(id=form.cleaned_data['customerId']).name
            client_name = Client.objects.get(id=form.cleaned_data['clientId']).name
            Project(
                name=form.cleaned_data['name'],
                contract=form.cleaned_data['contract'],
                customerId=form.cleaned_data['customerId'],
                customerName=customer_name,
                clientId=form.cleaned_data['clientId'],
                clientName=client_name
            ).save()
            # Always redirect after a POST
            return redirect('/project')
        else:
            print form.errors

    else:
        # This the the first page load, display a blank form
        form = ProjectForm()

    params = {
        'projects_map': get_projects_map(),
        'clients': Client.objects.order_by('name'),
        'customers': Customer.objects.order_by('name'),
        'form': form
    }

    return render_to_response('project.html', params, context_instance=RequestContext(request))

@login_required
def manage_tasks(request):
    employee = get_employee(request)
    if employee.admin != True:
        return redirect('/')

    if request.method == 'DELETE':
        task_id = request.REQUEST['id']
        if len(TimeEntry.objects(taskDefinitionId=task_id)) > 0:
            return HttpResponse(status=400)
        else:
            TaskDefinition.objects.get(id=task_id).delete()
            return HttpResponse(status=204)

    if request.method == 'PUT':
        try:
            request.method = "POST"
            request._load_post_and_files()
            request.method = "PUT"
        except AttributeError:
            request.META['REQUEST_METHOD'] = 'POST'
            request._load_post_and_files()
            request.META['REQUEST_METHOD'] = 'PUT'
            
        request.PUT = request.POST

        form = TaskForm(request.PUT)
        if form.is_valid() and request.REQUEST['id']:
            # update item
            project = Project.objects.get(id=form.cleaned_data['projectId'])

            TaskDefinition.objects(id=request.REQUEST['id']).update_one(
                set__name=form.cleaned_data['name'],
                set__customerId=project.customerId,
                set__customerName=project.customerName,
                set__clientId=project.clientId,
                set__clientName=project.clientName,
                set__projectId=form.cleaned_data['projectId'],
                set__projectName=project.name,
                set__disabled=form.cleaned_data['disabled'],
                set__billable=form.cleaned_data['billable'],
                set__pto=form.cleaned_data['pto'],
                set__commentRequired=form.cleaned_data['commentRequired']
            )
            # Always redirect after a POST
            return HttpResponse(status=204)
        else:
            print form.errors
            return HttpResponse(status=400)


    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # create a new item
            project = Project.objects.get(id=form.cleaned_data['projectId'])

            TaskDefinition(
                name=form.cleaned_data['name'],
                customerId=project.customerId,
                customerName=project.customerName,
                clientId=project.clientId,
                clientName=project.clientName,
                projectId=form.cleaned_data['projectId'],
                projectName=project.name,
                disabled=form.cleaned_data['disabled'],
                billable=form.cleaned_data['billable'],
                pto=form.cleaned_data['pto'],
                commentRequired=form.cleaned_data['commentRequired']
            ).save()
            # Always redirect after a POST
            return redirect('/task')
        else:
            print form.errors

    else:
        # This the the first page load, display a blank form
        form = TaskForm()

    params = {
        'projects_map': get_projects_map(),
        'projects_tasks_map': get_projects_tasks_map(),
        'form': form
    }

    return render_to_response('task.html', params, context_instance=RequestContext(request))

@login_required
def manage_employees(request):
    employee = get_employee(request)
    if employee.admin != True:
        return redirect('/')

    if request.method == 'DELETE':
        employee_id = request.REQUEST['id']
        employee = Employee.objects.get(id= employee_id)

        if len(TimeEntry.objects(employee=employee.email)) > 0:
            return HttpResponse(status=400)
        else:
            Employee.objects.get(id=employee_id).delete()
            return HttpResponse(status=204)


    if request.method == 'PUT':
        try:
            request.method = "POST"
            request._load_post_and_files()
            request.method = "PUT"
        except AttributeError:
            request.META['REQUEST_METHOD'] = 'POST'
            request._load_post_and_files()
            request.META['REQUEST_METHOD'] = 'PUT'
            
        request.PUT = request.POST

        form = EmployeeForm(request.PUT)
        if form.is_valid() and request.REQUEST['id']:
            # update item

            Employee.objects(id=request.REQUEST['id']).update_one(
                set__name=form.cleaned_data['name'],
                set__active=form.cleaned_data['active'],
                set__admin=form.cleaned_data['admin'],
                set__startDate=form.cleaned_data['startDate']
            )
            # Always redirect after a POST
            return HttpResponse(status=204)
        else:
            print form.errors
            return HttpResponse(status=400)


    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            # create a new item
            try:
                Employee(
                    email=form.cleaned_data['email'],
                    name=form.cleaned_data['name'],
                    active=form.cleaned_data['active'],
                    admin=form.cleaned_data['admin'],
                    startDate=form.cleaned_data['startDate']
                ).save()
                # Always redirect after a POST
                return redirect('/employee')
            except Exception, e:
                errors = form._errors.setdefault('email', ErrorList())
                errors.append(u"Duplicate Address")

        else:
            print form.errors

    else:
        # This the the first page load, display a blank form
        form = EmployeeForm()

    params = {
        'employees': Employee.objects,
        'form': form
    }

    return render_to_response('employee.html', params, context_instance=RequestContext(request))

@login_required
def manage_pto(request):
    employee = get_employee(request)
    if employee.admin != True:
        return redirect('/')

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
                PaidTimeOff(
                    id=pto['id'],
                    employee=pto['employee'],
                    hours=pto['hours'],
                    year=year,
                    taskDefinitionId=pto['taskDefinitionId']
                ).save()
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