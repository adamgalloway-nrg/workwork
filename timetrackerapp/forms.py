from django import forms
from django.forms.formsets import BaseFormSet
from django.forms.formsets import formset_factory
from bson import ObjectId
from models import Client, Comment, Customer, Employee, PaidTimeOff, Project, TaskDefinition, TimeEntry, WeekEntry
import decimal

class BaseTimeEntryFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return

        sunTotal = decimal.Decimal('0')
        monTotal = decimal.Decimal('0')
        tueTotal = decimal.Decimal('0')
        wedTotal = decimal.Decimal('0')
        thuTotal = decimal.Decimal('0')
        friTotal = decimal.Decimal('0')
        satTotal = decimal.Decimal('0')

        for form in self.forms:
            # add up hours for each day
            sunTotal += form.cleaned_data['sundayHours']
            monTotal += form.cleaned_data['mondayHours']
            tueTotal += form.cleaned_data['tuesdayHours']
            wedTotal += form.cleaned_data['wednesdayHours']
            thuTotal += form.cleaned_data['thursdayHours']
            friTotal += form.cleaned_data['fridayHours']
            satTotal += form.cleaned_data['saturdayHours']

        if sunTotal > decimal.Decimal('24'):
            raise forms.ValidationError("Too many hours for Sunday")
        if monTotal > decimal.Decimal('24'):
            raise forms.ValidationError("Too many hours for Monday")
        if tueTotal > decimal.Decimal('24'):
            raise forms.ValidationError("Too many hours for Tuesday")
        if wedTotal > decimal.Decimal('24'):
            raise forms.ValidationError("Too many hours for Wednesday")
        if thuTotal > decimal.Decimal('24'):
            raise forms.ValidationError("Too many hours for Thursday")
        if friTotal > decimal.Decimal('24'):
            raise forms.ValidationError("Too many hours for Friday")
        if satTotal > decimal.Decimal('24'):
            raise forms.ValidationError("Too many hours for Saturday")



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

        task_id_string = cleaned_data['taskDefinitionId']

        task = TaskDefinition.objects.get(id=ObjectId(task_id_string))
        if task.commentRequired:
            self.validate_required_field(cleaned_data, 'comment')

        return cleaned_data


class EmployeeForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Enter an email address','required':'required'}), required=True, max_length=120)
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter a name','required':'required'}), required=True, max_length=120)
    active = forms.BooleanField(required=False)
    admin = forms.BooleanField(required=False)
    startDate = forms.DateField(widget=forms.DateInput(format="%m/%d/%Y",attrs={'placeholder':'mm/dd/yyyy','required':'required'}), required=True)


class ClientForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter a name','required':'required'}), required=True, max_length=120)


class CustomerForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter a name','required':'required'}), required=True, max_length=120)
    invoicingId = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter an invoicing id'}), required=False, max_length=120)


class ProjectForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter a name','required':'required'}), required=True, max_length=120)
    contract = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter a contract name or number'}), required=False, max_length=120)
    customerId = forms.CharField(required=True, max_length=120)
    clientId = forms.CharField(required=True, max_length=120)


class TaskForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter a name','required':'required'}), required=True, max_length=120)
    projectId = forms.CharField(required=True, max_length=120)
    disabled = forms.BooleanField(required=False)
    billable = forms.BooleanField(required=False)
    pto = forms.BooleanField(required=False)
    commentRequired = forms.BooleanField(required=False)

