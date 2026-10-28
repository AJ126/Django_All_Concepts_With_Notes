from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from app_008_auth.forms import *

# Create your views here.
def register_default(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            return redirect('home')
    else:
        form = UserForm()
    return render(request, 'app_008_auth/register.html', {'form': form})

# create a custom login, register and logout
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'User is not found')
            return redirect('login')
    return render(request, 'app_008_auth/login.html')

def register(request):
    if request.method=='POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.error(request,'username is already taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request,'email is already taken')
                return redirect('register')
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password1)
                user.save()
                messages.success(request, 'User is created successfully.')
                return redirect('login')
        else:
            messages.error(request,'password is not matched')
            return redirect('register')
        return redirect('/')
    return render(request,'app_008_auth/register_form.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

@login_required
def login_required(request):
    return render(request,'app_008_auth/login_required.html')
