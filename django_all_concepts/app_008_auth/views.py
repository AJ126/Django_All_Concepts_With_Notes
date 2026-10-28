from django.shortcuts import render, redirect
from app_008_auth.forms import *

# Create your views here.
def register(request):
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