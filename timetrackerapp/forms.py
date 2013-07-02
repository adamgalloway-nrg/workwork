from django import forms
from django.forms.formsets import formset_factory
from bson import ObjectId
from models import Client, Comment, Customer, Employee, PaidTimeOff, Project, TaskDefinition, TimeEntry, WeekEntry

class TimeEntryForm(forms.Form):
    taskDefinitionId = forms.CharField(widget=forms.HiddenInput())
    rowId = forms.IntegerField(widget=forms.HiddenInput(),required=False)
    sundayHours = forms.DecimalField(max_value=24.0, min_value=0.0, decimal_places=2)
    mondayHours = forms.DecimalField(max_value=24.0, min_value=0.0, decimal_places=2)
    tuesdayHours = forms.DecimalField(max_value=24.0, min_value=0.0, decimal_places=2)
    wednesdayHours = forms.DecimalField(max_value=24.0, min_value=0.0, decimal_places=2)
    thursdayHours = forms.DecimalField(max_value=24.0, min_value=0.0, decimal_places=2)
    fridayHours = forms.DecimalField(max_value=24.0, min_value=0.0, decimal_places=2)
    saturdayHours = forms.DecimalField(max_value=24.0, min_value=0.0, decimal_places=2)
    comment = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Comment'}), required=False, max_length=500)

    def __init__(self, *args, **kwargs):
        super(TimeEntryForm, self).__init__(*args, **kwargs)

        # if you want to do it to all of them
        for field in self.fields.values():
            field.error_messages = {'required':'Required'.format(fieldname=field.label)}

        self.fields['taskDefinitionId'].error_messages = {'required': 'Task Definition Id is required.'}


    def validate_required_field(self, cleaned_data, field_name, message="Comments are required"):
        if(field_name in cleaned_data and cleaned_data[field_name] is None):
            self._errors[field_name] = self.error_class([message])
            del cleaned_data[field_name]

    def clean(self):
        cleaned_data = super(TimeEntryForm, self).clean()
        print cleaned_data
        task_id_string = cleaned_data['taskDefinitionId']
        task = TaskDefinition.objects.get(id=ObjectId(task_id_string))
        if task.commentRequired:
            self.validate_required_field(cleaned_data, 'comment')