from django.urls import path
from app_009_media.views import *

urlpatterns = [
    path('uploadimage', upload_image, name="uploadimage")
]
