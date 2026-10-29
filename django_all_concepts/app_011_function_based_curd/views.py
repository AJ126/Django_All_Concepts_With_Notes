from django.shortcuts import render, redirect
from django.contrib import messages
from app_011_function_based_curd.models import *
# Create your views here.

# Show records
def showCustomers(request):
    data = customer.objects.all()
    return render(request, 'app_011_function_based_curd/show.html',{'data':data})

def createCustomer(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        name = request.POST['name']
        customerId = request.POST['customerId']
        details = request.POST['details']
        status = request.POST.get('status') == 'on'
        if checkValue(name) and checkValue(details) and checkValue(customerId):
            data = customer.objects.create(profilepic = image, name = name, customerId = customerId, details = details, status = status)
            if data:
                messages.success(request, 'Custoomer save successfully')
                return redirect('showcustomers')
        else:
            messages.error(request,'Please enter valid data')
    return render(request, 'app_011_function_based_curd/create.html')

# update customer
def updateCustomer(request, id):
    data = customer.objects.get(id=id)
    if request.method =='POST':
        data.name = request.POST['name']
        data.customerId = request.POST['customerId']
        data.details = request.POST['details']
        data.status = request.POST.get('status') == 'on'
        data.save()
        return redirect('showcustomers')
    print('data',data)
    return render(request, 'app_011_function_based_curd/create.html', {'data': data})

#delete customer
def deleteCustomer(request, id):
    data = customer.objects.get(id=id)
    data.delete()
    return redirect('showcustomers')


# check fields is empty or not
def checkValue(value):
    return bool(value and value.strip())