from django.shortcuts import render, redirect
from app_005_modelForms.models import *
from app_005_modelForms.forms import *

# Create your views here.
def form_save(request):
    if request.method == 'POST':
        form = demoDataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = demoDataForm()
    return render(request, 'app_005_modelForms/form.html', {'form': form})

# show customer widget
def formWidget(request):
    if request.method == 'POST':
        form = addWidgetOnForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = addWidgetOnForm()
    return render(request, 'app_005_modelForms/form.html', {'form': form})

# show customer widget with date field
def dateFormWidget(request):
    if request.method == 'POST':
        form = dateModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = dateModelForm()
    return render(request, 'app_005_modelForms/form.html', {'form': form})