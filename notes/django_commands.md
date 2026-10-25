# Django Commands – Complete Notes

## 1. Install Django

Install Django:

```bash
pip install django
```

Install a specific version:

```bash
pip install django==4.1
```

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
django-admin startproject projectname
```

Replace `projectname` with your project name.

## 4. Run the Django Project

Navigate to the directory containing `manage.py`:

```bash
cd projectname
```

Start the development server:

```bash
python manage.py runserver
```

Run the server on a specific port:

```bash
python manage.py runserver 7777
```

## 5. Create an App

```bash
python manage.py startapp appname
```

Example:

```bash
python manage.py startapp customers
```

## 6. Create Migration Files

```bash
python manage.py makemigrations
```

Create migrations for a specific app:

```bash
python manage.py makemigrations appname
```

## 7. View Generated SQL

```bash
python manage.py sqlmigrate modelApp_003 0001
```

**Note:** Provide the app name and migration number to view the SQL for a particular migration.

Example migration file:

```text
modelApp_003/migrations/0001_initial.py
```

This command displays SQL; it does not execute it.

## 8. Apply Migrations to the Database

```bash
python manage.py migrate
```

Typical workflow:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 9. Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an administrator account.

## 10. Install Django REST Framework

Install or upgrade Django REST Framework:

```bash
pip install -U djangorestframework
```

Check package details:

```bash
pip show djangorestframework
```

Add it to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # Other apps...
    "rest_framework",
]
```

## 11. Upgrade Django

```bash
pip install -U django
```

Check the installed version:

```bash
django-admin --version
```

## 12. Create a Requirements File

```bash
pip freeze > requirements.txt
```

This saves the installed packages and their versions to `requirements.txt`.

## 13. Install Packages from a Requirements File

```bash
pip install -r requirements.txt
```

Run this command from the directory containing `requirements.txt`, preferably with your project's virtual environment activated.

## 14. Create a Project in the Current Directory

If you already have a folder and want to create the Django project directly inside it, run:

```bash
django-admin startproject config .
```

The dot (`.`) means **create the project in the current directory**.

**Without the dot:**

```bash
django-admin startproject config
```

Directory structure:

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

**With the dot:**

```bash
django-admin startproject config .
```

Directory structure:

```text
current-folder/
├── manage.py
└── config/
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

Run the command inside the intended destination folder.

## 15. Reset a User's Password

```bash
python manage.py changepassword username
```

Replace `username` with the actual Django username.

Example:

```bash
python manage.py changepassword admin
```

Django will prompt you to enter and confirm the new password.

---

## Quick Command Reference

| Task | Command |
|---|---|
| Install Django | `pip install django` |
| Install specific version | `pip install django==4.1` |
| Check Django version | `django-admin --version` |
| Create project | `django-admin startproject projectname` |
| Run server | `python manage.py runserver` |
| Run on port 7777 | `python manage.py runserver 7777` |
| Create app | `python manage.py startapp appname` |
| Create migrations | `python manage.py makemigrations` |
| View migration SQL | `python manage.py sqlmigrate appname 0001` |
| Apply migrations | `python manage.py migrate` |
| Create superuser | `python manage.py createsuperuser` |
| Install Django REST Framework | `pip install -U djangorestframework` |
| Upgrade Django | `pip install -U django` |
| Create requirements file | `pip freeze > requirements.txt` |
| Install requirements | `pip install -r requirements.txt` |
| Create project in current folder | `django-admin startproject config .` |
| Change password | `python manage.py changepassword username` |

## Important Tips

1. Activate your virtual environment before installing packages.
2. Run `manage.py` commands from the directory containing `manage.py`.
3. Run `makemigrations` after model changes, followed by `migrate`.
4. Keep your `requirements.txt` updated.
5. Never commit passwords or other secrets to Git.
