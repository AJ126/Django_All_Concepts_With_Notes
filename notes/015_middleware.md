# Django Middleware – Complete Notes

## 1. What is Middleware in Django?

Middleware is a framework of hooks that allows us to execute code during Django's request and response processing.

In simple words:

**Middleware is a layer between the client and Django's view that allows us to perform operations before and after a view executes.**

It is a lightweight, low-level plugin system that allows us to globally modify or process incoming requests and outgoing responses.

### Real-life example

Consider a security guard at an office entrance.

1. A visitor arrives at the office.
2. The security guard checks the visitor's identity.
3. If everything is correct, the visitor is allowed to enter.
4. The visitor completes their work.
5. Before leaving, the security guard may check their exit pass.

Django middleware works similarly:

- Before the view executes, middleware can check the request.
- After the view executes, middleware can check or modify the response.

### Django request-response flow

**Request flow:**

```text
Client
  |
  | HTTP Request
  v
Middleware 1
  |
  v
Middleware 2
  |
  v
Middleware 3
  |
  v
URL Resolver
  |
  v
View Function / Class-Based View
  |
  | HTTP Response
  v
Middleware 3
  |
  v
Middleware 2
  |
  v
Middleware 1
  |
  v
Client
```

**Important:** Request processing generally follows middleware registration order, while response processing follows the reverse order.

---

## 2. Why Do We Need Middleware?

Suppose we have 100 views in our Django project and we want to perform the following operations:

- Check whether the user is authenticated.
- Log every incoming request.
- Track how much time a request takes.
- Add security headers to responses.
- Handle certain exceptions.
- Check whether a particular IP address is blocked.

We could write this logic separately inside every view, but that would create duplicate code.

Instead, we can write the logic once inside middleware.

Django will automatically execute the middleware for applicable requests.

### Common real-life use cases

| Requirement | Middleware usage |
|---|---|
| Request logging | Record incoming URLs and request methods |
| Authentication checks | Check whether a user is logged in |
| Security | Add or validate security-related headers |
| Performance monitoring | Calculate request processing time |
| IP restrictions | Block requests from specific IP addresses |
| Response modification | Add custom headers to responses |
| Error handling | Return a custom response for certain exceptions |

**Note:** Django authentication and authorization are different concepts. Authentication middleware makes the current user available; permission checks are generally handled separately.

---

## 3. Built-in Middleware in Django

Django provides several built-in middleware classes.

They are configured inside the `MIDDLEWARE` list in `settings.py`.

Example:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

### Important built-in middleware

| Middleware | Purpose |
|---|---|
| `SecurityMiddleware` | Provides security-related protections and headers |
| `SessionMiddleware` | Enables session handling |
| `CommonMiddleware` | Provides common request and response processing |
| `CsrfViewMiddleware` | Protects against Cross-Site Request Forgery (CSRF) |
| `AuthenticationMiddleware` | Adds the current user to the request |
| `MessageMiddleware` | Enables temporary messages for users |
| `XFrameOptionsMiddleware` | Helps prevent clickjacking through frame restrictions |

### Example: AuthenticationMiddleware

When we use:

```python
request.user
```

inside a view, Django provides information about the currently authenticated user.

The built-in `AuthenticationMiddleware` makes this possible.

Example:

```python
def home(request):

    if request.user.is_authenticated:
        return HttpResponse("Welcome, authenticated user!")

    return HttpResponse("Please log in.")
```

### Important point

Middleware is generally executed for every request that passes through Django's middleware chain.

However, middleware can short-circuit the request by returning a response early. Some middleware methods also run only under specific conditions.

---

## 4. Custom Middleware in Django

Apart from built-in middleware, Django allows us to create our own middleware based on our requirements.

A custom middleware is generally a Python class.

For modern Django middleware, the basic structure is:

```python
class MyMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Code before the view
        response = self.get_response(request)

        # Code after the view
        return response
```

Let's understand each method.

### A. `__init__()` method

The `__init__()` method is called when Django initializes the middleware.

It is generally called once per middleware instance when the application loads the middleware chain.

Its main responsibilities are:

- Perform one-time initialization.
- Store configuration.
- Store the next middleware or handler reference.

Example:

```python
class MyMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response

        print("Middleware initialized")
```

Here, `get_response` is a callable that invokes the next middleware in the chain or, eventually, the Django view handler.

### B. `__call__()` method

The `__call__()` method is executed whenever a request passes through this middleware.

It is responsible for processing the request and response.

Example:

```python
class MyMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        print("Before View")

        response = self.get_response(request)

        print("After View")

        return response
```

Execution:

```text
Request received
      |
      v
Before View
      |
      v
Django View executes
      |
      v
After View
      |
      v
Response returned
```

**Important:** Always return the response from `__call__()` unless you intentionally return an alternative response.

---

## 5. Optional Middleware Hooks

Django provides additional middleware hooks that can be implemented when required.

Common hooks include:

1. `process_view()`
2. `process_exception()`
3. `process_template_response()`

These are optional. You do not need to implement them in every middleware.

### A. `process_view()`

This method executes just before Django calls the selected view.

It provides access to:

- `request`: The current HTTP request.
- `view_func`: The selected view function.
- `view_args`: Positional arguments passed to the view.
- `view_kwargs`: Keyword arguments passed to the view.

Syntax:

```python
def process_view(self, request, view_func, view_args, view_kwargs):

    # Logic before the view executes

    return None
```

Example:

```python
class ViewCheckMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):

        print("Selected view:", view_func.__name__)

        print("View arguments:", view_args)

        print("View keyword arguments:", view_kwargs)

        return None
```

**Important:**

- Return `None` to allow the view to execute normally.
- Return an `HttpResponse` object to stop further request processing and return that response instead.
- This hook is called after URL resolution and before the view executes.

### B. `process_exception()`

This method is executed when an exception is raised during the execution of a view.

It allows us to handle certain view exceptions and return a custom response.

Syntax:

```python
def process_exception(self, request, exception):

    # Logic to handle the exception

    return None
```

Example:

```python
from django.http import HttpResponse

class ErrorMessageMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):

        return HttpResponse(
            "<h1>Currently we are facing some technical problems. Please try again later!</h1>",
            status=500
        )
```

**Important:**

- `exception` contains the exception object.
- Return an `HttpResponse` to handle the exception.
- Return `None` to allow Django's normal exception handling to continue.
- This hook is for exceptions raised by the view, not a general handler for every possible middleware or server error.

### C. `process_template_response()`

This method is executed after a view returns a response that supports template-response processing, such as Django's `TemplateResponse`.

It is useful when we want to modify:

- Template context.
- Template information.
- Other properties of the template response.

Syntax:

```python
def process_template_response(self, request, response):

    # Modify template response

    return response
```

Example:

```python
class TemplateResponseMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        return response

    def process_template_response(self, request, response):

        response.context_data['website_name'] = 'My Django Website'

        return response
```

For this example, the view must return a template response:

```python
from django.template.response import TemplateResponse

def home(request):

    return TemplateResponse(
        request,
        'home.html',
        {'message': 'Welcome'}
    )
```

Inside `home.html`:

```html
<h1>{{ message }}</h1>

<h2>{{ website_name }}</h2>
```

**Important:** This hook is not called for every `HttpResponse`. It applies to responses that implement template-response processing, such as `TemplateResponse`.

---

## 6. Execution Order of Middleware Methods

Let's understand the execution sequence for a single middleware class.

Consider:

```python
class MyMiddleware:

    def __init__(self, get_response):

        print("1. Middleware initialized")

        self.get_response = get_response

    def __call__(self, request):

        print("2. Before View")

        response = self.get_response(request)

        print("6. After View")

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        print("3. Process View")

        return None

    def process_exception(self, request, exception):

        print("Exception occurred")

        return None

    def process_template_response(self, request, response):

        print("Template response processing")

        return response
```

### Normal request execution

For a normal request where the view returns an ordinary `HttpResponse`, the sequence is:

```text
1. __init__()                  Application initialization
2. __call__()                  Before view
3. process_view()              Before view
4. View function executes
5. View function returns response
6. __call__()                  After view
7. Response returned
```

The initialization step does not run again for each request.

### When the view raises an exception

```text
__call__() - Before view
      |
      v
process_view()
      |
      v
View executes
      |
      v
Exception raised
      |
      v
process_exception()
      |
      v
Custom response or normal exception handling
```

The `process_exception()` hook runs for an exception raised during view execution.

If an exception hook returns a response, Django uses that response. Otherwise, normal exception handling continues.

### When the view returns TemplateResponse

```text
__call__() - Before view
      |
      v
process_view()
      |
      v
View executes
      |
      v
TemplateResponse returned
      |
      v
process_template_response()
      |
      v
Template response rendered
      |
      v
__call__() - After view
      |
      v
Response returned
```

**Note:** This sequence describes one middleware's hooks. With multiple middleware classes, the order of their hooks is affected by the overall middleware chain.

---

## 7. Practical Example: Custom Error Middleware

### Requirement

Suppose we have a Django application with many views.

Sometimes a view may raise an exception. Instead of displaying an unfriendly error page, we want to return a meaningful response to the user.

We can use `process_exception()` for this purpose.

### Step 1: Create `middleware.py`

Inside your Django app, create:

```text
app_name/
    __init__.py
    admin.py
    apps.py
    middleware.py
    models.py
    views.py
```

### Step 2: Write the middleware

`middleware.py`

```python
from django.http import HttpResponse


class ErrorMessageMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        return response

    def process_exception(self, request, exception):

        print("Exception:", exception)

        return HttpResponse(
            """
            <h1>Something went wrong!</h1>
            <p>We are currently facing a technical problem.</p>
            <p>Please try again later.</p>
            """,
            status=500
        )
```

### Step 3: Register middleware in `settings.py`

Add your middleware to the `MIDDLEWARE` list:

```python
MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'app_name.middleware.ErrorMessageMiddleware',
]
```

Replace `app_name` with your actual Django app name.

### Step 4: Create a view that raises an exception

`views.py`

```python
from django.http import HttpResponse


def home(request):

    result = 10 / 0

    return HttpResponse("Home Page")
```

Here, dividing 10 by 0 raises a `ZeroDivisionError`.

### Step 5: Configure URL

`urls.py`

```python
from django.urls import path

from . import views

urlpatterns = [

    path('', views.home, name='home'),

]
```

### Step 6: Run the server

```bash
python manage.py runserver
```

Open your home page in the browser.

Instead of the normal Django error page, the custom error response will be returned.

**Note:** This example is for learning. In production, log unexpected exceptions securely and avoid exposing internal exception details to users. Django's normal exception handling should remain available for errors outside the scope of this middleware.

---

## 8. How to Register Custom Middleware

We must register custom middleware inside the `MIDDLEWARE` setting.

Example:

```python
MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'app_010_class_based_view.middleware.MyMiddleware',

]
```

### Important rules

1. The middleware class must be importable using the specified Python path.
2. Middleware order matters.
3. Middleware request processing generally follows top-to-bottom order.
4. Middleware response processing generally follows bottom-to-top order.
5. A middleware can return a response early and prevent later request processing.
6. `__init__()` should be used for one-time setup, not request-specific processing.

---

## 9. Middleware vs Decorators

Middleware and decorators can both execute additional logic around views, but they have different purposes.

| Middleware | Decorators |
|---|---|
| Generally applies globally to requests | Usually applied to selected views or functions |
| Registered in `settings.py` | Added above a function or method |
| Can process requests and responses | Can wrap a particular function or view |
| Useful for common application-wide logic | Useful for view-specific logic |
| Can use middleware hooks | Uses wrapper functions |

Example of a decorator:

```python
from functools import wraps

from django.http import HttpResponse


def check_user_login(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:

            return HttpResponse("Please log in first.")

        return view_func(request, *args, **kwargs)

    return wrapper
```

Usage:

```python
@check_user_login
def dashboard(request):

    return HttpResponse("Dashboard")
```

Use middleware when the logic should be applied broadly. Use decorators when it should be applied only to particular views.

---

## 10. Common Mistakes in Middleware

### Mistake 1: Forgetting to return the response

Incorrect:

```python
def __call__(self, request):

    response = self.get_response(request)
```

Correct:

```python
def __call__(self, request):

    response = self.get_response(request)

    return response
```

Without returning a response, the middleware chain cannot work correctly.

### Mistake 2: Forgetting to register middleware

Creating a `middleware.py` file is not enough.

You must add its dotted Python path to `MIDDLEWARE` in `settings.py`.

### Mistake 3: Using `process_exception()` for every error

`process_exception()` is intended for exceptions raised during view execution. It is not a universal handler for all application, middleware, or server errors.

### Mistake 4: Assuming `process_template_response()` runs for every response

It only runs for template responses that support the required rendering interface.

### Mistake 5: Performing request-specific work inside `__init__()`

Incorrect:

```python
def __init__(self, get_response):

    print("Request received")
```

This runs during middleware initialization, not for every request.

Correct:

```python
def __call__(self, request):

    print("Request received")

    response = self.get_response(request)

    return response
```

### Mistake 6: Storing request-specific data on the middleware instance

Middleware instances can handle multiple requests. Avoid storing information about the current request in instance attributes because that data could be shared across requests.

Use local variables or `request` attributes instead.

---

## 11. Quick Revision

| Method | When does it execute? | Purpose |
|---|---|---|
| `__init__()` | Middleware initialization | One-time configuration |
| `__call__()` | For each request passing through the middleware | Process request and response |
| `process_view()` | Before the view executes | Inspect or stop view execution |
| `process_exception()` | When the view raises an exception | Handle view exceptions |
| `process_template_response()` | When the view returns a template response | Modify template response/context |

### Important points to remember

- Middleware is a layer between the client and Django's view processing.
- It can execute logic before and after a view.
- Django provides built-in middleware.
- We can create custom middleware using a Python class.
- `__init__()` is used for initialization.
- `__call__()` is the core middleware entry point.
- `process_view()` runs before the selected view.
- `process_exception()` handles exceptions raised by the view.
- `process_template_response()` processes template responses.
- Custom middleware must be registered in `settings.py`.
- Request and response middleware ordering is important.

---

## 12. Practice Questions

Try answering these questions to check your understanding.

1. What is middleware in Django?
2. Why do we need middleware when we can write logic inside views?
3. What is the difference between `__init__()` and `__call__()`?
4. When does `process_view()` execute?
5. What is the purpose of `process_exception()`?
6. Does `process_template_response()` execute for every `HttpResponse`?
7. Where do we register custom middleware?
8. What happens if we forget to return the response from `__call__()`?
9. What is the difference between middleware and decorators?
10. Why does middleware response processing generally happen in reverse order?

### Practical task

Create a custom middleware that:

1. Prints the requested URL before the view executes.
2. Prints the HTTP method (`GET`, `POST`, etc.).
3. Calculates how much time the view takes to execute.
4. Prints the response status code after the view executes.

Hint: Use Python's `time` module and `request.path`, `request.method`, and `response.status_code`.

This exercise will help you understand the most important part of Django middleware: processing requests and responses globally.