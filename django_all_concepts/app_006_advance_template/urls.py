from django.urls import path
from app_006_advance_template.views import *

urlpatterns = [
    path('showtemplate', show_template, name="showtemplate"),
    path('showcustomtemplate', show_custom_template, name="showcustomtemplate")
]
