from django.urls import path
from app_011_function_based_curd.views import *

urlpatterns = [
    path('showcustomers', showCustomers, name="showcustomers"),
    path('createcustomer', createCustomer, name="createcustomer"),
    path('updatecustomer/<int:id>/', updateCustomer, name="updatecustomer"),
    path('deletecustomer/<int:id>/', deleteCustomer, name="deletecustomer"),
]
