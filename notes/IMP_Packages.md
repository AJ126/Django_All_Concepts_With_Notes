# Important Django Modules and Packages – Complete Notes

## Table of Contents

1. Django Admin Customization – HIdP Admin
2. Django Admin CAPTCHA – Multi CAPTCHA Admin
3. FastAdmin
4. Pillow – Image Processing
5. Login History
6. Django Taggit – Tagging System
7. Logging in Django and DRF
8. Additional Module Notes
9. Quick Revision

---

# 1. Django Admin Customization – `django-hidp-django-admin`

## What is `django-hidp-django-admin`?

`django-hidp-django-admin` is described on PyPI as a Django admin-themed template pack for HIdP.

Its intended purpose is to provide a different visual appearance for an admin interface.

**Installation:**

```bash
pip install -U django-hidp-django-admin
```

### Configuration

Your original notes contain this configuration:

```python
# settings.py

INSTALLED_APPS = [
    'hidp_django_admin',
    'hidp',
]
```

Your original URL configuration:

```python
# urls.py

from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib import admin

urlpatterns = [
    path(
        'django-admin/login/',
        RedirectView.as_view(
            pattern_name='hidp_accounts:login'
        ),
    ),
    path('admin/', admin.site.urls),
]
```

**Important:** The package listing identifies the package as a themed template pack, but does not provide a complete project description or enough configuration documentation to confirm that these exact settings and URL patterns work with every version. Check the package's official repository and documentation before adding them to an existing project.

Also check compatibility with your installed Django version.

Reference: [django-hidp-django-admin on PyPI](https://pypi.org/project/django-hidp-django-admin/).

---

# 2. Django Admin CAPTCHA – `django-multi-captcha-admin`

## What is CAPTCHA?

CAPTCHA stands for Completely Automated Public Turing test to tell Computers and Humans Apart.

It helps distinguish human users from automated bots.

Example:

When a user tries to log in to the Django admin panel, they may be asked to solve a CAPTCHA before the login is accepted.

**Purpose:**

- Help prevent automated login attempts.
- Add another verification step to admin login.
- Reduce automated abuse of the login page.

**Installation:**

```bash
pip install -U django-multi-captcha-admin
```

The package requires a supported CAPTCHA engine. One option is `django-simple-captcha`.

Install:

```bash
pip install django-simple-captcha
```

### Configuration

Add the applications in the correct order:

```python
# settings.py

INSTALLED_APPS = [
    # Other Django applications

    'captcha',
    'multi_captcha_admin',
    'django.contrib.admin',

    # Other applications
]
```

Configure the CAPTCHA engine:

```python
MULTI_CAPTCHA_ADMIN = {
    'engine': 'simple-captcha',
}
```

### URL configuration

Add the CAPTCHA URL patterns to your main `urls.py`:

```python
# urls.py

from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('captcha/', include('captcha.urls')),
    path('admin/', admin.site.urls),
]
```

Run migrations:

```bash
python manage.py migrate
```

**Important points:**

- `multi_captcha_admin` should be placed before `django.contrib.admin` in `INSTALLED_APPS`.
- Install the CAPTCHA engine you select.
- The `captcha/` URL configuration is needed for the simple CAPTCHA engine's URL endpoints.
- Test the admin login after configuration.
- CAPTCHA is an additional security measure, not a replacement for strong passwords, rate limiting, MFA or secure deployment practices.

The package's PyPI documentation lists `simple-captcha`, `recaptcha` and `recaptcha2` as supported engines.

Reference: [django-multi-captcha-admin on PyPI](https://pypi.org/project/django-multi-captcha-admin/).

---

# 3. FastAdmin

## What is FastAdmin?

FastAdmin is an admin dashboard package that provides an admin interface for applications built with frameworks such as Django, FastAPI and Flask.

It is inspired by the Django admin interface.

It provides features such as:

- Model administration.
- CRUD operations.
- Search and filtering.
- Authentication and permissions.
- File uploads.
- CSV and JSON export.
- Dashboard charts.

**Important:** FastAdmin is a separate admin dashboard package. It is not the same as Django's built-in admin panel.

### Installation

For a Django application using Django ORM:

```bash
pip install "fastadmin[django]"
```

The basic package name is:

```bash
pip install fastadmin
```

However, the official package documentation recommends installing the appropriate framework extras.

### Configuration

The package documentation provides these environment variables:

```bash
ADMIN_USER_MODEL=User
ADMIN_USER_MODEL_USERNAME_FIELD=username
ADMIN_SECRET_KEY=secret_key
```

For a Windows command prompt, you can set them using:

```cmd
set ADMIN_USER_MODEL=User
set ADMIN_USER_MODEL_USERNAME_FIELD=username
set ADMIN_SECRET_KEY=your_secret_key
```

For Django URL configuration, the package documents this integration:

```python
# urls.py

from django.urls import path
from fastadmin import get_django_admin_urls

urlpatterns = [
    path('admin/', get_django_admin_urls()),
]
```

**Important:**

- Follow the current official documentation for model registration, authentication and permissions.
- Do not assume that installing FastAdmin automatically replaces Django's built-in admin.
- Use environment variables for secrets instead of hardcoding production credentials.
- The current PyPI package documentation lists Python 3.12+ for its latest release, so check Python compatibility before installing it.

Reference: [FastAdmin on PyPI](https://pypi.org/project/fastadmin/).

---

# 4. Pillow – Image Processing

## What is Pillow?

Pillow is a Python imaging library used to open, create, edit and process images.

It is useful when working with image uploads in Django applications.

**Installation:**

```bash
pip install Pillow
```

### Main features

- Open images.
- Resize images.
- Crop images.
- Rotate images.
- Convert image formats.
- Compress images.
- Process uploaded images.

### Real-life example

Suppose we are developing a Customer Management System.

When Shiv uploads a profile picture, we may want to resize it before displaying it on the customer profile page.

Pillow can help us perform this operation.

### Example: Resize an image

```python
from PIL import Image

image = Image.open('profile.jpg')

resized_image = image.resize((300, 300))

resized_image.save('resized_profile.jpg')
```

### Example: Convert image to another format

```python
from PIL import Image

image = Image.open('profile.png')

image.convert('RGB').save('profile.jpg')
```

### Pillow with Django

Django provides `ImageField` for storing image uploads.

```python
from django.db import models


class Customer(models.Model):

    name = models.CharField(max_length=100)

    profile_pic = models.ImageField(
        upload_to='customer_profiles/'
    )
```

**Important points:**

- Pillow is required by Django to validate and work with `ImageField`.
- Configure `MEDIA_ROOT` and `MEDIA_URL` for uploaded files.
- Use `request.FILES` when handling uploaded images.
- Use `enctype="multipart/form-data"` in HTML upload forms.
- Validate uploaded image types and sizes.
- Do not trust the file extension alone when validating uploaded files.

---

# 5. Login History

## What is Login History?

Login History means maintaining a record of user login activities.

It can help administrators understand when users log in and which accounts are being accessed.

### Information that can be stored

| Field | Purpose |
|---|---|
| User | Identifies the account |
| Login time | When the user logged in |
| Logout time | When the user logged out |
| IP address | IP address associated with the request |
| User agent | Browser or client information |
| Status | Successful or failed login |

### Real-life example

Suppose Shiv logs in to a Customer Management System.

The application can record:

```text
User: Shiv
Login Time: 10:30 AM
IP Address: 192.168.1.10
Status: Successful
```

If Shiv logs out at 11:30 AM, the application can record the logout time too.

### How can we implement Login History?

One approach is to create a custom model.

```python
# models.py

from django.db import models
from django.conf import settings


class LoginHistory(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    login_time = models.DateTimeField(auto_now_add=True)

    logout_time = models.DateTimeField(
        null=True,
        blank=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    user_agent = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        default='success'
    )

    def __str__(self):
        return f'{self.user} - {self.login_time}'
```

### Django Login Signals

Django provides authentication signals that can help track login activity.

Important signals:

| Signal | Purpose |
|---|---|
| `user_logged_in` | Triggered after successful login |
| `user_logged_out` | Triggered after logout |
| `user_login_failed` | Triggered after failed login authentication |

Import:

```python
from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed
)
```

You can connect receivers to these signals and save the relevant information.

**Important security points:**

- Do not store passwords in login history.
- Treat IP addresses and user-agent information as potentially sensitive data.
- Be careful when trusting forwarded IP headers from proxies.
- Define a suitable retention policy for audit records.
- A failed login signal does not necessarily give you every detail of the original HTTP request.

---

# 6. Django Taggit – Tagging System

## What is Django Taggit?

`django-taggit` is a reusable Django application that makes it easy to add tags to model objects.

Tags help organize and categorize records.

### Real-life example

Suppose we are developing a blog application.

A blog post can have multiple tags:

```text
Django
Python
Web Development
Backend
```

Instead of creating a separate tag-management system manually, we can use Django Taggit.

### Installation

```bash
pip install django-taggit
```

### Step 1: Add Taggit to `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    # Other applications
    'taggit',
]
```

### Step 2: Add `TaggableManager` to a model

```python
# models.py

from django.db import models
from taggit.managers import TaggableManager


class BlogPost(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    tags = TaggableManager()

    def __str__(self):
        return self.title
```

### Step 3: Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create tags

```python
post = BlogPost.objects.create(
    title='Django Tutorial',
    description='Learn Django step by step.'
)

post.tags.add('Django', 'Python', 'Backend')
```

### Step 5: Retrieve tags

```python
post = BlogPost.objects.get(id=1)

for tag in post.tags.all():
    print(tag.name)
```

### Step 6: Filter records using tags

```python
BlogPost.objects.filter(tags__name='Django')
```

### Step 7: Remove a tag

```python
post.tags.remove('Python')
```

### Step 8: Clear all tags

```python
post.tags.clear()
```

**Advantages:**

- Easy tag management.
- Multiple tags per object.
- Reusable tagging functionality.
- Easy filtering using tags.
- Avoids manually implementing many-to-many tagging logic.

Reference: [Django Taggit documentation](https://django-taggit.readthedocs.io/en/latest/getting_started.html).

---

# 7. Logging in Django and Django REST Framework

## 7.1 What is Logging?

Logging is the process of recording information about what happens inside an application.

It helps developers monitor application behavior and investigate problems.

### Real-life example

Suppose a customer tries to log in to an application.

We may want to record:

```text
INFO: Customer login successful
WARNING: Multiple failed login attempts
ERROR: Database connection failed
```

Logging is useful for:

- Debugging.
- Monitoring.
- Error tracking.
- Security auditing.
- Performance analysis.
- Troubleshooting production issues.

## 7.2 Python's Built-in Logging Package

Python already provides a built-in logging package.

We do not need to install an external package to use basic logging.

Import:

```python
import logging
```

Create a logger:

```python
logger = logging.getLogger(__name__)
```

### Logging Levels

| Level | Purpose |
|---|---|
| `DEBUG` | Detailed debugging information |
| `INFO` | General application information |
| `WARNING` | Something unexpected happened |
| `ERROR` | An operation failed |
| `CRITICAL` | A serious failure occurred |

### Example

```python
import logging

logger = logging.getLogger(__name__)


def customer_view(request):

    logger.info('Customer view accessed')

    try:
        # Application logic
        pass

    except Exception:
        logger.exception(
            'An error occurred in customer_view'
        )
```

`logger.exception()` records the exception traceback when called inside an exception handler.

## 7.3 How to Configure Logging in Django?

Django provides the `LOGGING` setting.

Example:

```python
# settings.py

LOGGING = {

    'version': 1,

    'disable_existing_loggers': False,

    'formatters': {
        'standard': {
            'format': (
                '{levelname} {asctime} '
                '{name} {message}'
            ),
            'style': '{',
        },
    },

    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django.log',
            'formatter': 'standard',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },

        'myapp': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

Now use logging inside your views:

```python
import logging

logger = logging.getLogger('myapp')


def customer_view(request):

    logger.info('Customer page opened')

    return HttpResponse('Customer page')
```

The logs will be written to `django.log`.

**Important:** For production, use log rotation or a centralized logging system so log files do not grow indefinitely.

## 7.4 Database Logging

Sometimes we want to store logs in a database instead of only storing them in files.

A database logging package can help with this.

Your original notes list these packages:

| Package | Intended area |
|---|---|
| `django-db-logger` | Django database logging |
| `drf-api-tracking` | Tracking DRF API requests |
| `drf-tracking` | DRF request tracking |
| `drf-api-logger` | DRF API request/response logging |
| `django-db-logs` | Database-backed logging |
| `db-logger` | Database logging |

**Important:** These packages are alternatives or separate tools, not packages that must all be installed together. Check their maintenance status, compatibility, configuration, security and data-retention behavior before choosing one.

### DRF API Logger

`drf-api-logger` is intended to record API request and response information.

Its documented setup includes:

```bash
pip install drf-api-logger
```

Add the application:

```python
INSTALLED_APPS = [
    # Other applications
    'drf_api_logger',
]
```

Add its middleware:

```python
MIDDLEWARE = [
    # Other middleware
    'drf_api_logger.middleware.api_logger_middleware.APILoggerMiddleware',
]
```

For database logging, configure the package as documented and run:

```bash
python manage.py migrate
```

The package documentation also describes options for masking sensitive fields.

Reference: [DRF API Logger on PyPI](https://pypi.org/project/drf-api-logger/).

## 7.5 Custom Logging Applications

Your project notes contain two ideas for custom logging applications.

### A. `drf_api_logger`

Purpose:

Create a custom application for recording API activity.

Possible information:

- API endpoint.
- HTTP method.
- Request timestamp.
- Response status code.
- Execution time.
- User information.
- Error details.

Example:

```text
API: /api/customers/
Method: GET
Status: 200
Execution Time: 120 ms
```

### B. `user_state_audit`

Purpose:

Create a custom application for tracking important user-related changes.

Possible information:

- User login activity.
- User logout activity.
- Profile updates.
- Account status changes.
- Permission changes.
- Administrative actions.

Example:

```text
User: Shiv
Action: Profile Updated
Changed Field: Email
Timestamp: 11:30 AM
```

**Important distinction:**

- API logging records API request and response activity.
- User audit logging records important actions and changes made by users.

Do not automatically record passwords, access tokens, refresh tokens or sensitive request bodies.

## 7.6 Logging vs Auditing

| Logging | Auditing |
|---|---|
| Records application events | Records important actions and changes |
| Helps debugging and monitoring | Helps accountability and security investigations |
| May contain technical information | Usually records who did what and when |
| Examples: database errors, warnings | Examples: permission changes, profile updates |

---

# 8. Additional Module Notes

Your original notes contain only the heading `8)` without a package name or explanation.

This section is intentionally left open so that another module can be added later.

Suggested format:

```text
8) Package Name

Purpose:
    What does this package do?

Installation:
    pip install package-name

Configuration:
    settings.py
    urls.py

Example:
    Practical use case

Important Points:
    Compatibility and security considerations
```

---

# 9. Quick Revision

| Package / Feature | Main Purpose |
|---|---|
| `django-hidp-django-admin` | HIdP-themed Django admin templates |
| `django-multi-captcha-admin` | CAPTCHA on Django admin login |
| `fastadmin` | Alternative admin dashboard |
| `Pillow` | Image processing |
| Login History | Track user login activity |
| `django-taggit` | Add tags to Django models |
| Python `logging` | Record application events |
| `drf-api-logger` | Record DRF API activity |
| `user_state_audit` | Custom user activity auditing |

## Important installation commands

```bash
pip install -U django-hidp-django-admin

pip install -U django-multi-captcha-admin

pip install "fastadmin[django]"

pip install Pillow

pip install django-simple-captcha

pip install django-taggit

pip install drf-api-logger
```

**Final recommendation:** Start with Pillow, Django Taggit and Python's built-in logging because they are useful in ordinary Django projects. Add admin customization, CAPTCHA and API logging packages only when your project actually needs those features. Always check package compatibility before installing it into your main project.