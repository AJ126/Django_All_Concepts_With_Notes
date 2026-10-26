# Django Template Inheritance – Complete Notes

## 1. What Is Template Inheritance?

When multiple HTML templates contain common code, such as a navbar, footer, Bootstrap CSS, JavaScript files, or page layout, writing the same code in every template is not recommended.

It:
- Increases code duplication.
- Makes templates longer and harder to read.
- Increases development and maintenance time.
- Makes changes difficult because the same code must be updated in multiple files.

**Template inheritance** allows us to place common HTML code in a single file called `base.html` and reuse it in other templates.

The child templates extend the base template and provide their own content inside predefined blocks.

### Real-life example

Imagine a website with Home, About, and Contact pages.

All three pages share:
- A navbar
- A footer
- Bootstrap CSS
- Common JavaScript files

Only the page content changes.

Instead of repeating the common code in every template, we create one `base.html` file and extend it in all three pages.

## 2. How Template Inheritance Works

<escape>
base.html
    |
    |-- Common HTML structure
    |-- Bootstrap CSS and JavaScript
    |-- Navbar and footer
    |-- {% block content %}{% endblock %}
                 |
        -----------------------
        |          |          |
     home.html  about.html  contact.html
</escape>

The base template defines the common structure, while child templates fill the blocks with page-specific content.

## 3. Recommended Folder Structure

```text
myproject/
│
├── myproject/
│   ├── settings.py
│   └── urls.py
│
├── myapp/
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       ├── base.html
│       ├── home.html
│       └── about.html
│
└── manage.py
```

This example assumes the application's templates directory is configured for Django to discover.

## 4. Create the Base Template

Create `base.html` inside the templates directory.

**`base.html`**

```html
<!DOCTYPE html>
{% load static %}

<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1">

    <title>Django All Concepts</title>

    <link rel="stylesheet"
          href="{% static 'css/bootstrap.css' %}">

    <link rel="stylesheet"
          href="{% static 'css/base.css' %}">

    {% block style %}
    {% endblock style %}
</head>

<body>
    <div class="container mt-3">
        <h1>Welcome to Django All Concepts</h1>

        {% block body %}
        {% endblock body %}
    </div>

    <script src="{% static 'js/bootstrap.bundle.min.js' %}"></script>

    {% block scripts %}
    {% endblock scripts %}
</body>
</html>
```

### Explanation

| Code | Purpose |
|---|---|
| `{% load static %}` | Loads Django's static-file template tag library. |
| `{% static 'css/base.css' %}` | Generates the URL for a static file. |
| `{% block style %}` | Allows child templates to add page-specific CSS. |
| `{% block body %}` | Allows child templates to add page-specific HTML content. |
| `{% block scripts %}` | Allows child templates to add page-specific JavaScript. |

**Important:** Make sure the Bootstrap JavaScript filename matches the file you actually have. If you are using a Bootstrap version that requires Popper, `bootstrap.bundle.min.js` is generally the convenient choice.

## 5. Create a Child Template

Create `home.html` in the same templates directory.

**`home.html`**

```html
{% extends 'base.html' %}

{% block style %}
<style>
    .home-title {
        color: blue;
    }
</style>
{% endblock style %}

{% block body %}
    <h2 class="home-title">Home Page</h2>

    <p>Welcome to our Django learning website.</p>

    <button class="btn btn-primary">
        Learn Django
    </button>
{% endblock body %}
```

### Explanation

- `{% extends 'base.html' %}` tells Django that this template inherits from `base.html`.
- `{% block style %}` supplies page-specific CSS.
- `{% block body %}` supplies page-specific HTML.
- The child template does not need to repeat the complete HTML structure, `<head>`, or `<body>`.

**Important rule:** Put `{% extends 'base.html' %}` at the beginning of the child template, before other template tags or ordinary HTML. Whitespace and comments before it are generally harmless, but placing it first is the clearest practice.

A child block replaces the corresponding parent block by default. If you want to preserve the parent block's content and add to it, use `{{ block.super }}` inside the child block.

## 6. Display the Template Using a View

**`views.py`**

```python
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
```

**`urls.py`**

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
```

If your application has its own `urls.py`, include those URLs in the project's main URL configuration.

When the user visits the Home page, Django renders `home.html` and combines it with the blocks from `base.html`.

## 7. Benefits of Template Inheritance

- **Code reusability:** Common HTML is written once.
- **Maintainability:** Update the navbar or footer in one place.
- **Consistency:** Every page shares the same layout.
- **Readability:** Child templates contain mostly page-specific content.
- **Faster development:** New pages can reuse the existing layout.

### Quick revision

| Template tag | Meaning |
|---|---|
| `{% extends 'base.html' %}` | Inherits from a parent template. |
| `{% block body %}` | Defines a replaceable content area. |
| `{% endblock body %}` | Ends the block. |
| `{{ block.super }}` | Includes the parent block's content. |
| `{% include 'navbar.html' %}` | Includes another template fragment. |

---

# Django Template Filters – Complete Notes

## 1. What Are Template Filters?

Template filters modify or format values before displaying them in an HTML template.

For example, you might want to:
- Convert text to uppercase.
- Convert text to lowercase.
- Display a string in title case.
- Show only part of a string.
- Format a date or number.

Django provides many built-in filters, and you can also create your own custom filters.

### Syntax

```django
{{ value|filtername }}
```

A filter can optionally receive an argument:

```django
{{ value|filtername:"argument" }}
```

For example:

```django
{{ name|upper }}
{{ name|truncatechars:10 }}
{{ price|floatformat:2 }}
```

## 2. Common Built-in Template Filters

Assume the following values are passed from a view:

```python
def filter_demo(request):
    context = {
        'name': 'django framework',
        'message': 'Welcome to Django template filters',
        'price': 125.5,
    }

    return render(request, 'filter_demo.html', context)
```

In `filter_demo.html`:

| Filter | Example | Output |
|---|---|---|
| `upper` | `{{ name\|upper }}` | `DJANGO FRAMEWORK` |
| `lower` | `{{ name\|lower }}` | `django framework` |
| `title` | `{{ name\|title }}` | `Django Framework` |
| `capfirst` | `{{ name\|capfirst }}` | `Django framework` |
| `truncatechars` | `{{ message\|truncatechars:10 }}` | `Welcome...` |
| `floatformat` | `{{ price\|floatformat:2 }}` | `125.50` |
| `length` | `{{ name\|length }}` | `16` |
| `default` | `{{ missing\|default:"N/A" }}` | `N/A` if the value is missing or falsey |

Filters are applied to the value before Django displays it.

---

## 3. How to Create Custom Template Filters

Custom filters let us define our own text formatting or transformation logic.

Follow these steps:

1. Create a `templatetags` folder inside the Django application.
2. Add an `__init__.py` file inside it.
3. Create a Python file for the custom filters.
4. Register each filter using `template.Library()`.
5. Load the custom filter library in the HTML template.

### Folder structure

```text
myapp/
│
├── __init__.py
├── models.py
├── views.py
├── apps.py
│
├── templatetags/
│   ├── __init__.py
│   └── custom_filter.py
│
└── templates/
    └── filter_demo.html
```

**Important:** The application containing `templatetags` must be installed in `INSTALLED_APPS`. After creating the files, restart the development server if Django does not detect the new library.

## 4. Create a Filter to Capitalize the First Letter

**`templatetags/custom_filter.py`**

```python
from django import template

register = template.Library()


@register.filter(name='firstLetterCapital')
def first_one_letter_upper(value):
    value = str(value)

    if not value:
        return value

    return value[0].upper() + value[1:]
```

### Explanation

- `template.Library()` creates a library for registering custom template filters.
- `@register.filter(...)` registers the function as a template filter.
- `value` receives the value passed from the template.
- `value[0].upper()` converts the first character to uppercase.
- `value[1:]` keeps the remaining characters unchanged.
- The empty-value check prevents an error when the input is an empty string.

### Use the filter in HTML

**`filter_demo.html`**

```django
{% load custom_filter %}

<p>{{ name|firstLetterCapital }}</p>
```

If `name` is `django framework`, the output is:

```text
Django framework
```

The name inside `{% load custom_filter %}` is the Python module filename without `.py`.

## 5. Create a Filter to Capitalize Every Word

Add this function to `custom_filter.py`:

```python
@register.filter(name='firstletterUpper')
def first_letter_capital_for_every_string(value):
    return str(value).title()
```

### Use it in the template

```django
{% load custom_filter %}

<p>{{ name|firstletterUpper }}</p>
```

**Output:**

```text
Django Framework
```

Python's `str.title()` capitalizes the first character of each word and lowercases other letters according to its title-casing rules. It may not be suitable for every person's name or every specialized capitalization rule.

## 6. Register a Filter Without a Decorator

You can also register a filter directly:

```python
from django import template

register = template.Library()


def first_one_letter_upper(value):
    value = str(value)

    if not value:
        return value

    return value[0].upper() + value[1:]


register.filter(
    'firstLetterCapital',
    first_one_letter_upper
)
```

Both approaches work:

- `@register.filter(...)` uses a decorator.
- `register.filter('name', function)` registers a function explicitly.

## 7. Common Mistakes

1. **Incorrect folder name:** It must be `templatetags`, not `template_tags`.
2. **Missing `__init__.py`:** Create an empty `__init__.py` file inside `templatetags`.
3. **Forgetting to load the filter:** Use `{% load custom_filter %}` in the template.
4. **Using the wrong module name:** The loaded name must match the Python filename without `.py`.
5. **Forgetting registration:** Django cannot use a custom filter unless it is registered.
6. **Creating the filter in the wrong app:** Make sure the app is installed and Django can discover the library.

## 8. Quick Revision

| Concept | Meaning |
|---|---|
| Template filter | Modifies or formats a value for display. |
| Built-in filter | A filter provided by Django, such as `upper` or `title`. |
| Custom filter | A filter created by the developer. |
| `template.Library()` | Creates a template tag/filter library. |
| `@register.filter` | Registers a custom filter. |
| `{% load custom_filter %}` | Loads the custom filter library. |
| `{{ value\|filtername }}` | Applies a filter to a value. |
| `{{ value\|filtername:arg }}` | Applies a filter with an argument. |

**Remember:** Template inheritance helps reuse HTML structure, while template filters help format values displayed in templates.