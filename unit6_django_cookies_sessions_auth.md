# Unit 6 — Cookies and Sessions, Users and Authentication

> **Scope:** Creating cookies and sessions in Django, creating and managing users in Django, login and logout URLs in Django, and using Django login in views (`authenticate()`, `login()`, `logout()`, `@login_required`, `request.user`).
>
> **Code source:** `Wednesday` project → `student` app (`setcookie`, `getcookie`, `deletecookie`, `setsession`, `getsession`, `deletesession`, `clearsession`, `createuser`/`showusers`/`updateuser`/`deleteuser`, `dashboard`), `Wednesday/urls.py` (login/logout URLs) and `Wednesday/settings.py` (`LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL`) in the class repository.
>
> **Tested on:** Django 6.x, Python 3.12+, PostgreSQL 16 with the class `DATABASES` settings. All outputs (response headers, session table data, redirects) come from running the class code.

---

## Table of Contents

1. [Why Cookies and Sessions? — HTTP is Stateless](#1-why-cookies-and-sessions--http-is-stateless)
2. [Creating Cookies in Django](#2-creating-cookies-in-django)
3. [Creating Sessions in Django](#3-creating-sessions-in-django)
4. [Cookies vs Sessions](#4-cookies-vs-sessions)
5. [Creating and Managing Users in Django](#5-creating-and-managing-users-in-django)
6. [Django's Authentication System — The Building Blocks](#6-djangos-authentication-system--the-building-blocks)
7. [Login and Logout URLs in Django](#7-login-and-logout-urls-in-django)
8. [Using Django Login in Views](#8-using-django-login-in-views)
9. [The Complete Login Story](#9-the-complete-login-story)
10. [Testing Cookies, Sessions and Login](#10-testing-cookies-sessions-and-login)
11. [Issues Found in the Class Code (and Fixes)](#11-issues-found-in-the-class-code-and-fixes)
12. [URL → View → Template Map for Unit 6](#12-url--view--template-map-for-unit-6)
13. [Summary and Practice Questions](#13-summary-and-practice-questions)

---

## Project Files Used in This Unit

```text
Wednesday/
├── Wednesday/
│   ├── settings.py        # SessionMiddleware, AuthenticationMiddleware,
│   │                      # LOGIN_URL, LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
│   └── urls.py            # login/ (LoginView), logout/ (LogoutView)
└── student/
    ├── views.py           # setcookie, getcookie, deletecookie,
    │                      # setsession, getsession, deletesession, clearsession,
    │                      # createuser, showusers, updateuser, deleteuser,
    │                      # dashboard (@login_required)
    ├── urls.py
    └── templates/student/
        ├── home.html        # "Welcome, {{c}}" — message page
        ├── cookie.html      # shows the cookie value
        ├── session.html     # shows the session values
        ├── Login.html       # login form (used by LoginView)
        ├── dashboard.html   # protected page with Logout button
        └── users.html       # list of users
```

**Settings already in the class project:**

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',          # users, login, permissions
    'django.contrib.contenttypes',
    'django.contrib.sessions',      # sessions (django_session table)
    'django.contrib.messages',
    ...
]

MIDDLEWARE = [
    ...
    'django.contrib.sessions.middleware.SessionMiddleware',        # gives request.session
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',     # gives request.user
    ...
]

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/student/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'
```

---

## 1. Why Cookies and Sessions? — HTTP is Stateless

### 1.1 The Problem

HTTP is **stateless**: every request is independent. The server does not remember anything about the previous request from the same browser.

```text
Request 1:  POST /login/  (username=rahul, password=...)   → "Login successful"
Request 2:  GET  /student/dashboard/                         → "Who are you?"
Request 3:  GET  /student/cars/                              → "Who are you?"
```

Without help, the user would have to log in on **every page**. Shopping carts, "remember me", language/theme choice and logins all need the server to **recognise the same browser** across requests.

### 1.2 The Solution

| Tool | Where data is stored | Idea |
|------|---------------------|------|
| **Cookie** | In the **browser** | Server gives the browser a small note; the browser shows it on every later request |
| **Session** | On the **server** (database) | Server keeps the data; the browser only keeps a random **session id** in a cookie |
| **Authentication** | Built on sessions | After login, the user's id is stored in the session → `request.user` on every request |

---

## 2. Creating Cookies in Django

### 2.1 What is a Cookie?

A **cookie** is a small piece of text (name = value, up to about **4 KB**) that the **server asks the browser to store**. The browser then **sends it back automatically** with every request to the same site.

```text
1. Browser:  GET /student/setcookie/
2. Server:   200 OK
             Set-Cookie: username=Rahul; Path=/          ← "please remember this"
3. Browser stores  username=Rahul
4. Browser:  GET /student/getcookie/
             Cookie: username=Rahul                       ← sent automatically
5. Server reads request.COOKIES['username'] → "Rahul"
```

### 2.2 The Three Operations

| Operation | Code | Object used |
|-----------|------|-------------|
| **Set** | `response.set_cookie('key', 'value')` | the **response** (server → browser) |
| **Get** | `request.COOKIES.get('key')` | the **request** (browser → server) |
| **Delete** | `response.delete_cookie('key')` | the **response** |

> Cookies are **set on the response** and **read from the request**. You cannot read a cookie in the same request that sets it — the browser sends it back only on the *next* request.

### 2.3 Class Code — Set, Get and Delete a Cookie

**Set — `setcookie`**

```python
def setcookie(request):

    response = render(request, 'student/home.html',{"c":"CookieSet"})

    response.set_cookie('username', 'Rahul')

    return response
```

`render()` returns a response object; we attach the cookie to it, then return it.

**Get — `getcookie`**

```python
def getcookie(request):

    u = request.COOKIES.get('username')

    return render(request, 'student/cookie.html',
                  {'u': u})
```

```html
<!-- cookie.html -->
<h2>Cookie Information</h2>
<p>Username: {{ u }}</p>
```

**Delete — `deletecookie`**

```python
def deletecookie(request):

    response = render(request, 'student/home.html',{"c":"cookie deleted"})

    response.delete_cookie('username')

    return response
```

**URLs:**

```python
path('setcookie/', views.setcookie, name='setcookie'),
path('getcookie/', views.getcookie, name='getcookie'),
path('deletecookie/', views.deletecookie, name='deletecookie'),
```

**What actually happens (verified — response headers):**

```text
GET /student/setcookie/      → Welcome, CookieSet
    Set-Cookie: username=Rahul; Path=/

GET /student/getcookie/      → Cookie Information  Username: Rahul

GET /student/deletecookie/   → Welcome, cookie deleted
    Set-Cookie: username=""; expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0; Path=/

GET /student/getcookie/      → Cookie Information  Username:          (cookie is gone)
```

Deleting a cookie = setting it again with an **empty value** and an **expiry date in the past**, so the browser throws it away.

### 2.4 Seeing Cookies in the Browser

**Chrome:** right-click → *Inspect* → **Application** tab → **Storage → Cookies → http://127.0.0.1:8000**

You will see `username`, `csrftoken` (Unit 4) and, after a session is used, `sessionid`. You can also **edit** values here — which is why cookies must never hold anything that should be trusted (Section 2.8).

### 2.5 `set_cookie()` Options

```python
response.set_cookie(
    key,                 # cookie name
    value='',            # value (stored as a string)
    max_age=None,        # lifetime in seconds
    expires=None,        # or an exact date/time
    path='/',            # URLs the cookie is sent to
    domain=None,         # e.g. ".lpu.in" to share across sub-domains
    secure=False,        # True → only sent over HTTPS
    httponly=False,      # True → JavaScript (document.cookie) cannot read it
    samesite=None,       # 'Lax' / 'Strict' / 'None' — CSRF protection
)
```

| Option | Use |
|--------|-----|
| none of `max_age` / `expires` | **Session cookie** — deleted when the browser is closed (class `setcookie`) |
| `max_age=60*60*24*7` | **Persistent cookie** — lives 7 days even after closing the browser |
| `httponly=True` | Protects the cookie from being stolen by malicious JavaScript (XSS) |
| `secure=True` | Never sent over plain HTTP (use in production) |
| `samesite='Lax'` | Not sent with cross-site POST requests (helps against CSRF) |

**Example with options (verified headers):**

```python
def setcookie2(request):
    response = render(request, 'student/home.html', {"c": "Cookies set"})
    response.set_cookie('username', 'Rahul', max_age=60 * 60 * 24 * 7)   # 7 days
    response.set_cookie('theme', 'dark')                                  # until browser closes
    response.set_cookie('token', 'abc123', httponly=True, samesite='Lax') # JS cannot read it
    response.set_signed_cookie('role', 'student', salt='unit6')           # tamper-proof
    return response
```

```text
Set-Cookie: username=Rahul; expires=Sun, 29 Nov 2026 16:40:01 GMT; Max-Age=604800; Path=/
Set-Cookie: theme=dark; Path=/
Set-Cookie: token=abc123; HttpOnly; Path=/; SameSite=Lax
Set-Cookie: role=student:1xVAbh:7IMO3Wu_A3vjkDHj2yscHmuM1uWVtEK1C1WJBoyH9Tk; Path=/
```

### 2.6 Reading Cookies Safely

```python
def getcookie2(request):
    context = {
        'username': request.COOKIES.get('username', 'Guest'),        # default if missing
        'theme': request.COOKIES.get('theme', 'light'),
        'role': request.get_signed_cookie('role', default='unknown', salt='unit6'),
        'all_cookies': request.COOKIES,                              # dictionary of every cookie
    }
    return render(request, 'student/cookie2.html', context)
```

```html
<!-- cookie2.html -->
<h2>Cookies</h2>
<p>Username : {{ username }}</p>
<p>Theme : {{ theme }}</p>
<p>Role (signed) : {{ role }}</p>
<h3>All cookies sent by the browser</h3>
<ul>
{% for key, value in all_cookies.items %}
    <li>{{ key }} = {{ value }}</li>
{% endfor %}
</ul>
```

`request.COOKIES['username']` (square brackets) raises `KeyError` → **500** when the cookie is missing. Always use `.get()` with a default.

### 2.7 Signed Cookies — Detecting Tampering

A **signed cookie** stores `value:timestamp:signature`. The signature is made with the project's `SECRET_KEY`, so if the user edits the value the signature no longer matches.

```python
response.set_signed_cookie('role', 'student', salt='unit6')
role = request.get_signed_cookie('role', default='unknown', salt='unit6')
```

**Verified:** after editing the cookie in the browser to `admin:fake:signature`, the page shows **`Role (signed) : unknown`** — the tampered value is rejected.

> Signed ≠ encrypted. The user can still **read** `student`; they just cannot **change** it unnoticed.

### 2.8 Cookie Example — Visit Counter

```python
def visitcookie(request):
    visits = int(request.COOKIES.get('visits', 0)) + 1           # cookie values are strings
    response = render(request, 'student/home.html', {"c": f"visit number {visits}"})
    response.set_cookie('visits', visits, max_age=60 * 60 * 24 * 30)
    return response
```

Third visit (verified): **`Welcome, visit number 3`**

### 2.9 Limitations and Security of Cookies

| Limitation | Consequence |
|------------|-------------|
| ~4 KB per cookie, ~50 per site | Only small values |
| Stored on the user's machine | User can **read, edit and delete** them |
| Sent with every request | Large cookies slow every page |
| Values are strings | Convert: `int(request.COOKIES.get('visits', 0))` |
| Can be blocked by the user | Site must still work without them |

**Never store passwords, roles, prices, marks or anything security-related in a plain cookie.** Use sessions for that.

---

## 3. Creating Sessions in Django

### 3.1 What is a Session?

A **session** stores data **on the server**, linked to one browser. The browser only receives a random **session id** in a cookie named **`sessionid`**.

```text
Browser                                Server (PostgreSQL)
───────                                ──────────────────────────────────────────
cookie: sessionid=lw9e31w9mg...  ──▶   django_session
                                        session_key   = lw9e31w9mg...
                                        session_data  = {"username": "Rahul", "course": "Django"}
                                        expire_date   = 2026-12-06
```

The user cannot see or change the data — only the meaningless id.

### 3.2 How Sessions Are Enabled

Already set in the class project:

| Setting | Role |
|---------|------|
| `'django.contrib.sessions'` in `INSTALLED_APPS` | Creates the `django_session` table (on `migrate`) |
| `SessionMiddleware` in `MIDDLEWARE` | Loads the session before the view, saves it after; provides **`request.session`** |

`request.session` behaves like a **Python dictionary**.

### 3.3 Class Code — Set, Get, Delete and Clear

**Set — `setsession`**

```python
def setsession(request):

    request.session['username'] = 'Rahul'
    request.session['course'] = 'Django'

    return render(request, 'student/home.html', {"c":"session created"})
```

**Get — `getsession`**

```python
def getsession(request):

    username = request.session.get('username')
    course = request.session.get('course')

    return render(request, 'student/session.html', {
        'username': username,
        'course': course
    })
```

```html
<!-- session.html -->
<h2>Session Details</h2>
<p>Username: {{ username }}</p>
<p>Course: {{ course }}</p>
```

**Delete one key — `deletesession`**

```python
def deletesession(request):

    if 'username' in request.session:
        del request.session['username']

    username = request.session.get('username')
    course = request.session.get('course')

    return render(request, 'student/session.html', {
        'username': username,
        'course': course
    })
```

**Delete everything — `clearsession`**

```python
def clearsession(request):

    request.session.flush()

    return render(request, 'student/session.html')
```

**URLs:**

```python
path('setsession/', views.setsession, name='setsession'),
path('getsession/', views.getsession, name='getsession'),
path('deletesession/', views.deletesession, name='deletesession'),
path('clearsession/', views.clearsession, name='clearsession'),
```

**What actually happens (verified):**

```text
GET /student/setsession/     → Welcome, session created
    Set-Cookie: sessionid=lw9e31w9mg6dh9g87hisqiq1552zjeli; expires=Sun, 06 Dec 2026 16:39:23 GMT;
                HttpOnly; Max-Age=1209600; Path=/; SameSite=Lax

GET /student/getsession/     → Username: Rahul    Course: Django
GET /student/deletesession/  → Username: None     Course: Django     (only 'username' removed)
GET /student/clearsession/   → Username:          Course:            (everything removed)
GET /student/getsession/     → Username: None     Course: None
```

Notice the `sessionid` cookie Django created automatically:

| Attribute | Meaning |
|-----------|---------|
| `Max-Age=1209600` | 2 weeks (`SESSION_COOKIE_AGE` default) |
| `HttpOnly` | JavaScript cannot steal it |
| `SameSite=Lax` | Not sent with cross-site POSTs |

### 3.4 Where the Data Lives — the `django_session` Table (verified)

```text
jot=> \d django_session
    Column    |           Type           | Nullable
--------------+--------------------------+----------
 session_key  | character varying(40)    | not null      ← value of the sessionid cookie
 session_data | text                     | not null      ← encoded + signed dictionary
 expire_date  | timestamp with time zone | not null
```

**Reading a session row in the shell:**

```python
>>> from django.contrib.sessions.models import Session
>>> s = Session.objects.get(session_key="duhq9lchp7t2dtq297mn9bfclpeutmh1")
>>> s.session_data
'eyJ1c2VybmFtZSI6IlJhaHVsIiwiY291cnNlIjoiRGphbmdvIn0:1xVAb5:aWOfQBYKefyScMUygj7hV...'
>>> s.expire_date
datetime.datetime(2026, 12, 6, 16, 39, 23, 328652, tzinfo=datetime.timezone.utc)
>>> s.get_decoded()
{'username': 'Rahul', 'course': 'Django'}
```

### 3.5 Session Operations

| Task | Code |
|------|------|
| Store | `request.session['key'] = value` |
| Read (safe) | `request.session.get('key', default)` |
| Read (error if missing) | `request.session['key']` → `KeyError` |
| Check | `'key' in request.session` |
| Delete one key | `del request.session['key']` *(guard with `if 'key' in ...`)* or `request.session.pop('key', None)` |
| Delete all + new id | `request.session.flush()` |
| Delete all, keep id | `request.session.clear()` |
| All keys / items | `request.session.keys()`, `.items()` |
| Session id | `request.session.session_key` |
| Set lifetime | `request.session.set_expiry(seconds)` |
| Remaining lifetime | `request.session.get_expiry_age()` |

Values must be **JSON-serialisable**: `str`, `int`, `float`, `bool`, `list`, `dict`, `None`. Store `user.id`, not a model object.

### 3.6 Session Example — Visit Counter

```python
def visitsession(request):
    request.session['visits'] = request.session.get('visits', 0) + 1
    return render(request, 'student/home.html', {"c": f"visit number {request.session['visits']}"})
```

Third visit (verified): **`Welcome, visit number 3`** — same result as the cookie version, but the number is kept **on the server** and the user cannot change it.

### 3.7 Session Example — A List (Course Cart)

```python
def addcourse(request, name):
    courses = request.session.get('courses', [])
    if name not in courses:
        courses.append(name)
    request.session['courses'] = courses          # assign back so Django saves it
    return render(request, 'student/home.html', {"c": f"courses: {', '.join(courses)}"})
```

```python
path('addcourse/<str:name>/', views.addcourse, name='addcourse'),
```

`/student/addcourse/Django/` then `/student/addcourse/Python/` → **`courses: Django, Python`** (verified).

> **Why assign back?** Django saves the session only when it sees an assignment (`request.session[...] = ...`) or deletion. `request.session['courses'].append('Python')` changes the list *inside* the session without Django noticing, so the change may be lost. Either assign back, or set `request.session.modified = True`.

### 3.8 Session Expiry

```python
def shortsession(request):
    request.session['otp'] = '4521'
    request.session.set_expiry(300)               # 5 minutes
    return render(request, 'student/home.html', {"c": f"expires in {request.session.get_expiry_age()} seconds"})
```

Output (verified): **`expires in 300 seconds`**

| `set_expiry(value)` | Session ends |
|---------------------|--------------|
| `300` (int) | After 300 seconds of **inactivity** |
| a `datetime` | At that moment |
| `0` | When the browser is closed |
| `None` | Use the global setting |

**Global settings (`settings.py`):**

```python
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14       # default: 2 weeks (in seconds)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False      # True → log out when the browser closes
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False                # True in production (HTTPS only)
SESSION_SAVE_EVERY_REQUEST = False           # True → expiry restarts on every request
```

Expired rows stay in the table until you clean them:

```bash
python manage.py clearsessions
```

### 3.9 Session Storage Engines

| `SESSION_ENGINE` | Stored in |
|------------------|-----------|
| `django.contrib.sessions.backends.db` *(default, class project)* | `django_session` table |
| `django.contrib.sessions.backends.cache` | Cache (Redis/Memcached) — fastest |
| `django.contrib.sessions.backends.cached_db` | Cache + database |
| `django.contrib.sessions.backends.file` | Files on disk |
| `django.contrib.sessions.backends.signed_cookies` | The cookie itself (signed, readable by user) |

---

## 4. Cookies vs Sessions

| | Cookie | Session |
|---|--------|---------|
| Data stored in | Browser | Server (`django_session`) |
| Browser holds | The actual value | Only `sessionid` |
| Size | ~4 KB | Practically unlimited |
| User can read / change | Yes / Yes | No / No |
| Data types | String only | Any JSON value (list, dict, int ...) |
| Set with | `response.set_cookie()` | `request.session['k'] = v` |
| Read with | `request.COOKIES.get()` | `request.session.get()` |
| Delete with | `response.delete_cookie()` | `del request.session['k']` / `flush()` |
| Default lifetime | Until browser closes | 2 weeks |
| Good for | Theme, language, "last visited", non-sensitive preferences | Login, cart, OTP, role, anything that must be trusted |

Sessions **use** a cookie — without cookies enabled, sessions (and login) do not work.

---

## 5. Creating and Managing Users in Django

### 5.1 The Built-in `User` Model (recap of Unit 5)

```python
from django.contrib.auth.models import User
```

Stored in the `auth_user` table with `username`, `password` (hashed), `email`, `first_name`, `last_name`, `is_active`, `is_staff`, `is_superuser`, `last_login`, `date_joined`.

| Kind of user | Created with | Can log in to site | Can open `/admin/` | Permissions |
|--------------|-------------|--------------------|--------------------|-------------|
| Normal user | `create_user()` / sign-up form | ✔ | ✘ | Only those given |
| Staff user | `is_staff=True` | ✔ | ✔ | Only those given |
| Superuser | `create_superuser()` / `createsuperuser` | ✔ | ✔ | All |
| Inactive user | `is_active=False` | ✘ | ✘ | — |

### 5.2 Creating Users — Three Ways

**1. Command line (superuser):**

```bash
python manage.py createsuperuser
```

**2. Shell or view code:**

```python
User.objects.create_user(username='rahul', email='rahul@lpu.in', password='Rahul@123')
User.objects.create_superuser(username='admin', email='admin@lpu.in', password='Admin@123')
```

**3. Admin:** `/admin/` → Users → Add user (Unit 5, Section 9).

### 5.3 Class Code — Managing Users from Views

```python
from django.contrib.auth.models import User

def createuser(request):

    user = User.objects.create_user(
        username='Parveen',
        email='parveen@gmail.com',
        password='parveen123'
    )

    return render(request, 'student/home.html', {"c":"user created"})

def showusers(request):

    users = User.objects.all()

    return render(request, 'student/users.html',
                  {'users': users})

def updateuser(request):

    user = User.objects.get(username='Navjot')

    user.email = 'navjot@gmail.com'

    user.save()

    return redirect('alluser')

def deleteuser(request):

    user = User.objects.get(username='Navjot')

    user.delete()

    return redirect('alluser')
```

```python
path('createuser/',views.createuser, name='createuser' ),
path('alluser/',views.showusers, name='alluser' ),
path('updateuser/',views.updateuser, name='updateuser' ),
path('deleteuser/',views.deleteuser, name='deleteuser' ),
```

```html
<!-- users.html -->
<h2>Registered Users</h2>
{% for user in users %}
    <p>{{ user.username }}</p>
    <p>{{ user.email }}</p>
{% endfor %}
```

These show **C**reate, **R**ead, **U**pdate, **D**elete on `auth_user`. Because the username is fixed, `createuser` fails the second time and `updateuser`/`deleteuser` fail if `Navjot` doesn't exist — improved versions are in the Unit 5 notes (Section 13, Issues 3–4).

> Inside the `for` loop, the name `user` hides the logged-in `{{ user }}` that Django gives every template. Use another name (`{% for u in users %}`) on pages that also show the logged-in user.

### 5.4 Sign-up — Users Creating Their Own Account

Django provides **`UserCreationForm`** with `username`, `password1`, `password2`, which checks that the username is free, the two passwords match, and the password is strong enough. It hashes the password when saving.

**View:**

```python
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()                    # creates the user with a hashed password
            login(request, user)                  # log in straight away
            messages.success(request, f"Welcome {user.username}, your account is created.")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'student/signup.html', {'form': form})
```

**Template — `signup.html`:**

```html
<h2>Create Account</h2>
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Sign up</button>
</form>
<p>Already registered? <a href="{% url 'mylogin' %}">Login</a></p>
```

```python
path('signup/', views.signup, name='signup'),
```

**Verified:**

```text
password "abc" / "abc"
  → password2: This password is too short. It must contain at least 8 characters.
               This password is too common.

username "rahul" (exists), passwords different
  → username:  A user with that username already exists.
  → password2: The two password fields didn’t match.

username "neha", "Strong@Pass99" twice
  → 302 /student/dashboard/   "Welcome neha"   (account created and logged in)
```

### 5.5 Password Validation Rules

The rules come from `AUTH_PASSWORD_VALIDATORS` in `settings.py` (already present in the class project):

| Validator | Rejects |
|-----------|---------|
| `UserAttributeSimilarityValidator` | Password too similar to username / email |
| `MinimumLengthValidator` | Fewer than 8 characters |
| `CommonPasswordValidator` | Common passwords (`password`, `12345678` ...) |
| `NumericPasswordValidator` | Only digits |

> These run in forms (`UserCreationForm`, `PasswordChangeForm`) and `createsuperuser` — **not** in `User.objects.create_user()`, which accepts any password.

### 5.6 Changing a Password

```python
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)   # stay logged in
            messages.success(request, "Password changed.")
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'student/change_password.html', {'form': form})
```

Changing a password logs the user out of every session (the session stores a hash of the password). **`update_session_auth_hash()`** keeps the *current* session logged in — verified: dashboard still returns 200 after the change.

From the command line: `python manage.py changepassword rahul`

### 5.7 A Profile Page Using `request.user`

```python
@login_required
def profile(request):
    return render(request, 'student/profile.html')
```

```html
<!-- profile.html — `user` is available in every template -->
<h2>My Profile</h2>
<p>Username : {{ user.username }}</p>
<p>Email : {{ user.email|default:"-" }}</p>
<p>Joined : {{ user.date_joined|date:"d M Y" }}</p>
<p>Last login : {{ user.last_login|date:"d M Y H:i" }}</p>
<p>Staff : {{ user.is_staff|yesno:"Yes,No" }}</p>
```

Verified output: `Username : rahul  Email : rahul@lpu.in  Joined : 22 Nov 2026  Last login : 22 Nov 2026 16:40  Staff : No`

---

## 6. Django's Authentication System — The Building Blocks

### 6.1 What Django Provides

| Piece | Purpose |
|-------|---------|
| `User` model | Stores users |
| `authenticate()` | Checks username + password → user or `None` |
| `login()` | Stores the user's id in the session (logs in) |
| `logout()` | Clears the session (logs out) |
| `request.user` | The current user on every request |
| `@login_required` | Protects a view |
| `LoginView`, `LogoutView`, password views | Ready-made pages |
| `UserCreationForm`, `AuthenticationForm`, `PasswordChangeForm` | Ready-made forms |

### 6.2 `authenticate()` — Checking Credentials

```python
from django.contrib.auth import authenticate

user = authenticate(request, username='rahul', password='Rahul@123')
# correct              → <User: rahul>
# wrong password       → None
# unknown username     → None
# is_active = False    → None
```

It hashes the typed password and compares it with `auth_user.password`. It does **not** log the user in.

### 6.3 `login()` — Starting the Logged-in Session

```python
from django.contrib.auth import login

login(request, user)
```

What `login()` stores in the session (verified, decoded from `django_session`):

```python
{'_auth_user_id': '10',
 '_auth_user_backend': 'django.contrib.auth.backends.ModelBackend',
 '_auth_user_hash': '001f06e7d14cd0b6750de6f0ff37719cbdb9c28abb5a7c8f46e303337a8f5167'}
```

It also:
- gives the browser a **new** `sessionid` (verified: the key changes on login — protects against *session fixation*), while keeping existing session data,
- updates `auth_user.last_login`.

### 6.4 `logout()` — Ending the Session

```python
from django.contrib.auth import logout

logout(request)
```

Flushes the whole session (verified: session is `{}` afterwards) — the user becomes anonymous. Any cart or other session data is removed too.

### 6.5 `request.user`

`AuthenticationMiddleware` reads `_auth_user_id` from the session on **every request** and sets `request.user`:

| Situation | `request.user` | `is_authenticated` |
|-----------|----------------|--------------------|
| Logged in | `User` object (`rahul`) | `True` |
| Not logged in | `AnonymousUser` | `False` |

```python
def some_view(request):
    if request.user.is_authenticated:
        print(request.user.username, request.user.email)
    else:
        print("Guest")
```

In templates `user` (from the `auth` context processor) and `request.user` are the same object:

```html
{% if user.is_authenticated %}
    <p>Welcome {{ user.username }}</p>
{% else %}
    <a href="{% url 'login' %}">Login</a>
{% endif %}
```

---

## 7. Login and Logout URLs in Django

### 7.1 Class Code — `Wednesday/urls.py`

```python
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include("user.urls")),
    path('student/',include("student.urls")),
    path("__debug__/", include("debug_toolbar.urls")),

    path('login/', auth_views.LoginView.as_view(
            template_name='student/login.html'
        ), name='login'),

    path('/logout/', auth_views.LogoutView.as_view(),
             name='logout'),
]
```

> ⚠ Two problems in these two lines — `template_name` case and the leading `/` in `'/logout/'`. Verified fixes are in Section 11 (Issues 1 and 2). The rest of this section uses the corrected lines:

```python
path('login/', auth_views.LoginView.as_view(template_name='student/Login.html'), name='login'),
path('logout/', auth_views.LogoutView.as_view(), name='logout'),
```

### 7.2 `LoginView` — the Ready-made Login Page

`LoginView` is a **class-based view** — `.as_view()` turns it into a function Django can call. It:

| Request | Does |
|---------|------|
| GET | Shows an empty `AuthenticationForm` (`username`, `password`) in the template |
| POST, valid | `authenticate()` + `login()`, then redirects to `next` or `LOGIN_REDIRECT_URL` |
| POST, invalid | Shows the form again with an error |

**Login template — `student/templates/student/Login.html` (class code):**

```html
<h2>User Login</h2>
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Login</button>
</form>
```

**Verified behaviour:**

```text
POST /login/ rahul / Rahul@123  → 302  /student/dashboard/       (LOGIN_REDIRECT_URL)
POST /login/ rahul / x          → 200  "Please enter a correct username and password.
                                        Note that both fields may be case-sensitive."
```

Useful `LoginView.as_view(...)` arguments:

| Argument | Default | Purpose |
|----------|---------|---------|
| `template_name` | `registration/login.html` | Template to show |
| `redirect_authenticated_user` | `False` | `True` → a logged-in user opening `/login/` is sent onward |
| `next_page` | `LOGIN_REDIRECT_URL` | Where to go after login |
| `authentication_form` | `AuthenticationForm` | Custom form |

### 7.3 `LogoutView` — Logout Must Be POST

Since **Django 5.0**, `LogoutView` accepts only **POST** (a GET link could be triggered by any website — Unit 4 CSRF). Verified:

```text
GET  /logout/   → 405 Method Not Allowed
POST /logout/   → 302 /login/                  (LOGOUT_REDIRECT_URL)
```

So logout is a **form with a button**, not a link — exactly as in `dashboard.html`:

```html
<form method="POST" action="{% url 'logout' %}">
    {% csrf_token %}
    <button type="submit">Logout</button>
</form>
```

### 7.4 The Three Login Settings

```python
LOGIN_URL = '/login/'                       # where @login_required sends anonymous users
LOGIN_REDIRECT_URL = '/student/dashboard/'  # after login (when there is no ?next=)
LOGOUT_REDIRECT_URL = '/login/'             # after logout
```

URL **names** also work: `LOGIN_URL = 'login'`, `LOGIN_REDIRECT_URL = 'dashboard'`.

| Setting | Default | Used by |
|---------|---------|---------|
| `LOGIN_URL` | `/accounts/login/` | `@login_required`, `permission_required` |
| `LOGIN_REDIRECT_URL` | `/accounts/profile/` | `LoginView` |
| `LOGOUT_REDIRECT_URL` | `None` (shows a "logged out" page) | `LogoutView` |

### 7.5 The `?next=` Parameter

```text
1. Anonymous user opens   /student/dashboard/
2. @login_required        → 302  /login/?next=/student/dashboard/
3. User logs in           → 302  /student/dashboard/   (back where they wanted to go)
```

Verified: `GET /student/dashboard/` (not logged in) → `302 /login/?next=/student/dashboard/`.

`LoginView` reads `next` automatically. In a custom template, keep it with a hidden input:

```html
<input type="hidden" name="next" value="{{ next }}">
```

### 7.6 All Built-in Auth URLs in One Line

Instead of writing each URL, include Django's set:

```python
urlpatterns = [
    ...
    path('accounts/', include('django.contrib.auth.urls')),
]
```

It adds (verified list):

| URL | Name | View |
|-----|------|------|
| `accounts/login/` | `login` | `LoginView` |
| `accounts/logout/` | `logout` | `LogoutView` |
| `accounts/password_change/` | `password_change` | `PasswordChangeView` |
| `accounts/password_change/done/` | `password_change_done` | `PasswordChangeDoneView` |
| `accounts/password_reset/` | `password_reset` | `PasswordResetView` |
| `accounts/password_reset/done/` | `password_reset_done` | `PasswordResetDoneView` |
| `accounts/reset/<uidb64>/<token>/` | `password_reset_confirm` | `PasswordResetConfirmView` |
| `accounts/reset/done/` | `password_reset_complete` | `PasswordResetCompleteView` |

These views look for templates in a **`registration/`** folder: `registration/login.html`, `registration/password_change_form.html`, etc. (The admin app supplies admin-styled versions of the password templates if you don't write your own.)

> Use **either** the class's separate `login/` and `logout/` paths **or** `include('django.contrib.auth.urls')` — not both with the same names.

### 7.7 Login / Logout Links in a Navbar

```html
<nav>
    <a href="{% url 'car_list' %}">Cars</a>
    {% if user.is_authenticated %}
        <span>Hi, {{ user.username }}</span>
        <a href="{% url 'dashboard' %}">Dashboard</a>
        <form method="POST" action="{% url 'logout' %}" style="display:inline">
            {% csrf_token %}
            <button type="submit">Logout</button>
        </form>
    {% else %}
        <a href="{% url 'login' %}">Login</a>
        <a href="{% url 'signup' %}">Sign up</a>
    {% endif %}
</nav>
```

---

## 8. Using Django Login in Views

### 8.1 Protecting a View — `@login_required` (class code)

```python
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):

    return render(request, 'student/dashboard.html')
```

```html
<!-- dashboard.html -->
<h1>Student Dashboard</h1>
<h3>Welcome {{ request.user.username }}</h3>
<p>You are successfully logged in.</p>
<form method="POST" action="{% url 'logout' %}">
    {% csrf_token %}
    <button type="submit">Logout</button>
</form>
```

```python
path('dashboard/', views.dashboard, name='dashboard'),
```

**Verified flow:**

```text
GET  /student/dashboard/  (anonymous)          → 302 /login/?next=/student/dashboard/
POST /login/  rahul / Rahul@123                → 302 /student/dashboard/
GET  /student/dashboard/                       → 200 "Welcome rahul  You are successfully logged in."
POST logout                                    → 302 /login/
GET  /student/dashboard/                       → 302 /login/?next=/student/dashboard/
```

`@login_required` options:

```python
@login_required(login_url='/student/mylogin/')            # override LOGIN_URL for this view
@login_required(redirect_field_name='go')                 # ?go= instead of ?next=
```

### 8.2 Writing Your Own Login View — `authenticate()` + `login()`

`LoginView` hides the steps. Writing the view yourself shows exactly what happens:

```python
from django.contrib.auth import authenticate, login, logout
from django.utils.http import url_has_allowed_host_and_scheme


def user_login(request):
    if request.user.is_authenticated:                      # already logged in
        return redirect('dashboard')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)   # 1. check

        if user is not None:
            login(request, user)                                             # 2. log in

            next_url = request.POST.get('next') or request.GET.get('next')   # 3. go back
            if next_url and url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
                return redirect(next_url)
            return redirect('dashboard')

        error = "Invalid username or password"                              # 4. failed
    return render(request, 'student/mylogin.html', {'error': error, 'next': request.GET.get('next', '')})
```

**Template — `mylogin.html`:**

```html
<h2>Login</h2>

{% for m in messages %}<p style="color:green;">{{ m }}</p>{% endfor %}
{% if error %}<p style="color:red;">{{ error }}</p>{% endif %}

<form method="POST">
    {% csrf_token %}
    <input type="hidden" name="next" value="{{ next }}">
    <label>Username</label>
    <input type="text" name="username" required><br><br>
    <label>Password</label>
    <input type="password" name="password" required><br><br>
    <button type="submit">Login</button>
</form>
<p>New user? <a href="{% url 'signup' %}">Sign up</a></p>
```

**Logout view — POST only:**

```python
from django.views.decorators.http import require_POST


@require_POST
def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('mylogin')
```

**URLs:**

```python
path('mylogin/', views.user_login, name='mylogin'),
path('mylogout/', views.user_logout, name='mylogout'),
```

**Verified:**

```text
POST /student/mylogin/  rahul / wrong                          → 200  "Invalid username or password"
POST /student/mylogin/?next=/student/profile/ (correct)        → 302  /student/profile/
POST /student/mylogin/  next=https://evil.com/ (correct)       → 302  /student/dashboard/   (unsafe next ignored)
POST /student/mylogin/  while already logged in                → 302  /student/dashboard/
inactive user (is_active=False), correct password              → "Invalid username or password"
GET  /student/mylogout/                                        → 405  Method Not Allowed
POST /student/mylogout/                                        → 302  /student/mylogin/
```

> **Why check `next`?** Without `url_has_allowed_host_and_scheme()`, an attacker could send a link like `/student/mylogin/?next=https://evil.com/` — after a real login the user lands on a fake site (*open redirect*). `LoginView` does this check automatically.

### 8.3 `LoginView` vs Your Own View

| | `LoginView` (class code) | Custom `user_login` |
|---|---|---|
| Code to write | 1 URL line + template | View + URL + template |
| Form | `AuthenticationForm` (`{{ form.as_p }}`) | Your own HTML inputs |
| `next` handling + safety check | Automatic | You write it |
| Error message | Built-in | You choose |
| Extra logic (log attempts, "remember me", block after 3 tries) | Needs subclassing | Easy |
| Teaches | How to configure | What happens inside |

### 8.4 Using `request.user` Inside Views

```python
@login_required
def my_cars(request):
    # show only the logged-in user's data (needs an owner = ForeignKey(User, ...) field)
    cars = Car.objects.filter(owner=request.user)
    return render(request, 'student/car_list.html', {'cars': cars})
```

```python
def car_create(request):
    ...
    if form.is_valid():
        car = form.save(commit=False)
        car.owner = request.user          # record who added it
        car.save()
```

Combining with Unit 5 permissions:

```python
from django.contrib.auth.decorators import permission_required

@login_required
@permission_required('student.delete_car', raise_exception=True)
def car_delete(request, id):
    ...
```

### 8.5 "Remember Me" with Sessions

```python
if user is not None:
    login(request, user)
    if not request.POST.get('remember_me'):
        request.session.set_expiry(0)          # log out when the browser closes
```

```html
<label><input type="checkbox" name="remember_me"> Remember me</label>
```

### 8.6 Messages After Login / Logout

The `messages` framework (Unit 4) stores one-time messages in the session:

```python
messages.success(request, "Welcome back!")
messages.info(request, "You have been logged out.")
```

```html
{% for m in messages %}<p>{{ m }}</p>{% endfor %}
```

---

## 9. The Complete Login Story

```text
 1. GET  /student/dashboard/
        AuthenticationMiddleware: no _auth_user_id in session → request.user = AnonymousUser
        @login_required → 302 /login/?next=/student/dashboard/

 2. GET  /login/?next=/student/dashboard/
        LoginView shows Login.html  (+ csrftoken cookie — Unit 4)

 3. POST /login/   username, password, csrfmiddlewaretoken
        CsrfViewMiddleware checks token                                  (Unit 4)
        authenticate() → compares hashed password in auth_user           (Unit 5)
        login()        → new sessionid; session = {_auth_user_id: 10, ...} (django_session)
                         last_login updated
        → 302 /student/dashboard/

 4. GET  /student/dashboard/      Cookie: sessionid=...
        SessionMiddleware loads the session from django_session
        AuthenticationMiddleware → request.user = <User: rahul>
        @login_required passes → dashboard.html "Welcome rahul"           (Unit 3 template)

 5. POST /logout/
        logout() → session flushed, sessionid replaced
        → 302 /login/
```

Everything from earlier units comes together: URLs and views (Unit 2), templates (Unit 3), forms and CSRF (Unit 4), the `auth_user` table and hashing (Unit 5), and now sessions.

---

## 10. Testing Cookies, Sessions and Login

All seven tests pass on PostgreSQL **after** the two URL fixes in Section 11.

**`student/test_unit6.py`**

```python
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class CookieTests(TestCase):
    def test_set_get_delete_cookie(self):
        self.client.get("/student/setcookie/")
        self.assertEqual(self.client.cookies["username"].value, "Rahul")
        response = self.client.get("/student/getcookie/")
        self.assertEqual(response.context["u"], "Rahul")
        self.client.get("/student/deletecookie/")
        self.assertEqual(self.client.cookies["username"].value, "")


class SessionTests(TestCase):
    def test_set_and_read_session(self):
        self.client.get("/student/setsession/")
        self.assertEqual(self.client.session["username"], "Rahul")
        response = self.client.get("/student/getsession/")
        self.assertEqual(response.context["course"], "Django")

    def test_clear_session(self):
        self.client.get("/student/setsession/")
        self.client.get("/student/clearsession/")
        self.assertNotIn("username", self.client.session)


class LoginLogoutTests(TestCase):
    def setUp(self):
        User.objects.create_user("rahul", "rahul@lpu.in", "Rahul@123")

    def test_dashboard_needs_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, "/login/?next=/student/dashboard/", fetch_redirect_response=False)

    def test_login_page_loads(self):
        self.assertEqual(self.client.get(reverse("login")).status_code, 200)

    def test_login_then_logout(self):
        response = self.client.post(reverse("login"), {"username": "rahul", "password": "Rahul@123"})
        self.assertRedirects(response, "/student/dashboard/")
        self.assertContains(self.client.get(reverse("dashboard")), "Welcome rahul")

        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, "/login/", fetch_redirect_response=False)
        self.assertEqual(self.client.get(reverse("dashboard")).status_code, 302)

    def test_wrong_password_stays_on_login_page(self):
        response = self.client.post(reverse("login"), {"username": "rahul", "password": "wrong"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
```

```text
$ python manage.py test student.test_unit6
.......
----------------------------------------------------------------------
Ran 7 tests in 1.733s
OK
```

| Test tool | Use |
|-----------|-----|
| `self.client.cookies["name"].value` | Cookie stored in the test client |
| `self.client.session["key"]` | Current session data |
| `self.client.login(username=..., password=...)` | Log in without the form |
| `self.client.force_login(user)` | Log in without a password |
| `response.wsgi_request.user` | Who the request was made as |
| `assertRedirects(..., fetch_redirect_response=False)` | Check a redirect URL only |

---

## 11. Issues Found in the Class Code (and Fixes)

### Issue 1 — Login page works on macOS but crashes on Linux/servers ❗

```python
path('login/', auth_views.LoginView.as_view(template_name='student/login.html'), name='login'),
```

The file is **`Login.html`** (capital L). macOS and Windows file systems ignore case, so it works on the class laptop. On Linux (every hosting server, GitHub Codespaces, a student's Ubuntu machine) — verified:

```text
GET /login/  → 500   django.template.exceptions.TemplateDoesNotExist: student/login.html
```

**Fix (verified — `GET /login/` → 200 on Linux):** make the names match exactly. Either change the code:

```python
template_name='student/Login.html'
```

or rename the file to lower case (recommended — keep all template names lower case):

```bash
git mv student/templates/student/Login.html student/templates/student/login.html
```

### Issue 2 — `'/logout/'` has a leading slash ❗

```python
path('/logout/', auth_views.LogoutView.as_view(), name='logout'),
```

Django's check warns: *"Your URL pattern '/logout/' [name='logout'] has a route beginning with a '/'. Remove this slash as it is unnecessary."* Verified effects:

```text
reverse('logout') / {% url 'logout' %}   → "/%2Flogout/"     (strange URL)
POST /logout/                            → 404 Not Found      (typing the normal URL fails)
POST /%2Flogout/  (dashboard button)     → 302 /login/        (works only by accident)
```

**Fix (verified — `{% url 'logout' %}` → `/logout/`, POST → 302 `/login/`, GET → 405):**

```python
path('logout/', auth_views.LogoutView.as_view(), name='logout'),
```

### Issue 3 — `createuser`, `updateuser`, `deleteuser` use fixed usernames

Second visit to `/student/createuser/` → `IntegrityError` (username exists) → 500; `updateuser`/`deleteuser` → `DoesNotExist` → 500 if `Navjot` is missing; `deleteuser` deletes on a GET link. Verified fixes with `exists()`, `get_object_or_404()` and `@require_POST` are in the **Unit 5 notes, Section 13, Issues 3–4**.

### Issue 4 — Cookie stores a username in plain text

`setcookie` stores `username=Rahul` in a normal cookie, which the user can edit in DevTools. Fine for demonstrating cookies, but anything used for identity or permissions must go in the **session** (or at least a **signed cookie**, Section 2.7).

### Issue 5 — No sign-up or custom login view yet

The class code uses the ready-made `LoginView`. The syllabus topic *"Using Django Login in Views"* is covered in Sections 5.4 and 8.2 with verified `signup`, `user_login` and `user_logout` views that call `authenticate()`, `login()` and `logout()` directly.

### Issue 6 — `home.html` login block is commented out

The `{% if request.user.is_authenticated %}` block in `home.html` is inside `{% comment %}`. Once Issue 2 is fixed, it can be enabled to show Login / Dashboard / Logout depending on the user (Section 7.7).

---

## 12. URL → View → Template Map for Unit 6

| URL | Name | View | Template | Topic |
|-----|------|------|----------|-------|
| `/student/setcookie/` | `setcookie` | `setcookie` | `home.html` | Set cookie |
| `/student/getcookie/` | `getcookie` | `getcookie` | `cookie.html` | Read cookie |
| `/student/deletecookie/` | `deletecookie` | `deletecookie` | `home.html` | Delete cookie |
| `/student/setsession/` | `setsession` | `setsession` | `home.html` | Set session |
| `/student/getsession/` | `getsession` | `getsession` | `session.html` | Read session |
| `/student/deletesession/` | `deletesession` | `deletesession` | `session.html` | Delete one key |
| `/student/clearsession/` | `clearsession` | `clearsession` | `session.html` | `flush()` |
| `/student/createuser/` | `createuser` | `createuser` | `home.html` | Create user |
| `/student/alluser/` | `alluser` | `showusers` | `users.html` | List users |
| `/student/updateuser/` | `updateuser` | `updateuser` | → `alluser` | Update user |
| `/student/deleteuser/` | `deleteuser` | `deleteuser` | → `alluser` | Delete user |
| `/login/` | `login` | `LoginView` | `Login.html` | Login URL |
| `/logout/` *(after fix)* | `logout` | `LogoutView` | → `/login/` | Logout URL |
| `/student/dashboard/` | `dashboard` | `dashboard` | `dashboard.html` | `@login_required` |

**Examples added in these notes (all verified):**

| URL | Name | View | Topic |
|-----|------|------|-------|
| `/student/setcookie2/`, `/student/getcookie2/` | `setcookie2`, `getcookie2` | cookie options, signed cookie | Cookies |
| `/student/visitcookie/`, `/student/visitsession/` | `visitcookie`, `visitsession` | visit counters | Cookie vs session |
| `/student/addcourse/<name>/` | `addcourse` | list in session | Sessions |
| `/student/shortsession/` | `shortsession` | `set_expiry()` | Sessions |
| `/student/signup/` | `signup` | `UserCreationForm` | Creating users |
| `/student/mylogin/`, `/student/mylogout/` | `mylogin`, `mylogout` | `authenticate`/`login`/`logout` | Login in views |
| `/student/changepassword/` | `change_password` | `PasswordChangeForm` | Managing users |
| `/student/profile/` | `profile` | `request.user` | Login in views |

---

## 13. Summary and Practice Questions

### 13.1 Unit Summary

| Concept | Key Point |
|---------|-----------|
| Stateless HTTP | Server forgets each request — cookies/sessions add memory |
| Cookie | Small text in the browser; sent back on every request |
| Set / get / delete cookie | `response.set_cookie()` / `request.COOKIES.get()` / `response.delete_cookie()` |
| `max_age` | Persistent cookie; without it the cookie ends when the browser closes |
| `httponly`, `secure`, `samesite` | Protect cookies from JS theft, HTTP, cross-site requests |
| Signed cookie | `set_signed_cookie` / `get_signed_cookie` — detects tampering |
| Session | Data on the server, only `sessionid` in the browser |
| `request.session` | Dictionary-like; needs `SessionMiddleware` + `django.contrib.sessions` |
| `del` / `flush()` | Remove one key / remove everything + new id |
| `django_session` | `session_key`, `session_data`, `expire_date` |
| Expiry | `set_expiry()`, `SESSION_COOKIE_AGE` (2 weeks), `clearsessions` |
| Users | `create_user()`, `createsuperuser`, `UserCreationForm` for sign-up |
| Password | Validators in forms; `PasswordChangeForm` + `update_session_auth_hash()` |
| `authenticate()` | Checks credentials → user or `None` |
| `login()` / `logout()` | Store / clear the user id in the session |
| `request.user` | `User` or `AnonymousUser`; `is_authenticated` |
| `LoginView` / `LogoutView` | Ready-made; logout is **POST only** (Django 5+) |
| Settings | `LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL` |
| `include('django.contrib.auth.urls')` | 8 login/logout/password URLs at once |
| `@login_required` | Redirects anonymous users to `LOGIN_URL?next=...` |
| `next` | Return to the requested page; validate it in custom views |

### 13.2 Practice Questions

**Short answer (2 marks)**

1. Why is HTTP called stateless? Name two ways Django overcomes it.
2. Write the code to set a cookie `city=Jalandhar` that lasts 3 days.
3. Why can a cookie set in a view not be read in the same request?
4. What is stored in the browser when Django uses sessions?
5. Differentiate between `del request.session['key']` and `request.session.flush()`.
6. Differentiate between `authenticate()` and `login()`.
7. What is `AnonymousUser`?
8. Why must logout be done with a POST request in Django 5+?
9. What does the `next` query parameter do?

**Medium answer (5 marks)**

10. Compare cookies and sessions on any five points.
11. Write views to set, read and delete a signed cookie `role`. Explain what happens if the user edits it.
12. Explain the `django_session` table and show how to decode a session in the shell.
13. List the settings `LOGIN_URL`, `LOGIN_REDIRECT_URL` and `LOGOUT_REDIRECT_URL` and explain the full redirect flow when an anonymous user opens a `@login_required` page.
14. Write a sign-up view using `UserCreationForm` that logs the new user in and redirects to a dashboard.

**Long answer (10 marks)**

15. Build a **course cart** using sessions: views to add a course, remove a course, view the cart and clear it, with URLs and a template. Explain why the list must be assigned back to the session.
16. Write a complete custom login system **without** `LoginView`: login view using `authenticate()` and `login()` (with safe `next` handling and an error message), logout view (POST only), a `@login_required` dashboard, URLs, templates and the three settings.
17. Explain the complete journey of a login request from `GET /student/dashboard/` to the dashboard being shown, naming the middleware, tables, cookies and redirects involved at each step.
18. Write test cases that check: a cookie is set and read, a session value is stored, an anonymous user is redirected from the dashboard, a correct login redirects to the dashboard, a wrong password stays on the login page, and logout ends the session.

---

*End of Unit 6 — Cookies and Sessions, Users and Authentication*
