from django.shortcuts import render
from app_006_advance_template.models import *

# Create your views here.
def show_template(request):
    data = userInfo.objects.all()
    return render(request, 'app_006_advance_template/adv_temp.html', {'data': data})

# custom filter
def show_custom_template(request):
    data = userInfo.objects.all()
    return render(request, 'app_006_advance_template/custom_temp.html', {'data': data})