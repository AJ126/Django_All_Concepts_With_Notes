# Django Forms – Complete Notes

## 1. What Are Django Forms?

Django Forms provide a convenient way to create HTML forms, validate user input, and process submitted data using Python.

### Advantages of Django Forms

1. **Easy form creation:** Generate form fields such as text inputs, email inputs, password inputs, and textareas using Python.
2. **HTML generation:** Django can generate HTML form fields and widgets.
3. **Data validation:** Validate user input before processing it.
4. **Data processing:** Access validated data through Python data structures, such as dictionaries.
5. **Model integration:** Django provides `ModelForm` to create forms based on database models.
6. **Security support:** Django provides CSRF protection and other useful security features when configured correctly.

## 2. Types of Django Forms

Django provides two commonly used form classes:

| Form type | Purpose |
|---|---|
| `forms.Form` | Creates a form by explicitly defining its fields |
| `forms.ModelForm` | Creates a form based on an existing Django model |

In this note, we will first learn `forms.Form`.

## 3. Creating a Django Form

### Step 1: Create `forms.py`

Inside your Django application, create a file named `forms.py`.

Example structure:

```text
myproject/
├── manage.py
├── myproject/
│   └── settings.py
└── myapp/
    ├── forms.py
    ├── views.py
    ├── models.py
    └── urls.py
```

Django does not automatically create `forms.py`; you create it manually.

### Step 2: Define the Form Class

File: `myapp/forms.py`

```python
from django import forms

class TestForm(forms.Form):
    name = forms.CharField()
```

**Explanation:**

- `from django import forms` imports Django's form functionality.
- `TestForm` is our custom form class.
- `forms.Form` is the parent class.
- `forms.CharField()` defines a field that accepts text.

The form class defines what fields the form should contain.

### Step 3: Add More Fields

```python
from django import forms

class TestForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    age = forms.IntegerField()
    address = forms.CharField(widget=forms.Textarea)
    password = forms.CharField(widget=forms.PasswordInput)
```

Django provides different field types and widgets for different kinds of input.

| Field | Purpose |
|---|---|
| `CharField` | Accepts text |
| `EmailField` | Validates email format |
| `IntegerField` | Validates integer input |
| `DateField` | Validates date input |
| `BooleanField` | Handles true/false-style input |
| `ChoiceField` | Allows selection from predefined choices |

Widgets control how fields are represented in HTML. For example, `Textarea` renders a multiline text field, and `PasswordInput` renders a password input.

## 4. Displaying a Form in a Template

### Step 1: Create a View

File: `myapp/views.py`

```python
from django.shortcuts import render
from .forms import TestForm

def form_view(request):
    form = TestForm()
    return render(request, 'form.html', {'form': form})
```

Here, `TestForm()` creates an unbound form, which is normally used to display an empty form.

### Step 2: Create an HTML Template

File: `templates/form.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Django Form</title>
</head>
<body>
    <h1>Student Form</h1>

    <form method="post">
        {% csrf_token %}

        {{ form.as_p }}

        <button type="submit">Submit</button>
    </form>
</body>
</html>
```

### What Does `{{ form.as_p }}` Do?

It renders the form's fields with each field wrapped in a paragraph element.

Other common rendering options include:

```django
{{ form.as_p }}
{{ form.as_div }}
{{ form.as_ul }}
```

`as_p` and `as_div` are useful for quick rendering. For full layout control, you can render individual fields and their labels and errors manually.

**Important:** Django does not automatically add the surrounding HTML `<form>` element or the submit button. You must create them in your template.

## 5. Configure the URL

File: `myapp/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('form/', views.form_view, name='form_view'),
]
```

Include the application URLs in the project's `urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]
```

Run the development server:

```bash
python manage.py runserver
```

Open:

`http://127.0.0.1:8000/form/`

You should see the form.

---

## 6. CSRF Token in Django Forms

**CSRF** stands for **Cross-Site Request Forgery**.

CSRF is an attack in which a malicious website attempts to make a user's browser send an unwanted request to another website where the user is authenticated.

Django provides CSRF protection to help prevent these attacks.

### How to Add a CSRF Token

Inside a POST form, include:

```django
<form method="post">
    {% csrf_token %}

    {{ form.as_p }}

    <button type="submit">Submit</button>
</form>
```

Django generates a hidden input containing a CSRF token.

For example, the rendered HTML contains a field similar to this:

```html
<input type="hidden" name="csrfmiddlewaretoken" value="generated-token">
```

The actual token value is generated by Django.

### Important Points

1. Include `{% csrf_token %}` inside the form when submitting a normal POST request to your Django application.
2. Django's CSRF middleware checks the submitted token.
3. The token is not a replacement for authentication or authorization.
4. The token is not guaranteed to change on every request; Django manages it according to its CSRF protection mechanism.
5. CSRF protection depends on correct middleware and request configuration.

---

## 7. Getting Form Data in `views.py`

To process submitted form data, we need to handle both GET and POST requests.

### Example: Processing a Form

File: `myapp/views.py`

```python
from django.shortcuts import render
from .forms import TestForm

def form_view(request):
    if request.method == 'POST':
        form = TestForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']

            return render(
                request,
                'success.html',
                {'name': name, 'email': email}
            )
    else:
        form = TestForm()

    return render(request, 'form.html', {'form': form})
```

This example assumes that `TestForm` defines both `name` and `email` fields.

### Understanding `request.POST`

`request.POST` contains the submitted form data for a POST request.

### Understanding `cleaned_data`

After calling `form.is_valid()`, Django makes successfully validated field values available through `form.cleaned_data`.

For example:

```python
name = form.cleaned_data['name']
```

**Important:** Do not access `cleaned_data` before validation. First check that `form.is_valid()` returns `True`.

### Create the Success Template

File: `templates/success.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Form Submitted</title>
</head>
<body>
    <h1>Form Submitted Successfully</h1>

    <p>Name: {{ name }}</p>
    <p>Email: {{ email }}</p>
</body>
</html>
```

---

## 8. Form Validation

Form validation checks whether user-submitted data meets the required rules.

For example:

- A name must not be empty.
- An email must have a valid format.
- An age must be an integer.
- A text field must not exceed a specified length.

Django performs field validation when `form.is_valid()` is called.

There are three common ways to add validation:

1. Use built-in field validation.
2. Use built-in validators or custom field-level `clean_fieldname()` methods.
3. Use the form-level `clean()` method to validate relationships between fields.

## 9. Field-Level Validation Using `clean_fieldname()`

Use a method named `clean_fieldname()` to add validation for a particular field.

For example, to ensure the name contains at least four characters:

File: `myapp/forms.py`

```python
from django import forms

class TestForm(forms.Form):
    name = forms.CharField(max_length=100)

    def clean_name(self):
        name = self.cleaned_data['name']

        if len(name.strip()) < 4:
            raise forms.ValidationError(
                'The name must contain at least 4 characters.'
            )

        return name
```

### Explanation

- `clean_name()` is called automatically during validation of the `name` field.
- `self.cleaned_data['name']` retrieves the field's cleaned value.
- `forms.ValidationError()` reports a validation error.
- `return name` returns the cleaned value for inclusion in `cleaned_data`.

Django displays the validation error when the template renders the bound form again, provided the template displays the field errors.

**Important:** Use the actual field name in the method. For a field called `email`, the method would be `clean_email()`.

---

## 10. Django's Built-In Validators

Django provides reusable validators for common validation rules.

Import validators using:

```python
from django.core import validators
```

### Example: Maximum Length Validation

```python
from django import forms
from django.core import validators

class TestForm(forms.Form):
    address = forms.CharField(
        widget=forms.Textarea,
        validators=[
            validators.MaxLengthValidator(50)
        ]
    )
```

This form limits the address to 50 characters.

### Other Common Validators

| Validator | Purpose |
|---|---|
| `MinLengthValidator(4)` | Requires at least four characters |
| `MaxLengthValidator(50)` | Allows at most 50 characters |
| `MinValueValidator(18)` | Requires a numeric value of at least 18 |
| `MaxValueValidator(100)` | Restricts a numeric value to at most 100 |
| `EmailValidator()` | Validates an email address format |

Example:

```python
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class AgeForm(forms.Form):
    age = forms.IntegerField(
        validators=[
            MinValueValidator(18),
            MaxValueValidator(100),
        ]
    )
```

This form accepts ages from 18 through 100.

**Note:** Some validation is already built into Django fields. For example, `EmailField` performs email-format validation, so you do not usually need to add `EmailValidator()` separately.

---

## 11. Whole-Form Validation Using `clean()`

Use `clean()` when validation depends on multiple fields or on the form as a whole.

For example, suppose a registration form contains `password` and `confirm_password`. Both values must match.

File: `myapp/forms.py`

```python
from django import forms

class RegistrationForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(
                'Passwords do not match.'
            )

        return cleaned_data
```

### Explanation

- Django calls `clean()` during form validation.
- `super().clean()` preserves the normal form-cleaning process.
- The method checks whether the two password values match.
- `forms.ValidationError()` adds a form-level validation error.
- Returning `cleaned_data` preserves the cleaned values.

You do not need to call `clean()` yourself. Django invokes it as part of `form.is_valid()`.

For a form-level error, render `{{ form.non_field_errors }}` in your template if you want to control where the message appears.

Example:

```django
<form method="post">
    {% csrf_token %}

    {{ form.non_field_errors }}
    {{ form.as_p }}

    <button type="submit">Register</button>
</form>
```

**Security note:** Passwords should be validated and handled carefully. For a real registration system, use Django's authentication facilities rather than storing raw passwords in a custom model.

---

## 12. Difference Between Field-Level and Form-Level Validation

| Feature | `clean_fieldname()` | `clean()` |
|---|---|---|
| Scope | One specific field | The entire form |
| Example | Validate name length | Check whether passwords match |
| Called by Django | Automatically during field cleaning | Automatically during form cleaning |
| Error handling | Usually associated with the field | Usually a non-field error unless assigned to a field |

## 13. ModelForm – Creating Forms from Models

Django also provides `ModelForm`, which creates a form based on an existing database model.

Example model:

```python
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
```

Create the form:

```python
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email']
```

Django derives the form fields from the model, reducing repeated code.

A `ModelForm` can also save validated data to the database:

```python
if form.is_valid():
    form.save()
```

The form must be configured correctly, and the model's database table must exist. This example assumes the form was created or bound to the submitted data appropriately.

---

## Quick Revision

| Concept | Purpose |
|---|---|
| `forms.py` | Defines form classes |
| `forms.Form` | Creates a regular Django form |
| `forms.ModelForm` | Creates a form based on a model |
| `forms.CharField()` | Accepts text input |
| `forms.EmailField()` | Validates email-format input |
| `forms.Textarea` | Renders a multiline text field |
| `{% csrf_token %}` | Adds the CSRF token to a template form |
| `request.POST` | Provides submitted POST data |
| `form.is_valid()` | Validates the form |
| `form.cleaned_data` | Provides validated field values |
| `clean_fieldname()` | Validates a specific field |
| `clean()` | Validates the form as a whole |
| `forms.ValidationError` | Reports validation errors |
| `form.save()` | Saves a valid `ModelForm` to its model |

