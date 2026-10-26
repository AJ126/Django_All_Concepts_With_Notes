from django.shortcuts import render
from app_003_models.models import *

# Create your views here.
def show_model_data(request):
    data = testData.objects.all()
    return render(request, 'app_003_models/show_data.html', {'data': data})