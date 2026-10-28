from django import forms
from app_009_media.models import *

# crearte this class for date input field
class DateInput(forms.DateInput):
    input_type = 'date'

class imageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    date = forms.DateField(widget=DateInput(attrs={'class': 'form-control'}))

    class Meta:
        model = images
        fields = ['image', 'date']