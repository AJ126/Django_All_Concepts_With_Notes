from django.urls import path
from app_013_advance_model.views import *

urlpatterns = [
    path('showbooks', showbooks, name="showbooks"),
    path('showcheapbooks', showcheapbooks, name="showcheapbooks"),
    path('showexpensivebooks', showexpensivebooks, name="showexpensivebooks"),
]
