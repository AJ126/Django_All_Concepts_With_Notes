from django.shortcuts import render
from app_013_advance_model.models import *
# Create your views here.
def showbooks(request):
    data = books.objects.showAllBooks()
    return render(request, 'app_013_advance_model/showBooks.html', {'data': data})

def showcheapbooks(request):
    data = books.objects.cheapBook()
    return render(request, 'app_013_advance_model/showBooks.html', {'data': data})

def showexpensivebooks(request):
    data = books.custom_manager.expensiveBook()
    return render(request, 'app_013_advance_model/showBooks.html', {'data': data})