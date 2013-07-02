from django import forms
from django.forms.formsets import formset_factory

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
    #sender = forms.EmailField()
    #cc_myself = forms.BooleanField(required=False)