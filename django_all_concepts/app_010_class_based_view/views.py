from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.urls import reverse_lazy
from app_010_class_based_view.models import *

# Create your views here.
class show_simple_class(View):
    def get(self, request):
        return HttpResponse('''
            <div class="d-flex justify-content-center">
                <h4>Welcome to the class based views</h4>
            </div>
        ''')

# show static template
class templateView(TemplateView):
    template_name = 'template.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

# get & show list of all records
class listView(ListView):
    context_object_name = 'testInfo_list'
    model = testInfo

# get & show single records
class detailViewClass(DetailView):
    context_object_name = 'testInfo'
    model = testInfo

# create a record
class createRecord(CreateView):
    model = testInfo
    fields =('name', 'address')

# update perticular record
class updateRecord(UpdateView):
    model = testInfo
    fields =('name', 'address')

class deleteRecord(DeleteView):
    model = testInfo
    success_url = reverse_lazy('listview')
