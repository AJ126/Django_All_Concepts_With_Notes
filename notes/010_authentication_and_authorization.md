# Django Authentication and Authorization – Complete Notes

## 1. What Is Authentication?

**Authentication** is the process of verifying the identity of a user.

It answers the question: **Who are you?**

For example, a user enters a username and password on a login page. Django checks whether the credentials are valid.

If they are valid, Django can log the user in.

## 2. What Is Authorization?

**Authorization** is the process of checking what an authenticated user is allowed to do.

It answers the question: **What are you allowed to access?**

For example:
- An administrator can manage users and application data.
- A normal user can view their dashboard.
- A staff member can access selected administrative features.

### Authentication vs Authorization

| Authentication | Authorization |
|---|---|
| Verifies a user's identity. | Checks the user's access rights. |
| Usually happens during login. | Happens when the user tries to access a protected resource. |
| Example: checking a username and password. | Example: checking whether a user can delete a record. |

**Remember:** Authentication identifies the user; authorization determines what that user can do.

## 3. Why Do We Need Authentication?

By default, many web pages can be accessed without logging in. However, some applications require users to register and log in before accessing certain pages.

For example, an e-commerce website may allow everyone to view products but require login to view an order history.

Django provides built-in authentication functionality to help implement these requirements.

## 4. Django's Built-in Authentication Applications

Django provides two important applications:

### A. `django.contrib.auth`

This application provides functionality for:

- User accounts.
- Password hashing and verification.
- Authentication.
- Login and logout.
- Groups and permissions.
- Password reset and password-change workflows.

### B. `django.contrib.contenttypes`

This application tracks the models installed in a Django project and provides a way to reference model types generically.

It also supports Django's permission framework, which associates permissions with models.

Both applications are included in the standard `INSTALLED_APPS` configuration of a newly created Django project.

Example from `settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your applications
]
```

Also check that the standard authentication and session middleware are enabled.

### Apply migrations

```bash
python manage.py migrate
```

This creates the necessary database tables for Django's built-in authentication and related functionality.

## 5. How Django Stores Passwords

Django does not store user passwords as plain text. It stores a **password hash** produced by a password-hashing algorithm.

In standard Django configurations, PBKDF2 with SHA-256 is the default password hasher.

For example, when a user registers with a password:

1. Django receives the password.
2. Django hashes it using the configured password hasher.
3. The resulting encoded hash is stored in the database.
4. During login, Django checks the entered password against the stored hash.

The original password is not stored in the database, and the hash is not intended to be decrypted back into the original password.

You can inspect the stored hash through the user's `password` field, but it is not the original password.

**Important:** Never store passwords manually in plain text. Use Django's authentication APIs, such as `create_user()`, `set_password()`, and `authenticate()`.

---

# Part 1: Protecting Pages with `login_required`

## 6. What Is the `login_required` Decorator?

The `login_required` decorator restricts access to a view to authenticated users.

If a user is not logged in, Django redirects them to the configured login page.

### Example

**`views.py`**

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    return render(request, 'authApp/dashboard.html')
```

Here, only an authenticated user can access the dashboard.

If a user who is not logged in tries to access it, Django redirects them to the login URL.

### Configure the login URL

In `settings.py`:

```python
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
```

These settings define:

- `LOGIN_URL`: Where unauthenticated users are redirected.
- `LOGIN_REDIRECT_URL`: The default destination after successful login when no other destination is specified.
- `LOGOUT_REDIRECT_URL`: The default destination after logout when no other destination is specified.

The values should match your project's actual URLs.

## 7. What Is the `next` Parameter?

When a user tries to access a protected page, Django can redirect them to login while preserving the original destination.

For example:

```text
/accounts/login/?next=/dashboard/
```

After successful login, Django's built-in login view can redirect the user to `/dashboard/`.

This is useful because users can return to the page they originally wanted to access.

---

# Part 2: Using Django's Built-in Login and Logout Views

## 8. Add Django's Authentication URLs

Django provides built-in views for login, logout, password changes, and password reset.

In your project's main `urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
```

This adds URLs such as:

| URL | Purpose |
|---|---|
| `/accounts/login/` | Login page |
| `/accounts/logout/` | Logout view |
| `/accounts/password_change/` | Change password |
| `/accounts/password_reset/` | Start password reset |

Django's built-in views generally expect templates with particular names. For example, the login view expects `registration/login.html` by default.

## 9. Create the Login Template

Create the following template structure:

```text
authApp/
└── templates/
    └── registration/
        └── login.html
```

**`login.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Login</title>
</head>
<body>
    <h2>User Login</h2>

    {% if form.errors %}
        <p>Username or password is incorrect.</p>
    {% endif %}

    <form method="post">
        {% csrf_token %}

        {{ form.as_p }}

        <button type="submit">Login</button>
    </form>
</body>
</html>
```

### Explanation

- `{{ form.as_p }}` displays the fields supplied by Django's login form.
- `{% csrf_token %}` adds CSRF protection to the POST form.
- The form submits the user's credentials to Django's built-in login view.

### Test the login page

Start the development server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/accounts/login/
```

To test login, create a user or superuser first.

```bash
python manage.py createsuperuser
```

You can use those credentials to test the login page.

**Note:** Django's built-in logout view uses POST requests in current versions. For a logout button, use a POST form rather than relying on a logout link.

---

# Part 3: User Registration

## 10. What Is User Registration?

Registration allows a new user to create an account.

Django provides a built-in user model:

```python
from django.contrib.auth.models import User
```

The default user model contains fields such as:

- `username`
- `password`
- `email`
- `first_name`
- `last_name`
- `is_active`
- `is_staff`
- `is_superuser`

The password must be handled through Django's password APIs, not assigned as plain text.

## 11. Create a Registration Form

Django provides `UserCreationForm`, which handles password fields and password validation.

Using this form is safer and simpler than creating your own password handling from scratch.

**`forms.py`**

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    first_name = forms.CharField(
        max_length=150,
        required=False
    )

    last_name = forms.CharField(
        max_length=150,
        required=False
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
```

`UserCreationForm` already provides `password1` and `password2` fields and checks that the passwords match.

You do not need to add those password fields to `Meta.fields`; the form handles them.

## 12. Create the Registration View

**`views.py`**

```python
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Your account has been created successfully.'
            )

            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(
        request,
        'authApp/register.html',
        {'form': form}
    )
```

### Explanation

1. A GET request displays an empty registration form.
2. A POST request submits the form data.
3. `form.is_valid()` validates the username, passwords, and other fields.
4. `form.save()` creates the user and securely hashes the password.
5. After registration, the user is redirected to the login page.
6. If validation fails, the form is displayed again with its errors.

## 13. Create the Registration Template

**`register.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Register</title>
</head>
<body>
    <h2>Create an Account</h2>

    {% for message in messages %}
        <p>{{ message }}</p>
    {% endfor %}

    <form method="post">
        {% csrf_token %}

        {{ form.as_p }}

        <button type="submit">Register</button>
    </form>

    <p>
        Already registered?
        <a href="{% url 'login' %}">Login here</a>
    </p>
</body>
</html>
```

Django's messages framework is included in the standard project template. If you use a customized configuration, ensure the messages app, middleware, and context processor are enabled.

---

# Part 4: Custom Login View

## 14. Create a Custom Login View

If you need a custom login page or custom login logic, you can use Django's `authenticate()` and `login()` functions.

**`views.py`**

```python
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            auth_login(request, user)

            return redirect('dashboard')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(
        request,
        'authApp/custom_login.html'
    )
```

### Explanation

- `authenticate()` checks the supplied credentials using Django's configured authentication backends.
- If authentication succeeds, it returns a user object.
- If authentication fails, it returns `None`.
- `auth_login()` logs in the authenticated user and associates the user with the session.
- `messages.error()` displays an error if authentication fails.

The import uses `login as auth_login` to avoid a naming conflict between Django's `login()` function and the custom view.

## 15. Create the Custom Login Template

**`custom_login.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Login</title>
</head>
<body>
    <h2>User Login</h2>

    {% for message in messages %}
        <p>{{ message }}</p>
    {% endfor %}

    <form method="post">
        {% csrf_token %}

        <label for="username">Username:</label>
        <input
            type="text"
            name="username"
            id="username"
            required
        >

        <br><br>

        <label for="password">Password:</label>
        <input
            type="password"
            name="password"
            id="password"
            required
        >

        <br><br>

        <button type="submit">Login</button>
    </form>
</body>
</html>
```

If you use this custom view instead of Django's built-in login view, make sure your URL configuration points to `custom_login`.

---

# Part 5: Logout

## 16. What Is Logout?

Logout ends the current authenticated session.

Django provides a built-in function:

```python
from django.contrib.auth import logout as auth_logout
```

A custom logout view can be written as follows:

```python
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect


def custom_logout(request):
    auth_logout(request)

    return redirect('login')
```

This clears the current session data and logs out the current user.

### Secure logout template

Use a POST form for logout:

```html
<form method="post" action="{% url 'custom_logout' %}">
    {% csrf_token %}

    <button type="submit">Logout</button>
</form>
```

This avoids changing authentication state through a simple GET request.

---

# Part 6: URL Configuration

## 17. Configure the Application URLs

For the custom login and registration examples, you can define the application routes in `authApp/urls.py`.

```python
from django.urls import path
from . import views

urlpatterns = [
    path(
        'register/',
        views.register,
        name='register'
    ),
    path(
        'login/',
        views.custom_login,
        name='login'
    ),
    path(
        'logout/',
        views.custom_logout,
        name='custom_logout'
    ),
    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),
]
```

Ensure you define the dashboard view:

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    return render(
        request,
        'authApp/dashboard.html'
    )
```

Include your application URLs in the project's main `urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authApp.urls')),
]
```

If you use these prefixed URLs, your custom login URL becomes `/auth/login/`, not `/accounts/login/`. Set `LOGIN_URL` accordingly if needed.

For example:

```python
LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/auth/dashboard/'
LOGOUT_REDIRECT_URL = '/auth/login/'
```

Use either the built-in login route or the custom login route consistently.

---

# Part 7: Authorization with Permissions

## 18. Authentication Does Not Automatically Grant Every Permission

A logged-in user is authenticated, but that does not mean they should be allowed to perform every action.

Django provides groups and model permissions for authorization.

By default, Django creates model permissions such as:

- `add`
- `change`
- `delete`
- `view`

These permissions are generally created for models during migrations.

### Example: Restrict a view to users with a permission

```python
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render


@permission_required(
    'auth.view_user',
    raise_exception=True
)
def user_management(request):
    return render(
        request,
        'authApp/user_management.html'
    )
```

This requires the user to have the `auth.view_user` permission. Without it, Django returns a permission-denied response.

Choose the permission that matches your actual model and action. For your own models, the permission format is usually `app_label.codename`.

### Restrict a view to staff users

```python
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def staff_dashboard(request):
    return render(
        request,
        'authApp/staff_dashboard.html'
    )
```

This restricts the view to users marked as staff. It does not automatically mean the user has every model permission.

## 19. Groups and Permissions

Groups make it easier to manage permissions for many users.

For example, you could create these groups:

| Group | Example permissions |
|---|---|
| Administrators | Manage users and application records |
| Editors | Add and update selected content |
| Viewers | View permitted records |

Assign users to appropriate groups and check permissions in your views.

**Important:** Hiding a button in an HTML template is not sufficient authorization. Always enforce permissions on the server side.

---

# Part 8: Common Mistakes

1. **Storing plain-text passwords**

   Do not use `User.objects.create(password=password)`. Use `create_user()` or a suitable Django user form.

2. **Forgetting CSRF protection**

   Include `{% csrf_token %}` inside POST forms.

3. **Using `login_required` without a configured login URL**

   Configure `LOGIN_URL` or use the default `/accounts/login/` route.

4. **Confusing authentication with authorization**

   A logged-in user may still lack permission to access a particular feature.

5. **Using GET requests for logout**

   Prefer POST for logout actions to avoid unintended state changes.

6. **Importing `login` and naming a custom view `login`**

   This can cause naming conflicts. Use aliases such as `login as auth_login` or name the view `custom_login`.

7. **Assuming the built-in login view creates registration pages**

   Django provides built-in login and password-management views, but a registration view generally needs to be implemented or supplied by an additional package.

---

# Part 9: Quick Revision

| Concept | Meaning |
|---|---|
| Authentication | Verifies who the user is. |
| Authorization | Determines what the user can do. |
| `django.contrib.auth` | Django's authentication and permissions framework. |
| `django.contrib.contenttypes` | Tracks installed models and supports generic model references. |
| `authenticate()` | Validates credentials and returns a user or `None`. |
| `login()` | Logs a user in and associates the user with the session. |
| `logout()` | Logs out the current user and clears their session. |
| `UserCreationForm` | Provides a registration form with password validation. |
| `@login_required` | Restricts a view to authenticated users. |
| `@permission_required` | Restricts a view based on a specific permission. |
| `@staff_member_required` | Restricts a view to staff users. |
| `LOGIN_URL` | Sets the login page URL. |
| `LOGIN_REDIRECT_URL` | Sets the default post-login destination. |
| `LOGOUT_REDIRECT_URL` | Sets the default post-logout destination. |

**Final takeaway:** Use Django's built-in authentication tools whenever possible. They handle many important security details and reduce the risk of errors in login, password storage, session management, and permissions.