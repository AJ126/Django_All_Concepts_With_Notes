# Django and Django REST Framework – Complete Interview Questions and Answers

## Table of Contents

1. Django Application and Server Basics
2. Database and ORM
3. Django Models and Model Managers
4. Function-Based Views and Class-Based Views
5. Authentication and Authorization
6. HTTP, APIs and Web Services
7. Python Concepts Used in Django
8. Django REST Framework Fundamentals
9. DRF Views, Generic Views, Mixins and ViewSets
10. DRF Serializers and Validation
11. API Development and Advanced Features
12. Django Signals and Utilities
13. Advanced Django Concepts
14. Important Commands and Quick Revision

---

# 1. Django Application and Server Basics

## 1.1 What is the difference between `wsgi.py` and `asgi.py`?

Both files provide an entry point through which an application server communicates with a Django project.

| Feature | `wsgi.py` | `asgi.py` |
|---|---|---|
| Full form | Web Server Gateway Interface | Asynchronous Server Gateway Interface |
| Main purpose | Traditional synchronous applications | Synchronous and asynchronous applications |
| Communication | Traditional request-response | Request-response and long-lived connections |
| WebSockets | Not supported by standard WSGI | Supported with a compatible ASGI application and server |
| Example server | Gunicorn, uWSGI | Uvicorn, Daphne |
| Typical usage | Conventional Django websites | Django applications requiring async features |

**WSGI example:**

```python
# myproject/wsgi.py

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'myproject.settings'
)

application = get_wsgi_application()
```

**ASGI example:**

```python
# myproject/asgi.py

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'myproject.settings'
)

application = get_asgi_application()
```

**Important points:**

- WSGI is designed around synchronous request-response handling.
- ASGI supports asynchronous request handling and protocols such as WebSockets.
- ASGI can also serve ordinary synchronous Django views.
- To use WebSockets in Django, you generally need an additional solution such as Django Channels.

**Real-life example:**

- WSGI: A customer sends a request, the server processes it and returns a response.
- ASGI: A customer connects to a live chat, and the connection can remain open for continuous communication.

## 1.2 What is the difference between `makemigrations` and `migrate`?

Both commands are used to manage database schema changes.

| Feature | `makemigrations` | `migrate` |
|---|---|---|
| Purpose | Creates migration files | Applies migration files |
| Input | Changes in Django models | Existing migration files |
| Output | Python migration files | Database schema changes |
| Database changes | Does not normally apply schema changes | Applies schema changes |
| Example | `python manage.py makemigrations` | `python manage.py migrate` |

**Example:**

Suppose we create a model:

```python
class Customer(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
```

**Step 1: Generate migration file**

```bash
python manage.py makemigrations
```

Django creates a migration file describing the database changes.

**Step 2: Apply migration**

```bash
python manage.py migrate
```

Django applies the migration to the database.

**Important correction:** `makemigrations` does not generate SQL code directly. It generates Python migration files. Django translates those operations into database-specific SQL when applying migrations.

To preview the SQL:

```bash
python manage.py sqlmigrate app_name 0001
```

## 1.3 Can we create nested projects in Django?

Yes. Django supports nested Python packages and multiple applications inside a project.

For example:

```text
myproject/
│
├── manage.py
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── customers/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── apps.py
│   │
│   └── orders/
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       └── apps.py
│
└── requirements.txt
```

You can organize applications into folders, provided that they are valid Python packages and Django can import them.

For example, add the correct application configuration to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'apps.customers',
    'apps.orders',
]
```

For larger projects, this structure helps separate functionality into modules.

## 1.4 Why do we install `dj-database-url`?

`dj-database-url` is a Python package that converts a database URL into Django's `DATABASES` configuration.

It is useful when deploying applications because hosting platforms commonly provide database connection information through environment variables.

Install:

```bash
pip install dj-database-url
```

Example:

```python
import os
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}
```

Example database URL:

```text
postgresql://username:password@localhost:5432/mydatabase
```

**Why use it?**

- Avoid writing database connection settings manually.
- Easily switch between development and production databases.
- Keep database credentials in environment variables.
- Support different database backends through connection URLs.

**Important:** Do not commit database passwords or sensitive connection URLs to Git.

---

# 2. Database and ORM

## 2.1 What is ORM?

ORM stands for Object Relational Mapping.

Django ORM allows us to communicate with a relational database using Python code instead of writing SQL queries manually.

**Example:**

Without ORM:

```sql
SELECT * FROM customer;
```

With Django ORM:

```python
Customer.objects.all()
```

Creating a record:

```python
Customer.objects.create(
    name='Shiv',
    mobile='9876543210'
)
```

Django converts ORM operations into database queries.

## 2.2 What is the difference between Aggregation and Annotation?

Both are used to perform calculations on database records.

| Feature | Aggregation | Annotation |
|---|---|---|
| Purpose | Calculates a summary of a queryset | Adds calculated values to individual records |
| Result | Usually a dictionary of summary values | QuerySet containing additional calculated fields |
| Scope | Overall queryset or groups | Individual objects or groups |
| Common methods | `aggregate()` | `annotate()` |

### Aggregation example

Suppose we have a `Customer` model with an `age` field.

```python
from django.db.models import Avg, Max, Min, Count, Sum

result = Customer.objects.aggregate(
    average_age=Avg('age'),
    maximum_age=Max('age'),
    minimum_age=Min('age'),
    total_customers=Count('id')
)

print(result)
```

Example output:

```python
{
    'average_age': 28.5,
    'maximum_age': 45,
    'minimum_age': 18,
    'total_customers': 10
}
```

### Annotation example

Suppose we have `Customer` and `Order` models.

```python
from django.db.models import Count

customers = Customer.objects.annotate(
    total_orders=Count('orders')
)

for customer in customers:
    print(customer.name, customer.total_orders)
```

Each customer receives an additional calculated attribute called `total_orders`.

**Remember:**

- `aggregate()` calculates a summary.
- `annotate()` adds calculated values to returned records.

## 2.3 What is the N+1 query problem?

The N+1 query problem occurs when an application executes one query to retrieve a collection of records and then executes an additional query for each record to retrieve related data.

**Example:**

Suppose we have two models:

```python
class Customer(models.Model):
    name = models.CharField(max_length=100)


class Order(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    amount = models.IntegerField()
```

Now execute:

```python
orders = Order.objects.all()

for order in orders:
    print(order.customer.name)
```

This can produce:

1. One query to retrieve all orders.
2. One additional query for each order's customer.

For 100 orders, this could result in approximately 101 queries.

This is the N+1 query problem.

### How do we solve it using `select_related()`?

```python
orders = Order.objects.select_related(
    'customer'
)

for order in orders:
    print(order.customer.name)
```

Django uses a SQL JOIN to retrieve the related customer data together with the orders.

This reduces unnecessary database queries.

### Difference between `select_related()` and `prefetch_related()`

| Feature | `select_related()` | `prefetch_related()` |
|---|---|---|
| Technique | SQL JOIN | Separate queries combined in Python |
| Best for | ForeignKey and OneToOneField | ManyToManyField and reverse relationships |
| Query count | Usually one query for the selected relationship | Usually one additional query per prefetched relationship |
| Usage | `select_related('customer')` | `prefetch_related('orders')` |

Example:

```python
Customer.objects.prefetch_related('orders')
```

**Interview tip:** Use `select_related()` for single-valued relationships and `prefetch_related()` for collections of related objects.

## 2.4 What is ORM optimization?

ORM optimization means improving database query performance by reducing unnecessary queries, retrieving only required fields and avoiding inefficient database operations.

Important techniques:

**1. Use `select_related()`**

```python
Order.objects.select_related('customer')
```

**2. Use `prefetch_related()`**

```python
Customer.objects.prefetch_related('orders')
```

**3. Retrieve only required fields**

```python
Customer.objects.values('id', 'name')
```

**4. Use `only()`**

```python
Customer.objects.only('id', 'name')
```

Be careful: accessing deferred fields later may cause additional queries.

**5. Use `exists()` instead of retrieving records just to check existence**

```python
if Customer.objects.filter(name='Shiv').exists():
    print('Customer exists')
```

**6. Use `count()` for record counts**

```python
total = Customer.objects.count()
```

**7. Add database indexes for frequently queried fields**

```python
class Customer(models.Model):
    email = models.EmailField(db_index=True)
```

**8. Use pagination**

Do not retrieve thousands of records when the user only needs one page.

**9. Inspect queries**

```python
queryset = Customer.objects.all()

print(queryset.query)
```

For more detailed query analysis, use Django Debug Toolbar or database query logging.

---

# 3. Django Models and Model Managers

## 3.1 What is a Model Manager?

A Model Manager is an interface through which Django provides database query operations.

By default, Django provides an `objects` manager.

```python
Customer.objects.all()
Customer.objects.filter(name='Shiv')
Customer.objects.get(id=1)
```

Here, `objects` is the default manager.

## 3.2 Can we customize database responses using a Model Manager?

Yes. We can customize query behavior by creating a custom manager.

**Example:**

```python
from django.db import models


class CustomerManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(
            status=True
        )


class Customer(models.Model):
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    objects = CustomerManager()
```

Now:

```python
Customer.objects.all()
```

returns only customers whose status is `True`.

**Important:** `get_queryset()` customizes the queryset returned by that manager. It does not modify the database response globally.

## 3.3 Which method should we override to customize the `all()` method behavior?

The method is:

```python
get_queryset()
```

Example:

```python
class ActiveCustomerManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(
            status=True
        )
```

When we call:

```python
Customer.objects.all()
```

the custom queryset behavior is applied.

## 3.4 Can we define new methods inside a Custom Manager?

Yes. We can create reusable query methods.

```python
class CustomerManager(models.Manager):

    def active_customers(self):
        return self.filter(status=True)

    def inactive_customers(self):
        return self.filter(status=False)

    def search_customer(self, keyword):
        return self.filter(name__icontains=keyword)
```

Use:

```python
Customer.objects.active_customers()

Customer.objects.inactive_customers()

Customer.objects.search_customer('shiv')
```

## 3.5 What is a Proxy Model?

A Proxy Model allows us to create a different Python model representation of an existing database model without creating a new database table.

It is useful when we want to change model behavior, default ordering or admin presentation without changing the database structure.

**Example:**

```python
class Customer(models.Model):
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)


class ActiveCustomer(Customer):

    class Meta:
        proxy = True
        ordering = ['name']

    def display_status(self):
        return 'Active' if self.status else 'Inactive'
```

**Important points:**

- A proxy model does not create a separate database table.
- It uses the original model's table.
- It cannot introduce new database fields.
- It can customize Python methods, managers and default ordering.
- It can have separate admin registration and presentation.

### Model inheritance types

| Type | New table? | Main purpose |
|---|---|---|
| Abstract base model | No table for the abstract parent | Share common fields |
| Multi-table inheritance | Yes, child table | Separate parent and child records |
| Proxy model | No additional table | Change Python behavior |

---

# 4. Function-Based Views and Class-Based Views

## 4.1 What is a Function-Based View (FBV)?

A Function-Based View is a Python function that receives an HTTP request and returns an HTTP response.

Example:

```python
from django.http import HttpResponse

def home(request):
    return HttpResponse('Welcome to Django')
```

## 4.2 What is a Class-Based View (CBV)?

A Class-Based View is a Python class used to handle HTTP requests.

Example:

```python
from django.views import View
from django.http import HttpResponse


class HomeView(View):

    def get(self, request):
        return HttpResponse('Welcome to Django')
```

URL configuration:

```python
from django.urls import path
from .views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
```

## 4.3 Which is more powerful: CBV or FBV?

Neither is universally more powerful. Both can implement complex application functionality.

| Feature | FBV | CBV |
|---|---|---|
| Structure | Function | Class |
| Learning | Usually easier for beginners | Requires understanding classes and inheritance |
| Code reuse | Helper functions and decorators | Inheritance and mixins |
| HTTP methods | Usually handled using conditions or decorators | Separate methods such as `get()` and `post()` |
| Complexity | Good for simple and custom logic | Good for reusable and structured logic |
| Extensibility | Can be extended with functions and decorators | Can be extended through inheritance and mixins |

**When to use FBV:**

- Simple views.
- Small operations.
- Custom request-processing logic.
- When straightforward code is preferred.

**When to use CBV:**

- Reusable views.
- CRUD operations.
- Applications with repeated view patterns.
- When inheritance and mixins make the code cleaner.

**Important corrections:**

- CBVs are not internally converted into FBVs.
- `as_view()` creates a callable view function that instantiates the class and dispatches requests to the appropriate method.
- CBVs are not simply wrappers around FBVs.
- FBVs are not inherently more powerful than CBVs.

## 4.4 What is `get_absolute_url()`?

`get_absolute_url()` is a model method that returns the canonical URL for a particular model object.

It is commonly used to determine where a user should go after creating or viewing an object.

Example:

```python
from django.db import models
from django.urls import reverse


class Company(models.Model):
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=64)

    def get_absolute_url(self):
        return reverse(
            'company-detail',
            kwargs={'pk': self.pk}
        )
```

URL:

```python
path(
    'company/<int:pk>/',
    CompanyDetailView.as_view(),
    name='company-detail'
)
```

**Usage:**

Django's generic editing views can use `get_absolute_url()` to determine the success URL when an explicit `success_url` is not provided.

**Important:** `get_absolute_url()` does not automatically mean redirect to the previous page. It returns the object's canonical URL.

## 4.5 What is `reverse()`?

`reverse()` generates a URL using its URL pattern name.

Example:

```python
from django.urls import reverse

url = reverse(
    'company-detail',
    kwargs={'pk': 1}
)
```

It returns a URL similar to:

```text
/company/1/
```

Use `reverse()` when you need to generate a URL immediately.

## 4.6 What is `reverse_lazy()` and why do we use it?

`reverse_lazy()` is similar to `reverse()`, but it delays URL resolution until the URL is actually needed.

Example:

```python
from django.urls import reverse_lazy
from django.views.generic import DeleteView


class CompanyDeleteView(DeleteView):

    model = Company
    template_name = 'company_confirm_delete.html'
    success_url = reverse_lazy('company-list')
```

**Why use it?**

Class attributes are evaluated when the class is defined. `reverse_lazy()` delays resolving the URL, which is useful in class-based views.

**Difference:**

| `reverse()` | `reverse_lazy()` |
|---|---|
| Resolves URL immediately | Resolves URL lazily |
| Returns a resolved URL string | Returns a lazy URL object |
| Common in functions and methods | Common in class attributes |

---

# 5. Authentication and Authorization

## 5.1 What is Authentication?

Authentication is the process of verifying the identity of a user.

In simple words:

**Authentication answers: Who are you?**

Example:

A user enters a username and password. Django verifies whether those credentials are valid.

Django provides authentication functions:

```python
from django.contrib.auth import authenticate

user = authenticate(
    username='shiv',
    password='password'
)
```

If the credentials are valid, Django returns the user object. Otherwise, it returns `None`.

## 5.2 What is Authorization?

Authorization is the process of checking whether an authenticated user has permission to access a particular resource or perform a particular action.

In simple words:

**Authorization answers: What are you allowed to do?**

Example:

- Shiv can view customer records.
- Parvati can create customer records.
- Only an administrator can delete all customer records.

Django provides permissions and groups to manage authorization.

## 5.3 Difference between Authentication and Authorization

| Feature | Authentication | Authorization |
|---|---|---|
| Purpose | Verifies identity | Checks permissions |
| Main question | Who are you? | What can you access? |
| Usually happens | Before authorization checks | After identity is established |
| Example | Login using password | Permission to delete customers |

## 5.4 How do we implement Forgot Password functionality using an email reset link?

Django provides built-in password reset views.

The typical flow is:

1. User enters their registered email address.
2. Django finds the corresponding user account.
3. Django generates a secure, time-limited password reset token.
4. Django sends a password reset link through email.
5. User opens the link.
6. Django validates the token.
7. User enters a new password.
8. Django saves the new password.

### Important built-in views

| View | Purpose |
|---|---|
| `PasswordResetView` | Requests password reset |
| `PasswordResetDoneView` | Shows email-sent confirmation |
| `PasswordResetConfirmView` | Validates token and accepts new password |
| `PasswordResetCompleteView` | Shows completion message |

Example URL configuration:

```python
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [

    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html'
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),

    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),

    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
]
```

Configure email settings in `settings.py` using an appropriate email backend.

**Security points:**

- Use Django's built-in token mechanism.
- Do not send passwords through email.
- Do not expose whether an email address exists in a way that allows account enumeration.
- Use HTTPS in production.
- Use a properly configured email service.

---

# 6. HTTP, APIs and Web Services

## 6.1 What is an API?

API stands for Application Programming Interface.

An API allows two applications to communicate with each other.

Example:

An Angular frontend sends a request to a Django backend:

```text
Angular Frontend
       |
       | HTTP Request
       v
Django API
       |
       v
Database
       |
       v
Django API
       |
       | JSON Response
       v
Angular Frontend
```

Example response:

```json
{
    "id": 1,
    "name": "Shiv",
    "mobile": "9876543210"
}
```

## 6.2 How many types of Web Services / APIs are available?

There are several API architectural styles and protocols. Two traditional web-service approaches are SOAP and REST.

### SOAP-based Web Service

SOAP stands for Simple Object Access Protocol.

Characteristics:

- SOAP messages use XML.
- Uses a defined message structure.
- Often uses WSDL to describe services.
- Can work over different transport protocols, such as HTTP and SMTP.
- Supports standards for security and reliable messaging.
- Can be more complex and verbose than REST for simple web APIs.

### REST-based Web Service

REST stands for Representational State Transfer.

Characteristics:

- Uses HTTP methods such as GET, POST, PUT, PATCH and DELETE.
- Represents data as resources.
- Uses resource URLs.
- Commonly exchanges JSON, but can also use XML and other representations.
- Usually simpler and lighter for web and mobile applications.
- Uses HTTP security mechanisms and application-level authentication and authorization.

### Difference between SOAP and REST

| Feature | SOAP | REST |
|---|---|---|
| Type | Protocol | Architectural style |
| Common format | XML | JSON is common, but not mandatory |
| Transport | Multiple transports | Commonly HTTP |
| Complexity | Generally more complex | Generally simpler |
| Performance | Can have more message overhead | Often lightweight |
| Contract | Commonly uses WSDL | Often uses OpenAPI |
| Security | Supports WS-Security standards | Can use HTTPS, tokens, OAuth and other mechanisms |

**Important corrections:**

- REST is not always JSON-based.
- SOAP is not always more secure than REST. Security depends on implementation.
- REST is commonly used with HTTP, but REST itself is an architectural style, not a protocol.
- Avoid memorizing claims that a particular company's services are all SOAP-based or all REST-based. Architectures vary between services.

## 6.3 What are HTTP methods (HTTP verbs)?

HTTP methods describe the operation a client wants to perform on a resource.

| Method | Purpose | Example |
|---|---|---|
| GET | Retrieve data | Get all customers |
| POST | Create a resource or submit data | Create customer |
| PUT | Replace/update a resource | Replace customer details |
| PATCH | Partially update a resource | Update customer address |
| DELETE | Delete a resource | Delete customer |
| HEAD | Retrieve response headers without the response body | Check resource headers |
| OPTIONS | Discover communication options | Check supported methods |
| CONNECT | Establish a tunnel | HTTPS proxy connection |
| TRACE | Diagnostic request tracing | Trace request path |

**Important:** MOVE, LOCK and PROPFIND are not standard core HTTP methods. They are associated with WebDAV extensions.

## 6.4 Can we send HTTP requests from the command prompt?

Yes. We can use command-line HTTP clients such as `curl` and HTTPie.

### Using curl

GET request:

```bash
curl http://127.0.0.1:8000/customer/
```

POST request:

```bash
curl -X POST http://127.0.0.1:8000/customer/ ^
-H "Content-Type: application/json" ^
-d "{\"name\":\"Shiv\",\"mobile\":\"9876543210\"}"
```

### Using HTTPie

Install:

```bash
pip install httpie
```

GET:

```bash
http GET http://127.0.0.1:8000/customer/
```

POST:

```bash
http POST http://127.0.0.1:8000/customer/ name=Shiv mobile=9876543210
```

HTTPie makes it convenient to send HTTP requests and inspect responses from the terminal.

## 6.5 What is the difference between Web Service Provider and Web Service Consumer?

**Web Service Provider:**

The application that provides an API or web service.

Example: A Django backend provides a customer API.

**Web Service Consumer:**

The application that consumes or uses the provided API.

Example: An Angular frontend calls the Django customer API.

| Provider | Consumer |
|---|---|
| Provides API | Uses API |
| Receives requests | Sends requests |
| Returns responses | Processes responses |
| Example: Django backend | Example: Angular frontend |

---

# 7. Python Concepts Used in Django

## 7.1 What is the difference between `*args` and `**kwargs`?

Both allow a function to accept a variable number of arguments.

### `*args`

- Accepts a variable number of positional arguments.
- Values are collected into a tuple.

Example:

```python
def display(*args):
    print(args)


display(1)
display(1, 2)
display(1, 2, 3)
```

Output:

```python
(1,)
(1, 2)
(1, 2, 3)
```

### `**kwargs`

- Accepts a variable number of keyword arguments.
- Values are collected into a dictionary.

Example:

```python
def display(**kwargs):
    print(kwargs)


display(name='Shiv')

display(
    name='Shiv',
    address='Kailash Parvat'
)
```

Output:

```python
{'name': 'Shiv'}

{
    'name': 'Shiv',
    'address': 'Kailash Parvat'
}
```

### Difference

| `*args` | `**kwargs` |
|---|---|
| Positional arguments | Keyword arguments |
| Stores values in tuple | Stores values in dictionary |
| Uses one asterisk | Uses two asterisks |

---

# 8. Django REST Framework Fundamentals

## 8.1 What is Django REST Framework (DRF)?

Django REST Framework is a toolkit built on top of Django for developing Web APIs.

It provides features such as:

- Serializers.
- Authentication.
- Permissions.
- API views.
- Generic views.
- ViewSets and routers.
- Pagination.
- Filtering.
- Throttling.
- Browsable API.
- API versioning.

## 8.2 What is the speciality of DRF?

Important advantages:

1. **Browsable API:** Developers can interact with APIs through a browser.
2. **Serialization:** Converts complex objects into Python-native data types and supports conversion back.
3. **Authentication:** Supports several authentication mechanisms.
4. **Permissions:** Controls access to API resources.
5. **Generic Views:** Reduces repeated CRUD code.
6. **ViewSets and Routers:** Simplifies CRUD API development.
7. **Pagination:** Divides large responses into pages.
8. **Filtering:** Allows clients to filter records.
9. **Throttling:** Controls request rates.
10. **Documentation support:** Integrates with OpenAPI documentation tools.

## 8.3 Can we create an API using Django without DRF?

Yes. Django can create APIs without Django REST Framework.

Example:

```python
from django.http import JsonResponse


def customer_api(request):

    data = {
        'id': 1,
        'name': 'Shiv',
        'mobile': '9876543210'
    }

    return JsonResponse(data)
```

Django's `JsonResponse` converts a Python dictionary into a JSON HTTP response.

**Difference:**

| Django without DRF | Django with DRF |
|---|---|
| Uses Django views | Uses DRF API views |
| Manual request parsing | Built-in request parsing |
| Manual serialization | Serializers |
| Manual validation | Serializer validation |
| Manual API features | Built-in authentication, permissions, pagination, etc. |
| Suitable for simple APIs | Suitable for structured API development |

DRF is not compulsory for creating an API. It simply provides tools that make API development easier.

## 8.4 What is Serialization?

Serialization is the process of converting complex Python objects into a representation that can be transferred or stored.

In DRF, serializers commonly convert:

```text
Django Model Instance
        |
        v
Serializer
        |
        v
Python Dictionary
        |
        v
JSON Response
```

Example:

```python
from rest_framework import serializers


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'
```

Usage:

```python
customer = Customer.objects.get(id=1)

serializer = CustomerSerializer(customer)

print(serializer.data)
```

Example output:

```python
{
    'id': 1,
    'name': 'Shiv',
    'mobile': '9876543210'
}
```

### What is Deserialization?

Deserialization is the process of converting incoming data into Python-native data and validating it so that it can be used to create or update objects.

Example:

```python
serializer = CustomerSerializer(
    data=request.data
)

if serializer.is_valid():
    serializer.save()
```

### Serialization vs Deserialization

| Serialization | Deserialization |
|---|---|
| Converts objects into representable data | Converts incoming data into validated Python data |
| Model instance → dictionary | Incoming dictionary → validated data |
| Used when returning API data | Used when accepting API data |
| `serializer.data` | `serializer.is_valid()` and `serializer.validated_data` |

**Important:** A serializer does not necessarily convert directly into JSON. It first produces Python-native data. A renderer, such as DRF's JSONRenderer, converts that data into JSON for the response.

## 8.5 What is `dumpdata`?

`dumpdata` is a Django management command used to export database data into a serialized format.

Example:

```bash
python manage.py dumpdata
```

Export one application:

```bash
python manage.py dumpdata app_name
```

Export to a JSON file:

```bash
python manage.py dumpdata app_name --indent 4 > data.json
```

Import data:

```bash
python manage.py loaddata data.json
```

**Important points:**

- JSON is the default output format.
- Other supported serializers include XML and YAML when the appropriate serializer support is installed.
- `dumpdata` exports data; it does not create database tables.
- `loaddata` imports fixture data.

---

# 9. DRF Views, Generic Views, Mixins and ViewSets

## 9.1 What is the difference between Django `View` and DRF `APIView`?

| Feature | Django `View` | DRF `APIView` |
|---|---|---|
| Framework | Django | Django REST Framework |
| Request object | Django `HttpRequest` | DRF `Request` |
| Response | Usually `HttpResponse` or `JsonResponse` | DRF `Response` |
| Parsing | Manual or Django forms | Configurable parsers |
| Authentication | Usually handled through Django | DRF authentication policies |
| Permissions | Usually custom or Django permissions | DRF permission classes |
| Content negotiation | Usually manual | Built in |

Example:

```python
from rest_framework.views import APIView
from rest_framework.response import Response


class CustomerAPIView(APIView):

    def get(self, request):
        return Response({
            'message': 'Customer list'
        })
```

## 9.2 What is APIView?

`APIView` is a DRF class that allows us to handle HTTP methods individually.

Example:

```python
from rest_framework.views import APIView
from rest_framework.response import Response


class CustomerAPIView(APIView):

    def get(self, request):
        return Response({'message': 'GET request'})

    def post(self, request):
        return Response({'message': 'POST request'})

    def put(self, request):
        return Response({'message': 'PUT request'})

    def delete(self, request):
        return Response({'message': 'DELETE request'})
```

Use APIView when we need custom request-handling logic or a non-standard API workflow.

## 9.3 What is a ViewSet?

A ViewSet groups related API actions into one class.

It commonly provides actions such as:

- `list`
- `create`
- `retrieve`
- `update`
- `partial_update`
- `destroy`

Example:

```python
from rest_framework.viewsets import ModelViewSet


class CustomerViewSet(ModelViewSet):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
```

A router can automatically create URLs for the ViewSet.

## 9.4 What is the difference between APIView and ViewSet?

| Feature | APIView | ViewSet |
|---|---|---|
| Structure | HTTP method handlers | Resource-oriented actions |
| Methods | `get()`, `post()`, `put()` | `list()`, `create()`, `retrieve()` |
| URL configuration | Usually written manually | Commonly uses routers |
| Control | More explicit HTTP handling | More structured action handling |
| Best use | Custom API workflows | Standard CRUD APIs |

**Real-life example:**

Imagine a library application.

With APIView, we manually handle:

- GET books.
- POST a new book.
- PUT book details.
- DELETE a book.

With a ViewSet, we organize the same functionality using actions such as `list`, `create`, `retrieve`, `update` and `destroy`.

Neither is always better. Select the approach that makes the API easiest to understand and maintain.

## 9.5 What are DRF Generic Views?

Generic Views are pre-built DRF views that provide common operations such as listing, creating, retrieving, updating and deleting records.

They reduce repeated code.

Import:

```python
from rest_framework import generics
```

### Important Generic Views

| Generic View | Purpose |
|---|---|
| `ListAPIView` | Retrieve a list of objects |
| `CreateAPIView` | Create a new object |
| `RetrieveAPIView` | Retrieve one object |
| `UpdateAPIView` | Update an object |
| `DestroyAPIView` | Delete an object |
| `ListCreateAPIView` | List objects and create an object |
| `RetrieveUpdateAPIView` | Retrieve and update an object |
| `RetrieveDestroyAPIView` | Retrieve and delete an object |
| `RetrieveUpdateDestroyAPIView` | Retrieve, update and delete an object |

Example:

```python
from rest_framework import generics


class CustomerListAPIView(generics.ListAPIView):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
```

URL:

```python
path(
    'customers/',
    CustomerListAPIView.as_view(),
    name='customer-list'
)
```

## 9.6 Why do we use Generic Views?

We use Generic Views because they provide reusable implementations of common API operations.

Advantages:

- Less repeated code.
- Faster CRUD development.
- Standardized API behavior.
- Easy integration with serializers.
- Support for filtering, pagination and permissions.
- Can be customized by overriding methods.

Use Generic Views when the API follows common CRUD patterns.

## 9.7 What is a Mixin?

A Mixin is a class that provides reusable functionality to another class through inheritance.

In DRF, mixins provide reusable implementations of common operations.

Import:

```python
from rest_framework import mixins
```

Important mixins:

| Mixin | Functionality |
|---|---|
| `ListModelMixin` | List records |
| `CreateModelMixin` | Create records |
| `RetrieveModelMixin` | Retrieve one record |
| `UpdateModelMixin` | Update records |
| `DestroyModelMixin` | Delete records |

Example:

```python
from rest_framework import generics, mixins


class CustomerListCreateAPIView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)
```

## 9.8 Why do we use Mixins?

We use mixins to reuse common functionality without writing the same code repeatedly.

For example, if multiple API views need the same list or create behavior, mixins provide reusable methods.

## 9.9 What is the difference between Mixin and Serializer?

| Feature | Mixin | Serializer |
|---|---|---|
| Purpose | Reusable view behavior | Data conversion and validation |
| Main responsibility | List, create, retrieve, update, delete operations | Convert and validate data |
| Location | Commonly used in views | Commonly used in serializers |
| Example | `CreateModelMixin` | `CustomerSerializer` |

**Simple explanation:**

- Serializer = Data handling.
- Mixin = Reusable view functionality.

A serializer does not handle HTTP requests by itself.

A mixin does not replace serializer validation or data conversion.

## 9.10 What is the difference between View and ViewSet?

In this context, View generally refers to Django or DRF views that handle HTTP requests, whereas a ViewSet groups related resource actions.

A DRF `APIView` uses methods such as `get()` and `post()`.

A DRF `ViewSet` uses methods such as `list()`, `create()` and `retrieve()`.

Example ViewSet structure for a larger project:

```text
customers/
│
├── models.py
├── serializers.py
├── urls.py
│
└── views/
    ├── __init__.py
    ├── api_views.py
    └── viewsets.py
```

This is an optional organizational pattern. It is not compulsory to create separate view files.

## 9.11 What is DefaultRouter and why do we use it?

`DefaultRouter` is provided by DRF. It automatically generates URL patterns for registered ViewSets.

Example:

```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(
    'customers',
    CustomerViewSet,
    basename='customer'
)

urlpatterns = router.urls
```

Alternatively, include the router URLs in the project:

```python
from django.urls import include, path

urlpatterns = [
    path('api/', include(router.urls)),
]
```

Typical generated routes include:

| URL | Action |
|---|---|
| `/api/customers/` | List and create |
| `/api/customers/1/` | Retrieve, update and delete |

`DefaultRouter` also provides an API root view.

**Important:** When the ViewSet does not define a class-level queryset, specify `basename` when registering it.

## 9.12 Can we write custom logic inside a ViewSet?

Yes. ViewSets can contain custom methods and can override their existing methods.

Example:

```python
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response


class CustomerViewSet(ModelViewSet):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        status_value = self.request.query_params.get('status')

        if status_value is not None:
            queryset = queryset.filter(
                status=status_value.lower() == 'true'
            )

        return queryset

    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        customer = self.get_object()

        return Response({
            'customer': customer.name,
            'total_orders': customer.orders.count()
        })
```

Here:

- `get_queryset()` customizes which records are returned.
- `@action()` adds a custom ViewSet endpoint.
- `detail=True` means the action works with an individual object.

---

# 10. DRF Serializers and Validation

## 10.1 What is Serializer Validation?

Serializer validation checks whether incoming data follows the required rules before saving it.

For example:

- Name should not be empty.
- Email should be valid.
- Mobile number should have the expected length.
- A particular field should be unique.

## 10.2 How do we add validation in a Serializer?

DRF supports field-level validation and object-level validation.

### 1. Field-level validation using `validate_fieldname()`

```python
from rest_framework import serializers


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'

    def validate_name(self, value):

        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                'Name must contain at least 3 characters.'
            )

        return value
```

The method name follows this pattern:

```python
validate_<field_name>()
```

### 2. Object-level validation using `validate()`

Use this when validation depends on multiple fields.

```python
def validate(self, attrs):

    if attrs.get('name') == 'Shiv' and not attrs.get('mobile'):
        raise serializers.ValidationError(
            'Mobile number is required.'
        )

    return attrs
```

### 3. Using validators

```python
from rest_framework.validators import UniqueValidator
```

Example:

```python
email = serializers.EmailField(
    validators=[
        UniqueValidator(
            queryset=Customer.objects.all()
        )
    ]
)
```

### 4. Run validation

```python
serializer = CustomerSerializer(data=request.data)

if serializer.is_valid():
    serializer.save()
else:
    print(serializer.errors)
```

**Important:** Always use `serializer.is_valid()` before accessing `validated_data` or calling `save()` for incoming data.

## 10.3 What is Nested Serializer?

A Nested Serializer allows us to represent related model data inside another serializer.

Example:

Suppose a customer has multiple orders.

```python
class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):

    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'orders']
```

Example response:

```json
{
    "id": 1,
    "name": "Shiv",
    "orders": [
        {
            "id": 1,
            "customer": 1,
            "amount": 500
        },
        {
            "id": 2,
            "customer": 1,
            "amount": 900
        }
    ]
}
```

**Important points:**

- Use `many=True` when the relationship contains multiple records.
- Use `read_only=True` when related data should only be displayed.
- Writable nested serializers require explicit create or update logic.
- Nested serializers should be designed carefully to avoid unnecessary database queries.

---

# 11. API Development and Advanced Features

## 11.1 What is Filtering and Searching?

Filtering means retrieving records that match particular conditions.

Searching means finding records based on search terms.

Example filtering:

```text
GET /api/customers/?status=true
```

Example searching:

```text
GET /api/customers/?search=shiv
```

DRF provides filter backends.

Install:

```bash
pip install django-filter
```

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django_filters',
]
```

Configure DRF:

```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ]
}
```

Example:

```python
from rest_framework import generics


class CustomerListAPIView(generics.ListAPIView):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    filterset_fields = ['status']
```

For searching:

```python
from rest_framework import filters


class CustomerListAPIView(generics.ListAPIView):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']
```

## 11.2 What is Pagination?

Pagination divides a large collection of records into smaller pages.

Example:

Instead of returning 1,000 customer records in one response, the API returns 10 or 20 records per page.

Configure:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',

    'PAGE_SIZE': 10,
}
```

Common pagination types:

- `PageNumberPagination`
- `LimitOffsetPagination`
- `CursorPagination`

Benefits:

- Reduces response size.
- Improves performance.
- Reduces unnecessary data transfer.
- Makes frontend rendering easier.

## 11.3 What is Throttling?

Throttling controls how frequently a client can make API requests.

Example:

A user is allowed to make only 100 API requests per hour.

DRF provides throttling classes such as:

- `AnonRateThrottle`
- `UserRateThrottle`
- `ScopedRateThrottle`

Configuration:

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],

    'DEFAULT_THROTTLE_RATES': {
        'anon': '20/hour',
        'user': '100/hour',
    }
}
```

**Why use throttling?**

- Controls request frequency.
- Helps protect application resources.
- Reduces accidental excessive requests.
- Helps manage API usage.

**Important:** DRF throttling is not a complete DDoS protection system or a substitute for infrastructure-level rate limiting.

## 11.4 What is API Versioning?

API versioning allows us to maintain different versions of an API while avoiding breaking existing clients.

Example:

```text
/api/v1/customers/
/api/v2/customers/
```

Suppose an Angular application uses API version 1. Later, we introduce new response fields or change the API structure.

Instead of breaking the existing application, we can provide version 2.

DRF supports:

- `URLPathVersioning`
- `NamespaceVersioning`
- `AcceptHeaderVersioning`
- `QueryParameterVersioning`
- `HostNameVersioning`

Example configuration:

```python
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS':
        'rest_framework.versioning.URLPathVersioning',

    'DEFAULT_VERSION': 'v1',

    'ALLOWED_VERSIONS': ['v1', 'v2'],
}
```

URL:

```python
path(
    'api/<str:version>/customers/',
    CustomerListAPIView.as_view()
)
```

## 11.5 What is Caching?

Caching stores frequently requested data temporarily so that it can be reused without repeatedly performing expensive operations.

Example:

Suppose a dashboard retrieves the total number of customers every time it loads.

Instead of running the same database query repeatedly, we can cache the result.

Django provides a caching framework.

Example using the cache API:

```python
from django.core.cache import cache


def get_customer_count():

    count = cache.get('customer_count')

    if count is None:
        count = Customer.objects.count()

        cache.set(
            'customer_count',
            count,
            timeout=300
        )

    return count
```

Here, the result is cached for 300 seconds.

Common caching options:

- Local-memory cache.
- Database cache.
- File-based cache.
- Memcached.
- Redis through an appropriate Django cache backend.

**Benefits:**

- Reduces repeated database queries.
- Improves response time.
- Reduces server workload.

**Important:** Cached data can become outdated. Plan cache invalidation when the underlying data changes.

## 11.6 What is Exception Handling in DRF?

Exception handling manages errors that occur while processing API requests.

DRF provides standard exceptions such as:

- `ValidationError`
- `NotAuthenticated`
- `PermissionDenied`
- `NotFound`
- `MethodNotAllowed`
- `Throttled`
- `AuthenticationFailed`

Example:

```python
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response


class CustomerDetailAPIView(APIView):

    def get(self, request, pk):

        try:
            customer = Customer.objects.get(pk=pk)

        except Customer.DoesNotExist:
            raise NotFound('Customer not found.')

        return Response({
            'id': customer.id,
            'name': customer.name
        })
```

### Custom exception handler

DRF allows us to define a custom exception handler.

```python
# utils.py

from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            'success': False,
            'errors': response.data
        }

    return response
```

Configure:

```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER':
        'myproject.utils.custom_exception_handler'
}
```

**Important:** Do not expose database passwords, stack traces or internal application details in production API responses.

## 11.7 What is API Documentation (Swagger/OpenAPI)?

API documentation describes how developers can use an API.

It commonly contains:

- API endpoints.
- HTTP methods.
- Request parameters.
- Request body structure.
- Response formats.
- Authentication requirements.
- Error responses.

OpenAPI is a standard specification for describing HTTP APIs.

Swagger UI is a browser-based interface that displays OpenAPI documentation and can allow developers to test endpoints.

Common Django tools include:

- `drf-spectacular`
- `drf-yasg`

Example using `drf-spectacular`:

Install:

```bash
pip install drf-spectacular
```

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'drf_spectacular',
]
```

Configure:

```python
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS':
        'drf_spectacular.openapi.AutoSchema',
}
```

URL configuration:

```python
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)

urlpatterns = [
    path(
        'api/schema/',
        SpectacularAPIView.as_view(),
        name='schema'
    ),

    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(
            url_name='schema'
        ),
        name='swagger-ui'
    ),
]
```

Open:

```text
http://127.0.0.1:8000/api/docs/
```

---

# 12. Django Signals and Utilities

## 12.1 What are Django Signals?

Django Signals allow different parts of an application to respond to events automatically.

Simple meaning:

**When something happens, Django can notify registered functions so they can perform another task.**

Real-life examples:

- When a new user is created, create a profile.
- When an order is placed, generate an invoice.
- When a record is deleted, perform a related cleanup operation.

### Without Signals

```python
user = User.objects.create_user(
    username='shiv',
    password='password'
)

Profile.objects.create(user=user)
```

The profile creation is written explicitly in the same workflow.

### With Signals

A signal receiver can create the profile when a new user is saved.

```python
# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    if created:
        Profile.objects.get_or_create(
            user=instance
        )
```

### Register signals

Inside the application's `apps.py`:

```python
from django.apps import AppConfig


class MyAppConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        from . import signals
```

Make sure the app configuration is registered in `INSTALLED_APPS`.

### Important signal arguments

| Argument | Meaning |
|---|---|
| `sender` | Model or class that sent the signal |
| `instance` | Current model object |
| `created` | Whether a new object was created |
| `**kwargs` | Additional signal information |

### Common Django Signals

| Signal | Trigger |
|---|---|
| `pre_save` | Before a model is saved |
| `post_save` | After a model is saved |
| `pre_delete` | Before a model is deleted |
| `post_delete` | After a model is deleted |
| `m2m_changed` | When a ManyToMany relationship changes |
| `request_started` | When Django starts processing a request |
| `request_finished` | When Django finishes processing a request |

Other signals include `pre_init`, `post_init`, `class_prepared`, `got_request_exception`, `pre_migrate`, `post_migrate` and `connection_created`.

**Important points:**

- Signals are synchronous by default.
- `QuerySet.update()` does not call each model's `save()` method and does not trigger `pre_save` or `post_save` for each affected object.
- `bulk_create()` also does not call each object's `save()` method or trigger normal save signals.
- Avoid putting large business workflows inside signals because they can make application behavior difficult to trace.
- `dispatch_uid` can prevent duplicate receiver registration.

### Custom Signals

We can create our own signals.

```python
# signals.py

from django.dispatch import Signal, receiver

order_placed = Signal()


@receiver(
    order_placed,
    dispatch_uid='order_placed_receiver'
)
def send_order_notification(sender, **kwargs):

    print('Order notification triggered')
```

Send the signal:

```python
order_placed.send(
    sender=None,
    order_id=1
)
```

### Difference between `send()` and `send_robust()`

| `send()` | `send_robust()` |
|---|---|
| Stops propagating when a receiver raises an exception | Catches receiver exceptions and continues to other receivers |
| Exceptions propagate to the sender | Returns exceptions as results |
| Use when receiver failure should propagate | Use when other receivers should still run |

Neither automatically makes a signal asynchronous.

## 12.2 What is `utils.py`?

`utils.py` usually contains reusable utility or helper functions.

It helps us avoid writing the same code repeatedly.

Example:

Suppose we need to send an email from several views.

Instead of repeating the email code in every view, create a reusable function.

```python
# utils.py

from django.core.mail import send_mail


def send_customer_email(subject, message, recipient):

    return send_mail(
        subject,
        message,
        'noreply@example.com',
        [recipient]
    )
```

Use it:

```python
from .utils import send_customer_email


def customer_view(request):

    send_customer_email(
        'Welcome',
        'Welcome to our application.',
        'customer@example.com'
    )
```

**Where can we create `utils.py`?**

Inside an app:

```text
customers/
    models.py
    views.py
    utils.py
```

Or as a project-level utility package:

```text
myproject/
    common/
        __init__.py
        utils.py
```

Use app-level utilities for app-specific logic and project-level utilities for genuinely shared functionality.

---

# 13. Advanced Django Concepts

## 13.1 What is Django Channels?

Django Channels extends Django to support protocols and communication patterns beyond traditional HTTP request-response handling.

It is commonly used for WebSocket-based applications.

Examples:

- Live chat applications.
- Real-time notifications.
- Live dashboards.
- Multiplayer applications.
- Real-time status updates.

### Traditional HTTP communication

```text
Client
  |
  | Request
  v
Django
  |
  | Response
  v
Client
```

### WebSocket communication

```text
Client <================> Server
        Persistent
        Connection
```

A WebSocket connection allows both the client and server to send messages over the same connection.

Django Channels commonly uses:

- Consumers.
- Routing.
- Channel layers.
- WebSocket connections.
- ASGI.

### What is a Consumer?

A Consumer is similar to a Django view, but it handles communication over a connection such as a WebSocket.

Simple example:

```python
# consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        await self.send(text_data=text_data)
```

This example accepts a WebSocket connection and sends received text back to the client.

## 13.2 How do we use Async in Django?

Django supports asynchronous views and several asynchronous operations.

An asynchronous function is defined using `async def`.

Example:

```python
from django.http import JsonResponse


async def home(request):

    return JsonResponse({
        'message': 'Async Django View'
    })
```

### Difference between synchronous and asynchronous views

Synchronous:

```python
def home(request):
    return JsonResponse({'message': 'Hello'})
```

Asynchronous:

```python
async def home(request):
    return JsonResponse({'message': 'Hello'})
```

### Using `await`

`await` is used to wait for an asynchronous operation without blocking the event loop in the usual asynchronous manner.

Example:

```python
import asyncio
from django.http import JsonResponse


async def home(request):

    await asyncio.sleep(2)

    return JsonResponse({
        'message': 'Completed'
    })
```

### Important points

- ASGI is generally preferred for deploying applications that need asynchronous request handling.
- Django supports both synchronous and asynchronous views.
- Not every Django operation has an asynchronous equivalent.
- Some database operations and third-party libraries may still be synchronous.
- Use `sync_to_async()` when an appropriate synchronous operation must be called from asynchronous code.
- Do not use blocking synchronous operations directly inside an async view if they can block the event loop.

## 13.3 What is Modular Programming and why do we use it?

Modular programming means dividing a large application into smaller, independent and reusable modules.

In Django, applications are commonly divided into modules such as:

- Customers.
- Orders.
- Products.
- Payments.
- Authentication.

Example:

```text
project/
│
├── customers/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── serializers.py
│
├── orders/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── serializers.py
│
└── products/
    ├── models.py
    ├── views.py
    ├── urls.py
    └── serializers.py
```

**Advantages:**

1. Easier maintenance.
2. Better code organization.
3. Reusability.
4. Easier testing.
5. Separation of responsibilities.
6. Better collaboration between developers.
7. Easier debugging.

---

# 14. Cookies and Sessions

## 14.1 What is a Cookie?

A cookie is a small piece of data stored by the browser and sent to the server with matching requests.

Example:

```python
from django.http import HttpResponse


def set_cookie(request):

    response = HttpResponse('Cookie created')

    response.set_cookie(
        'username',
        'shiv',
        max_age=3600
    )

    return response
```

Read cookie:

```python
def get_cookie(request):

    username = request.COOKIES.get('username')

    return HttpResponse(username or 'No cookie found')
```

## 14.2 What is a Session?

A session allows an application to store user-related state across multiple requests.

Django's default session backend stores session data on the server side and uses a session identifier in a browser cookie.

Example:

```python
def set_session(request):

    request.session['username'] = 'shiv'

    return HttpResponse('Session created')
```

Read session:

```python
def get_session(request):

    username = request.session.get('username')

    return HttpResponse(username or 'No session found')
```

Delete session key:

```python
del request.session['username']
```

## 14.3 Difference between Cookie and Session

| Feature | Cookie | Session |
|---|---|---|
| Storage | Browser | Usually server-side |
| Data sent with request | Cookie is sent to matching requests | Session identifier cookie is sent |
| Data size | Limited | Depends on session backend |
| Security | Client can inspect or modify ordinary cookie values | Server-side session data is not directly exposed in the session cookie |
| Expiry | Can have an expiry date | Configurable expiry |
| Common use | Preferences and identifiers | Login state and user-specific state |

**Important:**

- Cookies can be configured with `HttpOnly`, `Secure` and `SameSite`.
- Django's default session cookie contains a session identifier, not the entire session dictionary.
- Cookie-based session backends are an exception: they store signed session data in the cookie itself.
- Never store sensitive information in ordinary cookies without appropriate protection.

---

# 15. Frequently Asked Questions – Quick Revision

| Question | Short Answer |
|---|---|
| What is authentication? | Verifying a user's identity. |
| What is authorization? | Checking a user's permissions. |
| What is ORM? | A way to interact with databases using Python objects and methods. |
| What is `get_queryset()`? | A method used to customize a manager or view's queryset. |
| Can custom managers contain new methods? | Yes. |
| What is a Proxy Model? | A model that changes Python behavior without creating a new database table. |
| What is `get_absolute_url()`? | A model method that returns the object's canonical URL. |
| What is `reverse()`? | Resolves a named URL immediately. |
| What is `reverse_lazy()`? | Resolves a named URL lazily. |
| What is Aggregation? | Calculates summary values from querysets. |
| What is Annotation? | Adds calculated values to queryset objects. |
| What is N+1? | One initial query plus repeated queries for related records. |
| How to solve N+1? | Use `select_related()` or `prefetch_related()` as appropriate. |
| What is a Serializer? | Converts and validates data. |
| What is a Mixin? | A reusable class that provides functionality through inheritance. |
| What is APIView? | A DRF class for handling HTTP methods. |
| What is ViewSet? | A class that groups related API actions. |
| What is GenericAPIView? | A base DRF view that provides common queryset and serializer behavior. |
| What is DefaultRouter? | Automatically generates URL patterns for registered ViewSets. |
| What is Throttling? | Controls how frequently clients can access an API. |
| What is Pagination? | Divides large result sets into smaller pages. |
| What is Caching? | Temporarily stores data for faster reuse. |
| What is API Versioning? | Maintains different versions of an API. |
| What is Django Channels? | Adds support for WebSockets and other communication patterns. |
| What is a Signal? | An event notification mechanism. |
| What is `utils.py`? | A module for reusable helper functions. |
| What is `dj-database-url`? | Converts database URLs into Django database configuration. |
| What is `dumpdata`? | Exports database data into a serialized format. |
| What is `loaddata`? | Loads fixture data into the database. |
| What is `*args`? | Variable positional arguments stored in a tuple. |
| What is `**kwargs`? | Variable keyword arguments stored in a dictionary. |

---

# 16. Important Django and DRF Commands

## Django Commands

```bash
# Create project
django-admin startproject myproject

# Create app
python manage.py startapp customers

# Run server
python manage.py runserver

# Generate migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Export data
python manage.py dumpdata

# Import data
python manage.py loaddata data.json

# Preview migration SQL
python manage.py sqlmigrate customers 0001

# Show migration status
python manage.py showmigrations

# Open Django shell
python manage.py shell

# Run system checks
python manage.py check
```

## DRF Installation

```bash
pip install djangorestframework
```

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'rest_framework',
]
```

## Useful Additional Packages

```bash
# Filtering
pip install django-filter

# API documentation
pip install drf-spectacular

# Database URL configuration
pip install dj-database-url

# API request testing
pip install httpie
```

---

# Final Revision Notes

1. **WSGI vs ASGI:** WSGI supports traditional synchronous applications; ASGI supports synchronous and asynchronous applications and can support WebSockets.
2. **Migrations:** `makemigrations` creates migration files; `migrate` applies them.
3. **FBV vs CBV:** Both can be powerful; choose based on code structure and requirements.
4. **Authentication vs Authorization:** Identity verification vs permission checking.
5. **ORM optimization:** Use `select_related()`, `prefetch_related()`, indexes and appropriate queryset methods.
6. **Managers:** Use custom managers to organize reusable query logic.
7. **Proxy models:** Change model behavior without adding another database table.
8. **Aggregation vs Annotation:** Summary calculation vs calculated values attached to queryset records.
9. **APIView vs ViewSet:** Explicit HTTP handlers vs grouped resource actions.
10. **Generic Views and Mixins:** Reduce repeated API code.
11. **Serializers:** Handle conversion and validation of API data.
12. **Signals:** Respond to application events, but avoid hiding important business logic inside them.
13. **Channels and Async:** Useful for real-time and asynchronous application requirements.
14. **API security:** Use authentication, permissions, HTTPS, validation and appropriate throttling.
15. **API performance:** Use pagination, filtering, caching and ORM optimization.

