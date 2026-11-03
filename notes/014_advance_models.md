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
---

# 14. Model Relationships in Django

Django provides relationship fields to connect records between different database tables.

The three main relationship types are:

1. One-to-One Relationship (`OneToOneField`)
2. One-to-Many Relationship (`ForeignKey`)
3. Many-to-Many Relationship (`ManyToManyField`)

## 14.1 One-to-One Relationship

A one-to-one relationship means one record in the first table is connected to exactly one record in the second table, and vice versa.

### Example

**`models.py`**

```python
from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()


class CustomerProfile(models.Model):
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE
    )
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
```

### How to access related data?

**Access the customer profile from a customer:**

```python
customer = Customer.objects.get(id=1)

# Access customer profile
profile = customer.customerprofile

print(profile.address)
print(profile.phone_number)
```

**Access the customer from a customer profile:**

```python
profile = CustomerProfile.objects.get(id=1)

# Access customer
print(profile.customer.name)
```

### Important point: Reverse relationship

Django automatically creates a reverse relationship.

By default, the reverse accessor in this example is `customerprofile`, so we can use:

```python
customer.customerprofile
```

You can customize the reverse accessor by setting `related_name` on the relationship field.

### When should we use `OneToOneField`?

Use it when you want to separate additional information into another table but maintain a one-to-one connection.

Examples:

- User and UserProfile
- Customer and CustomerProfile
- Product and ProductDetails

## 14.2 One-to-Many Relationship

A one-to-many relationship means one record in the first table can be connected to multiple records in the second table.

However, each record in the second table belongs to only one record in the first table.

**Example:** One customer can place multiple orders, but each order belongs to one customer.

### Why do we use `ForeignKey`?

We use `ForeignKey` because one customer can have multiple orders.

A `ForeignKey` creates a many-to-one relationship from the perspective of the model containing the field (`Order`).

### Example

```python
from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)


class Order(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
```

### How to access related data?

**Get the customer of an order:**

```python
order = Order.objects.get(id=101)
print(order.customer.name)
```

**Get all orders of a customer:**

```python
customer = Customer.objects.get(id=1)
orders = customer.orders.all()

for order in orders:
    print(order.id, order.amount)
```

### What is `related_name='orders'`?

It allows us to access all related orders using:

```python
customer.orders.all()
```

Without `related_name`, Django uses the default reverse accessor:

```python
customer.order_set.all()
```

## 14.3 Many-to-Many Relationship

A many-to-many relationship means multiple records in the first table can be connected to multiple records in the second table.

**Example: Students and Courses**

- One student can enroll in multiple courses.
- One course can have multiple students.

Django automatically creates an intermediate database table to maintain this relationship.

### Example

```python
from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    courses = models.ManyToManyField(
        "Course",
        related_name="students"
    )


class Course(models.Model):
    name = models.CharField(max_length=100)
```

### How to access related data?

**Get all courses of a student:**

```python
student = Student.objects.get(id=1)
courses = student.courses.all()

for course in courses:
    print(course.name)
```

**Get all students enrolled in a course:**

```python
course = Course.objects.get(id=1)
students = course.students.all()

for student in students:
    print(student.name)
```

### Other examples

- Students and Courses
- Products and Tags
- Posts and Categories
- Employees and Projects
- Users and Groups

### Easy trick to remember

- `OneToOneField` = One person, one profile.
- `ForeignKey` = One customer, many orders.
- `ManyToManyField` = Many students, many courses.

---

# 15. Aggregation in Django

Imagine you have an e-commerce application with thousands of orders.

Your manager asks:

1. What is the total sales amount?
2. What is the average order amount?
3. What is the maximum order amount?
4. How many orders have been placed?

You could retrieve all orders and calculate these values using Python. However, that would be inefficient for large datasets.

**Aggregation** allows us to perform calculations directly in the database and return summarized results.

For example, a shopkeeper can calculate order amounts and sales totals directly using aggregation.

### Import aggregation functions

```python
from django.db.models import Sum, Avg, Max, Min, Count
```

### Calculate total sales

```python
result = Order.objects.aggregate(
    total_sales=Sum("amount")
)

# Example output:
# {'total_sales': Decimal('5000')}
```

### Calculate average order amount

```python
result = Order.objects.aggregate(
    average_amount=Avg("amount")
)

# Example output:
# {'average_amount': Decimal('1250')}
```

### Find maximum order amount

```python
result = Order.objects.aggregate(
    maximum_amount=Max("amount")
)

# Example output:
# {'maximum_amount': Decimal('2000')}
```

### Count total orders

```python
result = Order.objects.aggregate(
    total_orders=Count("id")
)

# Example output:
# {'total_orders': 4}
```

### What does `aggregate()` return?

`aggregate()` returns a Python dictionary.

Example:

```python
{
    "total_sales": Decimal("5000"),
    "average_amount": Decimal("1250")
}
```

### Calculate multiple values in one query

```python
result = Order.objects.aggregate(
    total_sales=Sum("amount"),
    average_amount=Avg("amount"),
    maximum_amount=Max("amount"),
    minimum_amount=Min("amount"),
    total_orders=Count("id")
)
```

---

# 16. Annotation in Django

Imagine your manager asks you to:

- Display every customer.
- Display how many orders each customer has placed.
- Display the total amount spent by each customer.

How can we calculate these values for every customer?

This is where **annotation** comes into the picture.

Annotation allows us to add calculated information to each individual record in a queryset.

## Count how many orders each customer has placed

Import `Count`:

```python
from django.db.models import Count
```

Use `annotate()`:

```python
customers = Customer.objects.annotate(
    total_orders=Count("orders")
)
```

### Explanation

- `Customer.objects` gets the Customer queryset.
- `annotate()` adds calculated information to each customer.
- `total_orders` is the name of our calculated attribute.
- `Count("orders")` counts the related orders of each customer.

### Access the calculated value

```python
for customer in customers:
    print(customer.name, customer.total_orders)
```

### Where did this attribute come from?

We did not create `total_orders` inside our `Customer` model.

Django dynamically attaches this calculated value to each `Customer` object returned by the annotated queryset.

## Calculate total spending per customer

```python
from django.db.models import Sum

customers = Customer.objects.annotate(
    total_spent=Sum("orders__amount")
)

for customer in customers:
    print(customer.name, customer.total_spent)
```

### Understanding `orders__amount`

- `orders` accesses the related `Order` records.
- `amount` accesses the amount field from those records.
- The double underscore (`__`) is used to navigate relationships and fields in Django ORM queries.

## Use multiple annotations together

```python
from django.db.models import Count, Sum, Avg

customers = Customer.objects.annotate(
    total_orders=Count("orders"),
    total_spent=Sum("orders__amount"),
    average_order=Avg("orders__amount")
)

for customer in customers:
    print("Customer:", customer.name)
    print("Orders:", customer.total_orders)
    print("Total Spent:", customer.total_spent)
    print("Average Order:", customer.average_order)
```

---

# 17. `select_related()` in Django

Imagine you have a Customer Management System.

You want to display all orders along with their customer names. Your `Order` model contains a `ForeignKey` relationship with `Customer`.

## Without `select_related()`

```python
orders = Order.objects.all()

for order in orders:
    print(order.id, order.customer.name)
```

It looks simple, but there can be a performance problem.

Let's say your database contains 100 orders. Django may execute:

1. One query to fetch all orders.
2. One additional query for each order to retrieve its customer.

That means approximately 101 database queries in this example. This problem is commonly called the **N+1 query problem**.

## Solution: `select_related()`

Django provides `select_related()` to solve this problem for `ForeignKey` and `OneToOneField` relationships.

```python
orders = Order.objects.select_related("customer")

for order in orders:
    print(order.id, order.customer.name)
```

Now Django uses a SQL `JOIN` to fetch the orders and their related customers together.

Instead of approximately 101 queries, it can retrieve the required data in one SQL query.

Conceptually, the SQL is similar to:

```sql
SELECT *
FROM orders
INNER JOIN customers
    ON orders.customer_id = customers.id;
```

### When should we use `select_related()`?

Use it when you need to retrieve related objects connected through:

- `ForeignKey`
- `OneToOneField`

**Note:** `select_related()` uses SQL `JOIN` and is generally best for single-valued relationships.

---

# 18. `prefetch_related()` in Django

Imagine you want to display:

- Every customer.
- Their name.
- All orders placed by that customer.

Here we are dealing with a one-to-many relationship.

## Without `prefetch_related()`

```python
customers = Customer.objects.all()

for customer in customers:
    print(customer.name)

    for order in customer.orders.all():
        print(order.id, order.amount)
```

Suppose there are 100 customers.

Django may execute:

- One query to fetch all customers.
- 100 additional queries to fetch orders for each customer.

Total: approximately 101 queries. This is another example of the N+1 query problem.

## Solution: `prefetch_related()`

```python
customers = Customer.objects.prefetch_related("orders")

for customer in customers:
    print(customer.name)

    for order in customer.orders.all():
        print(order.id, order.amount)
```

Now Django generally executes two queries:

1. Fetch all customers.
2. Fetch all related orders for those customers.

Conceptually, the queries are similar to:

```sql
SELECT * FROM customer;

SELECT *
FROM orders
WHERE customer_id IN (1, 2, 3);
```

Django connects the orders to their respective customers in Python. This means you do not need to execute a separate query for every customer.

### When should we use `prefetch_related()`?

It is useful for:

- `ManyToManyField`
- Reverse `ForeignKey` relationships
- Other multi-valued relationships

### Easy way to remember

Imagine you have a Customer and Orders relationship:

- One Order belongs to one Customer → `select_related("customer")`.
- One Customer has multiple Orders → `prefetch_related("orders")`.

---

# 19. Transactions in Django

## What is a transaction?

A transaction is a group of database operations that should be treated as one single unit.

Either all database operations should succeed, or none of them should be saved.

This is important when multiple database operations depend on each other.

### Example: Bank money transfer

Imagine Shiv transfers ₹5,000 to Parvati.

There are two database operations:

1. Deduct ₹5,000 from Shiv's account.
2. Add ₹5,000 to Parvati's account.

Suppose the first operation succeeds but the second operation fails.

What happens?

Shiv loses ₹5,000, but Parvati does not receive ₹5,000. That is a serious problem!

We need a mechanism that ensures both operations succeed together. This is exactly what database transactions provide.

## Example model

```python
from django.db import models


class BankAccount(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
```

## Without transactions

```python
shiv = BankAccount.objects.get(name="Shiv")
parvati = BankAccount.objects.get(name="Parvati")

shiv.balance -= 5000
parvati.balance += 5000

shiv.save()
parvati.save()
```

Suppose an error occurs after `shiv.save()` and before `parvati.save()`.

The amount is deducted from Shiv's account but is not credited to Parvati's account.

This is where transactions become important.

## Solution: `transaction.atomic()`

We can use `transaction.atomic()` to execute multiple database operations as one transaction.

```python
from django.db import transaction


def transfer_money():
    with transaction.atomic():
        shiv = BankAccount.objects.get(name="Shiv")
        parvati = BankAccount.objects.get(name="Parvati")

        shiv.balance -= 5000
        shiv.save()

        parvati.balance += 5000
        parvati.save()
```

- If an exception occurs inside the atomic block, Django rolls back the transaction.
- If everything succeeds, Django commits the changes.

## Another real-life example: Customer order

Suppose a customer places an order. Your application needs to:

1. Create a new order.
2. Add products to that order.
3. Reduce the stock quantity of those products.
4. Save the order details.

These operations should succeed or fail together.

## Using `transaction.atomic()` as a decorator

You can also use `atomic()` as a decorator.

```python
from django.db import transaction


@transaction.atomic
def create_customer():
    customer = Customer.objects.create(name="Shiv")

    CustomerProfile.objects.create(
        customer=customer,
        date_of_birth="1998-05-10",
        address="Pune"
    )
```

The function's database operations are committed together if they complete successfully. If an exception causes the transaction to roll back, the database changes made within it are rolled back.
