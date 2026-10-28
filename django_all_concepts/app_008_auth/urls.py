from django.urls import path
from app_008_auth.views import *

urlpatterns = [
    path('register', register, name="register"),
]
