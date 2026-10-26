from django.urls import path
from app_005_modelForms.views import *

urlpatterns = [
    path('formmodel', form_save, name = "formmodel"),
    path('widgetform', formWidget, name = "widgetform"),
    path('dateform', dateFormWidget, name = "dateform"),
]
