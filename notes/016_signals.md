# Django Signals – Complete Notes

## 1. What are Django Signals?

Django Signals allow one part of a Django application to automatically notify another part when a particular event occurs.

In simple words:

**Signals allow us to execute additional code automatically when a specific action happens in Django, without manually calling that code from every place where the action occurs.**

Signals are utilities that allow us to associate events with actions.

They allow certain senders to notify a set of receivers that an action has taken place.

### Real-life example: Online shopping notification

Imagine that you order a product from an online shopping application.

What happens?

1. You place an order.
2. The application saves your order.
3. You automatically receive an order confirmation message.
4. The shopkeeper receives an order notification.

You did not manually call the notification system from every place that creates an order.

Instead, the application can use an event-based mechanism to trigger these additional operations when an order is created.

Django Signals provide this kind of mechanism.

---

## 2. Why do we need Django Signals?

Suppose we are developing a Customer Management System.

We have a `Customer` model:

```python
from django.db import models


class Customer(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField()
```

Whenever a new customer is registered, we want to:

1. Save customer information in the database.
2. Create a customer profile automatically.
3. Send a welcome email.
4. Create an activity log.

### Without signals

We might write all these operations inside our view:

```python
from django.shortcuts import redirect

from .models import Customer


def create_customer(request):

    customer = Customer.objects.create(
        name="Shiv",
        email="shiv@example.com"
    )

    # Create customer profile

    # Send welcome email

    # Create activity log

    return redirect('customer_list')
```

This creates a problem:

- Our view becomes responsible for too many tasks.
- The same additional operations might need to be repeated in multiple views.
- If another part of the application creates a customer, we must remember to repeat those operations.

### With signals

We can separate the additional operations from the main business logic.

For example:

```text
Customer Created
       |
       v
   post_save Signal
       |
       +----------------------+
       |                      |
       v                      v
Create Profile           Create Activity Log
       |
       v
Send Welcome Email
```

Now, whenever a customer is saved, Django can notify the registered receiver function.

**Important:** Signals help separate event-driven tasks from the code that triggers an event. However, they should not be used for every operation. If the business process must be explicit, predictable, and easy to follow, calling a service function directly may be a better choice.

---

## 3. Important Terms: Signal, Sender and Receiver

There are three important terms in Django Signals.

| Term | Meaning |
|---|---|
| Signal | Announces that an event has happened. |
| Sender | The model or object that generates the event. |
| Receiver | The function that responds to the event. |

### Example

```python
@receiver(post_save, sender=Customer)
def create_customer_profile(sender, instance, created, **kwargs):

    if created:

        CustomerProfile.objects.create(customer=instance)
```

Here:

- `post_save` is the signal.
- `Customer` is the sender.
- `create_customer_profile` is the receiver.

---

## 4. Types of Django Signals

Django provides several built-in signals.

The important signal groups covered in these notes are:

1. Login and Logout Signals
2. Model Signals
3. Management Signals
4. Request/Response Signals
5. Database Signals
6. Test-related Signals
7. Custom Signals

The sections below explain the main built-in signal groups and their important signals.

---

## 5. How to Create Custom Model Signals

Let's create a signal that automatically creates a customer profile whenever a new customer is registered.

### Step 1: Create the models

`models.py`

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

    address = models.CharField(
        max_length=200,
        blank=True
    )
```

We use `OneToOneField` because each customer should have one customer profile.

### Step 2: Create a `signals.py` file

Inside the application folder, create a separate file named `signals.py`.

```text
customer_app/
    __init__.py
    admin.py
    apps.py
    models.py
    signals.py
    views.py
```

### Step 3: Write the receiver function

`signals.py`

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Customer, CustomerProfile


@receiver(post_save, sender=Customer)
def create_customer_profile(sender, instance, created, **kwargs):

    if created:

        CustomerProfile.objects.create(
            customer=instance
        )

        print("Customer profile created successfully!")
```

Let's understand the code.

#### A. `post_save`

```python
from django.db.models.signals import post_save
```

`post_save` is a built-in Django model signal.

It is sent after a model instance's `save()` method completes.

#### B. `receiver`

```python
from django.dispatch import receiver
```

The `receiver` decorator connects a Python function to a signal.

#### C. `@receiver()`

```python
@receiver(post_save, sender=Customer)
```

This connects our receiver function to the `post_save` signal for the `Customer` model.

It means:

Whenever a `Customer` object is saved, Django calls this receiver function.

#### D. `sender=Customer`

```python
sender=Customer
```

This specifies which model generates the signal.

Our receiver will respond to `post_save` events sent by the `Customer` model.

#### E. `instance`

```python
instance
```

It represents the actual model object that was saved.

For example, if we save this customer:

```python
Customer.objects.create(
    name="Shiv",
    email="shiv@example.com"
)
```

The `instance` argument represents that newly created customer object.

#### F. `created`

```python
if created:
```

This tells us whether the object was newly created.

| Situation | `created` value |
|---|---|
| New customer created | `True` |
| Existing customer updated | `False` |

We use this condition because we only want to create a customer profile when a new customer is registered.

#### G. `**kwargs`

```python
**kwargs
```

It accepts additional keyword arguments passed by Django when the signal is sent.

Signal receivers should accept the documented signal arguments and `**kwargs` so they remain compatible with the signal's arguments.

---

## 6. Register Signals in `apps.py`

One important thing:

Django must import your `signals.py` file so that the receiver functions get registered.

We can do this using the `ready()` method of an application's configuration class.

`apps.py`

```python
from django.apps import AppConfig


class CustomerAppConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'

    name = 'customer_app'

    def ready(self):

        from . import signals
```

### What is `ready()`?

The `ready()` method runs when Django initializes the application registry.

It imports `signals.py`, which registers the receiver functions.

### Register the application in `settings.py`

Add the AppConfig class path to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [

    # Django applications

    'customer_app.apps.CustomerAppConfig',

]
```

Use your actual application name and AppConfig class.

**Important:** In modern Django versions, registering the AppConfig class path is the recommended approach. The old `default_app_config` setting in an app's `__init__.py` is no longer needed.

---

## 7. Test the Signal

Now we can test whether the signal works.

Open the terminal and run:

```bash
python manage.py shell
```

Create a customer:

```python
from customer_app.models import Customer

customer = Customer.objects.create(
    name="Shiv",
    email="shiv@example.com"
)
```

Expected result:

```text
Customer profile created successfully!
```

Check whether the profile was created:

```python
from customer_app.models import CustomerProfile

CustomerProfile.objects.all()
```

We can also check the related profile:

```python
customer.customerprofile
```

The exact reverse relation name depends on the field's `related_name`. Without a custom `related_name`, Django uses the model's lowercase name.

### Test an update

```python
customer.name = "Shiv Updated"

customer.save()
```

The `post_save` signal will execute again, but `created` will be `False`.

Therefore, another profile will not be created.

---

## 8. Two Ways to Connect a Receiver to a Signal

Django provides two common ways to connect a receiver function to a signal.

### Method 1: Manual connection using `connect()`

We can register a receiver function using the signal's `connect()` method.

Example:

```python
from django.db.models.signals import post_save

from .models import Customer


def receiver_fun(sender, instance, **kwargs):

    print("Customer saved:", instance.name)


post_save.connect(
    receiver_fun,
    sender=Customer
)
```

Syntax:

```python
signal.connect(
    receiver,
    sender=None,
    weak=True,
    dispatch_uid=None
)
```

#### Parameters

| Parameter | Meaning |
|---|---|
| `receiver` | The callback function connected to the signal. |
| `sender` | Specifies the particular sender to receive signals from. |
| `weak` | Controls whether Django stores the receiver as a weak reference. |
| `dispatch_uid` | A unique identifier used to prevent duplicate registration of the same receiver. |

**Understanding `weak`:**

Django stores signal receivers as weak references by default.

If a receiver is a local function or another object that has no strong reference, it may be garbage-collected.

To prevent that, we can use:

```python
signal.connect(
    receiver_fun,
    sender=Customer,
    weak=False
)
```

**Understanding `dispatch_uid`:**

It provides a unique identifier for a receiver.

Example:

```python
post_save.connect(
    receiver_fun,
    sender=Customer,
    dispatch_uid='customer_post_save_receiver'
)
```

This helps prevent duplicate registration when the same receiver is connected multiple times with the same dispatch UID.

### Method 2: Using the `@receiver` decorator

This is a convenient and commonly used method.

Example:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Customer


@receiver(post_save, sender=Customer)
def receiver_fun(sender, instance, **kwargs):

    print("Customer saved:", instance.name)
```

This decorator connects the function to the specified signal.

It is equivalent to registering the function using `signal.connect()`.

---

## 9. Built-in Django Signals

Django provides built-in signals that allow application code to get notified when particular actions happen inside Django.

The following sections cover the built-in signal groups from the original notes.

### 9.1 Login and Logout Signals

The Django authentication framework provides signals that notify us when a user logs in or logs out.

Import them from:

```python
from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed
)
```

#### A. `user_logged_in`

Sent when a user successfully logs in.

Arguments:

| Argument | Meaning |
|---|---|
| `sender` | The class of the user that just logged in. |
| `request` | The current `HttpRequest` instance. |
| `user` | The user instance that just logged in. |

Example:

```python
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


@receiver(user_logged_in)
def login_success(sender, request, user, **kwargs):

    print(user.username, "logged in successfully")
```

#### B. `user_logged_out`

Sent when the logout process occurs.

Arguments:

| Argument | Meaning |
|---|---|
| `sender` | The user class, or `None` if the user was not authenticated. |
| `request` | The current `HttpRequest` instance. |
| `user` | The user who logged out, or `None` if the user was not authenticated. |

Example:

```python
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver


@receiver(user_logged_out)
def logout_success(sender, request, user, **kwargs):

    print("User logged out:", user)
```

#### C. `user_login_failed`

Sent when a user fails to log in successfully.

Arguments:

| Argument | Meaning |
|---|---|
| `sender` | The authentication backend path or identifier. |
| `credentials` | A dictionary of credentials passed to authentication, with sensitive values filtered. |
| `request` | The `HttpRequest` object, if provided. |

Example:

```python
from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver


@receiver(user_login_failed)
def login_failed(sender, credentials, request, **kwargs):

    print("Login failed")
```

**Security note:** Do not print or store raw login credentials. Django filters sensitive credential values before sending this signal, but applications should still treat authentication data carefully.

---

### 9.2 Model Signals

Model signals are sent by Django's model system when certain model-related operations happen.

Import them from:

```python
from django.db.models import signals
```

Important model signals:

#### A. `pre_init`

Sent at the beginning of a model's `__init__()` method.

It happens whenever a model instance is initialized.

Arguments:

| Argument | Meaning |
|---|---|
| `sender` | The model class being initialized. |
| `args` | Positional arguments passed to `__init__()`. |
| `kwargs` | Keyword arguments passed to `__init__()`. |

#### B. `post_init`

Sent after a model's `__init__()` method finishes.

Arguments:

| Argument | Meaning |
|---|---|
| `sender` | The model class being initialized. |
| `instance` | The newly initialized model instance. |

#### C. `pre_save`

Sent at the beginning of a model's `save()` operation.

Arguments:

| Argument | Meaning |
|---|---|
| `sender` | The model class. |
| `instance` | The model instance being saved. |
| `raw` | `True` when saving fixture data in raw mode. |
| `using` | Database alias being used. |
| `update_fields` | The fields being updated, or `None`. |

**Important:** When `raw=True`, avoid querying or modifying other records because the database may not yet be in a consistent state while fixtures are being loaded.

#### D. `post_save`

Sent at the end of a model's `save()` operation.

Arguments:

| Argument | Meaning |
|---|---|
| `sender` | The model class. |
| `instance` | The model instance being saved. |
| `created` | `True` for a newly created record; otherwise `False`. |
| `raw` | Indicates whether the model is being saved in raw fixture mode. |
| `using` | Database alias being used. |
| `update_fields` | Fields being updated, or `None`. |

Example:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Customer


@receiver(post_save, sender=Customer)
def customer_saved(sender, instance, created, raw, using, update_fields, **kwargs):

    if created:
        print("New customer created:", instance.name)
    else:
        print("Customer updated:", instance.name)
```

#### E. `pre_delete`

Sent at the beginning of a model's `delete()` operation or a queryset's `delete()` operation.

Arguments:

| Argument | Meaning |
|---|---|
| `sender` | The model class. |
| `instance` | The model instance being deleted. |
| `using` | Database alias being used. |

#### F. `post_delete`

Sent at the end of a model's `delete()` operation or a queryset's `delete()` operation.

Arguments:

| Argument | Meaning |
|---|---|
| `sender` | The model class. |
| `instance` | The model instance that was deleted. |
| `using` | Database alias being used. |

**Important:** After deletion, the object no longer exists in the database. Be careful when accessing or modifying related data using this instance.

#### G. `m2m_changed`

Sent when a Many-to-Many relationship changes.

Arguments:

| Argument | Meaning |
|---|---|
| `sender` | The intermediate Many-to-Many model. |
| `instance` | The model instance whose relationship is changing. |
| `action` | The operation being performed. |
| `reverse` | Indicates whether the operation is on the reverse relation. |
| `model` | The class of the related objects. |
| `pk_set` | Set of related object primary keys, where applicable. |
| `using` | Database alias being used. |

Common `action` values include:

- `pre_add`
- `post_add`
- `pre_remove`
- `post_remove`
- `pre_clear`
- `post_clear`

Example:

```python
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Student


@receiver(m2m_changed, sender=Student.courses.through)
def courses_changed(sender, instance, action, **kwargs):

    print("Many-to-Many action:", action)
```

This example assumes that `Student` has a Many-to-Many field named `courses`.

#### H. `class_prepared`

Sent when a model class has been prepared and registered with Django's model system.

Argument:

| Argument | Meaning |
|---|---|
| `sender` | The model class that was just prepared. |

Django uses this signal internally. It is not generally needed in ordinary application development.

---

### 9.3 Request/Response Signals

These signals are sent by Django's core framework while processing HTTP requests.

Import them from:

```python
from django.core.signals import (
    request_started,
    request_finished,
    got_request_exception
)
```

#### A. `request_started`

Sent when Django begins processing an HTTP request.

Arguments:

| Argument | Meaning |
|---|---|
| `sender` | The handler class processing the request. |
| `environ` | The WSGI environment dictionary, when applicable. |

#### B. `request_finished`

Sent when Django finishes delivering an HTTP response.

Argument:

| Argument | Meaning |
|---|---|
| `sender` | The handler class. |

#### C. `got_request_exception`

Sent when Django encounters an exception while processing an incoming HTTP request.

Arguments:

| Argument | Meaning |
|---|---|
| `sender` | Unused; normally `None`. |
| `request` | The current request object. |

**Correction:** The `request` argument is an `HttpRequest` object, not an `HttpResponse` object.

---

### 9.4 Management Signals

Management signals are sent by Django's management commands, such as the `migrate` command.

Import them from:

```python
from django.core.signals import pre_migrate, post_migrate
```

#### A. `pre_migrate`

Sent before Django starts applying migrations for an application.

Arguments:

| Argument | Meaning |
|---|---|
| `sender` | The `AppConfig` instance for the application being migrated. |
| `app_config` | The same application configuration instance. |
| `verbosity` | Controls how much information the command displays. |
| `interactive` | Indicates whether command-line interaction is allowed. |
| `using` | Database alias being used. |
| `plan` | Migration plan for the operation. |
| `apps` | Historical app registry for the migration operation. |

Important points:

- If `interactive=True`, it is safe for receivers to prompt for user input.
- If `interactive=False`, receivers should not prompt for input.
- Use the supplied historical `apps` registry when retrieving models for migration-related operations.

#### B. `post_migrate`

Sent at the end of the `migrate` command, even if no migrations were applied.

It is also sent at the end of the `flush` command.

Arguments:

| Argument | Meaning |
|---|---|
| `sender` | The `AppConfig` instance for the application. |
| `app_config` | The application configuration instance. |
| `verbosity` | Controls output detail. |
| `interactive` | Indicates whether interactive input is allowed. |
| `using` | Database alias being used. |
| `plan` | Migration plan used for the operation. |
| `apps` | Historical app registry after migration. |

**Important:** A `post_migrate` receiver must not perform database schema alterations. Doing so can cause problems, particularly when the signal is sent during `flush`.

---

### 9.5 Database Signals

Django provides database signals that notify us about database connection events.

Import them from:

```python
from django.db.backends.signals import connection_created
```

#### `connection_created`

Sent when Django's database wrapper creates a new database connection.

Arguments:

| Argument | Meaning |
|---|---|
| `sender` | The database wrapper class. |
| `connection` | The database connection that was opened. |

It is useful when we need to perform additional setup immediately after a database connection is created.

Example:

```python
from django.db.backends.signals import connection_created
from django.dispatch import receiver


@receiver(connection_created)
def database_connected(sender, connection, **kwargs):

    print("Database connection created:", connection.alias)
```

In a multiple-database configuration, `connection.alias` helps identify which database connection was created.

---

### 9.6 Test Signals

Django also provides signals related to the test framework.

One example is:

`setting_changed`

It is sent when a setting changes through Django's test utilities, such as `override_settings()`.

Import:

```python
from django.test.signals import setting_changed
```

It can be useful when test code needs to respond to changes in Django settings.

---

## 10. Custom Signals

Apart from Django's built-in signals, we can define our own signals.

Custom signals are useful when we want to notify other parts of our application that a particular business event has happened.

For example:

- An order has been placed.
- A payment has been completed.
- A report has been generated.
- A customer has been approved.

### Step 1: Define a custom signal

`signals.py`

```python
import django.dispatch


order_placed = django.dispatch.Signal()
```

### Step 2: Connect a receiver

```python
from django.dispatch import receiver

from .signals import order_placed


@receiver(order_placed)
def order_notification(sender, order, **kwargs):

    print("New order received:", order)
```

### Step 3: Send the signal

From the business logic that completes an order:

```python
from .signals import order_placed


order_placed.send(
    sender=Order,
    order=order
)
```

The receiver function will be called when the signal is sent.

**Important:** The sender and keyword arguments supplied when sending a custom signal must match what the receiver expects.

For new code, custom signal definitions can also declare expected keyword argument names using `Signal(providing_args=...)` only in older Django versions. That parameter was removed in modern Django versions, so do not use it.

---

## 11. Important Points About Django Signals

1. Signals allow different parts of an application to communicate through events.
2. A signal announces that an event has happened.
3. A sender generates the signal.
4. A receiver responds to the signal.
5. Receiver functions can be connected using `signal.connect()` or the `@receiver` decorator.
6. `signals.py` is a conventional place to define receiver functions, but Django does not require this filename.
7. Use `AppConfig.ready()` to import the signals module and register receivers.
8. Register the AppConfig class path in `INSTALLED_APPS`.
9. Use `dispatch_uid` when duplicate receiver registration is a concern.
10. Avoid placing slow operations such as sending emails directly inside a receiver when they can delay the request. Consider a background task system.
11. Avoid creating circular imports between models and signals. Import models carefully, and use `apps.get_model()` when appropriate.
12. Signals are not automatically sent by every possible database operation. For example, `QuerySet.update()` does not call each object's `save()` method and does not emit `pre_save` or `post_save` signals for each updated object.

---

## 12. Common Mistakes

### Mistake 1: Forgetting to import signals

Creating `signals.py` alone does not register the receivers.

Correct approach:

```python
class CustomerAppConfig(AppConfig):

    name = 'customer_app'

    def ready(self):

        from . import signals
```

### Mistake 2: Creating duplicate profiles

Incorrect:

```python
@receiver(post_save, sender=Customer)
def create_profile(sender, instance, **kwargs):

    CustomerProfile.objects.create(customer=instance)
```

This creates a profile every time the customer is saved, including updates.

Correct:

```python
@receiver(post_save, sender=Customer)
def create_profile(sender, instance, created, **kwargs):

    if created:

        CustomerProfile.objects.create(customer=instance)
```

### Mistake 3: Using signals for every operation

Signals can make the flow of an application harder to understand when too much business logic is hidden inside receivers.

Use signals for suitable event-driven side effects, not as a replacement for all normal function calls.

### Mistake 4: Assuming `post_save` runs for `QuerySet.update()`

Example:

```python
Customer.objects.filter(id=1).update(name="Shiv Updated")
```

This performs a direct database update. It does not call the model's `save()` method and does not emit `pre_save` or `post_save`.

### Mistake 5: Assuming signals are asynchronous

Signals normally execute synchronously in the same process.

If a receiver sends an email or performs a slow API call, the operation can delay the request that triggered the signal.

Use a background task queue when asynchronous execution is required.

---

## 13. Middleware vs Signals

Both middleware and signals allow us to execute additional logic, but they solve different problems.

| Middleware | Signals |
|---|---|
| Works with Django's request/response processing | Works with events occurring in Django |
| Commonly used for request-wide processing | Used to notify receivers about specific events |
| Registered in `settings.py` | Receivers registered through signal connections |
| Example: log every incoming request | Example: create a profile after customer creation |
| Has request/response hooks | Has senders and receivers |

### Simple difference

- **Middleware:** Execute code around HTTP request/response processing.
- **Signals:** Execute code when a particular event happens.

---

## 14. Quick Revision

| Signal | When does it execute? |
|---|---|
| `pre_init` | Before a model instance is initialized. |
| `post_init` | After a model instance is initialized. |
| `pre_save` | Before a model is saved. |
| `post_save` | After a model is saved. |
| `pre_delete` | Before a model is deleted. |
| `post_delete` | After a model is deleted. |
| `m2m_changed` | When a Many-to-Many relationship changes. |
| `user_logged_in` | When a user logs in successfully. |
| `user_logged_out` | When a user logs out. |
| `user_login_failed` | When authentication fails. |
| `request_started` | When Django starts processing a request. |
| `request_finished` | When Django finishes delivering a response. |
| `got_request_exception` | When Django encounters a request-processing exception. |
| `pre_migrate` | Before migration operations. |
| `post_migrate` | After migration operations. |
| `connection_created` | When a database connection is created. |
| `setting_changed` | When a setting changes through the test utilities. |

### Most important concepts

- Signal = Event notification.
- Sender = Event generator.
- Receiver = Function that responds.
- `post_save` = Runs after saving a model.
- `pre_save` = Runs before saving a model.
- `@receiver()` = Decorator used to connect a receiver.
- `connect()` = Method used to connect a receiver manually.
- `ready()` = Used to import and register receivers when Django initializes an application.
- `created` = Indicates whether the saved record is new.
- `instance` = The actual model object involved in the event.

---

## 15. Practice Questions

Try answering these questions to check your understanding.

1. What are Django Signals?
2. Why do we need signals?
3. What are the three important terms in Django Signals?
4. What is the difference between `pre_save` and `post_save`?
5. What is the purpose of the `created` argument?
6. What is the difference between `connect()` and `@receiver()`?
7. Why do we create a `signals.py` file?
8. What is the purpose of `AppConfig.ready()`?
9. What is the difference between `user_logged_in` and `user_login_failed`?
10. What is the purpose of `m2m_changed`?
11. What is the purpose of `connection_created`?
12. Do signals execute asynchronously by default?
13. Does `QuerySet.update()` trigger `post_save`?
14. What is the difference between middleware and signals?

### Practical task

Create a Customer Management System using Django Signals.

Requirements:

1. Create a `Customer` model.
2. Create a `CustomerProfile` model with a `OneToOneField` relationship.
3. Create a `post_save` receiver for the `Customer` model.
4. Automatically create a customer profile when a new customer is registered.
5. Do not create another profile when an existing customer is updated.
6. Test the signal using Django shell.

This practical task will help you understand how Django Signals work in a real-world application.