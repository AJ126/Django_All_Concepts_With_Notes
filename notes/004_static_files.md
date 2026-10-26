# Django Static Files – Complete Notes

## 1. What Are Static Files in Django?

Static files are files used to design and improve the appearance and functionality of a website.

Examples of static files:

- **CSS:** Used to style web pages.
- **JavaScript:** Used to add interactive functionality.
- **Images:** Used to display images, logos, icons, etc.
- **Bootstrap:** Used to create responsive website layouts.

In Django, we commonly create a folder named `static` to store these files, similar to how we use a `templates` folder to store HTML files.

## 2. Static Files Folder Structure

A simple project-level static folder can have the following structure:

```text
project_name/
│
├── manage.py
├── project_name/
│   ├── settings.py
│   └── urls.py
│
├── templates/
│   └── home.html
│
└── static/
    ├── css/
    │   └── base.css
    ├── js/
    │   └── one.js
    └── images/
        └── one.jpg
```

**Note:** Django can also discover static files stored inside individual applications, usually in an app-level `static/` directory.

## 3. Configure Static Files in `settings.py`

### A. Old Way to Define the Base Directory

Older Django tutorials commonly use `os.path` to define the base directory and static folder.

```python
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

static_dir = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    static_dir,
]
```

**Explanation:**

- `os.path.abspath(__file__)` gets the absolute path of the current `settings.py` file.
- `os.path.dirname()` gets the parent directory.
- `os.path.join()` combines the base directory with the `static` folder.
- `STATIC_URL` defines the URL prefix used to reference static files.
- `STATICFILES_DIRS` tells Django where to look for additional static files.

### B. Modern Way to Define the Static Folder

Modern Django projects commonly use `pathlib.Path` for directory configuration.

A typical Django project already has this in `settings.py`:

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
```

Configure static files like this:

```python
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
```

**Important correction:** The following configuration is incorrect:

```python
STATICFILES_DIRS = [BASE_DIR, "static"]
```

It creates a list containing two separate entries instead of one path to the static folder. Use `BASE_DIR / 'static'` instead.

`STATICFILES_DIRS` is only necessary when you have additional static directories, such as a project-level `static` folder. Django can also discover app-level static directories automatically when the relevant app is installed.

## 4. Load the Static Template Tag

To reference static files inside a Django HTML template, use Django's `{% static %}` template tag.

At the beginning of the template, add:

```django
{% load static %}
```

Example:

```html
<!DOCTYPE html>
{% load static %}
<html>
<head>
    <title>Django Static Files</title>
</head>
<body>
    <h1>Welcome to Django</h1>
</body>
</html>
```

**Why do we use `{% load static %}`?**

It loads the template tag library that provides the `{% static %}` tag. Without it, Django templates that use `{% static %}` may raise a template syntax error.

**Note:** Django templates use the Django Template Language by default. They are not necessarily Jinja templates.

## 5. Add Static Files to HTML

### A. Add an Image

Suppose your image is located at:

```text
static/images/one.jpg
```

Use this in your HTML template:

```django
{% load static %}

<img src="{% static 'images/one.jpg' %}"
     width="400"
     height="500"
     alt="Sample image">
```

The `{% static %}` tag generates the appropriate URL for the image.

### B. Add a CSS File

Suppose your CSS file is located at:

```text
static/css/base.css
```

Add it inside the HTML `<head>` section:

```django
{% load static %}

<!DOCTYPE html>
<html>
<head>
    <title>My Django Website</title>

    <link rel="stylesheet"
          href="{% static 'css/base.css' %}">
</head>
<body>
    <h1>Welcome to Django</h1>
</body>
</html>
```

Example `base.css`:

```css
body {
    background-color: lightblue;
}

h1 {
    color: darkblue;
}
```

### C. Add a JavaScript File

Suppose your JavaScript file is located at:

```text
static/js/one.js
```

Add it before the closing `</body>` tag:

```django
{% load static %}

<script src="{% static 'js/one.js' %}"></script>
```

Example `one.js`:

```javascript
console.log("Django static JavaScript loaded!");
```

### D. Add a Local Bootstrap CSS File

If your Bootstrap CSS file is located at:

```text
static/css/bootstrap.css
```

Reference it like this:

```django
{% load static %}

<link rel="stylesheet"
      href="{% static 'css/bootstrap.css' %}">
```

Make sure the path and filename match your actual folder structure.

## 6. Difference Between `STATIC_URL`, `STATICFILES_DIRS`, and `STATIC_ROOT`

| Setting | Purpose |
|---|---|
| `STATIC_URL` | Defines the URL prefix used to reference static files. |
| `STATICFILES_DIRS` | Specifies additional directories where Django searches for static files. |
| `STATIC_ROOT` | Specifies the destination directory for collected static files during deployment. |

For example:

```python
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'
```

For a typical production deployment, run:

```bash
python manage.py collectstatic
```

Django collects static files into `STATIC_ROOT`, and your production web server or static-file hosting service can serve them.

**Important:** `STATIC_ROOT` is a collection destination, not normally the folder in which you develop and edit your static files.

## 7. Important Points to Remember

1. Create a `static` folder for project-level static files.
2. Configure `STATICFILES_DIRS` if you use that project-level folder.
3. Use `{% load static %}` in templates that reference static files.
4. Use `{% static 'relative/path/to/file' %}` to reference images, CSS, and JavaScript.
5. Check file paths and filenames carefully if static files do not load.
6. During local development, Django's development server can serve static files when `DEBUG=True` and the static-file configuration is correct.
7. In production, configure proper static-file serving and use `collectstatic` when appropriate.