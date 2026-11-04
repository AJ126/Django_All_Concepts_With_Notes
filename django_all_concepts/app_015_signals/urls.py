from django.urls import path
from app_015_signals.views import *

urlpatterns = [
    path('createcustomer', create_customer, name="createcustomer")
]
