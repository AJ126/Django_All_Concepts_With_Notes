# Django Advanced Models – Complete Notes

Django provides several advanced model features that help us write reusable, maintainable and well-organized database code.

The important topics covered in this lesson are:

1. Model Inheritance
2. Abstract Base Class Inheritance
3. Multi-Table Inheritance
4. Multi-Level Inheritance
5. Multiple Inheritance
6. Model Manager
7. Custom Model Manager
8. `get_queryset()` Method
9. Proxy Model Inheritance

---

# 1. Model Inheritance

Model inheritance is a powerful feature of Django that allows one model to inherit fields and behavior from another model.

It is useful when multiple models share common fields or functionality.

For example, suppose we have two models:

- `Student`
- `Employee`

Both models need common fields such as `name`, `email` and `address`.

Instead of defining these fields separately in both models, we can create a common parent model and inherit it.

### Types of model inheritance

Django supports three primary model inheritance styles:

1. Abstract Base Class Inheritance
2. Multi-Table Inheritance
3. Proxy Model Inheritance

Python also supports multiple inheritance, which can be used with Django models subject to Django's model inheritance rules.

---

# 2. Abstract Base Class Inheritance

Abstract Base Class Inheritance is used when multiple models share common fields and we want to avoid writing those fields repeatedly.

The parent model is called an **Abstract Base Model**.

### Important characteristics

- The parent model contains common fields.
- Child models inherit the parent's fields.
- Django does not create a separate database table for the abstract parent.
- Each child model gets its own database table containing the inherited fields and its own fields.
- Abstract models cannot be registered directly in the Django admin because they do not have their own database table.

### Example

**`models.py`**

```python
from django.db import models


# Abstract Base Model
class BaseInfo(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True


# Child Model 1
class Student(BaseInfo):
    address = models.CharField(max_length=100)


# Child Model 2
class Employee(BaseInfo):
    salary = models.IntegerField()
```

### Explanation

Here:

- `BaseInfo` is the parent model.
- `abstract = True` makes it an abstract model.
- `Student` inherits the `name` field.
- `Employee` also inherits the `name` field.

### Database structure

Django creates two tables:

**Student table**

| id | name | address |
|---|---|---|
| 1 | Akash | Pune |
| 2 | Amit | Mumbai |

**Employee table**

| id | name | salary |
|---|---|---|
| 1 | Shiv | 50000 |
| 2 | Rahul | 60000 |

There is no separate `BaseInfo` table.

### When should we use Abstract Base Class Inheritance?

Use it when:

- Multiple models share common fields.
- You want to avoid duplicate code.
- You don't need a separate database table for the parent model.

**Real-life example:** A student and employee both have a name, email and address. These common fields can be defined in an abstract base model.

---

# 3. Multi-Table Inheritance

Multi-Table Inheritance is used when the parent model is a normal Django model rather than an abstract model.

In this inheritance:

- Django creates a separate database table for the parent.
- Django also creates a separate database table for each child model.
- Django automatically creates a parent-link `OneToOneField` to connect the child table to its parent table.
- Parent fields are stored in the parent table, not duplicated as ordinary columns in the child table.

### Example

**`models.py`**

```python
from django.db import models


class ParentTable(models.Model):
    name = models.CharField(max_length=100)


class ChildTable(ParentTable):
    address = models.CharField(max_length=100)
```

### Database structure

Django creates two tables.

**ParentTable**

| id | name |
|---|---|
| 1 | Akash |
| 2 | Amit |

**ChildTable**

| parenttable_ptr_id | address |
|---|---|
| 1 | Pune |
| 2 | Mumbai |

The `parenttable_ptr_id` field is an automatically created one-to-one link to the parent record. It also serves as the child's primary key by default.

### How does it work?

When we create a child record:

```python
child = ChildTable.objects.create(
    name="Akash",
    address="Pune"
)
```

Django creates:

1. A record in the `ParentTable`.
2. A related record in the `ChildTable`.

The child record is connected to its parent record through the automatically created one-to-one relationship.

### Accessing parent fields

```python
child = ChildTable.objects.get(pk=1)

print(child.name)
print(child.address)
```

We can access both parent and child fields through the child object.

### When should we use Multi-Table Inheritance?

Use it when:

- The parent model needs its own database table.
- Parent records must exist independently.
- Child models need to extend the parent model with additional fields.

**Real-life example:** A general `Person` model can store common information, while `Student` and `Employee` models store their specific information.

---

# 4. Multi-Level Inheritance

Multi-Level Inheritance means a model inherits from another model, which itself inherits from another model.

It is a Python inheritance pattern that can be used with Django models.

### Example

```python
from django.db import models


class Parent(models.Model):
    name = models.CharField(max_length=100)


class Child(Parent):
    info = models.CharField(max_length=100)


class Son(Child):
    details = models.CharField(max_length=100)
```

Here:

- `Parent` contains the `name` field.
- `Child` inherits `name` and adds `info`.
- `Son` inherits `name` and `info`, and adds `details`.

### Database structure

Because these are normal, non-abstract models, this example uses multi-table inheritance.

Django creates three tables:

1. `Parent`
2. `Child`
3. `Son`

Each child table is linked to its parent table through an automatically generated one-to-one parent link.

### Important point

Multi-Level Inheritance is not a separate fourth model inheritance style in Django. It describes the inheritance structure. The actual database behavior depends on whether the parent models are abstract or concrete.

---

# 5. Multiple Inheritance

Multiple Inheritance means a class inherits from more than one parent class.

Python supports multiple inheritance, and Django supports it for models with certain restrictions.

### Example

```python
from django.db import models


class DetailTest(models.Model):
    address = models.CharField(max_length=100)


class Info(models.Model):
    city = models.CharField(max_length=100)


class Test(DetailTest, Info):
    name = models.CharField(max_length=100)
```

Here, `Test` inherits fields from both `DetailTest` and `Info`.

### Important correction about primary keys

You do not always need to define custom primary keys in multiple inheritance.

Django can handle multiple inherited primary keys when the parent models are set up appropriately. However, multiple concrete model inheritance has additional restrictions and can produce complex database relationships.

For example, if two parent models both define a primary key, you must understand how Django handles the inherited parent links and primary-key structure.

### Recommended approach

If you only want to reuse common fields, prefer abstract base classes.

```python
class AddressInfo(models.Model):
    address = models.CharField(max_length=100)

    class Meta:
        abstract = True


class CityInfo(models.Model):
    city = models.CharField(max_length=100)

    class Meta:
        abstract = True


class Test(AddressInfo, CityInfo):
    name = models.CharField(max_length=100)
```

Here, both parent classes are abstract, so Django creates only the `Test` table containing all three fields.

### When should we use Multiple Inheritance?

Use it when:

- A model needs reusable fields or behavior from multiple parent classes.
- The inheritance structure is clear and does not create conflicting fields.
- You understand Django's model inheritance and Python method resolution order (MRO).

---

# 6. Model Manager

A Model Manager is an interface through which we interact with the database using Django models.

By default, every Django model gets a manager named:

```python
objects
```

Example:

```python
Employee.objects.all()
```

Here:

- `Employee` is the model.
- `objects` is the model manager.
- `all()` is a manager/queryset method.

### Real-life example

Think about a library:

| Django concept | Library example |
|---|---|
| Database | All books in the library |
| Model | Structure of a book |
| Model Manager | Librarian |
| QuerySet | List of books returned by the librarian |

We don't need to search through the entire library ourselves. We ask the librarian to find the books we need.

Similarly, we use a model manager to retrieve and manage database records.

### Default Model Manager

```python
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
```

Django automatically provides:

```python
Book.objects.all()
Book.objects.filter(price__lt=100)
Book.objects.get(pk=1)
```

### Why do we need Model Managers?

- To centralize reusable database queries.
- To reduce repeated code.
- To keep views clean.
- To provide a consistent way to retrieve records.
- To encapsulate commonly used query logic.

---

# 7. Custom Model Manager

Django allows us to create our own model manager by inheriting from `models.Manager`.

We can define custom methods inside the manager to perform reusable database queries.

### Example

**`models.py`**

```python
from django.db import models


class BookManager(models.Manager):

    def show_all_books(self):
        return self.all()

    def cheap_books(self):
        return self.filter(price__lt=100)

    def expensive_books(self):
        return self.filter(price__gt=250)


class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()

    objects = BookManager()
```

### Explanation

Here:

- `BookManager` is our custom manager.
- It inherits from `models.Manager`.
- `show_all_books()` retrieves all books.
- `cheap_books()` retrieves books costing less than 100.
- `expensive_books()` retrieves books costing more than 250.
- `objects = BookManager()` assigns our custom manager to the model.

### Calling custom manager methods

```python
# Get all books
Book.objects.show_all_books()

# Get cheap books
Book.objects.cheap_books()

# Get expensive books
Book.objects.expensive_books()
```

### Using the custom manager in views

**`views.py`**

```python
from django.shortcuts import render
from .models import Book


def show_books(request):
    data = Book.objects.show_all_books()

    return render(
        request,
        "app_013_advance_model/showBooks.html",
        {"data": data}
    )


def show_cheap_books(request):
    data = Book.objects.cheap_books()

    return render(
        request,
        "app_013_advance_model/showBooks.html",
        {"data": data}
    )


def show_expensive_books(request):
    data = Book.objects.expensive_books()

    return render(
        request,
        "app_013_advance_model/showBooks.html",
        {"data": data}
    )
```

### Template

**`showBooks.html`**

```html
<h2>Book List</h2>

<table>
    <thead>
        <tr>
            <th>Book Name</th>
            <th>Price</th>
        </tr>
    </thead>

    <tbody>
        {% for book in data %}
            <tr>
                <td>{{ book.title }}</td>
                <td>{{ book.price }}</td>
            </tr>
        {% empty %}
            <tr>
                <td colspan="2">No books found.</td>
            </tr>
        {% endfor %}
    </tbody>
</table>
```

---

# 8. Multiple Model Managers

We can define multiple managers in a single model.

For example, we may want to keep Django's default manager and also define our own custom manager.

### Example

```python
from django.db import models


class BookManager(models.Manager):

    def cheap_books(self):
        return self.filter(price__lt=100)

    def expensive_books(self):
        return self.filter(price__gt=250)


class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()

    objects = models.Manager()       # Default manager
    custom = BookManager()            # Custom manager
```

### Calling the managers

```python
# Default manager
Book.objects.all()

# Custom manager
Book.custom.cheap_books()

Book.custom.expensive_books()
```

### Important points

- A model can have multiple managers.
- Each manager provides its own query interface.
- A manager works at the model/table level, not on a single model instance.
- Manager methods commonly return QuerySets.
- QuerySets can be chained with other queryset methods.
- Managers help us follow the DRY principle: Don't Repeat Yourself.

**Important:** The first manager defined on a model is normally treated as its default manager unless `Meta.default_manager_name` specifies another one. Django also has a base manager, which can be configured separately.

---

# 9. The `get_queryset()` Method

`get_queryset()` is an important method of Django's Model Manager.

It returns the base QuerySet used by that manager.

When we call methods such as `all()` or `filter()`, Django uses the manager's queryset as the starting point.

We can override `get_queryset()` to customize the default queryset.

### Example 1: Sort records automatically

**`models.py`**

```python
from django.db import models


class EmployeeManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().order_by("eno")


class Employee(models.Model):
    eno = models.IntegerField()
    name = models.CharField(max_length=100)
    salary = models.IntegerField()

    objects = EmployeeManager()
```

### Explanation

```python
def get_queryset(self):
    return super().get_queryset().order_by("eno")
```

This means that the manager's base queryset is sorted by `eno` in ascending order.

Now:

```python
Employee.objects.all()
```

will return employees ordered by `eno`.

The ordering also applies when using this manager's queryset for other operations, unless the ordering is overridden.

### Example 2: Add custom manager methods

```python
class EmployeeManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().order_by("eno")

    def get_emp_sal_range(self, esal1, esal2):
        return self.get_queryset().filter(
            salary__range=(esal1, esal2)
        )

    def get_employees_sorted_by(self, param):
        allowed_fields = {"eno", "name", "salary"}

        if param.lstrip("-") not in allowed_fields:
            raise ValueError("Invalid sorting field")

        return self.get_queryset().order_by(param)
```

Model:

```python
class Employee(models.Model):
    eno = models.IntegerField()
    name = models.CharField(max_length=100)
    salary = models.IntegerField()

    objects = EmployeeManager()
```

### Calling the methods

```python
# All employees ordered by eno
Employee.objects.all()

# Employees whose salaries are between 20000 and 50000
Employee.objects.get_emp_sal_range(20000, 50000)

# Employees sorted by name
Employee.objects.get_employees_sorted_by("name")

# Employees sorted by salary descending
Employee.objects.get_employees_sorted_by("-salary")
```

### Why validate the sorting parameter?

Avoid directly accepting arbitrary field names from user input.

For example, if a user can control the sorting parameter, validate it against an allowed list before passing it to `order_by()`.

This helps prevent unexpected behavior and keeps the query interface controlled.

### Difference between `Manager` and `QuerySet`

| Manager | QuerySet |
|---|---|
| Entry point for model-level database operations | Represents a collection of database records |
| Accessed through `Model.objects` | Returned by methods such as `all()` and `filter()` |
| Used to define reusable query entry points | Used to filter, sort and chain queries |
| Can define custom methods | Can define custom chainable queryset methods |

**Note:** If you want custom methods that can be chained with other QuerySet operations, consider creating a custom `QuerySet` class and exposing it through a manager.

---

# 10. Proxy Model Inheritance

Proxy Model Inheritance allows us to create a different Python model interface for an existing model without creating another database table.

The proxy model uses the same database table as its original model.

### Important characteristics

- No new database table is created.
- The proxy model uses the original model's database table.
- We can customize default ordering.
- We can add or override model methods.
- We can customize the Django admin interface.
- We cannot add new database fields to a proxy model.

### Example

**`models.py`**

```python
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.title


# Proxy Model
class ProxyBook(Book):

    class Meta:
        proxy = True
        ordering = ["price"]
```

### Explanation

Here:

- `Book` is the original model.
- `ProxyBook` inherits from `Book`.
- `proxy = True` tells Django that this is a proxy model.
- `ordering = ["price"]` sorts records by price in ascending order.

### Database structure

Django creates only one database table:

```text
Book table
-------------------------
id
title
price
```

Both `Book` and `ProxyBook` use the same table.

### Accessing records

```python
# Original model
Book.objects.all()

# Proxy model
ProxyBook.objects.all()
```

Both query the same underlying database records, but the proxy model uses its own model behavior and default ordering.

### Creating records

```python
Book.objects.create(
    title="Python Basics",
    price=200
)
```

The newly created record is also visible through:

```python
ProxyBook.objects.all()
```

Similarly, a record created through `ProxyBook` is visible through `Book`.

### Customizing proxy model behavior

We can override model methods:

```python
class ProxyBook(Book):

    class Meta:
        proxy = True
        ordering = ["price"]

    def display_book_info(self):
        return f"{self.title} - Rs. {self.price}"
```

### Proxy Model in Django Admin

We can register the original model and proxy model separately.

**`admin.py`**

```python
from django.contrib import admin
from .models import Book, ProxyBook


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "price")


@admin.register(ProxyBook)
class ProxyBookAdmin(admin.ModelAdmin):
    list_display = ("title", "price")
    ordering = ("price",)
```

Both admin entries display records from the same underlying table.

Changes made through either model are reflected when viewing the records through the other model.

### When should we use Proxy Model Inheritance?

Use it when:

- You want different default sorting.
- You want different model methods.
- You want a separate admin presentation.
- You want a different manager for the same database table.
- You do not want to create another database table.

---

# 11. Difference Between Model Inheritance Types

| Feature | Abstract Base Class | Multi-Table | Proxy Model |
|---|---|---|---|
| Parent database table | No | Yes | Existing original table |
| Child database table | Yes | Yes | No new table |
| Inherits fields | Yes | Yes | Uses original model's fields |
| Can add new database fields | Yes, in child | Yes | No |
| Main purpose | Reuse common fields | Extend concrete models | Customize existing model behavior |
| Separate database storage | Child tables | Parent and child tables | Same table |

---

# 12. Common Mistakes and Important Points

| Mistake | Correct approach |
|---|---|
| Forgetting `abstract = True` | Django treats the parent as a concrete model and uses multi-table inheritance |
| Registering an abstract model in admin | Register concrete child models instead |
| Assuming multi-table inheritance creates only one table | Django creates parent and child tables |
| Assuming proxy models create a new table | Proxy models use the original model's table |
| Adding new database fields to a proxy model | Use a concrete child model or another suitable inheritance type |
| Defining custom manager methods without returning a queryset | Return the queryset or result expected by the caller |
| Assuming every manager method is automatically chainable | Use a custom QuerySet when chainable custom methods are needed |
| Passing arbitrary user input to `order_by()` | Validate allowed sorting fields |

---

# 13. Quick Revision

### Model Inheritance

- Abstract Base Class: Reuses common fields without creating a parent table.
- Multi-Table: Creates separate parent and child tables.
- Proxy Model: Uses the original model's table without creating a new one.
- Multi-Level Inheritance: A chain of parent-child inheritance.
- Multiple Inheritance: One model inherits from multiple parent classes.

### Model Manager

- Every model normally has a default manager named `objects`.
- Managers provide the interface for interacting with model data.
- Custom managers inherit from `models.Manager`.
- Multiple managers can be defined in a model.
- `get_queryset()` returns the manager's base QuerySet.
- Custom manager methods help centralize reusable database queries.

### Important syntax

```python
# Default manager
Book.objects.all()

# Custom manager
Book.custom.cheap_books()

# Custom get_queryset()
class BookManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().order_by("price")

# Abstract model
class BaseInfo(models.Model):

    name = models.CharField(max_length=100)

    class Meta:
        abstract = True

# Proxy model
class ProxyBook(Book):

    class Meta:
        proxy = True
        ordering = ["price"]
```

**Final tip:** Use abstract models when you want to reuse common fields, multi-table inheritance when parent and child need separate database tables, and proxy models when you only want to change the behavior or presentation of an existing model without changing its database structure.