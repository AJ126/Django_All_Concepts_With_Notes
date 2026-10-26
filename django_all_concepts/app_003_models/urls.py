from django.urls import path
from app_003_models.views import *

urlpatterns = [
    path('showData', show_model_data, name="showData")
]
