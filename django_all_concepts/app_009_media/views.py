from django.shortcuts import render, redirect
from django.contrib import messages
from app_009_media.models import *
# Create your views here.

def upload_image(request):
    if request.method == 'POST':
        name = request.POST['name']
        image = request.FILES.get('image')
        if image:
            data = media(name = name, image = image)
            data.save()
            messages.success(request, 'Image Uploaded successfully')
            return redirect('home')
    return render(request,'app_009_media/upload.html')

