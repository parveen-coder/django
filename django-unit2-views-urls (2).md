# Unit 2 — Views & URLs

**From incoming request to outgoing response — Django's routing and logic layer**

*Prerequisite: the `mysite` project + `blog` app from Unit 1, with `runserver` working.*

Everything in this unit lives in two files students already created: `views.py` and `urls.py`.

## Contents

1. [Creating views and mapping to URLs](#1-creating-views-and-mapping-to-urls)
2. [Creating views and view logic](#2-creating-views-and-view-logic)
3. [HTTP requests](#3-http-requests)
4. [Creating requests and responses](#4-creating-requests-and-responses)
5. [Displaying Python data structures](#5-displaying-python-data-structures) — list, set, tuple, dict, list of list, list of dict
6. [Understanding URLs](#6-understanding-urls)
7. [Mapping URLs with params](#7-mapping-urls-with-params)
8. [Query parameters in the URL](#8-query-parameters-in-the-url)
9. [Regular expressions in URLs](#9-regular-expressions-in-urls)
10. [Error handling](#10-error-handling)
11. [Summary — the request/response loop](#11-summary--the-requestresponse-loop)
12. [Exercises](#12-exercises)

---

## 1. Creating views and mapping to URLs

A **view** is a Python function; a **URL pattern** is its address.

### The view — `blog/views.py`

```python
from django.http import HttpResponse

def welcome(request):
    # every view takes a request,
    # and returns a response
    return HttpResponse('Welcome!')
```

### The address — `blog/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('welcome/', views.welcome),
]
```

### The view contract

| Rule | What it means |
|---|---|
| **Takes an `HttpRequest`** | Django builds it from the incoming HTTP message and passes it as the first argument. |
| **Returns an `HttpResponse`** | Forgetting the `return` is the classic beginner bug — you get a `ValueError`. |
| **Is found by the URLconf** | The `path()` line is what connects `/welcome/` to your function. |

> **Try it:** add `/welcome/` and hit it in the browser before moving on.

---

## 2. Creating views and view logic

A view can contain **any Python logic** — compute, branch, loop — then return a response.

```python
from datetime import date
from django.http import HttpResponse

def greeting(request):
    hour = 14   # pretend: current hour
    if hour < 12:
        msg = 'Good morning!'
    else:
        msg = 'Good afternoon!'

    today = date.today().strftime('%A')
    html = f'<h1>{msg}</h1><p>Happy {today}</p>'
    return HttpResponse(html)
```

**Four ideas to hold on to:**

- **Plain Python** — variables, `if`/`else`, loops, imports. A view is just a function.
- **Build the output** — f-strings work for learning; real pages use templates (Unit 3).
- **One job per view** — one URL, one purpose, one response.
- **Test in the browser** — save the file, `runserver` reloads, refresh to see changes.

> **Demo idea:** change `hour`, refresh, watch the message flip. There is no magic — just a function returning a string.

---

## 3. HTTP requests

Every click and form submit is a **structured text message**.

### A raw HTTP request

```http
GET /blog/3/ HTTP/1.1
Host: 127.0.0.1:8000
User-Agent: Mozilla/5.0 ...
Accept: text/html

(body — empty for GET)
```

**method + path + headers + optional body — that's the whole message.**

### Common methods

| Method | Purpose |
|---|---|
| `GET` | Fetch a page or data. No side effects — safe to repeat. |
| `POST` | Submit data that changes something: forms, sign-ups, comments. |
| `PUT` / `PATCH` | Update an existing resource (common in APIs). |
| `DELETE` | Remove a resource (common in APIs). |

GET and POST cover ~95% of what a browser sends — master these two first.

### The `HttpRequest` object

Django parses the raw message into a friendly Python object.

| Attribute | What it holds |
|---|---|
| `request.method` | `'GET'`, `'POST'`, ... — branch on this in form views |
| `request.GET` | Query-string params (`?q=...`) as a dict-like object |
| `request.POST` | Submitted form fields — only filled on POST |
| `request.path` | The URL path being requested, e.g. `/blog/3/` |
| `request.headers` | All HTTP headers, case-insensitive lookup |

```python
def inspect(request):
    info = f'''
      Method: {request.method}
      Path:   {request.path}
      Query:  {request.GET}
      Agent:  {request.headers["User-Agent"]}
    '''
    return HttpResponse(info, content_type='text/plain')

# /inspect/?q=django&page=2
# request.GET['q']    →  'django'
# request.GET['page'] →  '2'  (a string!)
```

> **Gotcha:** everything in `request.GET` is a **string** — `'2'`, not `2`. Convert before doing arithmetic.

---

## 4. Creating requests and responses

Four response types cover almost every situation.

| Type | Use it for | Example |
|---|---|---|
| `HttpResponse` | Plain text or HTML you build yourself | `return HttpResponse('<h1>Hi!</h1>')` |
| `JsonResponse` | Dicts → JSON, for APIs & JavaScript | `return JsonResponse({'likes': 42})` |
| `render(...)` | Combine a template with data (Unit 3) | `return render(request, 'home.html', ctx)` |
| `redirect(...)` | Send the browser to another URL | `return redirect('/welcome/')` |

**Imports:** `HttpResponse` and `JsonResponse` come from `django.http`; `render` and `redirect` come from `django.shortcuts`.

Every response carries a **status code**: `200` OK, `302` redirect, `404` not found, `500` server error.

---

## 5. Displaying Python data structures

A view can hold any Python object, but the browser only understands **text**. So every structure has to be turned into a string (HTML or plain text) or into JSON before it leaves the view. Until templates arrive in Unit 3, we build that string ourselves.

Two tools do all the work:

- `'...'.join(...)` and f-strings → build HTML
- `JsonResponse(...)` → hand the structure to JavaScript as JSON

### List

```python
def show_list(request):
    subjects = ['Django', 'Flask', 'FastAPI']

    items = ''.join(f'<li>{s}</li>' for s in subjects)
    html = f'<h2>Subjects ({len(subjects)})</h2><ul>{items}</ul>'
    return HttpResponse(html)
```

As JSON, a top-level list needs `safe=False`:

```python
return JsonResponse(subjects, safe=False)   # ["Django", "Flask", "FastAPI"]
```

> `JsonResponse` only allows a `dict` at the top level by default — that check is what `safe=False` switches off.

### Tuple

Same handling as a list; only the source object is immutable. JSON has no tuple type, so it comes out as an array.

```python
def show_tuple(request):
    point = ('CSE', 4, 'B.Tech')

    rows = ''.join(f'<li>{value}</li>' for value in point)
    return HttpResponse(f'<ul>{rows}</ul>')

# JsonResponse(list(point), safe=False)  →  ["CSE", 4, "B.Tech"]
```

### Set

A set is **unordered** and **not JSON-serializable**, so convert it first — `sorted()` also gives a stable display order.

```python
def show_set(request):
    tags = {'python', 'web', 'python', 'orm'}   # duplicates dropped
    tags = sorted(tags)                         # → ['orm', 'python', 'web']

    items = ''.join(f'<li>{t}</li>' for t in tags)
    return HttpResponse(f'<ul>{items}</ul>')

# JsonResponse(tags, safe=False)         →  works (it is a list now)
# JsonResponse({'python'}, safe=False)   →  TypeError: not JSON serializable
```

### Dict

Iterate `.items()` to get keys and values together.

```python
def show_dict(request):
    student = {'name': 'Aman', 'roll': 21, 'branch': 'CSE'}

    rows = ''.join(
        f'<tr><th>{key}</th><td>{value}</td></tr>'
        for key, value in student.items()
    )
    return HttpResponse(f'<table border="1">{rows}</table>')
```

A dict is the one structure `JsonResponse` accepts as-is:

```python
return JsonResponse(student)     # {"name": "Aman", "roll": 21, "branch": "CSE"}
```

### List of lists

A nested list is naturally a **table**: outer list → rows, inner list → cells.

```python
def show_matrix(request):
    marks = [
        ['Aman', 78, 85],
        ['Simran', 91, 88],
        ['Ravi', 65, 72],
    ]
    headers = ['Name', 'DBMS', 'Django']

    head = ''.join(f'<th>{h}</th>' for h in headers)
    body = ''.join(
        '<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>'
        for row in marks
    )
    html = f'<table border="1"><tr>{head}</tr>{body}</table>'
    return HttpResponse(html)
```

Two loops: the outer one per row, the inner one per cell.

### List of dicts

The most common shape in real Django work — it is exactly what a database query returns (`Post.objects.values()` in Unit 3) and exactly what an API sends.

```python
def show_records(request):
    students = [
        {'name': 'Aman',   'roll': 21, 'branch': 'CSE'},
        {'name': 'Simran', 'roll': 22, 'branch': 'IT'},
        {'name': 'Ravi',   'roll': 23, 'branch': 'ECE'},
    ]

    headers = students[0].keys()            # column names from the first record
    head = ''.join(f'<th>{h}</th>' for h in headers)
    body = ''.join(
        '<tr>' + ''.join(f'<td>{row[h]}</td>' for h in headers) + '</tr>'
        for row in students
    )
    return HttpResponse(f'<table border="1"><tr>{head}</tr>{body}</table>')
```

As an API endpoint:

```python
return JsonResponse(students, safe=False)
# [{"name": "Aman", "roll": 21, ...}, ...]
```

> Taking headers from `students[0]` assumes every dict has the same keys, and it raises `IndexError` on an empty list — guard with `if not students:` before indexing.

### Quick reference

| Structure | HTML idea | JSON |
|---|---|---|
| `list` | `<ul>` of `<li>` | `JsonResponse(data, safe=False)` |
| `tuple` | same as list | convert: `list(data)` |
| `set` | sort first, then list | convert: `sorted(data)` |
| `dict` | 2-column table (`key` / `value`) | `JsonResponse(data)` |
| list of lists | table — outer = rows, inner = cells | `safe=False` |
| list of dicts | table — keys = headers, values = cells | `safe=False` |

> Building HTML with f-strings is a teaching device. From Unit 3 onward the same structures go into a template as context and `{% for %}` does the looping — the Python side stays identical.

---

## 6. Understanding URLs

Anatomy of an address, and how Django matches it:

```
https://   mysite.com   :8000   /blog/3/   ?tag=py
scheme     host          port    path       query string
                                 ↑
                        Django matches THIS
```

- **Django only sees the path.** Scheme, host, port and query string are ignored by URL matching — `request.GET` holds the query separately.
- **First match wins.** `urlpatterns` is checked top to bottom; the first pattern that fits handles the request. **Order matters.**
- **`include()` delegates.** `config/urls.py` strips the matched prefix and hands the rest of the path to the app's own `urls.py`.
- **Trailing slashes matter.** Django's convention is `/blog/`, not `/blog` — `APPEND_SLASH` redirects for you on GET.

> First-match-wins explains most "why is the wrong view running?" mysteries.

---

## 7. Mapping URLs with params

Capture parts of the path and pass them to the view.

### Built-in path converters

| Converter | Matches | Example URL |
|---|---|---|
| `<int:...>` | Digits only → Python `int` | `post/7/` |
| `<str:...>` | Any text except `/` (default) | `user/sam/` |
| `<slug:...>` | Letters, digits, `-` and `_` | `tag/my-post/` |
| `<uuid:...>` | A UUID value | `order/075a.../` |
| `<path:...>` | Any text, including `/` | `files/a/b/c.txt` |

```python
# blog/urls.py
urlpatterns = [
    path('post/<int:post_id>/', views.post_detail),
    path('tag/<slug:tag>/', views.posts_by_tag),
]
```

```python
# blog/views.py — the param arrives as an argument
def post_detail(request, post_id):
    # /post/7/  →  post_id == 7 (int!)
    return HttpResponse(f'Post number {post_id}')
```

> The parameter name in the pattern must **exactly match** the view's argument name. The `int` converter both validates (letters give a 404) and converts — no manual casting.

### End-to-end: two captures in one pattern

```python
# blog/urls.py
path('archive/<int:year>/<int:month>/',
     views.archive,
     name='archive'),
# e.g.  /archive/2026/07/
```

```python
# blog/views.py
def archive(request, year, month):
    if not 1 <= month <= 12:
        raise Http404('Bad month')
    return HttpResponse(f'Posts from {month}/{year}')
```

**Step by step:**

1. Browser asks for `/archive/2026/07/`
2. Pattern matches; captures `year=2026`, `month=7` as ints
3. Django calls `archive(request, year=2026, month=7)`
4. View validates, builds and returns the response

`name='archive'` lets templates and redirects refer to this URL without hard-coding the path.

> Converters validate **format** (digits) but not **meaning** — month `13` passes the pattern, hence the range check inside the view.

---

## 8. Query parameters in the URL

Everything after the `?` is the **query string**. It never appears in `urlpatterns` — Django hands it to the view inside `request.GET`.

```
/search/?q=django&page=2&tag=web&tag=orm
        └──────────── query string ────────────┘
```

- `?` starts the query string
- `key=value` is one parameter
- `&` separates parameters
- a key may repeat (`tag=web&tag=orm`)

### Reading them safely

```python
def search(request):
    q    = request.GET.get('q', '')        # missing → '' instead of an error
    page = request.GET.get('page', 1)
    tags = request.GET.getlist('tag')      # ['web', 'orm'] — all values

    return HttpResponse(f'q={q} page={page} tags={tags}')
```

| Expression | Behaviour |
|---|---|
| `request.GET['q']` | Raises `MultiValueDictKeyError` if the key is absent |
| `request.GET.get('q')` | Returns `None` if absent — **preferred** |
| `request.GET.get('q', '')` | Returns a default of your choosing |
| `request.GET.getlist('tag')` | All values for a repeated key; `[]` if absent |
| `'q' in request.GET` | Test whether the parameter was sent at all |

### Values are always strings

```python
page = request.GET.get('page', '1')

try:
    page = int(page)                 # '2' → 2 ; 'abc' → ValueError
except ValueError:
    page = 1                         # fall back instead of crashing

start = (page - 1) * 10              # now the arithmetic is safe
```

Unlike `<int:...>` in a path, **no converter runs on the query string** — validation is your job.

### Query params vs path params

| | Path parameter | Query parameter |
|---|---|---|
| Looks like | `/post/7/` | `/search/?q=django` |
| Declared in | `urlpatterns` | nowhere — just sent |
| Read with | view argument | `request.GET` |
| Converted | yes (`int`, `slug`, `uuid`) | no — always `str` |
| Required | yes, or the URL doesn't match | no, it's optional |
| Use for | identifying **which** resource | filtering, sorting, searching, paging |

Rule of thumb: **what the page is about** goes in the path; **how you want it shown** goes in the query string.

### A worked example

```python
# blog/urls.py
path('search/', views.search, name='search'),
```

```python
# blog/views.py
def search(request):
    posts = ['Django ORM', 'Flask basics', 'Django URLs', 'CSS grid']

    q = request.GET.get('q', '').strip()
    if q:
        posts = [p for p in posts if q.lower() in p.lower()]

    if not posts:
        return HttpResponse(f'<p>No results for <b>{q}</b></p>')

    items = ''.join(f'<li>{p}</li>' for p in posts)
    return HttpResponse(f'<h2>{len(posts)} result(s)</h2><ul>{items}</ul>')

# /search/            → all 4 posts
# /search/?q=django   → 2 posts
# /search/?q=zzz      → "No results"
```

### Building a query string in code

```python
from urllib.parse import urlencode

url = '/search/?' + urlencode({'q': 'django', 'page': 2})
# '/search/?q=django&page=2'
```

`urlencode` escapes spaces and special characters correctly — don't glue query strings together by hand.

> Because query params are optional, a view that reads them must still work when they are missing. Always supply a default.

---

## 9. Regular expressions in URLs

`re_path()` — for patterns `path()` can't express.

### Regex mini-cheatsheet

| Symbol | Meaning |
|---|---|
| `^` `$` | start / end of the path |
| `[0-9]{4}` | exactly four digits |
| `[a-z-]+` | one or more lowercase letters or `-` |
| `(?P<name>...)` | capture group → view argument `name` |
| `?` | previous item is optional |

```python
from django.urls import path, re_path

urlpatterns = [
    re_path(r'^post/(?P<year>[0-9]{4})/$', views.year_archive),
    # matches /post/2026/  but not /post/26/
]
```

### Same idea, both styles

```python
path('post/<int:year>/', ...)            # simple
re_path(r'^post/(?P<year>[0-9]{4})/$', ...)
# regex adds: exactly 4 digits
```

> **Rule of thumb:** reach for `path()` first; use `re_path()` only when you truly need the extra precision.
>
> **Gotcha:** regex captures always arrive as **strings** — `(?P<year>[0-9]{4})` gives `'2026'`, not `2026`. Another reason to prefer `path()` when it suffices.

---

## 10. Error handling

Fail loudly in development, gracefully in production.

| Code | Name | Cause |
|---|---|---|
| `404` | Not found | Bad URL or missing object — `raise Http404` |
| `403` | Forbidden | Logged in, but not allowed — `PermissionDenied` |
| `500` | Server error | An unhandled exception in your code |

### Raising a 404 in a view

```python
from django.http import Http404

def post_detail(request, post_id):
    if post_id > 100:      # no such post
        raise Http404('Post not found')
    return HttpResponse(f'Post {post_id}')
```

### The shortcut you'll use with models

```python
from django.shortcuts import get_object_or_404

post = get_object_or_404(Post, id=post_id)
```

### `DEBUG = True` vs `False`

With `DEBUG=True` you get the yellow traceback page — read it top-down, it names the file and line. In production (`DEBUG=False`) users see clean error pages instead: add templates named `404.html` and `500.html`.

### Reading errors like a developer

**404 — page not found**

```
Page not found (404)
Request URL: /welcom/

Django tried these URL patterns:
  1. admin/
  2. welcome/
  3. post/<int:post_id>/

The current path, welcom/, didn't match any of these.
```

*Fix:* compare the requested path against the listed patterns — here it's a typo.

**500 — ValueError (forgot the return)**

```
ValueError at /welcome/
The view blog.views.welcome didn't return an HttpResponse object.
It returned None instead.

blog/views.py, line 4, in welcome
    HttpResponse('Welcome!')
    # ↑ missing the word 'return'
```

*Fix:* read the last frame of the traceback — it points at your file and line.

> Recreate both errors live: mistype a URL, then delete a `return`. Students who can read these two screens can self-rescue for the rest of the course.

---

## 11. Summary — the request/response loop

| # | Beat | What happens |
|---|---|---|
| 1 | **Route** | `path()` & `re_path()` match the URL, capture params |
| 2 | **Run** | Your view: any Python, request object in hand |
| 3 | **Respond** | `HttpResponse`, `JsonResponse`, `redirect` — or `Http404` |

*Next unit: templates & models — real HTML pages backed by a database.*

---

## 12. Exercises

1. **Challenge 1** — build `/archive/<year>/<month>/` with month validation (404 on bad months).
2. **Challenge 2** — add an `/api/status/` view returning `JsonResponse({'ok': True})`.
3. **Challenge 3** — write `/students/` that renders a list of dicts as an HTML table, and `/api/students/` that returns the same data with `JsonResponse(..., safe=False)`.
4. **Challenge 4** — extend `/students/` with query parameters: `?branch=CSE` filters the rows and `?sort=roll` orders them. Both must be optional, and an unknown value must not crash the view.
5. **Stretch** — use `re_path` to match `/post/<4-digit-year>/<slug>/`.
