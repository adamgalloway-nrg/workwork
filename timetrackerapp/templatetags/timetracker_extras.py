from django import template
from bson import ObjectId
from timetrackerapp.models import Client, Comment, Customer, Employee, PaidTimeOff, Project, TaskDefinition, TimeEntry, WeekEntry

register = template.Library()

@register.tag(name="get_task_name")
def do_get_task_name(parser, token):
	tag_name, var_name = token.split_contents()
	return TaskNameNode(var_name)

class TaskNameNode(template.Node):
	def __init__(self, task_id):
		self.task_id = template.Variable(task_id)
	def render(self, context):
		try:
			task_id_string = self.task_id.resolve(context)
			task = TaskDefinition.objects.get(id=ObjectId(task_id_string))
			return task.name
		except template.VariableDoesNotExist:
			return ''


@register.tag(name="get_task_desc")
def do_get_task_desc(parser, token):
	tag_name, var_name = token.split_contents()
	return TaskDescriptionNode(var_name)

class TaskDescriptionNode(template.Node):
	def __init__(self, task_id):
		self.task_id = template.Variable(task_id)
	def render(self, context):
		try:
			task_id_string = self.task_id.resolve(context)
			task = TaskDefinition.objects.get(id=ObjectId(task_id_string))
			if task.customerName.strip() == task.clientName.strip():
				return task.customerName + ' - ' + task.projectName
			else:
				return task.customerName + ' - ' + task.clientName + ' - ' + task.projectName
		except template.VariableDoesNotExist:
			return ''
