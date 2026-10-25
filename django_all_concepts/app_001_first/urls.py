from django.urls import path
from app_001_first.views import *

urlpatterns = [
    path('first', show, name='first'),
    path('showdatetime', showTime, name = 'showdatetime')
]
