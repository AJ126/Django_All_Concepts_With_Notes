from django.shortcuts import render
from app_007_session.forms import *
import datetime

# Create your views here.

def set_cookie(request):
    request.session.set_test_cookie()
    data = 'cokie is set'
    return render(request, 'app_007_session/check_cookie.html', {'data': data}) 

# check & delete cookie
def check_cookie(request):
    if request.session.test_cookie_worked():
        data = 'cookie is working perfectly'
        request.session.delete_test_cookie()
    else:
        data = 'cookie is not working'
    return render(request, 'app_007_session/check_cookie.html', {'data': data})

# count check using cookie
def coount_view(request):
    if 'count' in  request.COOKIES:
        newcount = int(request.COOKIES['count']) + 1
    else:
        newcount = 1
    response = render(request, 'app_007_session/page_load_count.html', {'count': newcount})
    response.set_cookie('count', newcount)
    return response

# below code for session management with cookie for loagin form

def show_form(request):
    form = loginForm()
    return render(request, 'app_007_session/form.html', {'form': form})

# date time view
def show_datetime(request):
    name = request.GET['name']
    response = render(request, 'app_007_session/datetime.html', {'name': name})
    response.set_cookie('name', name)
    return response

def show_form_result(request):
    name = request.COOKIES['name']
    date = datetime.datetime.now()
    data = {'name': name, 'date': date}
    return render(request, 'app_007_session/form_result.html', {'data': data})

# enter data of bf and gf
def name_view(request):
    return render(request,'app_007_session/name.html')

def age_view(request):
    name = request.GET['name']
    response = render(request,'app_007_session/age_view.html',{'name':name})
    response.set_cookie('name',name)
    return response

def gf_view(request):
    age = request.GET['age']
    name = request.COOKIES['name']
    response = render(request,'app_007_session/gf_view.html',{'name':name})
    response.set_cookie('age',age)
    return response

def result_view(request):
    name = request.COOKIES['name']
    age = request.COOKIES['age']
    gf = request.GET['gf']
    response = render(request,'app_007_session/result.html',{'name':name,'age':age,'gf':gf})
    response.set_cookie('gf',gf)
    return response

def thankyouPage(request):
    name = request.COOKIES['name']
    age = request.COOKIES['age']
    gf = request.COOKIES['gf']
    return render(request, 'app_007_session/thankyouPage.html', {'name':name,'age':age,'gf':gf})

# session using session database
def page_count(request):
    data = 'session data come from databse session table'
    count = request.session.get('count',0)
    new_count = count +1
    request.session['count'] = new_count
    print("expiry age (time)..............",request.session.get_expiry_age())
    print("expiry date..............",request.session.get_expiry_date())
    return render(request,'app_007_session/count.html',{'count':new_count,'data':data})
