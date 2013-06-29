from mongoengine import *
from timetracker.settings import DBNAME

# Create your models here.

connect(DBNAME)

class Post(Document):
    title = StringField(max_length=120, required=True)
    content = StringField(max_length=500, required=True)
    last_update = DateTimeField(required=True)

class Client(Document):
	#name,id
	name = StringField(max_length=120, required=True)
    

class Comment(Document):
	#employee,text,rowId,id,weekId
	employee = EmailField(max_length=120, required=True)
	text = StringField(max_length=500, required=True)
	rowId = IntField(required=True)
	weekId = LongField(required=True)


class Customer(Document):
	#invoicingId,name,id
	name = StringField(max_length=120, required=True)
	invoicingId = StringField(max_length=120)

class Employee(Document):
	#active,admin,name,id,startDate
	key = EmailField(max_length=120, required=True, primary_key=True)
	name = StringField(max_length=120, required=True)
	active = BooleanField(required=True, default=True)
	admin = BooleanField(required=True, default=False)
	startDate = DateTimeField(required=True)

class PaidTimeOff(Document):
	meta = {'collection': 'paid_time_off'}
	#employee,hours,year,id,taskDefinitionId
	employee = EmailField(max_length=120, required=True)
	year = LongField(required=True)
	taskDefinitionId = ObjectIdField(required=True)
	hours = DecimalField(min_value=0,force_string=True,required=True)

class Project(Document):
	#customerName,contract,clientId,id,customerId,clientName,name
	name = StringField(max_length=120, required=True)
	customerId = ObjectIdField(required=True)
	customerName = StringField(max_length=120, required=True)
	clientId = ObjectIdField(required=False)
	clientName = StringField(max_length=120, required=False)
	contract = StringField(max_length=120, required=False)

class TaskDefinition(Document):
	meta = {'collection': 'task_definition'}
	#pto,customerName,projectId,projectName,clientId,name,disabled,id,billable,active,customerId,clientName,commentRequired
	name = StringField(max_length=120, required=True)
	customerId = ObjectIdField(required=True)
	customerName = StringField(max_length=120, required=True)
	clientId = ObjectIdField(required=False)
	clientName = StringField(max_length=120, required=False)
	projectId = ObjectIdField(required=True)
	projectName = StringField(max_length=120, required=True)
	disabled = BooleanField(required=True, default=True)
	billable = BooleanField(required=True, default=False)
	pto = BooleanField(required=True, default=False)
	commentRequired = BooleanField(required=True, default=False)

class TimeEntry(Document):
	meta = {'collection': 'time_entry'}
	#rowId,weekId,employee,durationInHours,id,date,taskDefinitionId
	employee = EmailField(max_length=120, required=True)
	rowId = IntField(required=True)
	weekId = LongField(required=True)
	taskDefinitionId = ObjectIdField(required=True)
	date = DateTimeField(required=True)
	durationInHours = DecimalField(min_value=0,force_string=True,required=True)

class WeekEntry(Document):
	meta = {'collection': 'week_entry'}
	#employee,complete,id,weekId
	employee = EmailField(max_length=120, required=True)
	weekId = LongField(required=True)
	complete = BooleanField(required=True, default=False)