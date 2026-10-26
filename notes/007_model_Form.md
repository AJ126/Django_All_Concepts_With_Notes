# Django Model Forms – Complete Notes

## 1. What is a ModelForm?

Sometimes, we need to create an HTML form based on an existing Django model. These forms are called **Model Forms (`ModelForm`)**.

A Django `ModelForm` automatically creates form fields based on the fields defined in a model.

### Advantages of ModelForms

- Automatically generates form fields from a model.
- Provides built-in form validation.
- Makes it easy to save user input into the database.
- Reduces repetitive code.
- Allows us to customize fields and widgets.

**Real-life example:** Suppose we have a `Student` model containing `name`, `email`, and `city`. We can create a form from this model without manually defining every field.

## 2. How to Create a ModelForm

Follow these steps:

1. Create a model in `models.py`.
2. Import the model into `forms.py`.
3. Create a class that inherits from `forms.ModelForm`.
4. Define an inner `Meta` class.
5. Specify the model and the fields to include in the form.
6. Use the form in a view and template.

### Step 1: Create a model

**`models.py`**

```python
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.name
```

If this model is new, create and apply its migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Create a ModelForm

Create a `forms.py` file inside your application folder.

**`forms.py`**

```python
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
```

**Explanation:**

| Code | Meaning |
|---|---|
| `forms.ModelForm` | Creates a form based on a Django model. |
| `class Meta:` | Provides configuration for the form. |
| `model = Student` | Specifies which model the form uses. |
| `fields = '__all__'` | Includes all eligible model fields in the form. |

Django automatically creates the appropriate form fields based on the model field types.

## 3. How to Select Model Fields

The `fields` option controls which model fields appear in the form.

### A. Include all fields

```python
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
```

This includes all eligible model fields.

### B. Include selected fields

```python
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('name', 'email')
```

Only the `name` and `email` fields are included.

You can also use a list:

```python
fields = ['name', 'email']
```

**When to use it:** Use this approach when a model has many fields but the form should display only a few.

### C. Exclude selected fields

```python
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['address']
```

This includes all eligible model fields except `address`.

**Important correction:** To exclude a field, use `exclude`, not `fields = ['name']`. The latter includes only `name`.

For production applications, explicitly selecting allowed fields is usually safer than exposing every model field with `fields = '__all__'`.

## 4. How to Save User Input into the Database

A `ModelForm` provides a built-in `save()` method. After validating the submitted data, call `form.save()` to create a database record.

### View

**`views.py`**

```python
from django.shortcuts import render, redirect
from .forms import StudentForm

def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('student_create')
    else:
        form = StudentForm()

    return render(
        request,
        'student_form.html',
        {'form': form}
    )
```

**How it works:**

1. For a `GET` request, Django displays an empty form.
2. For a `POST` request, Django receives the submitted data.
3. `form.is_valid()` validates the submitted values.
4. `form.save()` creates and saves a new `Student` record.
5. `redirect()` sends the user to the form page again after successful submission.
6. If validation fails, the form is rendered again with its errors.

### URL configuration

**Application `urls.py`**

```python
from django.urls import path
from . import views

urlpatterns = [
    path(
        'students/add/',
        views.student_create,
        name='student_create'
    ),
]
```

Make sure the application's URLs are included in the project's main `urls.py`.

### HTML template

**`student_form.html`**

```html
<h2>Add Student</h2>

<form method="POST">
    {% csrf_token %}

    {{ form.as_p }}

    <button type="submit">Save Student</button>
</form>
```

- `method="POST"` submits the form data.
- `{% csrf_token %}` enables Django's CSRF protection for the form.
- `{{ form.as_p }}` renders the form fields inside paragraph elements.
- The Save button submits the form.

## 5. How to Customize ModelForm Widgets

A **widget** controls how a form field is displayed in HTML.

For example, you can use widgets to add Bootstrap classes, render a multiline text area, or display a date input.

### Example: Add Bootstrap classes

**`forms.py`**

```python
from django import forms
from .models import Student

class StudentWidgetForm(forms.ModelForm):

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control'}
        )
    )

    address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3
            }
        )
    )

    city = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = Student
        fields = ['name', 'email', 'address', 'city']
```

### Explanation

| Widget | Purpose |
|---|---|
| `forms.TextInput()` | Single-line text input |
| `forms.EmailInput()` | Email input |
| `forms.NumberInput()` | Numeric input |
| `forms.Textarea()` | Multiline text input |
| `forms.PasswordInput()` | Password input |
| `forms.DateInput()` | Date input |

The `attrs` dictionary sets HTML attributes on the generated input.

For example:

```python
forms.TextInput(
    attrs={
        'class': 'form-control',
        'placeholder': 'Enter your name'
    }
)
```

This generates an HTML input with a Bootstrap class and placeholder.

### Important: Use the correct widget for a phone number

Avoid using `forms.IntegerField` for phone numbers. Phone numbers are identifiers, not quantities; they can contain leading zeros or a `+` country code.

Instead, define the model field as text:

```python
# models.py
phone = models.CharField(max_length=15)
```

Then customize its form widget:

```python
# forms.py
phone = forms.CharField(
    widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone number'
        }
    )
)
```

If you add or change a model field, create and apply migrations as needed.

Also, `forms.IntegerField(widget=forms.IntegerField())` is incorrect because `IntegerField` is a form field, not a widget. For a genuine integer field, use `forms.IntegerField(widget=forms.NumberInput(...))`.

## 6. Save Without Saving Immediately

Sometimes, you need to validate user input but modify the object before saving it.

Use `commit=False`:

```python
if form.is_valid():
    student = form.save(commit=False)

    # Modify the object before saving
    student.city = 'Pune'

    student.save()
```

Here, `form.save(commit=False)` creates a model instance without saving it to the database immediately. Calling `student.save()` saves it afterward.

## 7. Update an Existing Database Record

A `ModelForm` can also update an existing model object. Pass the object using the `instance` argument.

```python
from django.shortcuts import get_object_or_404, redirect, render
from .models import Student
from .forms import StudentForm

def student_update(request, student_id):
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        form = StudentForm(
            request.POST,
            instance=student
        )

        if form.is_valid():
            form.save()
            return redirect('student_create')
    else:
        form = StudentForm(instance=student)

    return render(
        request,
        'student_form.html',
        {'form': form}
    )
```

**Remember:**

- `StudentForm()` creates a form for a new object.
- `StudentForm(instance=student)` loads an existing object's values.
- `form.save()` creates a new record when no instance is supplied, or updates the supplied instance.

## 8. ModelForm vs Form

| Feature | `forms.Form` | `forms.ModelForm` |
|---|---|---|
| Based on a model | No | Yes |
| Fields | Defined manually | Generated from model fields, with optional customization |
| Built-in validation | Yes | Yes |
| Database saving | Must be implemented separately | Supports `save()` |
| Best suited for | Search forms, contact forms, custom input | Forms that create or update model records |

## 9. Common Mistakes

1. **Forgetting to import the model**

   ```python
   from .models import Student
   ```

2. **Forgetting the inner `Meta` class**

   `model` and `fields` must be configured inside `Meta`.

3. **Using the wrong field-selection option**

   ```python
   fields = ['name']   # Include only name
   exclude = ['name']  # Include other eligible fields
   ```

4. **Saving without validating**

   Always call `form.is_valid()` before calling `form.save()` on submitted data.

5. **Forgetting the CSRF token**

   Include `{% csrf_token %}` inside POST forms when using Django's normal CSRF protection.

6. **Using the wrong widget**

   Use `forms.TextInput()` for text inputs, `forms.NumberInput()` for number inputs, and `forms.Textarea()` for multiline text.

7. **Exposing sensitive fields**

   Avoid including fields such as internal status flags, permissions, or administrative fields in a public form unless explicitly intended. Select only the fields the user is allowed to edit.

## 10. Quick Revision

- `forms.ModelForm` creates a form from a Django model.
- `class Meta:` defines the model and field configuration.
- `model = Student` identifies the model.
- `fields = '__all__'` includes all eligible model fields.
- `fields = ['name', 'email']` includes only selected fields.
- `exclude = ['address']` omits selected fields.
- `form.is_valid()` validates submitted data.
- `form.save()` creates or updates a database record.
- `form.save(commit=False)` creates an unsaved model instance.
- `instance=student` allows an existing record to be edited.
- `widgets` and `attrs` customize how form fields appear in HTML.
