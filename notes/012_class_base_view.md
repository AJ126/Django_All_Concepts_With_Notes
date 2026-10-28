# Django Class-Based Views (CBVs) – Complete Notes

## 1. Types of Views in Django

Django supports two main approaches to writing views:

1. **Function-Based Views (FBVs)**
2. **Class-Based Views (CBVs)**

A view receives an HTTP request, processes the required logic, and returns an HTTP response.

### 1.1 Function-Based View (FBV)

A Function-Based View is a Python function that accepts an HTTP request and returns an HTTP response.

**Example:**

```python
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to Django")
```

### 1.2 Class-Based View (CBV)

A Class-Based View is a Python class that handles HTTP requests through methods such as `get()` and `post()`.

**Example:**

```python
from django.views import View
from django.http import HttpResponse

class HomeView(View):

    def get(self, request):
        return HttpResponse("Welcome to Django")
```

Both examples produce the same response, but they organize the code differently.

## 2. FBV vs CBV

| Feature | Function-Based View | Class-Based View |
|---|---|---|
| Definition | Python function | Python class |
| HTTP methods | Usually handled with conditions | Separate methods such as `get()` and `post()` |
| Code reuse | Functions and decorators | Inheritance, mixins and reusable classes |
| Beginner friendliness | Easy to understand initially | Requires understanding classes and inheritance |
| Simple CRUD | Requires writing logic manually | Generic views can reduce boilerplate |
| Complex custom logic | Often straightforward | Can require multiple methods or mixins |
| Best choice | Custom or specialized workflows | Standard reusable patterns such as CRUD |

**Important:** Neither approach is always better. Choose the approach that makes your code easier to understand, maintain and test.

Class-Based Views were introduced in Django 1.3. They provide a class-based way to organize view logic, including reusable generic views.

A CBV is not simply a wrapper around an FBV. Django's `as_view()` method creates a callable that instantiates the class and dispatches requests to the appropriate handler method.

## 3. Important Classes in `django.views.generic`

Django provides several built-in classes for common operations.

```python
from django.views import View
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
```

| Class | Purpose |
|---|---|
| `View` | Handle HTTP requests using methods such as `get()` and `post()` |
| `TemplateView` | Display a template |
| `ListView` | Display multiple database records |
| `DetailView` | Display one database record |
| `CreateView` | Create a database record |
| `UpdateView` | Update an existing record |
| `DeleteView` | Delete a record after confirmation |

## 4. The `View` Class

The base `View` class allows us to handle different HTTP methods separately.

### Example

```python
from django.views import View
from django.http import HttpResponse

class StudentView(View):

    def get(self, request):
        return HttpResponse("GET request received")

    def post(self, request):
        return HttpResponse("POST request received")
```

### Common HTTP handler methods

- `get()` — handles GET requests.
- `post()` — handles POST requests.
- `put()` — handles PUT requests.
- `patch()` — handles PATCH requests.
- `delete()` — handles DELETE requests.
- `head()` — handles HEAD requests.
- `options()` — handles OPTIONS requests.

Django dispatches a request to the corresponding handler when the class supports that HTTP method. If the method is not supported, Django normally returns `405 Method Not Allowed`.

### URL configuration

A CBV must be converted into a callable view using `as_view()`.

**`urls.py`**

```python
from django.urls import path
from .views import StudentView

urlpatterns = [
    path("student/", StudentView.as_view(), name="student"),
]
```

**Remember:** Use `StudentView.as_view()` rather than passing `StudentView` directly to `path()`.

## 5. TemplateView

`TemplateView` is used when we simply want to display a template without manually writing a `render()` call.

### Example

**`views.py`**

```python
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "app_010_class_based_view/home.html"
```

**`urls.py`**

```python
from django.urls import path
from .views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]
```

**Template path:**

```text
project/
├── app_010_class_based_view/
│   ├── templates/
│   │   └── app_010_class_based_view/
│   │       └── home.html
│   ├── views.py
│   └── urls.py
```

### Passing data to a template

Override `get_context_data()` when the template needs additional data.

```python
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "app_010_class_based_view/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "Welcome to Django"
        return context
```

**`home.html`**

```html
<h1>{{ message }}</h1>
```

## 6. ListView

`ListView` is used to display a list of database records.

For example, suppose we have an employee model and want to display all employees.

### 6.1 Example model

**`models.py`**

```python
from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name
```

Create the database table:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6.2 Create a ListView

**`views.py`**

```python
from django.views.generic import ListView
from .models import Employee

class EmployeeListView(ListView):
    model = Employee
```

Here, `model = Employee` tells Django which model to query.

Django retrieves the records and makes them available to the template.

### 6.3 Default template name

For the `Employee` model, Django looks for:

```text
employee_list.html
```

The default naming pattern is:

```text
modelname_list.html
```

The template search location depends on your template settings and configured template directories.

For an app-level template, a recommended location is:

```text
app_010_class_based_view/
└── templates/
    └── app_010_class_based_view/
        └── employee_list.html
```

### 6.4 Default context variable

By default, `ListView` provides the records using the context variable `object_list`. It also provides a model-specific variable named `employee_list` in this example.

You can define your own context variable:

```python
class EmployeeListView(ListView):
    model = Employee
    context_object_name = "employees"
```

Now use `employees` in the template.

**`employee_list.html`**

```html
<h2>Employee List</h2>

<ul>
    {% for employee in employees %}
        <li>
            {{ employee.name }} - {{ employee.address }}
        </li>
    {% empty %}
        <li>No employees found.</li>
    {% endfor %}
</ul>
```

### 6.5 Configure the URL

**`urls.py`**

```python
from django.urls import path
from .views import EmployeeListView

urlpatterns = [
    path("employees/", EmployeeListView.as_view(), name="employee_list"),
]
```

### 6.6 Specify a custom template

You can explicitly configure the template instead of using the default name.

```python
class EmployeeListView(ListView):
    model = Employee
    template_name = "app_010_class_based_view/template_list.html"
    context_object_name = "employees"
```

This is useful when you want to keep templates in a project-level template directory or use a custom template filename. Ensure the template is inside a directory configured in `TEMPLATES`.

**Important:** Django does not automatically create templates. Generic views only follow default naming conventions when `template_name` is not supplied.

## 7. DetailView

`DetailView` is used to display the details of one database record.

For example, clicking an employee's name in the employee list should display that employee's details.

### 7.1 Create a DetailView

**`views.py`**

```python
from django.views.generic import DetailView
from .models import Employee

class EmployeeDetailView(DetailView):
    model = Employee
```

### 7.2 Default template name

For the `Employee` model, the default template is:

```text
employee_detail.html
```

The naming pattern is:

```text
modelname_detail.html
```

Recommended location:

```text
app_010_class_based_view/
└── templates/
    └── app_010_class_based_view/
        └── employee_detail.html
```

### 7.3 Default context variable

For a single record, the default context variable is `object`. Django also provides the model-specific name, which is `employee` in this example.

You can customize it:

```python
class EmployeeDetailView(DetailView):
    model = Employee
    context_object_name = "emp"
```

**`employee_detail.html`**

```html
<h2>Employee Details</h2>

<p>Name: {{ emp.name }}</p>
<p>Address: {{ emp.address }}</p>
```

### 7.4 Configure the URL

```python
from django.urls import path
from .views import EmployeeDetailView

urlpatterns = [
    path(
        "employees/<int:pk>/",
        EmployeeDetailView.as_view(),
        name="employee_detail",
    ),
]
```

The `pk` is the primary key of the employee whose details we want to display.

### 7.5 Add a detail link to the list page

**`employee_list.html`**

```html
{% for employee in employees %}
    <p>
        <a href="{% url 'employee_detail' employee.pk %}">
            {{ employee.name }}
        </a>
    </p>
{% endfor %}
```

Each link passes the selected employee's primary key. Therefore, Django displays the selected employee, not necessarily the first record.

## 8. CreateView

`CreateView` is used to create a new database record through a form.

Django can generate a ModelForm automatically from the model, provided that you specify the fields to expose.

### 8.1 Create a CreateView

**`views.py`**

```python
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Employee

class EmployeeCreateView(CreateView):
    model = Employee
    fields = ["name", "address"]
    template_name = "app_010_class_based_view/employee_form.html"
    success_url = reverse_lazy("employee_list")
```

### Explanation

- `model` identifies the model to create.
- `fields` specifies which model fields the form should contain.
- `template_name` specifies the template.
- `success_url` specifies where the user goes after a successful save.

**Important:** If you omit `fields` and do not provide a suitable custom form, Django raises an error because it cannot determine which fields should be exposed.

Avoid `fields = "__all__"` for sensitive models unless you have carefully reviewed every field that should be editable.

### 8.2 Default template name

For the `Employee` model, Django's default template name is:

```text
employee_form.html
```

Recommended location:

```text
app_010_class_based_view/
└── templates/
    └── app_010_class_based_view/
        └── employee_form.html
```

### 8.3 Create the template

**`employee_form.html`**

```html
<h2>Create Employee</h2>

<form method="post">
    {% csrf_token %}

    {{ form.as_p }}

    <button type="submit">Save</button>
</form>
```

Django provides the generated form through the `form` context variable.

### 8.4 Configure the URL

```python
from django.urls import path
from .views import EmployeeCreateView

urlpatterns = [
    path(
        "employees/create/",
        EmployeeCreateView.as_view(),
        name="employee_create",
    ),
]
```

### 8.5 Understand the “No URL to redirect to” error

If you define neither `success_url` nor a suitable `get_absolute_url()` method on the model, Django cannot determine where to redirect after a successful creation.

**Option 1: Define `success_url` in the view.**

```python
success_url = reverse_lazy("employee_list")
```

**Option 2: Define `get_absolute_url()` on the model.**

```python
from django.db import models
from django.urls import reverse

class Employee(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse(
            "employee_detail",
            kwargs={"pk": self.pk},
        )
```

When `CreateView` saves the object, Django can use this method to determine the redirect destination if `success_url` is not specified.

`reverse()` resolves a URL immediately. `reverse_lazy()` delays URL resolution, which is convenient in class attributes.

## 9. UpdateView

`UpdateView` is used to update an existing database record.

It is similar to `CreateView`, but it loads an existing object based on its primary key.

### 9.1 Create an UpdateView

**`views.py`**

```python
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .models import Employee

class EmployeeUpdateView(UpdateView):
    model = Employee
    fields = ["name", "address"]
    template_name = "app_010_class_based_view/employee_form.html"
    success_url = reverse_lazy("employee_list")
```

### 9.2 Default template name

The default template is also:

```text
employee_form.html
```

Both `CreateView` and `UpdateView` use the `modelname_form.html` naming convention.

You can reuse the same template for creating and updating records.

### 9.3 Configure the URL

```python
from django.urls import path
from .views import EmployeeUpdateView

urlpatterns = [
    path(
        "employees/<int:pk>/update/",
        EmployeeUpdateView.as_view(),
        name="employee_update",
    ),
]
```

### 9.4 Add an update link

```html
<a href="{% url 'employee_update' employee.pk %}">
    Edit
</a>
```

When the user opens this URL, Django retrieves the selected employee and pre-populates the form with the existing values.

When the user submits the form, Django validates and saves the changes.

**Remember:** `UpdateView` needs a way to identify the object, commonly through `pk` in the URL.

## 10. DeleteView

`DeleteView` is used to delete an existing database record.

Django normally displays a confirmation page before deleting the object.

### 10.1 Create a DeleteView

**`views.py`**

```python
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from .models import Employee

class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = (
        "app_010_class_based_view/employee_confirm_delete.html"
    )
    success_url = reverse_lazy("employee_list")
```

### 10.2 Default template name

For the `Employee` model, the default template is:

```text
employee_confirm_delete.html
```

The naming pattern is:

```text
modelname_confirm_delete.html
```

The default context variable is `object`, and Django also provides the model-specific variable `employee`.

### 10.3 Create the confirmation template

**`employee_confirm_delete.html`**

```html
<h2>Delete Employee</h2>

<p>
    Are you sure you want to delete
    {{ employee.name }}?
</p>

<form method="post">
    {% csrf_token %}

    <button type="submit">Confirm Delete</button>
    <a href="{% url 'employee_list' %}">Cancel</a>
</form>
```

The form sends a POST request to confirm deletion. Opening the page with a GET request should only display the confirmation page; it should not delete the record.

### 10.4 Configure the URL

```python
from django.urls import path
from .views import EmployeeDeleteView

urlpatterns = [
    path(
        "employees/<int:pk>/delete/",
        EmployeeDeleteView.as_view(),
        name="employee_delete",
    ),
]
```

### 10.5 Add a delete link

```html
<a href="{% url 'employee_delete' employee.pk %}">
    Delete
</a>
```

### 10.6 Understand `success_url`

```python
success_url = reverse_lazy("employee_list")
```

After a successful deletion, Django redirects the user to the employee list page.

`reverse_lazy()` resolves the URL name lazily. It does not itself wait for the deletion to finish; the view performs the deletion and then redirects.

## 11. Complete CRUD URL Example

After creating the views, your app's `urls.py` could look like this:

```python
from django.urls import path

from .views import (
    EmployeeListView,
    EmployeeDetailView,
    EmployeeCreateView,
    EmployeeUpdateView,
    EmployeeDeleteView,
)

urlpatterns = [
    path(
        "employees/",
        EmployeeListView.as_view(),
        name="employee_list",
    ),
    path(
        "employees/<int:pk>/",
        EmployeeDetailView.as_view(),
        name="employee_detail",
    ),
    path(
        "employees/create/",
        EmployeeCreateView.as_view(),
        name="employee_create",
    ),
    path(
        "employees/<int:pk>/update/",
        EmployeeUpdateView.as_view(),
        name="employee_update",
    ),
    path(
        "employees/<int:pk>/delete/",
        EmployeeDeleteView.as_view(),
        name="employee_delete",
    ),
]
```

Include the app's URLs in the project-level `urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app_010_class_based_view.urls")),
]
```

**URL ordering note:** More-specific paths should be considered when designing routes. Django checks patterns in order. These particular routes have distinct shapes, so the shown ordering works.

## 12. How Django Finds Templates

Django's template discovery depends on the `TEMPLATES` configuration in `settings.py`.

### App-level templates

A common structure is:

```text
project/
├── manage.py
├── project_name/
│   └── settings.py
└── app_010_class_based_view/
    ├── views.py
    ├── models.py
    ├── urls.py
    └── templates/
        └── app_010_class_based_view/
            ├── employee_list.html
            ├── employee_detail.html
            ├── employee_form.html
            └── employee_confirm_delete.html
```

When using app-level template discovery, ensure `APP_DIRS=True` and that the application is included in `INSTALLED_APPS`.

### Project-level templates

You can also store shared templates in a project-level folder:

```text
project/
├── templates/
│   └── app_010_class_based_view/
│       └── template_list.html
├── manage.py
└── project_name/
    └── settings.py
```

Configure the project-level directory in `settings.py`:

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
```

Then a view can specify:

```python
class EmployeeListView(ListView):
    model = Employee
    template_name = (
        "app_010_class_based_view/template_list.html"
    )
```

Django does not automatically search only in `project/app/templates/app/`. It searches the configured template directories and app template directories according to the template engine settings.

## 13. Important Concepts to Remember

### `as_view()`

Converts a class-based view into a callable that Django can use in URL patterns.

```python
EmployeeListView.as_view()
```

### `model`

Specifies which model a generic view should work with.

```python
model = Employee
```

### `template_name`

Specifies the template to render.

```python
template_name = "app_010_class_based_view/employee_list.html"
```

### `context_object_name`

Customizes the name of the object or queryset provided to the template.

```python
context_object_name = "employees"
```

### `fields`

Specifies the model fields to include in a generated form.

```python
fields = ["name", "address"]
```

### `success_url`

Specifies where to redirect after a successful operation.

```python
success_url = reverse_lazy("employee_list")
```

### `get_absolute_url()`

A model method that returns the canonical URL for a particular object. It is commonly used after creating an object when no explicit success URL is configured.

### `get_context_data()`

Allows you to add extra information to the template context.

### `get_queryset()`

Allows you to customize which records a generic view retrieves.

Example:

```python
class EmployeeListView(ListView):
    model = Employee

    def get_queryset(self):
        return Employee.objects.filter(name__startswith="A")
```

This example displays employees whose names begin with the letter `A`.

## 14. Common Mistakes and Solutions

| Problem | Solution |
|---|---|
| `as_view()` is missing | Use `MyView.as_view()` in the URL pattern |
| `CreateView` raises a missing `fields` error | Define `fields` or a suitable custom form |
| No URL to redirect to after saving | Define `success_url` or implement `get_absolute_url()` |
| Template not found | Check `template_name`, folder structure and template settings |
| Update or detail view cannot find an object | Pass the correct primary key in the URL |
| Delete confirmation page is missing | Create `modelname_confirm_delete.html` or specify `template_name` |
| Context variable is unavailable | Check `context_object_name` and the template variable |
| Form submission fails CSRF validation | Include `{% csrf_token %}` in the POST form |
| Record is deleted through an unsafe link | Use a confirmation form with POST rather than a GET link that performs deletion |

## 15. Quick Revision

- Django provides **Function-Based Views** and **Class-Based Views**.
- Use FBVs when straightforward, explicit custom logic is a good fit.
- Use CBVs when class-based organization, reuse or generic view behavior is helpful.
- `View` handles HTTP methods through methods such as `get()` and `post()`.
- `TemplateView` displays a template.
- `ListView` displays multiple records.
- `DetailView` displays one record.
- `CreateView` creates a record.
- `UpdateView` updates a record.
- `DeleteView` displays a confirmation page and deletes the record after confirmation.
- Use `as_view()` in URL patterns.
- `ListView` normally uses `modelname_list.html`.
- `DetailView` normally uses `modelname_detail.html`.
- `CreateView` and `UpdateView` normally use `modelname_form.html`.
- `DeleteView` normally uses `modelname_confirm_delete.html`.
- Use `context_object_name` to customize the template variable.
- Use `reverse_lazy()` for URL names in class attributes when lazy resolution is appropriate.
- Never assume Django creates missing templates automatically.

