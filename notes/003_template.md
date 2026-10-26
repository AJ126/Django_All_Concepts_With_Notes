# Django Templates – Complete Notes

## 1. What Is a Template in Django?

In Django, it is generally not recommended to write large amounts of HTML directly inside a view.

For example, writing HTML inside a Python view can make the code difficult to read and maintain because Python and HTML are mixed together.

### Example: HTML Inside a View (Not Recommended for Large Pages)

```python
from django.http import HttpResponse

def home(request):
    html = """
        <html>
            <body>
                <h1>Welcome to Django</h1>
            </body>
        </html>
    """
    return HttpResponse(html)
```

### Problems with This Approach

- Python and HTML are mixed together.
- The code becomes difficult to maintain.
- Reusing HTML across multiple pages becomes harder.
- Designers and developers cannot easily work on separate parts of the application.

### Solution: Use Django Templates

A **template** is an HTML file that can contain dynamic data and Django Template Language (DTL) syntax.

For example, we can create a separate HTML file named `home.html` and render it through a Django view.

```python
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
```

This keeps the view and HTML separate.

## 2. Creating a Templates Folder

A project-level `templates` folder can be shared by multiple applications in the same Django project.

### Project Structure

```text
project_name/
│
├── manage.py
│
├── project_name/
│   ├── settings.py
│   └── urls.py
│
├── app_one/
│   └── views.py
│
├── app_two/
│   └── views.py
│
└── templates/
    ├── home.html
    ├── about.html
    │
    ├── app_one/
    │   └── index.html
    │
    └── app_two/
        └── index.html
```

You can organize templates in either of these ways:

1. Place HTML files directly inside the project-level `templates` folder.
2. Create application-specific subfolders inside `templates`.

Using application-specific subfolders helps avoid filename conflicts when multiple applications contain templates with the same name.

## 3. Configure Templates in `settings.py`

### A. Old Method Using `os.path`

Older Django tutorials often use the `os` module to define directory paths.

```python
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

template_dir = os.path.join(BASE_DIR, 'templates')
```

Then configure the `TEMPLATES` setting:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [template_dir],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### B. Modern Method Using `pathlib`

Modern Django projects generally use `pathlib.Path`.

A typical project already contains:

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
```

Configure the `TEMPLATES` setting like this:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

**Important correction:** This is incorrect:

```python
'DIRS': [BASE_DIR, 'templates'],
```

It creates two separate list entries rather than one complete path. Use:

```python
'DIRS': [BASE_DIR / 'templates'],
```

### What Do `DIRS` and `APP_DIRS` Mean?

- `DIRS`: Specifies additional directories where Django searches for templates.
- `APP_DIRS=True`: Allows Django to search for templates inside installed applications' `templates` directories.

For example, Django can discover a template at `app_one/templates/app_one/index.html` when `app_one` is installed and the standard template loader configuration is enabled.

## 4. What Is Django Template Language (DTL)?

Django Template Language allows us to display dynamic data, apply conditions, loop over data, and reuse HTML layouts.

DTL is not Python syntax and is not ordinary HTML syntax. It is a template language interpreted by Django.

There are three important syntax styles:

| Syntax | Purpose | Example |
|---|---|---|
| `{{ }}` | Display a variable or expression result | `{{ name }}` |
| `{% %}` | Execute template logic or a template tag | `{% if name %}` |
| `{# #}` | Add a template comment | `{# This is a comment #}` |

**Note:** Django Template Language is different from Jinja, although both use similar syntax.

## 5. Display Dynamic Data in a Template

We can pass data from a view to an HTML template using a **context dictionary**.

### Step 1: Create a View

File: `views.py`

```python
from django.shortcuts import render

def home(request):
    context = {
        'name': 'Akash',
        'city': 'Pune',
    }

    return render(request, 'home.html', context)
```

### Step 2: Display the Data in a Template

File: `templates/home.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Home Page</title>
</head>
<body>
    <h1>Welcome, {{ name }}!</h1>
    <p>City: {{ city }}</p>
</body>
</html>
```

### Output

```text
Welcome, Akash!
City: Pune
```

Here, `name` and `city` are keys in the context dictionary. Django makes their values available to the template.

## 6. Template Variables

Template variables display values supplied by the view or obtained through supported template lookups.

### Syntax

```django
{{ variable_name }}
```

Example:

```django
{{ name }}
{{ age }}
{{ student.name }}
```

If a view passes a dictionary like this:

```python
context = {
    'name': 'Akash',
    'age': 25,
}
```

The template can display:

```html
<h1>{{ name }}</h1>
<p>Age: {{ age }}</p>
```

Django replaces these expressions with the corresponding values when rendering the template.

## 7. Template Tags

Template tags use `{% %}` syntax to perform template operations, such as conditions, loops, loading static files, and template inheritance.

### A. `if` and `else`

Use conditions to display different content depending on the supplied data.

```django
{% if data %}
    <p>Data is available.</p>
{% else %}
    <p>No data is available.</p>
{% endif %}
```

### B. `for` Loop

Use a loop to display items from a list or another iterable.

```django
{% for student in students %}
    <p>{{ student.name }}</p>
{% empty %}
    <p>No students found.</p>
{% endfor %}
```

The optional `{% empty %}` section is displayed when the iterable has no items.

### C. `with` Tag

Use `{% with %}` to assign a value to a temporary template variable.

```django
{% with data as value %}
    <p>{{ value }}</p>
{% endwith %}
```

You can also use a more explicit example:

```django
{% with name="Akash" %}
    <p>{{ name }}</p>
{% endwith %}
```

The temporary variable is available within the `with` block.

## 8. Template Inheritance

Template inheritance allows multiple pages to share a common HTML layout.

For example, several pages may use the same navigation bar, header, footer, and CSS files. Instead of repeating that HTML in every page, create a base template and extend it.

### A. Create `base.html`

File: `templates/base.html`

```django
<!DOCTYPE html>
{% load static %}

<html>
<head>
    <title>{% block title %}My Website{% endblock %}</title>

    <link rel="stylesheet" href="{% static 'css/base.css' %}">
</head>
<body>

    <header>
        <h1>My Django Website</h1>
    </header>

    <main>
        {% block body %}
        {% endblock %}
    </main>

    <footer>
        <p>Copyright 2026</p>
    </footer>

</body>
</html>
```

### B. Create a Child Template

File: `templates/home.html`

```django
{% extends 'base.html' %}

{% block title %}Home Page{% endblock %}

{% block body %}
    <h2>Welcome to the Home Page</h2>
    <p>This content comes from the child template.</p>
{% endblock %}
```

### How Does It Work?

- `{% extends 'base.html' %}` tells Django to use the base template.
- `{% block title %}` overrides the title block defined in the base template.
- `{% block body %}` supplies content for the corresponding block in the base template.
- `{% endblock %}` closes a block.

**Important rules:**

1. The `{% extends %}` tag should normally be the first template tag in the child template.
2. The base template defines the blocks.
3. The child template fills in or overrides those blocks.
4. Put `{% load static %}` in the template where it is needed. Inheritance does not automatically make every library loaded in one template available to another.

## 9. URL Template Tag

The `{% url %}` tag generates a URL from the name of a URL pattern.

This is preferable to hardcoding URLs because the URL can change without requiring you to update every template link.

### A. Create a Named URL Pattern

File: `urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update/<int:context_id>/', views.update, name='update'),
]
```

The view functions `index` and `update` must exist.

### B. Create a Link to the Index Page

```django
<a href="{% url 'index' %}">Back</a>
```

### C. Create a Link to the Update Page

```django
<a href="{% url 'update' data.id %}">Update</a>
```

Here, `data.id` supplies the ID required by the URL pattern.

**Note:** If the URL is declared inside an application and that application's URLs are namespaced, the URL name may need to include the namespace, for example `{% url 'student_app:index' %}`.

## 10. Custom Template Tags

Django provides many built-in template tags. Sometimes, however, an application needs custom template behavior.

In that case, we can create **custom template tags**.

Common uses include:

- Formatting or calculating values.
- Returning data for a reusable template component.
- Performing small pieces of presentation-related processing.

### Important Correction: Modern Django Helpers

The three helper types in older notes need an update:

- `simple_tag`: Runs a function and returns a value that can be displayed in the template.
- `inclusion_tag`: Runs a function and renders a specified template using the returned context.
- `assignment_tag`: This was used to assign a function's result to a template variable, but it was removed in Django 2.0. In modern Django, use `simple_tag` with the `as` syntax instead.

### Step 1: Create a `templatetags` Folder

Inside your Django application, create a folder named `templatetags`.

```text
student_app/
├── __init__.py
├── views.py
├── models.py
└── templatetags/
    ├── __init__.py
    └── custom_tags.py
```

Both `student_app` and `templatetags` should be Python packages, so include the `__init__.py` files.

### Step 2: Create a Custom `simple_tag`

File: `student_app/templatetags/custom_tags.py`

```python
from django import template

register = template.Library()

@register.simple_tag
def greet(name):
    return f"Hello, {name}!"
```

### Step 3: Load and Use the Custom Tag

In your template:

```django
{% load custom_tags %}

<p>{% greet "Akash" %}</p>
```

Output:

```text
Hello, Akash!
```

You can also assign the result to a variable:

```django
{% load custom_tags %}

{% greet "Akash" as greeting %}
<p>{{ greeting }}</p>
```

### Step 4: Create an `inclusion_tag`

An inclusion tag renders a separate template.

Add this function to `custom_tags.py`:

```python
@register.inclusion_tag('student_app/student_list.html')
def show_students(students):
    return {'students': students}
```

Create `templates/student_app/student_list.html`:

```django
<ul>
    {% for student in students %}
        <li>{{ student.name }}</li>
    {% empty %}
        <li>No students found.</li>
    {% endfor %}
</ul>
```

Use the tag in a parent template after passing a `students` collection into its context:

```django
{% load custom_tags %}

{% show_students students %}
```

### Important Notes About Custom Tags

1. The application containing the `templatetags` package must be installed in `INSTALLED_APPS`.
2. Restart the development server after creating a new custom tag module if Django does not detect it.
3. Use `simple_tag` for simple computations and values.
4. Use `inclusion_tag` when a function should render a reusable template component.
5. Use modern `simple_tag` assignment syntax instead of the removed `assignment_tag`.

---

## Quick Revision

| Concept | Syntax or File | Purpose |
|---|---|---|
| Template | `home.html` | Separates HTML from Python view logic |
| Template directory | `templates/` | Stores HTML templates |
| Template variable | `{{ name }}` | Displays dynamic data |
| Template tag | `{% if data %}` | Performs template operations |
| Template inheritance | `{% extends 'base.html' %}` | Reuses a common layout |
| Template block | `{% block body %}` | Defines a replaceable section |
| URL tag | `{% url 'index' %}` | Generates a URL from its name |
| Simple custom tag | `@register.simple_tag` | Returns a value from a Python function |
| Inclusion custom tag | `@register.inclusion_tag(...)` | Renders a reusable template component |
| Template configuration | `TEMPLATES` in `settings.py` | Configures template discovery and rendering |