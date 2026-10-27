# Django Session Management – Complete Notes

## 1. What Is Session Management?

A client and server communicate using HTTP. HTTP is a **stateless protocol**, which means the server does not automatically remember information from one request when processing the next request.

For example, suppose a user logs in to a website. The server needs a way to recognize that user on subsequent requests instead of asking them to log in again on every page.

**Session management** is the mechanism used to maintain information associated with a client across multiple requests.

### Real-life example

Imagine you log in to an online shopping website.

1. You log in using your username and password.
2. You add products to your cart.
3. You visit another page.
4. The website remembers your session and continues to associate your requests with your shopping activity.

Sessions help maintain this information across requests.

## 2. Session Management Techniques

Common techniques include:

| Technique | Description |
|---|---|
| Cookies | Store small pieces of information in the browser. |
| Server-side sessions | Store session data on the server and identify the session using a session ID. |
| URL rewriting | Pass information through URL parameters. |
| Hidden form fields | Pass values through hidden HTML form inputs. |

Django provides built-in cookie support and a Session API. Server-side sessions are generally preferable for maintaining application state.

---

# Part 1: Cookie-Based Session Management

## 3. What Is a Cookie?

A **cookie** is a small piece of information that a website asks the browser to store. The browser can send that cookie back to the server with subsequent requests when the cookie's scope and security settings permit it.

A cookie can contain a preference, an identifier, or other small values.

### Cookie request-response flow

<escape>
Client (Browser)
      |
      | 1. Sends request
      v
Django Server
      |
      | 2. Sends response with Set-Cookie header
      v
Client (Browser)
      |
      | 3. Stores cookie
      |
      | 4. Sends Cookie header on matching requests
      v
Django Server
</escape>

### How it works

1. The browser sends a request to the server.
2. The server returns a response containing a `Set-Cookie` header.
3. The browser stores the cookie according to its attributes.
4. The browser sends the cookie with matching future requests.
5. The server can read the cookie from the request.

## 4. How to Create a Cookie in Django

Django provides the `set_cookie()` method on an `HttpResponse` object.

**`views.py`**

```python
from django.http import HttpResponse

def set_user_cookie(request):
    response = HttpResponse('Cookie created successfully')

    response.set_cookie(
        key='username',
        value='Akash',
        max_age=180
    )

    return response
```

Here:

- `key` is the cookie name.
- `value` is the cookie value.
- `max_age=180` means the cookie expires after 180 seconds.

### URL configuration

```python
from django.urls import path
from . import views

urlpatterns = [
    path(
        'set-cookie/',
        views.set_user_cookie,
        name='set_user_cookie'
    ),
]
```

## 5. How to Retrieve a Cookie

Django provides `request.COOKIES`, which behaves like a dictionary.

```python
from django.http import HttpResponse

def get_user_cookie(request):
    username = request.COOKIES.get('username', 'Guest')

    return HttpResponse(f'Welcome, {username}')
```

If the browser sends a cookie named `username` with value `Akash`, the response displays:

```text
Welcome, Akash
```

Use `.get()` when a cookie might not exist. Accessing `request.COOKIES['username']` directly raises a `KeyError` if it is missing.

## 6. How to Delete a Cookie

Use `delete_cookie()` on the response object.

```python
from django.http import HttpResponse

def delete_user_cookie(request):
    response = HttpResponse('Cookie deleted')

    response.delete_cookie('username')

    return response
```

The browser deletes the cookie when the deletion response matches the cookie's relevant scope and attributes.

## 7. Temporary Cookies vs Persistent Cookies

### Temporary cookies

A temporary cookie, also called a session cookie, normally expires when the browser session ends.

```python
response.set_cookie(
    'username',
    'Akash'
)
```

No `max_age` or `expires` is specified here, so the cookie is generally treated as a browser-session cookie.

However, browser session restoration can sometimes preserve session cookies after the browser is closed.

### Persistent cookies

A persistent cookie has an expiry time or maximum age.

```python
response.set_cookie(
    'username',
    'Akash',
    max_age=180
)
```

The cookie expires after 180 seconds.

**Important:** Persistent cookies are not stored permanently. They are stored by the browser according to its policies until they expire or are deleted.

## 8. How to Check Whether the Browser Supports Cookies

Older Django tutorials use these session methods:

```python
request.session.set_test_cookie()
request.session.test_cookie_worked()
request.session.delete_test_cookie()
```

These methods were removed from modern Django versions. For current Django projects, you can test cookie support using a two-request approach.

### Step 1: Set a test cookie

```python
from django.http import HttpResponse

def cookie_test(request):
    response = HttpResponse(
        'Cookie test started. Reload this page to check.'
    )

    response.set_cookie(
        'cookie_test',
        'working',
        max_age=300
    )

    return response
```

### Step 2: Check the cookie on a subsequent request

```python
from django.http import HttpResponse

def check_cookie(request):
    if request.COOKIES.get('cookie_test') == 'working':
        return HttpResponse('Cookies are working')

    return HttpResponse(
        'Cookie not found. Cookies may be disabled.'
    )
```

Visit the first URL, then visit the second URL in the same browser. This tests whether the browser sends the cookie back.

---

## 9. Limitations of Cookies

- **Limited storage:** Cookies have size limits, commonly around 4 KB per cookie.
- **String-based values:** Cookies carry text values; complex Python objects need serialization and decoding.
- **Client-side storage:** Users can inspect or modify ordinary cookie values, so never trust them for authorization decisions.
- **Network overhead:** Matching cookies are sent with requests, adding to request size.
- **Browser restrictions:** Browsers limit cookie sizes and counts.
- **Security concerns:** Cookies require appropriate attributes and handling to reduce risks.

For example, avoid storing passwords or other secrets directly in cookies.

Useful cookie security attributes include:

- `httponly=True`: prevents JavaScript from reading the cookie.
- `secure=True`: sends the cookie only over HTTPS.
- `samesite='Lax'`: restricts some cross-site cookie sending.

Django's session cookie settings can configure similar attributes globally.

---

# Part 2: Django Session API

## 10. What Is a Django Session?

A Django session allows the server to store information associated with a particular browser session.

With the standard database-backed session configuration:

- Session data is stored in the server-side database.
- The browser normally stores a session ID in a cookie.
- The browser sends the session ID with subsequent matching requests.
- Django uses that ID to retrieve the corresponding session data.

The browser does not normally receive the entire server-side session dictionary.

### Django session flow

<escape>
Browser
   |
   | Request
   v
Django Server
   |
   | Creates or retrieves session
   v
Database (django_session table)
   |
   | Session data
   v
Django Server
   |
   | Response with session ID cookie
   v
Browser
</escape>

The default session cookie name is `sessionid`, unless you change `SESSION_COOKIE_NAME`.

## 11. Enable Sessions in Django

Django projects created using the standard project template normally have session support enabled already.

### Step 1: Check `INSTALLED_APPS`

In `settings.py`:

```python
INSTALLED_APPS = [
    # Other installed applications
    'django.contrib.sessions',
]
```

### Step 2: Check session middleware

In `settings.py`, confirm that session middleware is enabled:

```python
MIDDLEWARE = [
    # Other middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
]
```

Keep the standard middleware configuration intact; session middleware should appear before middleware that needs to access sessions.

### Step 3: Apply migrations

```bash
python manage.py migrate
```

This creates the database table required by Django's database-backed session engine.

## 12. Where Does Django Store Session Data?

Django supports several session storage backends, including:

- Database-backed sessions.
- Cache-backed sessions.
- File-based sessions.
- Cookie-based sessions.

The default backend is database-backed sessions.

The database model is:

```python
from django.contrib.sessions.models import Session
```

The corresponding database table is commonly named:

```text
django_session
```

The table contains fields such as:

| Field | Purpose |
|---|---|
| `session_key` | Unique identifier for the session. |
| `session_data` | Encoded session data. |
| `expire_date` | Expiration date and time. |

The exact database representation depends on Django's session implementation.

**Important:** With database-backed sessions, Django stores the session data in the database. The browser's `sessionid` cookie normally contains the session key, not all of the session data.

## 13. How to Store Data in a Session

Use `request.session` to access the current session dictionary.

**`views.py`**

```python
from django.http import HttpResponse

def set_session(request):
    request.session['username'] = 'Akash'
    request.session['city'] = 'Pune'
    request.session['logged_in'] = True

    return HttpResponse('Session data stored successfully')
```

### Explanation

```python
request.session['username'] = 'Akash'
```

This stores the value under the `username` key in the current session.

Other values can be stored in the same way.

Django normally marks the session as modified when you assign a top-level value, so you do not need to set `request.session.modified = True` for these assignments.

## 14. How to Retrieve Session Data

```python
from django.http import HttpResponse

def get_session(request):
    username = request.session.get('username', 'Guest')
    city = request.session.get('city', 'Unknown')

    return HttpResponse(
        f'Username: {username}, City: {city}'
    )
```

If the session contains those values, the response might display:

```text
Username: Akash, City: Pune
```

Use `.get()` when a key may not exist. It lets you provide a default value instead of raising a `KeyError`.

You can also access a key directly:

```python
username = request.session['username']
```

But this raises a `KeyError` if the key is missing.

## 15. How to Update Session Data

Assign a new value to an existing key.

```python
def update_session(request):
    request.session['city'] = 'Mumbai'

    return HttpResponse('Session updated')
```

The value for `city` is updated for that session.

## 16. How to Delete Session Data

### Delete one key

```python
def delete_session_key(request):
    request.session.pop('city', None)

    return HttpResponse('City removed from session')
```

### Delete all session data and start with an empty session

```python
def clear_session(request):
    request.session.flush()

    return HttpResponse('Session cleared')
```

`flush()` removes the current session data and session key. It is useful during logout because it removes the session associated with the current browser.

---

## 17. Useful Django Session Methods

| Method | Purpose |
|---|---|
| `request.session['key'] = value` | Store a value. |
| `request.session.get('key', default)` | Retrieve a value safely. |
| `request.session.pop('key', None)` | Remove one key. |
| `request.session.flush()` | Clear the current session and remove its key. |
| `request.session.set_expiry(seconds)` | Set the session's expiry policy. |
| `request.session.get_expiry_age()` | Get the approximate remaining lifetime in seconds. |
| `request.session.get_expiry_date()` | Get the session's calculated expiry date and time. |
| `request.session.clear()` | Remove session data while retaining the current session key. |
| `request.session.modified = True` | Explicitly mark the session as modified. |

## 18. How to Set Session Expiry Time

Use `set_expiry()` to control how long the session remains valid.

```python
def set_session_expiry(request):
    request.session['username'] = 'Akash'

    # Session expires after 180 seconds of inactivity
    request.session.set_expiry(180)

    return HttpResponse('Session expiry set')
```

The number represents seconds.

Other supported options include:

```python
request.session.set_expiry(0)
```

This makes the session cookie expire when the browser session ends.

```python
request.session.set_expiry(None)
```

This uses the configured default session expiry policy.

You can inspect the expiry settings:

```python
expiry_age = request.session.get_expiry_age()
expiry_date = request.session.get_expiry_date()
```

The expiry age is an estimate of the remaining lifetime based on the current session and configuration.

## 19. Save Session Data on Every Request

In `settings.py`:

```python
SESSION_SAVE_EVERY_REQUEST = True
```

When enabled, Django saves the session on every request, including requests where the session data has not changed. This also refreshes the session cookie's expiry information when applicable.

By default, Django saves a session when it has been modified.

### What does `request.session.modified = True` do?

Sometimes, you modify a mutable object stored inside a session instead of assigning a new top-level value.

For example:

```python
request.session['cart'] = {'product_1': 1}

# Modify the nested dictionary
cart = request.session['cart']
cart['product_2'] = 2

# Mark the session as modified
request.session.modified = True
```

Django does not always detect changes made inside nested dictionaries or lists. Setting `modified = True` tells Django that the session needs to be saved.

**Important:** You generally do not need to set this flag after ordinary assignments such as `request.session['username'] = 'Akash'`.

---

## 20. Complete Example: Session Management

### `views.py`

```python
from django.http import HttpResponse
from django.shortcuts import render


def session_home(request):
    return render(
        request,
        'session_home.html'
    )


def set_session(request):
    request.session['username'] = 'Akash'
    request.session['city'] = 'Pune'

    return HttpResponse('Session data saved')


def get_session(request):
    username = request.session.get('username', 'Guest')
    city = request.session.get('city', 'Unknown')

    return HttpResponse(
        f'Username: {username}<br>City: {city}'
    )


def delete_session(request):
    request.session.flush()

    return HttpResponse('Session cleared')
```

### Application `urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.session_home, name='session_home'),
    path('set-session/', views.set_session, name='set_session'),
    path('get-session/', views.get_session, name='get_session'),
    path('delete-session/', views.delete_session, name='delete_session'),
]
```

### `session_home.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Django Session Demo</title>
</head>
<body>
    <h1>Django Session Management</h1>

    <a href="{% url 'set_session' %}">Set Session</a>
    <br><br>

    <a href="{% url 'get_session' %}">Get Session</a>
    <br><br>

    <a href="{% url 'delete_session' %}">Delete Session</a>
</body>
</html>
```

### Test the example

1. Open the session home page.
2. Click **Set Session**.
3. Click **Get Session**. The stored username and city should appear.
4. Click **Delete Session**.
5. Click **Get Session** again. The default values should appear because the session data was cleared.

Ensure these application URLs are included in the project's main URL configuration.

---

## 21. How to View Session Data in Django Admin

Django's session model is not registered in the admin by default. You can register it if you want to inspect database-backed sessions.

In `admin.py`:

```python
from django.contrib import admin
from django.contrib.sessions.models import Session


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'expire_date')
    readonly_fields = (
        'session_key',
        'session_data',
        'expire_date',
    )
```

Then open Django Admin and navigate to **Sessions**.

The `session_data` field contains encoded data, so it may not be immediately readable in the admin interface. You can decode a session for inspection using Django's session model methods in trusted server-side code.

Expired sessions can be removed with:

```bash
python manage.py clearsessions
```

This command is useful for periodic session cleanup.

---

## 22. Cookie vs Django Session API

| Feature | Cookies | Database-backed Django sessions |
|---|---|---|
| Storage | Browser | Server-side database |
| Browser typically stores | Cookie value | Session ID cookie |
| Suitable for complex data | No, not directly | Yes, for serializable values |
| Client can directly change stored server data | Cookie values can be changed; server must not trust them | Not by changing the session ID alone |
| Data size | Limited | More suitable for larger session data |
| Common use | Preferences, identifiers | Shopping cart state, workflow state, user-related session data |

Django's signed cookie session backend is a different option: it stores session data in a signed cookie rather than the database. Its data is signed for integrity but is not encrypted by default.

## 23. Security Best Practices

- Do not store passwords or unnecessary sensitive information in sessions.
- Use HTTPS in production.
- Configure secure session cookies, for example `SESSION_COOKIE_SECURE = True` when serving the site over HTTPS.
- Keep `SESSION_COOKIE_HTTPONLY = True` to prevent JavaScript from reading the session cookie.
- Use appropriate `SESSION_COOKIE_SAMESITE` settings.
- Use `request.session.flush()` when logging out if you want to clear the current session.
- Never trust a client-provided cookie value as proof of identity or authorization.
- Use Django's authentication framework for login and permissions rather than implementing authentication from scratch.

## 24. Quick Revision

- HTTP is stateless by default.
- Session management helps preserve state across requests.
- Cookies are stored by the browser.
- Django's `request.COOKIES` reads cookies sent by the browser.
- `response.set_cookie()` creates a cookie.
- `response.delete_cookie()` requests deletion of a cookie.
- `request.session` accesses the current Django session.
- `request.session['key'] = value` stores session data.
- `request.session.get('key')` retrieves session data.
- `request.session.set_expiry(180)` configures expiry in seconds.
- `request.session.flush()` clears the current session and removes its key.
- `django.contrib.sessions` enables Django's session framework.
- `python manage.py migrate` creates the database-backed session table.
- `python manage.py clearsessions` removes expired database sessions.
