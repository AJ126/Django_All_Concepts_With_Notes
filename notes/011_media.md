# Django Media Files and Image Uploads – Complete Notes

## 1. What Are Media Files in Django?

Media files are files uploaded by users through a Django application.

Examples include:
- Profile photos
- Product images
- Documents and PDFs
- Uploaded videos
- User-submitted files

Django uses **media settings** to define the URL and filesystem location for uploaded files.

## 2. Static Files vs Media Files

| Static files | Media files |
|---|---|
| Usually provided by developers. | Usually uploaded by users. |
| CSS, JavaScript, logos, icons. | Profile photos, documents, product images. |
| Configured using `STATIC_URL` and related settings. | Configured using `MEDIA_URL` and `MEDIA_ROOT`. |
| May be collected using `collectstatic` for deployment. | Stored in the configured media storage. |

Example folder structure:

```text
myproject/
│
├── manage.py
├── myproject/
│   ├── settings.py
│   └── urls.py
│
├── media/
│   ├── images/
│   └── documents/
│
└── myapp/
    ├── models.py
    ├── forms.py
    ├── views.py
    └── templates/
        └── upload_img.html
```

Django can create the subfolders specified by `upload_to` when a file is saved. You do not necessarily need to create them manually.

## 3. Configure the Media Folder

### Step 1: Create a media folder

Create a folder named `media` in your project's root directory, alongside `manage.py`.

For example:

```text
E:/Django/myproject/media/
```

Django can create this folder when saving files if it does not already exist.

### Step 2: Configure `settings.py`

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**Explanation:**

- `MEDIA_URL` defines the URL prefix used to access uploaded media files.
- `MEDIA_ROOT` defines the filesystem directory where uploaded files are stored.
- `BASE_DIR / 'media'` uses `pathlib` to construct the directory path.

For example, an uploaded image might be stored at:

```text
media/images/photo.jpg
```

Its development URL might be:

```text
http://127.0.0.1:8000/media/images/photo.jpg
```

The URL is not the filesystem path; Django maps the URL to the file during development.

## 4. Create a Model for Uploaded Files

Django provides two commonly used model fields for file uploads.

### A. `FileField`

Use `FileField` when users can upload different types of files.

```python
from django.db import models

class UploadedFile(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.name
```

The uploaded file is stored under:

```text
media/documents/
```

### B. `ImageField`

Use `ImageField` when the field should contain images.

```python
from django.db import models

class UploadedImage(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name
```

The uploaded image is stored under:

```text
media/images/
```

### What does `upload_to` mean?

The `upload_to` parameter specifies the subdirectory inside `MEDIA_ROOT` where uploaded files should be stored.

For example:

```python
photo = models.ImageField(upload_to='images/')
```

If the uploaded file is named `profile.jpg`, it might be stored at:

```text
media/images/profile.jpg
```

Django stores the relative file path in the database. The file's binary content is stored in the filesystem or the configured storage backend.

## 5. Install the Pillow Library

Django's `ImageField` requires the Pillow library to process and validate images.

Activate your virtual environment and run:

```bash
python -m pip install Pillow
```

Verify the installation:

```bash
python -m pip show Pillow
```

**Important:** `FileField` does not require Pillow, but `ImageField` does.

## 6. Create and Apply Migrations

After creating or modifying your model, run:

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates or updates the database table for your model.

## 7. Create a ModelForm for Image Upload

Create a `forms.py` file inside your application.

**`forms.py`**

```python
from django import forms
from .models import UploadedImage


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['name', 'photo']

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'photo': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            ),
        }
```

### Explanation

- `forms.ModelForm` creates a form based on a model.
- `model = UploadedImage` specifies the model.
- `fields = ['name', 'photo']` selects the fields shown in the form.
- `widgets` customizes the HTML form controls.

## 8. Create a View to Upload an Image

**`views.py`**

```python
from django.shortcuts import render, redirect
from .forms import ImageUploadForm


def upload_img(request):
    if request.method == 'POST':
        form = ImageUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()
            return redirect('upload_img')
    else:
        form = ImageUploadForm()

    return render(
        request,
        'app_009_media/upload_img.html',
        {'form': form}
    )
```

### Explanation

- `request.POST` contains submitted text form values.
- `request.FILES` contains uploaded files.
- `form.is_valid()` validates the submitted data.
- `form.save()` saves the model record and uploaded image.
- `redirect('upload_img')` returns the user to the upload page after success.

**Important:** When uploading files, pass both `request.POST` and `request.FILES` to the form.

## 9. Create the HTML Template

Create `upload_img.html` inside your application's templates directory.

**`upload_img.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>Upload Image</title>
</head>
<body>
    <h2>Upload an Image</h2>

    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}

        {{ form.as_p }}

        <button type="submit">Upload Image</button>
    </form>
</body>
</html>
```

### Why is `enctype="multipart/form-data"` required?

This attribute allows the browser to send file data as part of the request.

Without it, the uploaded file will not be submitted in the format Django expects, and `request.FILES` will not contain the selected file.

Always use it for HTML forms that upload files.

## 10. Configure the Application URL

**Application `urls.py`**

```python
from django.urls import path
from . import views

urlpatterns = [
    path(
        'upload/',
        views.upload_img,
        name='upload_img'
    ),
]
```

Make sure the application's URLs are included in your project's main URL configuration.

## 11. Configure Media URLs in the Project URL File

For local development, add media-serving configuration to the **project's main `urls.py`**.

**Project `urls.py`**

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mediaapp/', include('app_009_media.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
```

### Explanation

- `settings.MEDIA_URL` defines the URL prefix.
- `document_root=settings.MEDIA_ROOT` tells Django where uploaded files are stored.
- The `if settings.DEBUG` condition restricts this development file-serving configuration to debug mode.

**Important:** This helper is for development only. In production, serve media using a suitable web server or storage service, such as object storage. Do not use Django's development media-serving helper as your production file server.

## 12. Display Uploaded Images in a Template

You can display an uploaded image by using the image field's `.url` property.

For example, pass a saved image object from a view:

```python
from django.shortcuts import render
from .models import UploadedImage


def image_list(request):
    images = UploadedImage.objects.all()

    return render(
        request,
        'app_009_media/image_list.html',
        {'images': images}
    )
```

**`image_list.html`**

```html
<h2>Uploaded Images</h2>

{% for item in images %}
    <div>
        <h3>{{ item.name }}</h3>

        {% if item.photo %}
            <img
                src="{{ item.photo.url }}"
                alt="{{ item.name }}"
                width="200"
            >
        {% endif %}
    </div>
{% empty %}
    <p>No images uploaded yet.</p>
{% endfor %}
```

The expression `{{ item.photo.url }}` generates the URL for the stored image.

Only use `.url` after checking that the file field contains a file. The example above does that with `{% if item.photo %}`.

## 13. View Uploaded Images in Django Admin

First, register your model in the application's `admin.py`.

```python
from django.contrib import admin
from .models import UploadedImage


@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'photo')
```

Create a superuser if needed:

```bash
python manage.py createsuperuser
```

Start the server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/admin/
```

After logging in, open the Uploaded Images section. Django Admin normally displays the stored file path in the `photo` column, not the actual image preview.

If you want a thumbnail preview, you can add a custom admin method:

```python
from django.contrib import admin
from django.utils.html import format_html
from .models import UploadedImage


@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_preview')

    @admin.display(description='Preview')
    def image_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="100" alt="Preview">',
                obj.photo.url
            )
        return 'No image'
```

The preview works when the media URL is accessible to the admin browser. For untrusted uploads, use appropriate validation and security controls.

## 14. Common Mistakes

| Mistake | Solution |
|---|---|
| Forgetting Pillow | Install it when using `ImageField`. |
| Forgetting `request.FILES` | Pass both `request.POST` and `request.FILES`. |
| Missing `enctype` | Add `enctype="multipart/form-data"`. |
| Incorrect media settings | Configure `MEDIA_URL` and `MEDIA_ROOT`. |
| Forgetting migrations | Run `makemigrations` and `migrate` after model changes. |
| Image uploads but does not display | Check the media URL configuration and file path. |
| Trying to serve media with static settings | Use media settings for user-uploaded files. |
| Expecting an image preview in admin automatically | Add a custom preview method if required. |

## 15. File Upload Security

File uploads require care because users can submit malicious or unexpected files.

- Validate file types and sizes.
- Do not rely only on the file extension to identify an image.
- Restrict access to sensitive uploaded documents.
- Store private documents outside publicly accessible media URLs or use protected download views.
- Configure production storage and permissions properly.
- Never execute uploaded files as server-side code.

## 16. Quick Revision

- `MEDIA_URL` defines the URL prefix for media.
- `MEDIA_ROOT` defines the filesystem directory for uploaded files.
- `FileField` stores a reference to an uploaded file.
- `ImageField` is intended for uploaded images and requires Pillow.
- `upload_to='images/'` stores files in a subdirectory under the media root.
- `request.FILES` contains uploaded file data.
- `form.save()` saves the file and model record.
- `enctype="multipart/form-data"` is required for HTML file uploads.
- `{{ item.photo.url }}` retrieves the URL of a saved image.
- Use `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` only for development media serving.
- Use Django Admin registration to manage uploaded file records.

**Remember:** Static files belong to your application's resources; media files are uploaded content. Configure and serve them separately.