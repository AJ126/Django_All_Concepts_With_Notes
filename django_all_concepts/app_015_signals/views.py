from django.shortcuts import render, redirect
from app_015_signals.models import *

# Create your views here.
def create_customer(request):
    if request.method == 'POST':
        name = request.POST['name']
        id = request.POST['customerId']
        customerData = customer.objects.create(name = name, customer_id = id)
        if customerData:
            return redirect('home')
    return render(request, 'app_015_signals/create_customer.html')