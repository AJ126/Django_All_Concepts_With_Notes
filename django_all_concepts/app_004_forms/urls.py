from django.urls import path
from app_004_forms.views import *

urlpatterns = [
    path('form', show_form, name="form"),
    path('validationform', validation_form, name="validationform"),
    path('cleanForm', clean_form, name="cleanForm")
]
