from tastypie_mongoengine import resources
from models import Client, Comment, Customer, Employee, PaidTimeOff, Project, TaskDefinition, TimeEntry, WeekEntry

class ClientResource(resources.MongoEngineResource):
    class Meta:
        queryset = Client.objects.all()
        resource_name = 'client'

class CustomerResource(resources.MongoEngineResource):
    class Meta:
        queryset = Customer.objects.all()
        resource_name = 'customer'

class ProjectResource(resources.MongoEngineResource):
    class Meta:
        queryset = Project.objects.all()
        resource_name = 'project'

class PaidTimeOffResource(resources.MongoEngineResource):
    class Meta:
        queryset = PaidTimeOff.objects.all()
        resource_name = 'paid-time-off'

class EmployeeResource(resources.MongoEngineResource):
    class Meta:
        queryset = Employee.objects.all()
        resource_name = 'employee'

class CommentResource(resources.MongoEngineResource):
    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comment'

class TaskDefinitionResource(resources.MongoEngineResource):
    class Meta:
        queryset = TaskDefinition.objects.all()
        resource_name = 'task-definition'

class TimeEntryResource(resources.MongoEngineResource):
    class Meta:
        queryset = TimeEntry.objects.all()
        resource_name = 'time-entry'

class WeekEntryResource(resources.MongoEngineResource):
    class Meta:
        queryset = WeekEntry.objects.all()
        resource_name = 'week-entry'