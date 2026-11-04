# Django Advanced Concepts – Complete Notes

# 01. Django Admin Page Customization

Django provides a built-in admin panel that allows us to manage database records without creating separate pages for every operation.

We can customize the admin list page and form page using different options inside `admin.py`.

Let's understand the important customization options.

## 1. `list_display`

**Purpose:** Displays specific model fields as columns on the Django admin list page.

Example:

Suppose we have a `Post` model:

```python
class Post(models.Model):

    title = models.CharField(max_length=200)

    author = models.CharField(max_length=100)

    publish = models.DateField()

    status = models.CharField(max_length=50)
```

`admin.py`

```python
from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ['id', 'title', 'author', 'publish', 'status']
```

Now the admin list page displays these fields as columns.

## 2. `list_filter`

**Purpose:** Adds filtering options to the Django admin list page.

Django normally displays these filter options on the right side of the admin list page.

Example:

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ['id', 'title', 'author', 'status']

    list_filter = ['status', 'publish']
```

Now we can filter posts based on their status and publication date.

**Note:** The fields specified in `list_filter` should be suitable for filtering.

## 3. `search_fields`

**Purpose:** Adds a search bar to the Django admin list page.

We can search records based on the fields specified in `search_fields`.

Example:

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ['id', 'title', 'author', 'status']

    search_fields = ['title', 'author']
```

Now the admin search bar can search posts using their title or author.

**Note:** For text fields, Django uses case-insensitive partial matching by default. We can also specify lookup types, such as `title__exact`.

## 4. `prepopulated_fields`

**Purpose:** Automatically populates one field based on the value entered in another field.

It is commonly used to generate a slug from a title.

Example:

Suppose we enter:

```text
Title: Django Tutorial for Beginners
```

Django automatically generates:

```text
Slug: django-tutorial-for-beginners
```

`admin.py`

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ['id', 'title', 'slug']

    prepopulated_fields = {
        'slug': ('title',)
    }
```

**Important:** The `prepopulated_fields` option is primarily an admin form feature. It generates the slug while entering the title in the admin form. It does not automatically guarantee slug generation when records are created through other code.

## 5. `raw_id_fields`

**Purpose:** Displays a lookup widget instead of a large dropdown list for ForeignKey or ManyToManyField relationships.

This is useful when a related model contains thousands of records.

Example:

Suppose a blog post has a ForeignKey relationship with an Author model.

```python
class Author(models.Model):

    name = models.CharField(max_length=100)


class Post(models.Model):

    title = models.CharField(max_length=200)

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE
    )
```

Admin configuration:

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    raw_id_fields = ('author',)
```

Normally, Django displays a dropdown containing available authors.

With `raw_id_fields`, Django displays an ID input field with a lookup button.

This is helpful when a large number of related records exist.

## 6. `date_hierarchy`

**Purpose:** Adds date-based navigation to the Django admin list page.

It allows us to navigate records by year, month, and day.

Example:

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ['id', 'title', 'publish']

    date_hierarchy = 'publish'
```

If our model contains a `publish` date field, Django displays date navigation above the records.

We can navigate through:

- Year
- Month
- Day

**Note:** The field specified must be a suitable `DateField` or `DateTimeField`.

## 7. `ordering`

**Purpose:** Displays records in a specific order on the admin list page.

It supports ascending and descending ordering.

Example:

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    ordering = ['publish']
```

Ascending order:

```python
ordering = ['publish']
```

Descending order:

```python
ordering = ['-publish']
```

Multiple fields:

```python
ordering = ['status', '-publish']
```

Here, records are ordered by status first and publication date in descending order within each status.

## 8. `autocomplete_fields`

**Purpose:** Adds a search-based autocomplete widget for ForeignKey and ManyToManyField relationships.

Normally, Django displays related records in a dropdown list.

If a related model contains thousands of records, finding a particular record becomes difficult.

Using `autocomplete_fields`, we can search and select related records instead of manually searching through a large dropdown.

Example:

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    autocomplete_fields = ['author']
```

**Important:** The related model must also be registered in the admin, and its `ModelAdmin` must define `search_fields`.

Example:

```python
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    search_fields = ['name']
```

Now the author field provides an autocomplete search widget.

## Admin customization quick revision

| Option | Purpose |
|---|---|
| `list_display` | Displays selected fields as columns |
| `list_filter` | Adds filters |
| `search_fields` | Adds a search bar |
| `prepopulated_fields` | Automatically populates fields in admin forms |
| `raw_id_fields` | Uses a lookup widget for relationships |
| `date_hierarchy` | Adds date-based navigation |
| `ordering` | Controls record ordering |
| `autocomplete_fields` | Adds autocomplete search for relationships |

---

# 02. Customize Django Admin Interface Using Jazzmin

Django provides a default admin interface, but we can customize its appearance using third-party packages.

One popular package is **Django Jazzmin**.

Jazzmin provides a modern, responsive, and attractive admin dashboard.

<escape>##</escape> 1. Install Django Jazzmin

Run the following command:

```bash
pip install -U django-jazzmin
```

## 2. Configure `INSTALLED_APPS`

After installation, add `jazzmin` to the `INSTALLED_APPS` section in `settings.py`.

**Important:** Add Jazzmin before `django.contrib.admin`.

```python
INSTALLED_APPS = [

    'jazzmin',

    'django.contrib.admin',

    'django.contrib.auth',

    'django.contrib.contenttypes',

    'django.contrib.sessions',

    'django.contrib.messages',

    'django.contrib.staticfiles',

    # Custom applications
]
```

### Why should Jazzmin be added before `django.contrib.admin`?

Jazzmin customizes Django's default admin templates.

Adding it before `django.contrib.admin` allows its templates to take priority when Django loads templates from installed applications.

## 3. Run the Django server

```bash
python manage.py runserver
```

Open the Django admin page:

```text
http://127.0.0.1:8000/admin/
```

You should now see the Jazzmin admin interface.

## 4. Customize Jazzmin Settings (Optional)

Jazzmin provides a `JAZZMIN_SETTINGS` dictionary that allows us to customize the admin dashboard.

Add the following configuration to `settings.py`:

```python
JAZZMIN_SETTINGS = {

    "site_title": "Django Admin",

    "site_header": "Django Dashboard",

    "site_brand": "Django Concepts",

    "welcome_sign": "Welcome to Django Admin",

    "copyright": "Django All Concepts",

    "show_sidebar": True,

    "navigation_expanded": True,

}
```

### Understanding the settings

| Setting | Purpose |
|---|---|
| `site_title` | Browser tab title |
| `site_header` | Admin page header |
| `site_brand` | Brand name displayed in the interface |
| `welcome_sign` | Welcome message |
| `copyright` | Copyright text |
| `show_sidebar` | Shows or hides the sidebar |
| `navigation_expanded` | Controls whether navigation is expanded |

---

# 03. Django Pagination

## 1. What is Pagination?

Pagination is the process of dividing a large number of records into smaller pages.

### Real-life example

Suppose we have 100 customer records in our database.

Instead of displaying all 100 records on a single page, we can display 10 records per page.

This creates 10 pages.

<escape>##</escape> 2. Why do we need Pagination?

- Makes large datasets easier to navigate.
- Avoids displaying too many records on one page.
- Improves the usability of list pages.
- Can reduce the amount of data retrieved for each page.

## 3. Django Pagination Classes

Django provides built-in pagination support through the `django.core.paginator` module.

It provides the following important classes and exceptions:

| Class / Exception | Purpose |
|---|---|
| `Paginator` | Divides records into multiple pages |
| `Page` | Represents a single page of records |
| `EmptyPage` | Handles requests for a page that does not exist |
| `PageNotAnInteger` | Handles page numbers that are not integers |

## 4. Create Pagination in Django View

Suppose we have a model named `Customer` and want to display 10 customers per page.

### Step 1: Import pagination classes

`views.py`

```python
from django.shortcuts import render

from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger
)

from .models import Customer
```

### Step 2: Create the pagination view

```python
def customerList(request):

    # Fetch all customer records
    customers = Customer.objects.all()

    # Create paginator (10 records per page)
    paginator = Paginator(customers, 10)

    # Get current page number
    page_number = request.GET.get('page')

    try:

        customers = paginator.page(page_number)

    except PageNotAnInteger:

        customers = paginator.page(1)

    except EmptyPage:

        customers = paginator.page(paginator.num_pages)

    return render(
        request,
        'customer.html',
        {
            'customers': customers
        }
    )
```

### Understanding the code

**A. Create a Paginator**

```python
paginator = Paginator(customers, 10)
```

Creates pagination with 10 records per page.

**B. Get the requested page number**

```python
page_number = request.GET.get('page')
```

Gets the requested page number from the URL.

For example:

```text
http://127.0.0.1:8000/customers/?page=2
```

Here, the requested page number is `2`.

**C. Get the requested page**

```python
customers = paginator.page(page_number)
```

Returns the requested page.

**D. Handle invalid page numbers**

```python
except PageNotAnInteger:
    customers = paginator.page(1)
```

If the page number is not an integer, display the first page.

```python
except EmptyPage:
    customers = paginator.page(paginator.num_pages)
```

If the requested page does not exist, display the last available page.

## 5. Display Pagination in HTML

`customer.html`

```html
<h2>Customer List</h2>

{% for customer in customers %}

    <p>{{ customer.name }}</p>

{% empty %}

    <p>No customers found.</p>

{% endfor %}


<div class="pagination">

    {% if customers.has_previous %}

        <a href="?page=1">First</a>

        <a href="?page={{ customers.previous_page_number }}">
            Previous
        </a>

    {% endif %}


    <span>
        Page {{ customers.number }}
        of {{ customers.paginator.num_pages }}
    </span>


    {% if customers.has_next %}

        <a href="?page={{ customers.next_page_number }}">
            Next
        </a>

        <a href="?page={{ customers.paginator.num_pages }}">
            Last
        </a>

    {% endif %}

</div>
```

## 6. Important Pagination Methods and Properties

| Method / Property | Purpose |
|---|---|
| `Paginator(queryset, 10)` | Creates pagination with 10 records per page |
| `request.GET.get('page')` | Gets the requested page number |
| `paginator.page(number)` | Returns the requested page |
| `paginator.num_pages` | Returns the total number of pages |
| `paginator.count` | Returns the total number of records |
| `paginator.page_range` | Returns available page numbers |
| `customers.has_previous()` | Checks whether a previous page exists |
| `customers.has_next()` | Checks whether a next page exists |
| `customers.previous_page_number()` | Returns the previous page number |
| `customers.next_page_number()` | Returns the next page number |
| `customers.number` | Returns the current page number |
| `customers.paginator.num_pages` | Returns the total number of pages |

**Correction:** `has_previous` and `has_next` are methods and must be called with parentheses in Python code. In Django templates, you can access them without parentheses.

## 7. Alternative: `get_page()`

Django also provides a simpler method called `get_page()`.

Example:

```python
def customerList(request):

    customers = Customer.objects.all()

    paginator = Paginator(customers, 10)

    page_number = request.GET.get('page')

    customers = paginator.get_page(page_number)

    return render(
        request,
        'customer.html',
        {
            'customers': customers
        }
    )
```

`get_page()` handles invalid page numbers automatically:

- Invalid non-integer page number: returns the first page.
- Page number outside the available range: returns the last page.

This is useful when we do not need custom exception handling.

---

# 04. How to Create a Dropdown Field in the Database

In Django, we can use the `choices` parameter of a model field to restrict its values to predefined options.

Django automatically generates a dropdown in forms and the admin interface for fields configured with `choices`.

### Example: Post status dropdown

Suppose we have a blog application.

A post can have two statuses:

- Draft
- Published

### Model example

`models.py`

```python
from django.db import models


class Post(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=200)

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='draft'
    )
```

### Understanding the choices

```python
('draft', 'Draft')
```

- `draft` is the actual value stored in the database.
- `Draft` is the human-readable label displayed in the dropdown.

Example:

| Stored value | Displayed label |
|---|---|
| `draft` | Draft |
| `published` | Published |

### Access the display value

```python
post = Post.objects.get(id=1)

print(post.status)
```

This returns the stored value, such as:

```text
draft
```

To get the human-readable label:

```python
print(post.get_status_display())
```

Output:

```text
Draft
```

**Important:** The `choices` parameter provides application-level validation and user-interface options. It does not automatically create a database-level CHECK constraint for every Django field configuration.

---

# 05. Django SlugField

## 1. What is a Slug?

A slug is a short, human-readable label used in URLs to identify a particular record or webpage.

A slug can contain:

- Letters
- Numbers
- Underscores (`_`)
- Hyphens (`-`)

Slugs are commonly used to create human-readable and SEO-friendly URLs.

Django provides a built-in `SlugField` to store slug values in the database.

### Example

Suppose we have a blog post with the following title:

```text
Title:
Shiv Puran Mahatmya
```

We can create a slug:

```text
shiv-puran-mahatmya
```

URL using the slug:

```text
http://127.0.0.1:8000/blog/shiv-puran-mahatmya/
```

## 2. Create a SlugField in a Model

```python
from django.db import models


class Post(models.Model):

    title = models.CharField(max_length=200)

    slug = models.SlugField(
        max_length=200,
        unique=True
    )
```

### Important SlugField Parameters

| Parameter | Purpose |
|---|---|
| `max_length` | Specifies the maximum length of the slug |
| `unique=True` | Ensures that each slug is unique in the table |
| `unique_for_date` | Declares that the slug should be unique for a particular date field |

**Note:** `unique_for_date` is enforced by Django model validation, not by a database-level unique constraint.

## 3. Automatically Generate Slug from Title

We can use Django's built-in `slugify()` function to generate a slug automatically from a title.

Example:

```python
from django.utils.text import slugify


title = "Django Tutorial for Beginners"

slug = slugify(title)

print(slug)
```

Output:

```text
django-tutorial-for-beginners
```

## 4. Automatically Generate Slug When Saving a Model

We can also generate a slug in the model's `save()` method.

Example:

```python
from django.db import models

from django.utils.text import slugify


class Post(models.Model):

    title = models.CharField(max_length=200)

    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True
    )

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(self.title)

        super().save(*args, **kwargs)
```

**Important:** This basic example does not handle duplicate titles. If two posts have the same title, they may generate the same slug and violate the unique constraint. A production application should implement a duplicate-slug strategy.

## 5. Use Slug in URLs

We can use a slug instead of an ID in Django URLs.

### `urls.py`

```python
from django.urls import path

from . import views


urlpatterns = [

    path(
        'blog/<slug:slug>/',
        views.post_detail,
        name='post_detail'
    ),

]
```

### `views.py`

```python
from django.shortcuts import get_object_or_404, render

from .models import Post


def post_detail(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug
    )

    return render(
        request,
        'post_detail.html',
        {
            'post': post
        }
    )
```

### Understanding the URL

```python
path('blog/<slug:slug>/', views.post_detail)
```

The `<slug:slug>` converter captures the slug from the URL and passes it to the view.

Example:

```text
/blog/shiv-puran-mahatmya/
```

The view receives:

```python
slug = 'shiv-puran-mahatmya'
```

Then we retrieve the corresponding post using:

```python
Post.objects.get(slug=slug)
```

Using `get_object_or_404()` is preferable when we want Django to return a 404 response if the post does not exist.

---

# 06. `post.comments.all()` – Understanding `related_name`

Suppose we have two models:

- `Post`
- `Comment`

One blog post can have multiple comments.

This is a **one-to-many relationship**.

We implement it using a `ForeignKey` in the `Comment` model.

### Step 1: Create the models

`models.py`

```python
from django.db import models


class Post(models.Model):

    title = models.CharField(max_length=200)


class Comment(models.Model):

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    message = models.TextField()
```

### Step 2: Understand `related_name`

```python
related_name='comments'
```

It defines the name used to access related comments from a post object.

Example:

```python
post = Post.objects.get(id=1)

comments = post.comments.all()
```

This returns all comments associated with that post.

### Without `related_name`

If we do not define `related_name`, Django provides a default reverse relationship name:

```text
modelname_set
```

For the `Post` and `Comment` example, we can access comments like this:

```python
post = Post.objects.get(id=1)

comments = post.comment_set.all()
```

### Difference

| With `related_name` | Without `related_name` |
|---|---|
| `post.comments.all()` | `post.comment_set.all()` |
| Custom reverse relation name | Default reverse relation name |
| Defined using `related_name='comments'` | Django generates the default name |

### Another example

Create multiple comments:

```python
post = Post.objects.get(id=1)

Comment.objects.create(
    post=post,
    message="Very useful article!"
)

Comment.objects.create(
    post=post,
    message="Thanks for sharing!"
)
```

Get all comments:

```python
post.comments.all()
```

**Important:** `related_name` is used for reverse access. It does not change the name of the ForeignKey field on the `Comment` model.

---

# 07. View SQLite Database Using DB Browser for SQLite

## 1. What is DB Browser for SQLite?

DB Browser for SQLite is a free, open-source tool that allows us to view and manage SQLite databases using a graphical user interface (GUI).

It is useful when we want to inspect the database without writing SQL commands.

Django uses SQLite by default in many new project configurations.

The database file is commonly named:

```text
db.sqlite3
```

## 2. Download DB Browser for SQLite

Follow these steps:

1. Open Google.
2. Search for `DB Browser for SQLite download`.
3. Open the official website:

   https://sqlitebrowser.org/

4. Open the Downloads section.
5. Review the available download options.
6. If you specifically want to try the Nightly Builds, locate the Nightly Builds section.
7. Open the appropriate download link.
8. Select the installer suitable for your operating system.
9. Download and install it.

**Note:** Nightly builds may include newer changes, but they can be less stable than regular releases. For normal usage, a stable release is generally preferable.

## 3. Open the Django Database

After installing DB Browser for SQLite:

1. Open your Django project folder.
2. Locate the `db.sqlite3` file in the project root directory.
3. Open DB Browser for SQLite.
4. Click **Open Database**.
5. Select your `db.sqlite3` file.
6. Click **Open**.

Now you can inspect your Django database.

## 4. View Database Records

After opening the database, we can use the following tabs:

| Tab | Purpose |
|---|---|
| Database Structure | Displays database tables and their structures |
| Browse Data | Displays records stored in tables |
| Execute SQL | Allows us to execute SQL queries |
| Edit Pragmas | Allows us to view and modify SQLite configuration |

### A. Database Structure

This tab displays:

- Table names
- Column names
- Data types
- Primary keys
- Indexes

For example, we may see Django tables such as:

```text
auth_user
django_admin_log
django_content_type
django_migrations
django_session
```

We can also see our custom application tables.

### B. Browse Data

This tab allows us to view the actual records stored in a selected table.

For example, we can select a customer table and view:

- Customer ID
- Customer name
- Email
- Address

### C. Execute SQL

This tab allows us to execute SQL queries directly against the SQLite database.

Example:

```sql
SELECT * FROM customer_app_customer;
```

To retrieve a specific customer:

```sql
SELECT *
FROM customer_app_customer
WHERE id = 1;
```

### D. Edit Pragmas

This tab allows us to inspect and modify SQLite database configuration settings (PRAGMA statements).

Be careful when changing database settings.

**Important:** DB Browser for SQLite is a database inspection and management tool. Changes made directly to the database may not be reflected in your Django model definitions or migration files.

---

# 08. Quick Revision

| Topic | Important concept |
|---|---|
| Admin customization | `list_display`, `list_filter`, `search_fields` |
| Jazzmin | Third-party package for customizing the Django admin interface |
| Pagination | `Paginator`, `Page`, `EmptyPage`, `PageNotAnInteger` |
| Dropdown fields | `choices` and `default` |
| Slug | Human-readable URL identifier |
| Slug generation | `slugify()` |
| Slug URLs | `<slug:slug>` |
| ForeignKey reverse access | `related_name` |
| Default reverse relation | `modelname_set` |
| SQLite GUI | DB Browser for SQLite |

# 09. Practice Questions

1. What is the purpose of `list_display`?
2. What is the difference between `list_filter` and `search_fields`?
3. Why do we use `prepopulated_fields`?
4. What is the difference between `raw_id_fields` and `autocomplete_fields`?
5. Why should Jazzmin be added before `django.contrib.admin`?
6. What is pagination?
7. What is the purpose of `Paginator`?
8. What is the difference between `page()` and `get_page()`?
9. How do we create a dropdown field using `choices`?
10. What is a slug?
11. What is the purpose of `slugify()`?
12. How can we use a slug in a Django URL?
13. What is the purpose of `related_name`?
14. What is the default reverse relationship name when `related_name` is not specified?
15. What is DB Browser for SQLite?
16. What is the purpose of the Browse Data tab?

## Practical Tasks

### Task 1: Admin customization

Create a `Post` model and customize its admin page using:

- `list_display`
- `list_filter`
- `search_fields`
- `ordering`
- `date_hierarchy`

### Task 2: Jazzmin

Install Django Jazzmin and customize:

- Site title
- Site header
- Site brand
- Welcome message
- Sidebar

### Task 3: Pagination

Create a customer list page that displays 10 records per page and provides:

- First
- Previous
- Next
- Last

### Task 4: Dropdown field

Create a post status field with:

- Draft
- Published

Display the selected status in the admin panel.

### Task 5: Slug

Create a blog post model that generates a slug from its title and displays post details using the slug in the URL.

### Task 6: Related name

Create `Post` and `Comment` models and retrieve all comments using:

```python
post.comments.all()
```

### Task 7: SQLite database

Open your Django `db.sqlite3` file using DB Browser for SQLite and inspect the tables and records.