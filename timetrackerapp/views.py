from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Post
from models import Client, Comment, Customer, Employee, PaidTimeOff, Project, TaskDefinition, TimeEntry, WeekEntry
import datetime

from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    if request.method == 'POST':
        # save new post
        title = request.POST['title']
        content = request.POST['content']

        post = Post(title=title)
        post.last_update = datetime.datetime.now() 
        post.content = content
        post.save()

    # Get all posts from DB
    posts = Post.objects 
    return render_to_response('index.html', {'Posts': posts}, context_instance=RequestContext(request))


def update(request):
    id = eval("request." + request.method + "['id']")
    post = Post.objects(id=id)[0]
    
    if request.method == 'POST':
        # update field values and save to mongo
        post.title = request.POST['title']
        post.last_update = datetime.datetime.now() 
        post.content = request.POST['content']
        post.save()
        template = 'index.html'
        params = {'Posts': Post.objects} 

    elif request.method == 'GET':
        template = 'update.html'
        params = {'post':post}
   
    return render_to_response(template, params, context_instance=RequestContext(request))
                              

def delete(request):
    id = eval("request." + request.method + "['id']")

    if request.method == 'POST':
        post = Post.objects(id=id)[0]
        post.delete() 
        template = 'index.html'
        params = {'Posts': Post.objects} 
    elif request.method == 'GET':
        template = 'delete.html'
        params = { 'id': id } 

    return render_to_response(template, params, context_instance=RequestContext(request))

def manage_customers(request):

    return render_to_response('customer.html', {'customers': Customer.objects}, context_instance=RequestContext(request))
    # response_data['result'] = 'data'
    # response_data['message'] = 'some other data'
    # return HttpResponse(json.dumps(response_data), mimetype="application/json")

def manage_clients(request):

    return render_to_response('client.html', {'clients': Client.objects}, context_instance=RequestContext(request))

def manage_projects(request):

    return render_to_response('project.html', {'projects': Project.objects}, context_instance=RequestContext(request))

def manage_tasks(request):

    return render_to_response('task.html', {'tasks': TaskDefinition.objects}, context_instance=RequestContext(request))

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