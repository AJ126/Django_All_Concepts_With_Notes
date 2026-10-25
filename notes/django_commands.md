# Django Commands – Complete Notes

## Table of Contents

1. [Install Django](#1-install-django)
2. [Check Django Version](#2-check-django-version)
3. [Create a Django Project](#3-create-a-django-project)
4. [Run the Django Project](#4-run-the-django-project)
5. [Create a Django App](#5-create-a-django-app)
6. [Create Migration Files](#6-create-migration-files)
7. [View Generated SQL](#7-view-generated-sql)
8. [Apply Migrations](#8-apply-migrations)
9. [Create a Superuser](#9-create-a-superuser)
10. [Reset a User's Password](#10-reset-a-users-password)
11. [Find a Username](#11-find-a-username)
12. [Export Database Data Using `dumpdata`](#12-export-database-data-using-dumpdata)
13. [Upgrade Django](#13-upgrade-django)
14. [Create a Requirements File](#14-create-a-requirements-file)
15. [Install Packages from a Requirements File](#15-install-packages-from-a-requirements-file)
16. [Install a Package](#16-install-a-package)
17. [Uninstall a Package](#17-uninstall-a-package)
18. [List Installed Packages](#18-list-installed-packages)
19. [Create a Project in the Current Directory](#19-create-a-project-in-the-current-directory)
20. [Quick Command Reference](#20-quick-command-reference)

---

## 1. Install Django

Install Django:

```bash
python -m pip install django
```

Install a specific version:

```bash
python -m pip install django==4.1
```

> Django 4.1 is an older release. For new projects, use a currently supported version compatible with your Python version.

## 2. Check Django Version

```bash
django-admin --version
```

Alternative:

```bash
python -m django --version
```

## 3. Create a Django Project

```bash
django-admin startproject project_name
```

Alternative:

```bash
py -m django startproject project_name
```

Example:

```bash
django-admin startproject myproject
```

## 4. Run the Django Project

Navigate to the folder containing `manage.py`:

```bash
cd myproject
```

Run the development server:

```bash
python manage.py runserver
```

Run on a specific port:

```bash
python manage.py runserver 7777
```

Local address:

```text
http://127.0.0.1:7777/
```

## 5. Create a Django App

```bash
python manage.py startapp app_name
```

Example:

```bash
python manage.py startapp customers
```

Register the app in `INSTALLED_APPS` inside `settings.py`:

```python
INSTALLED_APPS = [
    # Existing apps...
    "customers",
]
```

## 6. Create Migration Files

```bash
python manage.py makemigrations
```

Create migrations for a particular app:

```bash
python manage.py makemigrations app_name
```

Example:

```bash
python manage.py makemigrations customers
```

This command creates migration files based on changes to Django models. It does not apply the changes to the database.

## 7. View Generated SQL

```bash
python manage.py sqlmigrate app_name migration_number
```

Example:

```bash
python manage.py sqlmigrate modelApp_003 0001
```

Example migration file:

```text
modelApp_003/
└── migrations/
    └── 0001_initial.py
```

This command displays the SQL associated with a migration but does not execute it.

## 8. Apply Migrations

```bash
python manage.py migrate
```

Typical workflow after changing models:

```bash
python manage.py makemigrations
python manage.py migrate
```

| Command | Purpose |
|---|---|
| `makemigrations` | Creates migration files. |
| `sqlmigrate` | Displays SQL for a migration. |
| `migrate` | Applies migrations to the database. |

## 9. Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an administrator account for the Django admin site.

## 10. Reset a User's Password

### Method 1: Using `changepassword`

```bash
python manage.py changepassword username
```

Example:

```bash
python manage.py changepassword admin
```

### Method 2: Using the Django shell

Open the shell:

```bash
python manage.py shell
```

Find the user and update the password:

```python
from django.contrib.auth.models import User

user = User.objects.get(username="admin")
user.set_password("newpassword123")
user.save()
```

Exit the shell:

```python
exit()
```

`set_password()` hashes the password before saving it. Do not assign a plain-text password directly to `user.password`.

> These examples use Django's default `User` model. If your project uses a custom user model, use the configured model instead.

## 11. Find a Username

Open the Django shell:

```bash
python manage.py shell
```

Import the default user model:

```python
from django.contrib.auth.models import User
```

Display all users:

```python
User.objects.all()
```

Display usernames only:

```python
User.objects.values_list("username", flat=True)
```

Find a username using an email address:

```python
User.objects.filter(
    email="user@example.com"
).values_list("username", flat=True)
```

## 12. Export Database Data Using `dumpdata`

The `dumpdata` command exports Django database records into a serialized format.

General syntax:

```bash
python manage.py dumpdata [app_label[.ModelName]] [options]
```

### Export data for a specific model

Example: the app label is `employees` and the model is `Employee`.

```bash
python manage.py dumpdata employees.Employee
```

Replace these names with your actual app label and model class name.

### Display formatted JSON

```bash
python manage.py dumpdata employees.Employee --indent 4
```

### Save data to a JSON file

```bash
python manage.py dumpdata employees.Employee --indent 4 > employees.json
```

### Specify JSON format explicitly

```bash
python manage.py dumpdata employees.Employee --format json --indent 4 > employees.json
```

### Display data in XML format

```bash
python manage.py dumpdata employees.Employee --format xml --indent 4
```

### Save data to an XML file

```bash
python manage.py dumpdata employees.Employee --format xml --indent 4 > employees.xml
```

### Export all installed-app data

```bash
python manage.py dumpdata --indent 4 > database.json
```

**Important notes:**

- `dumpdata` exports records; it does not create a complete database-engine backup.
- JSON is the default output format.
- XML is supported by Django's built-in serializers.
- Exported data may contain sensitive information, so protect the output files.
- Use `loaddata` when you need to import a compatible Django fixture.

Example import command:

```bash
python manage.py loaddata employees.json
```

## 13. Upgrade Django

```bash
python -m pip install -U django
```

Check the installed version:

```bash
django-admin --version
```

Check compatibility and test your project before upgrading Django in an existing application.

## 14. Create a Requirements File

```bash
python -m pip freeze > requirements.txt
```

This saves the installed packages and their versions to `requirements.txt`.

Example contents:

```text
Django==4.1
```

The actual file will contain the packages installed in your active environment.

## 15. Install Packages from a Requirements File

```bash
python -m pip install -r requirements.txt
```

Run this command from the directory containing `requirements.txt`, preferably with your project's virtual environment activated.

## 16. Install a Package

General command:

```bash
python -m pip install package_name
```

Example:

```bash
python -m pip install pillow
```

Install a specific package version:

```bash
python -m pip install pillow==10.0.0
```

The version is an example; choose a version compatible with your project.

## 17. Uninstall a Package

```bash
python -m pip uninstall package_name
```

Example:

```bash
python -m pip uninstall pillow
```

## 18. List Installed Packages

List installed packages:

```bash
python -m pip list
```

List packages with newer versions available:

```bash
python -m pip list --outdated
```

Display details about a particular package:

```bash
python -m pip show django
```

## 19. Create a Project in the Current Directory

### Without the dot

```bash
django-admin startproject config
```

This creates a new `config` directory:

```text
current-folder/
└── config/
    ├── manage.py
    └── config/
        ├── settings.py
        ├── urls.py
        ├── asgi.py
        └── wsgi.py
```

### With the dot

```bash
django-admin startproject config .
```

The dot (`.`) tells Django to use the current directory as the destination:

```text
current-folder/
├── manage.py
└── config/
    ├── settings