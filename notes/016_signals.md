# Django Signals

## 1. What are Django Signals?

Django Signals provide a way for one part of a Django application to notify another part when a particular event happens.

In simple words:

- An event happens in Django.
- Django sends a signal to announce that the event occurred.
- A receiver function that is connected to that signal is called automatically.
- The receiver performs an additional task.

You do not call the receiver function directly at the place where the event occurs. Django's signal dispatcher calls it when the signal is sent.

**Example:** When a customer is created, Django can automatically call a receiver function to create that customer's profile.

> Signals are useful when separate parts of an application need to react to the same event without the sender needing to know about those receivers.

## 2. Real-life example: online shopping notification

Imagine that a customer places an order in an online shopping application.

1. The customer places an order.
2. The application saves the order.
3. The customer receives an order confirmation.
4. The shopkeeper receives an order notification.

The order-creation code does not necessarily need to know the internal details of every notification task. A signal can announce that an order has been created, and registered receivers can react to that event.

This is the basic idea behind Django Signals.

## 3. Why do we need Django Signals?

Suppose we are developing a Customer Management System and have a `Customer` model:

```python
from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
```

Whenever a new customer is registered, we want to:

1. Save the customer's information in the database.
2. Create a customer profile automatically.
3. Send a welcome email.
4. Create an activity log.

Without signals, we might put all these operations inside the view:

```python
from django.shortcuts import redirect
from .models import Customer


def create_customer(request):
    customer = Customer.objects.create(
        name="Shiv",
        email="shiv@example.com",
    )

    # Create customer profile.
    # Send welcome email.
    # Create activity log.

    return redirect("customer_list")
```

As the application grows, the view can become responsible for too many tasks. If another part of the application creates a customer, we may also have to remember to repeat those additional operations.

Signals can move suitable follow-up tasks into separate receiver functions. The customer-creation code sends the event, and the registered receivers respond to it.

**Important:** Signals do not replace views, services, or business logic. They are one tool for separating event-related tasks.

## 4. How do Django Signals work?

There are three important terms:

| Term | Meaning |
|---|---|
| **Signal** | Announces that an event has happened. |
| **Sender** | The model or object that sends the signal. |
| **Receiver** | The function or method that responds to the signal. |

For example, when a `Customer` object is saved:

- **Signal:** `post_save`
- **Sender:** `Customer` model class
- **Receiver:** `create_customer_profile()`
- **Instance:** The particular customer object that was saved

A simplified flow:

```text
Customer object is saved
          |
          v
     post_save signal
          |
          v
   Receiver function runs
          |
          v
Create customer profile
```

## 5. Types of Django Signals

Django provides built-in signals for different events. The main categories are:

1. Authentication signals (login and logout)
2. Model signals
3. Management signals
4. Request/response signals
5. Test signals
6. Database connection signals

Django also allows us to define custom signals.

The detailed signals in each category are explained below.

## 6. Creating and registering a model signal

We will use the Customer Management System example to understand how to create a signal.

### Step 1: Create the models

In `models.py`:

```python
from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()


class CustomerProfile(models.Model):
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    bio = models.TextField(blank=True)
```

Here, each customer has one related profile.

### Step 2: Create a `signals.py` file

Create `signals.py` inside the same Django application, alongside files such as `models.py` and `apps.py`.

Example application structure:

```text
customer_app/
    migrations/
    __init__.py
    admin.py
    apps.py
    models.py
    signals.py
    views.py
```

### Step 3: Write the receiver function

In `signals.py`:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Customer, CustomerProfile


@receiver(post_save, sender=Customer)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        CustomerProfile.objects.create(customer=instance)
        print("Customer profile created successfully!")
```

Explanation:

- `post_save` is sent after Django saves a model instance.
- `@receiver(...)` connects the function to the signal.
- `sender=Customer` means this receiver listens for `post_save` events from the `Customer` model.
- `sender` is the model class that sent the signal.
- `instance` is the actual model object that was saved.
- `created` is `True` when a new database record was created and `False` when an existing record was updated.
- `**kwargs` accepts the other keyword arguments sent with the signal.

The `if created:` condition ensures that the profile is created only when a new customer is inserted, not every time an existing customer is updated.

**Note:** This example assumes the profile does not already exist. If other code can create profiles independently, handle the possibility of an existing profile (for example, with `get_or_create()`) to avoid a one-to-one uniqueness error.

### Step 4: Register the signals in `apps.py`

Django must import the `signals.py` module so that the receiver is registered.

In `apps.py`:

```python
from django.apps import AppConfig


class CustomerAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "customer_app"

    def ready(self):
        from . import signals
```

Explanation:

- `AppConfig` stores configuration for a Django application.
- `ready()` is called when Django has loaded the application registry.
- Importing `signals` runs the `@receiver` decorator and connects the receiver function to the signal.

The import is intentionally inside `ready()`. This avoids importing signal handlers too early during application loading.

### Step 5: Register the application configuration

In `settings.py`, add the application configuration class to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # Django applications...

    "customer_app.apps.CustomerAppConfig",
]
```

Use your actual application package and configuration class names.

**Important:** In modern Django versions, do not add `default_app_config` to the app's `__init__.py`. That setting is obsolete. Register the `AppConfig` class in `INSTALLED_APPS` as shown above. If Django can automatically discover your app configuration, the short app name may also work, but the explicit configuration path makes the registration clear.

### Step 6: Test the signal

Start the Django shell:

```bash
python manage.py shell
```

Create a customer:

```python
from customer_app.models import Customer, CustomerProfile

customer = Customer.objects.create(
    name="Shiv",
    email="shiv@example.com",
)
```

The `post_save` signal is sent, and the receiver creates the profile.

Check the profile:

```python
CustomerProfile.objects.get(customer=customer)
```

Update the same customer:

```python
customer.name = "Shiv Updated"
customer.save()
```

The receiver runs again because `post_save` is sent after the update too. However, `created` is `False`, so the profile is not created again.

## 7. Receiver functions

A receiver is a Python function or method that is called when a connected signal is sent.

A receiver must accept the `sender` argument and should accept `**kwargs`:

```python
def my_receiver(sender, **kwargs):
    print("A signal was received.")
```

Why use `**kwargs`?

Django sends signal data as keyword arguments. The arguments depend on the particular signal. Accepting `**kwargs` makes the receiver compatible with the documented signal arguments and future additions.

A receiver can be an ordinary function, a method, or an asynchronous function. For most beginner examples, a normal function is sufficient.

## 8. Connecting a receiver to a signal

There are two common ways to connect a receiver.

### Method 1: Using `Signal.connect()`

```python
from django.db.models.signals import post_save
from .models import Customer


def customer_saved(sender, instance, created, **kwargs):
    print("Customer save event received.")


post_save.connect(customer_saved, sender=Customer)
```

Syntax:

```python
signal.connect(
    receiver,
    sender=None,
    weak=True,
    dispatch_uid=None,
)
```

Parameters:

| Parameter | Explanation |
|---|---|
| `receiver` | The callback function or method to connect. |
| `sender` | Optional. Limits the receiver to a particular sender. |
| `weak` | Defaults to `True`. Django stores receivers as weak references. |
| `dispatch_uid` | Optional unique identifier used to prevent duplicate registrations. |

**About `weak`:** If a receiver is a local function and nothing else keeps a strong reference to it, it may be garbage-collected. Use `weak=False` when you need to prevent that:

```python
post_save.connect(
    customer_saved,
    sender=Customer,
    weak=False,
)
```

### Method 2: Using the `@receiver` decorator

This is a convenient and commonly used approach:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Customer


@receiver(post_save, sender=Customer)
def customer_saved(sender, instance, created, **kwargs):
    print("Customer save event received.")
```

The decorator connects the function to `post_save`.

The `sender=Customer` argument means that the receiver responds only to save events sent by the `Customer` model.

## 9. Important arguments received by model signal handlers

The exact arguments depend on the signal.

| Argument | Meaning |
|---|---|
| `sender` | The model class that sent the signal. |
| `instance` | The model object involved in the event, when provided by that signal. |
| `created` | For `post_save`, indicates whether a new record was created. |
| `raw` | For save signals, indicates whether the model is being saved as presented while loading a fixture. |
| `using` | The database alias used for the operation. |
| `update_fields` | The set of fields passed to `save(update_fields=...)`, or `None`. |

For example, if a new customer named Shiv is saved, `instance` represents that particular customer object. You can access its fields:

```python
print(instance.name)
print(instance.email)
```

The `created` argument is specific to `post_save`; it is not supplied by every signal.

## 10. Built-in Django Signals

Django's built-in signals are grouped by the part of the framework that sends them.

### 10.1 Authentication signals

**Module:** `django.contrib.auth.signals`

Django's authentication framework sends these signals when a user logs in, logs out, or fails to log in.

#### 1. `user_logged_in`

Sent after a user successfully logs in.

Arguments:

- `sender`: The class of the user that just logged in.
- `request`: The current `HttpRequest` instance.
- `user`: The user instance that just logged in.

Example use cases:

- Record a successful login.
- Update a user's last-activity information.
- Create an audit log.

#### 2. `user_logged_out`

Sent when the logout process is called.

Arguments:

- `sender`: The user class, or `None` if the user was not authenticated.
- `request`: The current `HttpRequest` instance.
- `user`: The user instance, or `None` if the user was not authenticated.

Example use case: Record when a user logs out.

#### 3. `user_login_failed`

Sent when authentication fails.

Arguments:

- `sender`: The name of the authentication backend.
- `credentials`: A dictionary containing the credentials supplied for authentication. Values matching sensitive patterns (including passwords) are cleansed before being sent.
- `request`: The `HttpRequest` object, if one was provided to `authenticate()`.

Example use cases:

- Monitor repeated failed login attempts.
- Record security-related events.

**Security note:** Do not log passwords or other sensitive authentication data.

### 10.2 Model signals

**Module:** `django.db.models.signals`

Model signals are sent by Django's model system during model initialization, saving, deleting, and many-to-many relationship changes.

#### 1. `pre_init`

Sent at the beginning of a model's `__init__()` method, whenever a model instance is initialized.

Arguments:

- `sender`: The model class being initialized.
- `args`: Positional arguments passed to `__init__()`.
- `kwargs`: Keyword arguments passed to `__init__()`.

#### 2. `post_init`

Sent after a model's `__init__()` method finishes.

Arguments:

- `sender`: The model class.
- `instance`: The newly initialized model instance.

**Note:** Avoid database queries in `pre_init` and `post_init` receivers. These signals can run for every model instance created while iterating over a queryset, which can cause performance problems.

#### 3. `pre_save`

Sent at the beginning of a model's `save()` method.

Arguments:

- `sender`: The model class.
- `instance`: The model instance being saved.
- `raw`: `True` when the object is being saved as presented during fixture loading. Avoid querying or modifying other records in this situation because the database may not be in a consistent state.
- `using`: The database alias being used.
- `update_fields`: The fields passed to `save(update_fields=...)`, or `None`.

Example use case: Perform a small preparation step before a model is saved.

#### 4. `post_save`

Sent at the end of a model's `save()` method.

Arguments:

- `sender`: The model class.
- `instance`: The model instance that was saved.
- `created`: `True` if a new record was created; otherwise `False`.
- `raw`: `True` when saving a fixture as presented.
- `using`: The database alias being used.
- `update_fields`: The fields passed to `save(update_fields=...)`, or `None`.

Example use cases:

- Create a related profile when a customer is created.
- Record an activity after a record is saved.
- Trigger a follow-up task.

#### 5. `pre_delete`

Sent at the beginning of a model instance's `delete()` method or a queryset's `delete()` method.

Arguments:

- `sender`: The model class.
- `instance`: The model instance being deleted.
- `using`: The database alias being used.
- `origin`: The model instance or queryset from which the deletion originated.

Example use case: Record information about a record before it is deleted.

#### 6. `post_delete`

Sent at the end of a model instance's `delete()` method or a queryset's `delete()` method.

Arguments:

- `sender`: The model class.
- `instance`: The model instance that was deleted.
- `using`: The database alias being used.
- `origin`: The model instance or queryset from which the deletion originated.

**Important:** The object has already been deleted from the database. The Python `instance` still exists in memory, so you can inspect its field values, but you cannot assume its database row still exists.

Example use case: Record a deletion in an audit log.

#### 7. `m2m_changed`

Sent when a `ManyToManyField` relationship changes.

Arguments:

- `sender`: The intermediate through model for the many-to-many relationship.
- `instance`: The model instance whose relationship is being changed.
- `action`: The operation being performed.
- `reverse`: Indicates whether the change is being made from the reverse side of the relationship.
- `model`: The class of the related objects.
- `pk_set`: The set of affected primary keys for add/remove actions; it is `None` for clear actions.
- `using`: The database alias being used.

Common `action` values:

| Action | Meaning |
|---|---|
| `pre_add` | Before objects are added. |
| `post_add` | After objects are added. |
| `pre_remove` | Before objects are removed. |
| `post_remove` | After objects are removed. |
| `pre_clear` | Before the relationship is cleared. |
| `post_clear` | After the relationship is cleared. |

Although it is documented with model signals, `m2m_changed` is sent by the many-to-many field's intermediate model manager.

Example use case: Track when a student is added to or removed from a course.

#### 8. `class_prepared`

Sent when a model class has been fully prepared and registered with Django's model system.

Arguments:

- `sender`: The model class that has just been prepared.

Django uses this signal internally. It is not commonly needed in normal application development.

**Important:** `class_prepared` is sent while Django is populating the application registry. `AppConfig.ready()` runs after the registry is populated, so registering a `class_prepared` receiver inside `ready()` is too late for model classes prepared earlier.

### 10.3 Request/response signals

**Module:** `django.core.signals`

These signals are sent by Django's core request-handling system.

#### 1. `request_started`

Sent when Django begins processing an HTTP request.

Arguments:

- `sender`: The handler class that handled the request, such as a WSGI or ASGI handler.
- `environ`: The WSGI environment dictionary. This argument is associated with the WSGI request handler; do not assume it is present for every request-handling path.

#### 2. `request_finished`

Sent when Django finishes delivering an HTTP response.

Argument:

- `sender`: The handler class that handled the request.

Example use case: Perform a lightweight action after request processing has finished.

#### 3. `got_request_exception`

Sent when Django encounters an exception while processing an incoming HTTP request.

Arguments:

- `sender`: The sender is documented as unused and is generally `None`.
- `request`: The current `HttpRequest` instance.

Example use case: Send an exception event to a monitoring or logging system.

**Note:** For request/response-wide behavior, middleware is often a clearer choice than request signals.

### 10.4 Management signals

**Module:** `django.db.models.signals`

Management signals are sent by Django management commands, particularly migration-related commands.

#### 1. `pre_migrate`

Sent by the `migrate` command before it starts applying migrations for an application.

It is not sent for applications that do not have a `models` module.

Arguments:

- `sender`: The `AppConfig` instance for the application about to be migrated.
- `app_config`: The same `AppConfig` instance as `sender`.
- `verbosity`: The verbosity level passed to the management command.
- `interactive`: Indicates whether the command may prompt for user input.
- `using`: The database alias on which the command operates.
- `plan`: The migration plan for the migration run.
- `apps`: The historical app registry representing the project state before the migration run.

**Important:** When working with models in migration signal handlers, use the supplied historical `apps` registry rather than importing current model classes. This helps ensure that the models match the migration state.

#### 2. `post_migrate`

Sent at the end of the `migrate` command, even if no migrations were run. It is also sent at the end of the `flush` command.

It is not sent for applications that do not have a `models` module.

Arguments:

- `sender`: The `AppConfig` instance for the application that was just migrated.
- `app_config`: The same `AppConfig` instance as `sender`.
- `verbosity`: The verbosity level passed to the command.
- `interactive`: Indicates whether the command may prompt for user input.
- `using`: The database alias used for synchronization.
- `plan`: The migration plan used for the migration run.
- `apps`: The historical app registry representing the project state after the migration run.

**Important:** A `post_migrate` receiver must not perform database schema alterations. Doing so can cause problems, especially when the signal is sent during the `flush` command.

Example use case: Create or update initial database data after migrations, when appropriate.

### 10.5 Test signals

**Module:** `django.test.signals`

#### `template_rendered`

Sent when Django's test system renders a template.

Arguments:

- `sender`: The `Template` object that was rendered.
- `template`: The rendered template (the same template object as `sender`).
- `context`: The context used to render the template.

**Note:** This signal is intended for Django's testing tools. It is not emitted during normal production request handling.

Example use case: Inspect which template was rendered and which context was supplied during a test.

### 10.6 Database connection signals

**Module:** `django.db.backends.signals`

#### `connection_created`

Sent when a database wrapper creates a new database connection.

Arguments:

- `sender`: The database wrapper class, such as a PostgreSQL or MySQL database wrapper.
- `connection`: The database connection that was opened.

Example use case: Run a database-specific setup command after a new connection is opened.

This signal can be useful in projects that use multiple databases because the `connection` object identifies the connection involved.

## 11. Custom Signals

Django allows us to create our own signals and send them when a specific event occurs in our application.

For example, suppose an order is marked as ready. We want another part of the application to be notified.

### Step 1: Define a custom signal

Create `signals.py` (or another suitable module) and define the signal:

```python
import django.dispatch

order_ready = django.dispatch.Signal()
```

### Step 2: Create a receiver

```python
from django.dispatch import receiver

@receiver(order_ready)
def notify_order_ready(sender, order_id, **kwargs):
    print(f"Order {order_id} is ready!")
```

### Step 3: Send the signal

From the code that marks the order as ready:

```python
from .signals import order_ready

order_ready.send(
    sender=Order,
    order_id=101,
)
```

When `order_ready.send()` runs, Django calls the registered receiver and passes `sender` and `order_id` to it.

**Important:** This is a simplified example. In a real application, keep the custom signal definition in a module that can be imported by both the sender and receiver, and register the receiver during application initialization. Avoid circular imports.

### `send()` and `send_robust()`

Django provides two common synchronous ways to send a signal:

- `send(sender, **kwargs)`: Calls the receivers. If a receiver raises an exception, that exception propagates and may prevent later receivers from being called.
- `send_robust(sender, **kwargs)`: Catches exceptions derived from `Exception`, continues notifying receivers, and returns the exception alongside the receiver's result.

For most simple examples, `send()` is sufficient. Choose `send_robust()` only when its error-handling behavior is appropriate for the use case.

## 12. Preventing duplicate signal execution

Sometimes a receiver may be registered more than once, especially if registration code runs repeatedly in tests or with recreated bound-method instances.

For manual connection, use a stable `dispatch_uid`:

```python
from django.db.models.signals import post_save

post_save.connect(
    customer_saved,
    sender=Customer,
    dispatch_uid="customer_saved_receiver",
)
```

Django uses this identifier to avoid registering the same receiver more than once for that sender and signal.

For ordinary module-level receiver functions, importing the same module normally does not create a new function object each time. However, be careful with bound methods and repeated initialization.

## 13. Important points and best practices

1. Put signal handlers in a dedicated `signals.py` module in the relevant app.
2. Import that module from the app configuration's `ready()` method.
3. Register the correct `AppConfig` class in `INSTALLED_APPS`.
4. Use `sender=YourModel` when the receiver should listen to one particular model.
5. Accept `sender` and `**kwargs` in receiver functions.
6. Use `created` in `post_save` when a task should happen only for newly created records.
7. Avoid slow work inside receivers because signal handlers run as part of signal dispatch. Consider a background task queue for long-running work.
8. Be careful when a receiver saves the same model that triggered it. This can cause the signal to run again and may create recursion.
9. Do not assume signals are sent for every possible database change. For example, `QuerySet.update()` does not call each model's `save()` method and does not send `pre_save` or `post_save`.
10. `QuerySet.delete()` does send `pre_delete` and `post_delete` for each deleted object, even though it does not call each model instance's `delete()` method.
11. Avoid unnecessary database queries in `pre_init` and `post_init`.
12. Be careful with fixture loading (`raw=True`) and do not query or modify related records from save receivers while fixtures are being loaded.
13. Signals are synchronous by default in the common `send()` path. A slow receiver can make the operation that sent the signal slower.
14. Use `transaction.on_commit()` when a follow-up action, such as sending a task to an external system, must happen only after the database transaction commits.
15. Do not use signals for every operation. If the sender and the follow-up operation are part of the same business workflow and are easy to call directly, an explicit function or service is often easier to understand and debug.

## 14. When should we use Django Signals?

Good situations include:

- Creating a related profile after a user or customer is created.
- Recording audit or activity information after a model event.
- Responding to login and logout events.
- Updating a separate system when an event occurs, using an appropriate reliable integration approach.
- Allowing independent parts of an application to react to the same event.

Avoid signals when:

- The code is part of one simple workflow and a direct function call is clearer.
- The receiver contains large amounts of business logic.
- Hidden side effects would make the application difficult to understand or debug.
- A task is slow and should instead run in a background worker.

## 15. Quick revision

| Question | Answer |
|---|---|
| What is a Django Signal? | A mechanism for notifying receivers when an event occurs. |
| What is a sender? | The object or model class that sends a signal. |
| What is a receiver? | The function or method that responds to a signal. |
| What does `pre_save` do? | Runs before a model's `save()` method completes its save operation. |
| What does `post_save` do? | Runs after a model's `save()` method completes. |
| What does `created` mean? | For `post_save`, it indicates whether a new record was created. |
| Where should signal handlers usually be written? | In the app's `signals.py` module. |
| Where should the signal module be imported? | In the app configuration's `ready()` method. |
| How can we connect a receiver? | With `Signal.connect()` or the `@receiver` decorator. |
| What does `dispatch_uid` do? | Helps prevent duplicate receiver registrations. |
| Can we create our own signals? | Yes, using `django.dispatch.Signal`. |
| Should every task use signals? | No. Prefer direct function calls when they make the workflow clearer. |