from django.shortcuts import render
from app_004_forms.forms import *

# Create your views here.
def show_form(request):
    form = testForm()
    if request.method == 'POST':
        form = testForm(request.POST)
        if form.is_valid():
            print('name of user: ', form.cleaned_data['name'])
            print('address of user: ', form.cleaned_data['address'])
    return render(request, 'app_004_forms/form.html', {'form': form})

def validation_form(request):
    if request.method == 'POST':
        form = validationForm(request.POST)
        if form.is_valid():
            print('form')
    else:
        form = validationForm()
    return render(request, 'app_004_forms/form.html', {'form': form})

def clean_form(request):
    if request.method == 'POST':
        form = validationForm(request.POST)
        if form.is_valid():
            print('form')
    else:
        form = validationForm()
    return render(request, 'app_004_forms/form.html', {'form': form})