from django.urls import path
from app_012_orm.views import *

urlpatterns = [
    path('ormdata', ormData, name="ormdata")
]
