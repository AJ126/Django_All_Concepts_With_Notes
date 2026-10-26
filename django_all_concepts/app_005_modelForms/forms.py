from django import forms
from app_005_modelForms.models import *

class demoDataForm(forms.ModelForm):
    class Meta:
        model = demoData
        fields = '__all__'

class addWidgetOnForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter phone number',
        'min': 1000000000,
        'max': 9999999999
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = demoData
        fields = ['name', 'phone', 'city', 'address']

# crearte this class for date input field
class DateInput(forms.DateInput):
    input_type = 'date'

class dateModelForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    date = forms.DateField(widget=DateInput(attrs={'class': 'form-control'}))

    class Meta:
        model = dateModel
        fields = ['name', 'date']