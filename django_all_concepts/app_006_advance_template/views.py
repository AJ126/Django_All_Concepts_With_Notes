from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app_006_advance_template.models import *

# Create your views here.
def show_template(request):
    data = userInfo.objects.all()
    return render(request, 'app_006_advance_template/adv_temp.html', {'data': data})

# custom filter
def show_custom_template(request):
    data = userInfo.objects.all()
    # Create paginator (10 records per page)
    paginator = Paginator(data, 10)

    # Get current page number
    page_number = request.GET.get('page')
    try:
        data = paginator.page(page_number)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    return render(request, 'app_006_advance_template/custom_temp.html', {'data': data})