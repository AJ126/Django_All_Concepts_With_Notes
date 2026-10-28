from django.shortcuts import render, redirect
from django.contrib import messages
from app_009_media.models import *
from app_009_media.forms import *
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

def upload_img(request):
    if request.method == 'POST':
        form = imageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = imageForm()
    return render(request, 'app_009_media/upload_img.html', {'form': form})

