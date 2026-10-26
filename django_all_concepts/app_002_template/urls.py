from django.urls import path
from app_002_template.views import *

urlpatterns = [
    path('firsttemplate', show_template, name = 'firsttemplate'),
    path('dynamictemplate', show_dynamic_data, name='dynamictemplate'),
    path('showimg', show_img, name='showimg')
]
