# Django Database Configuration and Models – Complete Notes

## 1. Database Configuration in Django

Django supports multiple databases, including SQLite, PostgreSQL, and MySQL.

By default, a newly created Django project uses **SQLite**, so you usually do not need to configure an external database to get started.

### Default SQLite Configuration

File: `settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Explanation:**

- `ENGINE`: Specifies which database backend Django should use.
- `NAME`: Specifies the database file's path. In this example, the file is `db.sqlite3` inside the project base directory.

SQLite stores the database in a local file, so you do not need to run a separate database server.

## 2. Database Configuration Parameters

When connecting Django to another database, you typically configure these parameters:

| Parameter | Purpose |
|---|---|
| `ENGINE` | Specifies the database backend |
| `NAME` | Specifies the database name or file path |
| `USER` | Database login username |
| `PASSWORD` | Database login password |
| `HOST` | Machine or hostname where the database server runs |
| `PORT` | Port on which the database server listens |

The exact configuration depends on the database backend.

## 3. Configure MySQL in Django

To use MySQL instead of SQLite, follow these steps.

### Step 1: Install and Start MySQL

Install MySQL Server and make sure the database service is running.

### Step 2: Create a Database

For example, create a database named `employeedb` using a MySQL client:

```sql
CREATE DATABASE employeedb;
```

### Step 3: Install the MySQL Python Driver

Activate your Django project's virtual environment, then run:

```bash
python -m pip install mysqlclient
```

`mysqlclient` allows Django to communicate with MySQL.

### Step 4: Configure `settings.py`

Replace the default SQLite configuration with the following:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'employeedb',
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

Replace the username and password with your actual MySQL credentials.

**Security tip:** Do not commit real database passwords to a public Git repository. Use environment variables or an appropriate secrets-management solution.

### Step 5: Apply Migrations

Run:

```bash
python manage.py migrate
```

Django creates the necessary built-in tables and applies pending migrations to the configured database.

**Important:** Changing `DATABASES` from SQLite to MySQL does not automatically copy your existing SQLite data into MySQL. Data migration requires a separate process.

## 4. How to Check the Database Connection

You can test whether Django can connect to the configured database using Django's shell.

### Step 1: Open the Django Shell

```bash
python manage.py shell
```

### Step 2: Test the Connection

```python
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT 1")
    print(cursor.fetchone())
```

Expected result:

```text
(1,)
```

If the query succeeds, Django has established a connection and executed a simple query successfully.

**Note:** This test verifies that a basic query can execute. It does not verify every database permission or the correctness of all your application models.

You can also check the connection without opening the shell:

```bash
python manage.py check --database default
```

This runs Django's system checks for the configured default database. It is useful, but it is not a substitute for testing an actual query.

---

## 5. What Is a Django Model?

A **Django model** is a Python class that describes the structure and behavior of data stored in a database.

A model is usually defined in the application's `models.py` file.

Important points:

1. Every standard Django model inherits from `django.db.models.Model`.
2. Model attributes define database fields.
3. Django maps each model to a database table by default.
4. Django's ORM (Object-Relational Mapper) lets you interact with database records using Python instead of writing SQL for every operation.
5. Model definitions are used to generate database migrations.

## 6. Creating a Model Class

File: `models.py`

```python
from django.db import models

class TestData(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name
```

### Explanation

- `TestData`: The model class name.
- `name`: Stores a text value up to 100 characters.
- `address`: Stores a text value up to 200 characters.
- `phone`: Stores a phone number as text.
- `__str__()`: Returns a readable representation of the object, useful in the Django admin and shell.

**Why use `CharField` for phone numbers?**

Phone numbers are identifiers, not quantities. They may contain leading zeros, a `+` sign, or formatting characters. Therefore, storing them as text is usually more appropriate than storing them as integers.

Also, `IntegerField` does not accept `max_length`. Use a suitable numeric field for numeric values, not for phone numbers.

### Example of a Model Table

Django normally creates a table named `yourapp_testdata`, where `yourapp` is the application name.

| id | name | address | phone |
|---:|---|---|---|
| 1 | Amit | Pune | 9876543210 |
| 2 | Priya | Mumbai | 9123456780 |

Django automatically adds a primary key field named `id` unless you define a different primary key.

---

## 7. Creating Database Migrations

After creating or modifying a model, Django needs to update the database schema.

Migrations provide a record of database schema changes.

### Step 1: Create Migration Files

```bash
python manage.py makemigrations
```

This command detects model changes and creates migration files inside the application's `migrations/` directory.

For example:

```text
yourapp/
└── migrations/
    ├── __init__.py
    └── 0001_initial.py
```

The migration file contains Python instructions describing the database changes Django should make.

**Important correction:** `makemigrations` does not directly execute SQL against your database. It generates migration files.

### Step 2: Apply Migrations

```bash
python manage.py migrate
```

This command applies pending migrations to the configured database, creating or modifying tables as required.

### Step 3: View SQL Generated for a Migration

Use the `sqlmigrate` command:

```bash
python manage.py sqlmigrate app_name migration_number
```

Example:

```bash
python manage.py sqlmigrate app_003_models 0001
```

This displays the SQL statements Django would use for that migration and database backend. It does not apply the migration.

### Migration Workflow

```text
Create or modify model
          |
          v
makemigrations
          |
          v
Migration file created
          |
          v
migrate
          |
          v
Database schema updated
```

---

## 8. Registering Models in Django Admin

Django provides a built-in administration interface that allows authorized users to manage database records.

To display a model in the admin interface, register it in `admin.py`.

### Step 1: Import the Model

File: `admin.py`

```python
from django.contrib import admin
from .models import TestData
```

### Step 2: Register the Model

```python
admin.site.register(TestData)
```

The model will now appear in Django admin when you log in with an authorized account.

### Step 3: Customize the Admin List Display

You can create a `ModelAdmin` class to control how records are displayed.

```python
from django.contrib import admin
from .models import TestData

class TestDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'phone']

admin.site.register(TestData, TestDataAdmin)
```

### What Is `list_display`?

`list_display` controls which fields or attributes appear as columns on the model's admin list page.

For example:

```python
list_display = ['name', 'address', 'phone']
```

This displays three columns: name, address, and phone.

You can also customize the admin interface using options such as:

- `search_fields`: Adds a search box for specified fields.
- `list_filter`: Adds filters to the sidebar.
- `ordering`: Sets the default ordering of records.
- `list_per_page`: Controls the number of records displayed per page.

Example:

```python
class TestDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'phone']
    search_fields = ['name', 'address']
    list_filter = ['address']
    ordering = ['name']
    list_per_page = 20
```

Register the model with this admin class:

```python
admin.site.register(TestData, TestDataAdmin)
```

**Note:** The application containing `TestData` must be added to `INSTALLED_APPS`, and the database migrations must be applied.

---

## 9. Creating a Superuser

A superuser account has full administrative permissions by default.

Run this command from the directory containing `manage.py`:

```bash
python manage.py createsuperuser
```

Django prompts you for the username, email address if required by the user model configuration, and password.

Start the development server:

```bash
python manage.py runserver
```

Open the admin page:

```text
http://127.0.0.1:8000/admin/
```

Log in using your superuser credentials.

## 10. Quick Revision

| Command or Concept | Purpose |
|---|---|
| `DATABASES` | Configures the database connection |
| `models.py` | Defines model classes |
| `makemigrations` | Creates migration files |
| `migrate` | Applies migrations to the database |
| `sqlmigrate` | Displays SQL for a migration |
| `python manage.py shell` | Opens the Django interactive shell |
| `admin.site.register()` | Registers a model in Django admin |
| `ModelAdmin` | Customizes the model's admin interface |
| `list_display` | Chooses columns shown on the admin list page |
| `createsuperuser` | Creates an administrative user |
