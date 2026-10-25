# Django Framework – Basic Concepts Notes

## 1. What is Django?

1. Django is a **free and open-source web framework**.
2. It is written in **Python**.
3. It follows the **Model–View–Template (MVT)** architectural pattern.
4. It is maintained by the **Django Software Foundation (DSF)**.
5. Django originated in 2003 as an internal project at the *Lawrence Journal-World* newspaper to help developers build web applications quickly.

## 2. Top 5 Features of Django

### 1. Fast

Django helps developers build web applications quickly by providing built-in features and reusable components.

### 2. Fully Loaded

Django includes many built-in features for common web development tasks, such as:

- User authentication and authorization
- Database management
- An administration interface
- Form handling
- Security protections
- Support for sitemaps and RSS feeds through available Django features and packages

These features reduce the amount of code developers need to write from scratch.

### 3. Security

Django provides built-in protections against many common web security risks, including:

- SQL injection
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Clickjacking

Django also provides a user authentication system to help manage user accounts and passwords securely.

**Note:** Developers must still follow Django's security recommendations and configure applications correctly.

### 4. Scalability

Django applications can be designed to handle increasing numbers of users and requests by using appropriate architecture, caching, database optimization, and deployment strategies.

### 5. Versatility

Django can be used to build different types of applications, such as:

- Blogs and news websites
- E-commerce websites
- Educational portals
- Social networking applications
- Business management systems

---

## 3. What Is a Django Project?

A **Django project** contains the settings and configurations required to run a complete web application. It can contain multiple Django applications.

### Real-Life Example

Imagine an organization that works to help poor people.

The organization is the **project**, and its different activities can be separate **applications**.

```text
Organization (Django Project)
│
├── Help Poor People (Application)
├── Collect Funds (Application)
└── Do Social Work (Application)
```

Each application handles a particular area of functionality within the overall project.

## 4. What Is a Django Application?

A **Django application** is a component of a Django project that handles a specific set of related features.

For example, an organization website might have applications for:

- Managing users
- Collecting donations
- Publishing news
- Managing events

Applications can often be reused in other Django projects when their code and dependencies are appropriately designed and configured.

## 5. Creating a Django Project

### Command

```bash
django-admin startproject project_name
```

Alternative command:

```bash
py -m django startproject project_name
```

Replace `project_name` with your desired project name.

### Default Project Structure

```text
project_name/
│
├── manage.py
└── project_name/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

### Files and Their Uses

#### 1. `__init__.py`

- It is a Python file that can be empty.
- It marks the directory as a regular Python package in the traditional package system.
- It can also contain package initialization code.

#### 2. `settings.py`

This file contains the project's settings and configurations, including:

- Installed applications (`INSTALLED_APPS`)
- Middleware configuration (`MIDDLEWARE`)
- Database configuration (`DATABASES`)
- Templates
- Static files
- Security settings

#### 3. `urls.py`

This file defines URL patterns that map incoming URL paths to the appropriate views.

For example:

```python
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
```

#### 4. `wsgi.py`

**WSGI** stands for **Web Server Gateway Interface**.

It provides the entry point for running a Django application through WSGI-compatible web servers, commonly used for traditional synchronous deployments.

#### 5. `asgi.py`

**ASGI** stands for **Asynchronous Server Gateway Interface**.

It provides the entry point for running Django through ASGI-compatible servers. ASGI supports asynchronous request handling and can support long-lived connections, such as WebSockets, when suitable application components are configured.

**Real-life example:** Think of a restaurant that serves regular customers and also manages ongoing conversations with customers. ASGI can support both traditional HTTP requests and suitable long-lived connections.

#### 6. `manage.py`

This is a command-line utility used to interact with a Django project.

Common tasks include:

```bash
python manage.py runserver
python manage.py startapp app_name
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py test
```

---

## 6. Creating a Django Application

### Command

```bash
python manage.py startapp app_name
```

Replace `app_name` with your desired application name.

### Default Application Structure

```text
app_name/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── tests.py
├── views.py
└── migrations/
    └── __init__.py
```

### Files and Their Uses

#### 1. `__init__.py`

This file identifies the application directory as a Python package in the traditional package system. It can be empty.

#### 2. `admin.py`

Use this file to register models with Django's built-in administration interface.

Example:

```python
from django.contrib import admin
from .models import Student

admin.site.register(Student)
```

This example assumes that a `Student` model exists in `models.py`.

#### 3. `apps.py`

This file contains the application's configuration class.

Django uses this configuration to identify and configure the application.

#### 4. `models.py`

This file defines the application's data models.

Models describe the structure of data stored in the database.

Example:

```python
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
```

#### 5. `tests.py`

Use this file to write automated tests for your application.

Tests help verify that your code behaves as expected.

#### 6. `views.py`

This file commonly contains functions or classes that process HTTP requests and return HTTP responses.

Example:

```python
from django.http import HttpResponse

def display(request):
    return HttpResponse("Welcome to Django!")
```

#### 7. `migrations/`

This directory stores migration files that describe changes to your database schema based on model changes.

Create migration files with:

```bash
python manage.py makemigrations
```

Apply migrations to the database with:

```bash
python manage.py migrate
```

---

## 7. Registering an Application in the Project

After creating an application, add it to the `INSTALLED_APPS` list in the project's `settings.py` file.

For example, if your application is named `student_app`:

```python
INSTALLED_APPS = [
    # Default Django applications
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom application
    'student_app',
]
```

**Why is this necessary?**

Registering the application allows Django to discover it and include its relevant functionality, such as models, templates, and other application components.

---

## 8. Types of Views in Django

Django supports two common ways of writing views.

### 1. Function-Based Views (FBVs)

A Function-Based View is a Python function that accepts an HTTP request and returns an HTTP response.

Example:

```python
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Home Page!")
```

### 2. Class-Based Views (CBVs)

A Class-Based View defines view behavior using a Python class.

Example:

```python
from django.http import HttpResponse
from django.views import View

class HomeView(View):
    def get(self, request):
        return HttpResponse("Welcome to the Home Page!")
```

Both approaches can handle requests and return responses. The best choice depends on the requirements and complexity of the application.

---

## 9. HTTP Request Flow in Django

A simplified request flow is:

```text
User / Browser
      |
      v
Project urls.py
      |
      v
Application urls.py (if configured)
      |
      v
View (views.py)
      |
      v
Model / Database (if required)
      |
      v
HTTP Response
      |
      v
User / Browser
```

### Explanation

1. The user enters a URL or interacts with a webpage.
2. Django receives the HTTP request.
3. Django checks the configured URL patterns.
4. The matching URL pattern directs the request to a view.
5. The view performs the required processing and may interact with a model or database.
6. The view returns an HTTP response.
7. The browser receives the response.

**Important:** The application-level URL configuration is optional. A project can route requests directly to views using the project-level `urls.py` file.

---

## 10. Application-Level URL Configuration

Instead of putting every URL pattern into the project's `urls.py`, you can create a separate `urls.py` file inside each application.

This makes the project easier to organize and helps make applications reusable.

### Step 1: Create `urls.py` Inside the Application

Example structure:

```text
project_name/
├── manage.py
├── project_name/
│   ├── settings.py
│   └── urls.py
└── student_app/
    ├── views.py
    └── urls.py
```

Django does not automatically create the application's `urls.py` file. Create it manually.

### Step 2: Add URL Patterns to the Application's `urls.py`

File: `student_app/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('demo/', views.display, name='demo'),
]
```

Here:

- `path()` defines a URL pattern.
- `'demo/'` is the URL path.
- `views.display` is the view that handles the request.
- `name='demo'` gives the URL pattern a name for use in URL reversing.

Make sure the `display` view exists in `student_app/views.py`.

Example:

```python
from django.http import HttpResponse

def display(request):
    return HttpResponse("This is the student application.")
```

### Step 3: Include Application URLs in the Project's `urls.py`

File: `project_name/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('student/', include('student_app.urls')),
]
```

### Step 4: Access the URL

Run the development server:

```bash
python manage.py runserver
```

Open this URL in your browser:

```text
http://127.0.0.1:8000/student/demo/
```

Django combines the project-level path `'student/'` with the application-level path `'demo/'` to match the request.

### Benefits of Application-Level URLs

- Keeps URL configurations organized.
- Makes large projects easier to maintain.
- Separates each application's URL patterns.
- Makes it easier to reuse applications in other projects.

---

## Quick Revision

| Concept | Purpose |
|---|---|
| Django project | Contains project settings and configurations and can include multiple applications |
| Django application | Handles a particular set of related features |
| `settings.py` | Stores project settings |
| `urls.py` | Defines URL patterns |
| `models.py` | Defines database models |
| `views.py` | Processes requests and returns responses |
| `admin.py` | Registers models with the Django admin interface |
| `apps.py` | Defines application configuration |
| `tests.py` | Contains automated tests |
| `migrations/` | Stores database schema migration files |
| `manage.py` | Provides command-line access to Django project tasks |
| `wsgi.py` | Entry point for WSGI-compatible servers |
| `asgi.py` | Entry point for ASGI-compatible servers |