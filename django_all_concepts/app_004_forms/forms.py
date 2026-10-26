from django import forms
from django.core import validators

class testForm(forms.Form):
    name = forms.CharField()
    address = forms.CharField()

class validationForm(forms.Form):
    name = forms.CharField()
    phone = forms.IntegerField()
    address = forms.CharField(widget=forms.Textarea, validators=[validators.MaxLengthValidator(50)])

    # check name
    def clean_name(self):
        inputname = self.cleaned_data['name']
        if len(inputname) <=3:
            raise forms.ValidationError('The minimus characters for name is 4')
        return inputname

class cleanValidationForm(forms.Form):
    name = forms.CharField()
    phone = forms.IntegerField()
    address = forms.CharField(widget=forms.Textarea)

    def clean(self):
        form_data = super().clean()
        name = form_data['name']
        if len(name) <=3:
            raise forms.ValidationError('The minimus characters for name is 4')
        address = form_data['address']
        if len(address) > 50:
            raise forms.ValidationError('Ensure this value has at most 50 characters')


