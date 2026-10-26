from django.shortcuts import render
import datetime

# Create your views here.
def show_template(request):
    return render(request, 'app_002_template/first.html')

def show_dynamic_data(request):
    s = 'Har har mahadev'
    date = datetime.datetime.now().strftime("%d/%m/%y")
    time = datetime.datetime.now().strftime("%I:%M:%p")
    data = {'name': s, 'date': date, 'time': time}
    return render(request, 'app_002_template/dynaimc_data.html', {'data': data})

def show_img(request):
    data = 'show image'
    return render(request, 'app_002_template/show_img.html', {'data':data})