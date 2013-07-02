from django import forms
from django.forms.formsets import formset_factory
from bson import ObjectId
from models import Client, Comment, Customer, Employee, PaidTimeOff, Project, TaskDefinition, TimeEntry, WeekEntry

class TimeEntryForm(forms.Form):
    taskDefinitionId = forms.CharField(widget=forms.HiddenInput())
    rowId = forms.IntegerField(widget=forms.HiddenInput())
    sundayHours = forms.DecimalField(required=False,max_value=24.0, min_value=0.0, decimal_places=2)
    mondayHours = forms.DecimalField(required=False,max_value=24.0, min_value=0.0, decimal_places=2)
    tuesdayHours = forms.DecimalField(required=False,max_value=24.0, min_value=0.0, decimal_places=2)
    wednesdayHours = forms.DecimalField(required=False,max_value=24.0, min_value=0.0, decimal_places=2)
    thursdayHours = forms.DecimalField(required=False,max_value=24.0, min_value=0.0, decimal_places=2)
    fridayHours = forms.DecimalField(required=False,max_value=24.0, min_value=0.0, decimal_places=2)
    saturdayHours = forms.DecimalField(required=False,max_value=24.0, min_value=0.0, decimal_places=2)
    comment = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Comment'}), max_length=500)

    def validate_required_field(self, cleaned_data, field_name, message="Comments are required"):
        if(field_name in cleaned_data and cleaned_data[field_name] is None):
            self._errors[field_name] = self.error_class([message])
            del cleaned_data[field_name]

    def clean(self):
        cleaned_data = super(TimeEntryForm, self).clean()
        task_id_string = cleaned_data['taskDefinitionId']
        task = TaskDefinition.objects.get(id=ObjectId(task_id_string))
        if task.commentRequired:
            self.validate_required_field(cleaned_data, 'comment')