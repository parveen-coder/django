# Error Handling in Django

> **Scope:** Handling errors with `HttpResponse` and its subclasses, custom error templates (`404.html`, `500.html`, `403.html`, `400.html`), the behaviour of `DEBUG = True` vs `DEBUG = False`, the complete list of Django exception types with their names and modules, and the full HTTP status code reference.
>
> **Tested on:** Django 4.2 / 5.x, Python 3.10+
>
> **Continues the `blog` app example used in Unit 3.**

---

## Table of Contents

1. [Introduction — Where Errors Occur](#1-introduction--where-errors-occur)
2. [HTTP Status Codes — Complete Reference](#2-http-status-codes--complete-reference)
3. [Types of Errors in Django (Exception Names)](#3-types-of-errors-in-django-exception-names)
4. [Error Handling using `HttpResponse`](#4-error-handling-using-httpresponse)
5. [Error Handling using Templates (Custom Error Pages)](#5-error-handling-using-templates-custom-error-pages)
6. [`DEBUG = True` — The Technical Error Page](#6-debug--true--the-technical-error-page)
7. [Practical Error-Handling Patterns in Views](#7-practical-error-handling-patterns-in-views)
8. [Logging, Middleware and Admin E-mail Reports](#8-logging-middleware-and-admin-e-mail-reports)
9. [Testing Error Handling](#9-testing-error-handling)
10. [Summary and Practice Questions](#10-summary-and-practice-questions)

---

## 1. Introduction — Where Errors Occur

Every HTTP response carries a **status code** that tells the browser whether the request succeeded. Error handling in Django means:

1. **Detecting** the problem (a missing object, an invalid form, a crashed query),
2. **Responding** with the correct status code, and
3. **Showing** the user a sensible page instead of a stack trace.

### 1.1 The Request–Response Cycle and its Failure Points

```text
Browser
   │  GET /blog/post/99/
   ▼
WSGI / ASGI server
   │
   ▼
Middleware (request phase) ───────────► DisallowedHost (400), SuspiciousOperation (400)
   │
   ▼
URL resolver (urls.py) ───────────────► Resolver404 → 404
   │
   ▼
View function ────────────────────────► Http404 (404), PermissionDenied (403),
   │                                     any uncaught Python exception → 500
   ▼
Model / ORM ──────────────────────────► DoesNotExist, MultipleObjectsReturned,
   │                                     IntegrityError → 500 if uncaught
   ▼
Template rendering ───────────────────► TemplateDoesNotExist, TemplateSyntaxError,
   │                                     NoReverseMatch → 500
   ▼
Middleware (response phase)
   │
   ▼
HttpResponse (status code) ──────────► Browser
```

### 1.2 The Three Ways to Handle an Error

| Approach | What you write | What the user sees | Best for |
|----------|----------------|--------------------|----------|
| **`HttpResponse` subclass** | `return HttpResponseNotFound("...")` | Exactly the body you wrote | APIs, quick checks, plain-text/JSON replies |
| **Raise an exception** | `raise Http404("...")` | The matching error **template** | Normal web pages — Django picks the handler |
| **`render()` with a status** | `render(request, 'x.html', status=404)` | Your template, with full context | Styled error pages that still need context data |

All three are covered in detail below.

---

## 2. HTTP Status Codes — Complete Reference

A status code is a three-digit number in the response's first line. The **first digit** defines the class.

| Class | Range | Meaning | Is it an error? |
|-------|-------|---------|-----------------|
| **1xx** | 100–199 | Informational — request received, continuing | No |
| **2xx** | 200–299 | Success — request received, understood, accepted | No |
| **3xx** | 300–399 | Redirection — further action needed | No |
| **4xx** | 400–499 | **Client error** — the request was wrong | Yes |
| **5xx** | 500–599 | **Server error** — the server failed | Yes |

### 2.1 1xx — Informational

| Code | Name | Meaning |
|------|------|---------|
| 100 | Continue | Client may continue sending the request body |
| 101 | Switching Protocols | Server is switching protocol (e.g. to WebSocket) |
| 102 | Processing | Server accepted the request but is still working (WebDAV) |
| 103 | Early Hints | Preload hints sent before the final response |

### 2.2 2xx — Success

| Code | Name | Meaning / Typical Django use |
|------|------|------------------------------|
| **200** | **OK** | The normal success response — what `render()` returns |
| **201** | **Created** | A resource was created (`POST` to an API) |
| 202 | Accepted | Accepted for processing, not finished (background task) |
| 203 | Non-Authoritative Information | Response modified by a proxy |
| **204** | **No Content** | Success, but nothing to return (`DELETE`, AJAX save) |
| 205 | Reset Content | Tells the client to clear the form |
| **206** | **Partial Content** | Range request — video streaming, resumable downloads |
| 207 | Multi-Status | Multiple independent statuses (WebDAV) |
| 208 | Already Reported | Member already enumerated (WebDAV) |
| 226 | IM Used | Result of one or more instance manipulations |

### 2.3 3xx — Redirection

| Code | Name | Meaning / Django class |
|------|------|------------------------|
| 300 | Multiple Choices | Several possible responses |
| **301** | **Moved Permanently** | `HttpResponsePermanentRedirect`, `redirect(..., permanent=True)` |
| **302** | **Found (Temporary Redirect)** | `HttpResponseRedirect`, `redirect()` — Django's default |
| 303 | See Other | Redirect after POST, forcing a GET |
| **304** | **Not Modified** | `HttpResponseNotModified` — cached copy is still valid |
| 305 | Use Proxy | Deprecated |
| 307 | Temporary Redirect | Like 302 but the HTTP method must not change |
| 308 | Permanent Redirect | Like 301 but the HTTP method must not change |

### 2.4 4xx — Client Errors

| Code | Name | Meaning / Django trigger |
|------|------|--------------------------|
| **400** | **Bad Request** | `HttpResponseBadRequest`, `BadRequest`, `SuspiciousOperation`, bad `ALLOWED_HOSTS` |
| **401** | **Unauthorized** | Authentication required and missing/invalid (needs `WWW-Authenticate`) |
| 402 | Payment Required | Reserved for future/commercial use |
| **403** | **Forbidden** | `HttpResponseForbidden`, `PermissionDenied`, CSRF failure |
| **404** | **Not Found** | `Http404`, `get_object_or_404`, no matching URL pattern |
| **405** | **Method Not Allowed** | `HttpResponseNotAllowed`, `@require_POST` on a GET request |
| 406 | Not Acceptable | No representation matches the `Accept` header |
| 407 | Proxy Authentication Required | Proxy needs credentials |
| 408 | Request Timeout | Client took too long to send the request |
| **409** | **Conflict** | State conflict — e.g. duplicate unique field |
| **410** | **Gone** | `HttpResponseGone` — resource deliberately removed, permanent |
| 411 | Length Required | `Content-Length` header missing |
| 412 | Precondition Failed | A conditional header failed |
| **413** | **Payload Too Large** | `RequestDataTooBig` — exceeds `DATA_UPLOAD_MAX_MEMORY_SIZE` |
| 414 | URI Too Long | The URL is longer than the server accepts |
| **415** | **Unsupported Media Type** | Wrong `Content-Type` on upload |
| 416 | Range Not Satisfiable | Requested byte range is invalid |
| 417 | Expectation Failed | `Expect` header cannot be met |
| 418 | I'm a teapot | April Fools' joke code (RFC 2324) |
| 421 | Misdirected Request | Request sent to the wrong server |
| **422** | **Unprocessable Content** | Syntactically valid but semantically wrong — common for validation errors in APIs |
| 423 | Locked | The resource is locked (WebDAV) |
| 424 | Failed Dependency | A previous request failed (WebDAV) |
| 425 | Too Early | Server refuses to risk replaying the request |
| 426 | Upgrade Required | Client must switch protocol |
| 428 | Precondition Required | Server requires a conditional request |
| **429** | **Too Many Requests** | Rate limiting / throttling |
| 431 | Request Header Fields Too Large | Headers exceed the server limit |
| 451 | Unavailable For Legal Reasons | Blocked due to a legal demand |

### 2.5 5xx — Server Errors

| Code | Name | Meaning / Django trigger |
|------|------|--------------------------|
| **500** | **Internal Server Error** | Any uncaught exception in a view, template or model |
| **501** | **Not Implemented** | The server does not support the requested functionality |
| **502** | **Bad Gateway** | Nginx/Apache cannot reach Gunicorn/uWSGI |
| **503** | **Service Unavailable** | Server down for maintenance or overloaded |
| **504** | **Gateway Timeout** | Upstream server did not respond in time |
| 505 | HTTP Version Not Supported | Protocol version unsupported |
| 506 | Variant Also Negotiates | Bad content-negotiation configuration |
| 507 | Insufficient Storage | Server out of storage (WebDAV) |
| 508 | Loop Detected | Infinite loop while processing (WebDAV) |
| 510 | Not Extended | Further extensions required |
| 511 | Network Authentication Required | Captive portal — log in to the network first |

### 2.6 Reading and Setting the Status Code

```python
from django.http import HttpResponse, JsonResponse
from http import HTTPStatus            # standard-library constants


def demo(request):
    response = HttpResponse("Created successfully", status=201)
    print(response.status_code)        # 201
    return response


def demo_with_constants(request):
    # Readable and self-documenting — preferred in larger projects
    return JsonResponse({'detail': 'Not found'}, status=HTTPStatus.NOT_FOUND)   # 404
```

Useful `HTTPStatus` members: `HTTPStatus.OK` (200), `CREATED` (201), `NO_CONTENT` (204), `MOVED_PERMANENTLY` (301), `FOUND` (302), `BAD_REQUEST` (400), `UNAUTHORIZED` (401), `FORBIDDEN` (403), `NOT_FOUND` (404), `METHOD_NOT_ALLOWED` (405), `CONFLICT` (409), `GONE` (410), `TOO_MANY_REQUESTS` (429), `INTERNAL_SERVER_ERROR` (500), `SERVICE_UNAVAILABLE` (503).

In tests:

```python
response = self.client.get('/blog/post/999/')
self.assertEqual(response.status_code, 404)
```

---

## 3. Types of Errors in Django (Exception Names)

Django defines its own exception hierarchy. Knowing the **name**, the **module it lives in** and the **status code it produces** is the core of error handling.

### 3.1 HTTP-Level Exceptions

| Exception | Import from | Resulting status | Raised when |
|-----------|-------------|------------------|-------------|
| `Http404` | `django.http` | **404** | A requested object or page does not exist |
| `PermissionDenied` | `django.core.exceptions` | **403** | The user is not allowed to perform the action |
| `BadRequest` | `django.core.exceptions` | **400** | The request is malformed (Django 3.2+) |
| `SuspiciousOperation` | `django.core.exceptions` | **400** | The user did something security-suspicious |
| `Resolver404` | `django.urls` | **404** | The URL resolver found no matching pattern (subclass of `Http404`) |
| `ViewDoesNotExist` | `django.core.exceptions` | 500 | A URLconf points to a view that cannot be imported |
| `RequestAborted` | `django.core.exceptions` | — | The client disconnected mid-request |

**`SuspiciousOperation` subclasses** (each one also produces **400**, and Django logs it to `django.security`):

| Subclass | Cause |
|----------|-------|
| `DisallowedHost` | The `Host` header is not in `ALLOWED_HOSTS` |
| `DisallowedRedirect` | Redirect to an unsafe scheme |
| `RequestDataTooBig` | POST body larger than `DATA_UPLOAD_MAX_MEMORY_SIZE` (→ **413** in some servers) |
| `TooManyFieldsSent` | More form fields than `DATA_UPLOAD_MAX_NUMBER_FIELDS` |
| `SuspiciousFileOperation` | A file path outside the allowed directory |
| `SuspiciousMultipartForm` | Malformed multipart/form-data |
| `SuspiciousSession` | The session was tampered with |

```python
from django.http import Http404
from django.core.exceptions import PermissionDenied, BadRequest


def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise Http404("No post found with id %s" % pk)

    if not post.is_published and not request.user.is_staff:
        raise PermissionDenied("This post is still a draft.")

    return render(request, 'blog/post_detail.html', {'post': post})


def archive(request):
    year = request.GET.get('year')
    if year and not year.isdigit():
        raise BadRequest("Year must be numeric.")
    ...
```

### 3.2 Model and ORM Exceptions

| Exception | Import from | Raised when |
|-----------|-------------|-------------|
| `ObjectDoesNotExist` | `django.core.exceptions` | Base class for every model's `DoesNotExist` |
| `Model.DoesNotExist` | auto-created on each model | `.get()` matched no row (e.g. `Post.DoesNotExist`) |
| `MultipleObjectsReturned` | `django.core.exceptions` / on the model | `.get()` matched more than one row |
| `ValidationError` | `django.core.exceptions` | `full_clean()` or a form/field validator failed |
| `FieldError` | `django.core.exceptions` | Invalid field name in `filter()`, `order_by()` etc. |
| `FieldDoesNotExist` | `django.core.exceptions` | The requested field is not on the model |
| `EmptyResultSet` | `django.core.exceptions` | A query can never return any rows |
| `AppRegistryNotReady` | `django.core.exceptions` | Models used before the app registry is loaded |
| `SynchronousOnlyOperation` | `django.core.exceptions` | Sync ORM code called from async context |

**Database-layer exceptions** (`django.db`), all wrapping the DB driver's own errors:

| Exception | Raised when |
|-----------|-------------|
| `Error` | Base class for all database errors |
| `DatabaseError` | General database failure |
| `IntegrityError` | Unique / foreign-key / not-null constraint violated |
| `DataError` | Value out of range or wrong type for the column |
| `OperationalError` | Connection lost, table locked, disk full |
| `ProgrammingError` | Table or column missing, SQL syntax error |
| `InterfaceError` | Problem with the database interface itself |
| `NotSupportedError` | Feature unsupported by this backend |
| `TransactionManagementError` | Illegal operation inside an atomic block |

```python
from django.core.exceptions import MultipleObjectsReturned, ValidationError
from django.db import IntegrityError


def add_post(request):
    try:
        post = Post.objects.create(title=request.POST['title'],
                                   slug=request.POST['slug'])
    except IntegrityError:
        return HttpResponse("A post with this slug already exists.", status=409)
    except KeyError:                      # MultiValueDictKeyError is a KeyError
        return HttpResponseBadRequest("Both title and slug are required.")

    try:
        post.full_clean()                 # runs model validators
    except ValidationError as e:
        return HttpResponseBadRequest(e.message_dict)

    return redirect('blog:post_detail', pk=post.pk)


def author_profile(request, name):
    try:
        author = Author.objects.get(name=name)
    except Author.DoesNotExist:
        raise Http404("Author not found.")
    except MultipleObjectsReturned:
        author = Author.objects.filter(name=name).first()
    ...
```

### 3.3 Template Exceptions

| Exception | Import from | Raised when |
|-----------|-------------|-------------|
| `TemplateDoesNotExist` | `django.template` | The template file was not found in any configured directory |
| `TemplateSyntaxError` | `django.template` | Invalid DTL — unclosed `{% if %}`, unknown tag, missing `{% load %}` |
| `TemplateEncodingError` | `django.template` | The template is not valid UTF-8 |
| `VariableDoesNotExist` | `django.template.base` | Internal — normally silenced into an empty string |
| `UnicodeDecodeError` | built-in | Non-UTF-8 bytes while rendering |

All of these become **500** if they reach the browser, because they mean the *developer* made a mistake, not the user.

### 3.4 URL / Routing Exceptions

| Exception | Import from | Raised when |
|-----------|-------------|-------------|
| `Resolver404` | `django.urls` | No URL pattern matched — becomes a 404 |
| `NoReverseMatch` | `django.urls` | `{% url %}` or `reverse()` could not build a URL (wrong name or wrong number of arguments) |
| `ViewDoesNotExist` | `django.core.exceptions` | The view named in `urls.py` cannot be imported |

`NoReverseMatch` is one of the most common errors in template work:

```text
NoReverseMatch: Reverse for 'post_detail' with arguments '()' not found.
1 pattern(s) tried: ['blog/post/(?P<pk>[0-9]+)/$']
```

Cause: `{% url 'blog:post_detail' %}` was written without the required `pk`. Fix: `{% url 'blog:post_detail' post.pk %}`.

### 3.5 Configuration and Setup Exceptions

| Exception | Import from | Raised when |
|-----------|-------------|-------------|
| `ImproperlyConfigured` | `django.core.exceptions` | A setting is missing or wrong (no `SECRET_KEY`, bad `DATABASES`, `DIRS` misconfigured) |
| `MiddlewareNotUsed` | `django.core.exceptions` | A middleware opts out of the chain (not an error) |
| `FieldError` | `django.core.exceptions` | Invalid field reference in a query |
| `AppRegistryNotReady` | `django.core.exceptions` | Models imported too early (e.g. at module level in `apps.py`) |

### 3.6 Python Built-in Errors You Will Meet in Django

| Exception | Typical Django cause |
|-----------|----------------------|
| `MultiValueDictKeyError` | `request.POST['key']` when the key is absent — use `.get('key', default)` |
| `KeyError` | Missing dictionary key in a context or session |
| `AttributeError` | `'NoneType' object has no attribute ...` — a query returned `None` |
| `TypeError` | Wrong number of arguments to a view (URL parameter mismatch) |
| `ValueError` | `int('abc')` while converting a query parameter |
| `ImportError` | Wrong module path in `INSTALLED_APPS` or `urls.py` |
| `ZeroDivisionError` | Computing an average over an empty queryset |

### 3.7 Master Mapping — Exception to Status Code

| Raised exception | Handler called | Status | Template rendered |
|------------------|----------------|--------|-------------------|
| `Http404` / `Resolver404` | `handler404` | 404 | `404.html` |
| `PermissionDenied` | `handler403` | 403 | `403.html` |
| `SuspiciousOperation` / `BadRequest` | `handler400` | 400 | `400.html` |
| CSRF verification failure | `CSRF_FAILURE_VIEW` | 403 | `403_csrf.html` |
| Any other uncaught exception | `handler500` | 500 | `500.html` |

Django's default handler views live in `django.views.defaults`:

| Handler variable | Default view | Signature |
|------------------|--------------|-----------|
| `handler400` | `django.views.defaults.bad_request` | `(request, exception)` |
| `handler403` | `django.views.defaults.permission_denied` | `(request, exception)` |
| `handler404` | `django.views.defaults.page_not_found` | `(request, exception)` |
| `handler500` | `django.views.defaults.server_error` | `(request)` — **no exception argument** |

---

## 4. Error Handling using `HttpResponse`

`HttpResponse` lets you return **any** status code with **any** body. This is the most direct form of error handling.

### 4.1 `HttpResponse` with an Explicit Status

```python
from django.http import HttpResponse


def check_age(request):
    age = request.GET.get('age')

    if age is None:
        return HttpResponse("Query parameter 'age' is required.", status=400)

    if not age.isdigit():
        return HttpResponse("'age' must be a number.", status=400)

    if int(age) < 18:
        return HttpResponse("Access denied for minors.", status=403)

    return HttpResponse("Welcome!", status=200)
```

You may also set the content type and extra headers:

```python
response = HttpResponse("Resource removed", status=410, content_type='text/plain')
response['X-Error-Reason'] = 'archived'
response.status_code = 410          # can also be assigned after creation
return response
```

### 4.2 Specialised `HttpResponse` Subclasses

All live in `django.http`. Each one hard-codes a status code so you never have to remember the number.

| Class | Status | Constructor notes |
|-------|--------|-------------------|
| `HttpResponse` | 200 (default) | Any status via `status=` |
| `HttpResponseRedirect(url)` | **302** | Temporary redirect |
| `HttpResponsePermanentRedirect(url)` | **301** | Permanent redirect |
| `HttpResponseNotModified()` | **304** | Must have **no** body |
| `HttpResponseBadRequest()` | **400** | Malformed request |
| `HttpResponseForbidden()` | **403** | Authenticated but not allowed |
| `HttpResponseNotFound()` | **404** | Resource missing |
| `HttpResponseNotAllowed(['GET'])` | **405** | **List of permitted methods is mandatory** |
| `HttpResponseGone()` | **410** | Resource permanently removed |
| `HttpResponseServerError()` | **500** | Server-side failure |
| `JsonResponse(dict, status=...)` | 200 by default | Serialises a dict to JSON |
| `FileResponse(open(f, 'rb'))` | 200 | Streams a file |
| `HttpResponseNotAcceptable` *(not built-in)* | 406 | Use `HttpResponse(status=406)` |

### 4.3 Worked Examples of Each

```python
from django.http import (
    HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect,
    HttpResponseNotModified, HttpResponseBadRequest, HttpResponseForbidden,
    HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseGone,
    HttpResponseServerError, JsonResponse,
)
from django.shortcuts import redirect
from .models import Post


# 400 — the client sent something invalid
def search(request):
    q = request.GET.get('q', '')
    if len(q) > 100:
        return HttpResponseBadRequest("Search term is too long (max 100 chars).")
    ...


# 403 — the user is not allowed
def edit_post(request, pk):
    post = Post.objects.get(pk=pk)
    if post.author != request.user.username:
        return HttpResponseForbidden("<h1>403 Forbidden</h1><p>You cannot edit this post.</p>")
    ...


# 404 — resource does not exist
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponseNotFound(f"<h1>404</h1><p>Post {pk} does not exist.</p>")
    return render(request, 'blog/post_detail.html', {'post': post})


# 405 — wrong HTTP method; the allowed list is REQUIRED
def create_post(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])     # sets the Allow header too
    ...


# 410 — deliberately removed, do not come back
def old_api(request):
    return HttpResponseGone("The v1 API was retired on 01-Jan-2026. Use /api/v2/.")


# 500 — server-side failure handled gracefully
def report(request):
    try:
        data = build_expensive_report()
    except Exception:
        return HttpResponseServerError("Report generation failed. Try again later.")
    return HttpResponse(data)


# 301 / 302 — redirects
def moved(request):
    return HttpResponsePermanentRedirect('/blog/')          # 301
def after_save(request):
    return HttpResponseRedirect('/blog/')                   # 302
def shortcut(request):
    return redirect('blog:post_list')                       # 302 via URL name
    # return redirect('blog:post_list', permanent=True)     # 301
```

### 4.4 `JsonResponse` for API-Style Errors

```python
from django.http import JsonResponse


def api_post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse(
            {'error': 'not_found', 'detail': f'Post {pk} does not exist.'},
            status=404,
        )

    if not post.is_published:
        return JsonResponse({'error': 'forbidden', 'detail': 'Draft post.'}, status=403)

    return JsonResponse({
        'id': post.pk,
        'title': post.title,
        'author': post.author,
    }, status=200)
```

A reusable helper keeps API errors consistent:

```python
def api_error(code, message, status):
    return JsonResponse({'error': code, 'message': message, 'status': status},
                        status=status)

# usage
return api_error('invalid_page', 'Page must be a positive integer.', 400)
```

### 4.5 `HttpResponseNotFound` vs `raise Http404`

| | `return HttpResponseNotFound("...")` | `raise Http404("...")` |
|---|---|---|
| Status sent | 404 | 404 |
| Page shown | **Exactly your string** | Your **`404.html` template** (or the debug page) |
| `handler404` called | No | Yes |
| Works with middleware error hooks | No | Yes |
| Best for | APIs, plain-text replies | Normal HTML pages |

```python
# Recommended for HTML pages — consistent, styled 404 page for the whole site
from django.http import Http404

def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise Http404("Post not found")
    ...
```

### 4.6 The `get_object_or_404` Shortcut

```python
from django.shortcuts import get_object_or_404, get_list_or_404

def post_detail(request, pk):
    # Equivalent to the try/except above, in one line
    post = get_object_or_404(Post, pk=pk, is_published=True)
    return render(request, 'blog/post_detail.html', {'post': post})


def category_posts(request, category):
    # Raises Http404 if the list is EMPTY
    posts = get_list_or_404(Post, category=category)
    return render(request, 'blog/by_category.html', {'posts': posts})
```

| Shortcut | Raises 404 when |
|----------|-----------------|
| `get_object_or_404(Model, **kwargs)` | `DoesNotExist` (still raises `MultipleObjectsReturned` → 500) |
| `get_list_or_404(Model, **kwargs)` | The resulting list is empty |
| `Model.objects.filter(...).first()` | Never — returns `None`, you must check it yourself |

---

## 5. Error Handling using Templates (Custom Error Pages)

Instead of plain text, Django can render a **template** for each error class, so error pages match the site's design.

### 5.1 The Four Special Templates

Place them in a directory listed in `TEMPLATES['DIRS']` — normally the project-level `templates/` folder, at the **top level** (not inside a subfolder).

```text
myproject/
└── templates/
    ├── base.html
    ├── 400.html        ← Bad Request
    ├── 403.html        ← Forbidden
    ├── 403_csrf.html   ← CSRF verification failed (optional)
    ├── 404.html        ← Not Found
    └── 500.html        ← Internal Server Error
```

Django finds these **automatically by filename** — no URL entry and no view is needed for the default behaviour.

### 5.2 Writing the Templates

**`templates/404.html`**

```html
{% extends "base.html" %}
{% load static %}

{% block title %}404 — Page Not Found{% endblock %}

{% block content %}
<div class="error-page">
    <img src="{% static 'images/404.svg' %}" alt="Not found" width="220">

    <h1>404</h1>
    <h2>We couldn't find that page</h2>

    {# 'request_path' is supplied by Django's default 404 view #}
    <p>The address <code>{{ request_path }}</code> does not exist on this site.</p>

    {% if exception %}
        <p class="detail">{{ exception }}</p>
    {% endif %}

    <a class="btn" href="{% url 'blog:post_list' %}">Go to the blog home</a>
    <a class="btn" href="{% url 'blog:search' %}">Search instead</a>
</div>
{% endblock %}
```

**`templates/403.html`**

```html
{% extends "base.html" %}

{% block title %}403 — Forbidden{% endblock %}

{% block content %}
    <h1>403</h1>
    <h2>You don't have permission to view this page</h2>

    {% if exception %}<p>{{ exception }}</p>{% endif %}

    {% if not user.is_authenticated %}
        <a href="{% url 'login' %}?next={{ request.path }}">Log in to continue</a>
    {% else %}
        <p>Logged in as {{ user.username }}, but this area needs higher privileges.</p>
    {% endif %}
{% endblock %}
```

**`templates/400.html`**

```html
{% extends "base.html" %}

{% block title %}400 — Bad Request{% endblock %}

{% block content %}
    <h1>400</h1>
    <h2>Your browser sent a request this server could not understand</h2>
    <p>Please check the address and try again.</p>
    <a href="{% url 'blog:post_list' %}">Back to home</a>
{% endblock %}
```

**`templates/500.html` — the important exception to the rules**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>500 — Server Error</title>
    <style>
        body { font-family: system-ui, sans-serif; text-align: center; padding: 6rem 1rem; }
        h1   { font-size: 5rem; margin: 0; color: #dc3545; }
        a    { color: #0d6efd; }
    </style>
</head>
<body>
    <h1>500</h1>
    <h2>Something went wrong on our side</h2>
    <p>The problem has been logged and our team has been notified.</p>
    <a href="/">Return to the home page</a>
</body>
</html>
```

> **Critical rule for `500.html`:** it is rendered with an **empty context** and **no context processors**. `{{ user }}`, `{{ request }}` and `{% url %}` may not work, and if the error was caused by `base.html` itself, `{% extends %}` would fail again — producing a second 500. Keep `500.html` completely **self-contained**: plain HTML, inline CSS, hard-coded links.

### 5.3 Custom Handler Views

When you need extra logic — logging, suggesting similar pages, returning JSON for API paths — write your own handler views and register them in the **root** URLconf.

**`blog/views.py`**

```python
from django.shortcuts import render
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)


def custom_400(request, exception):
    return render(request, '400.html', {'exception': exception}, status=400)


def custom_403(request, exception):
    logger.warning('403 for %s on %s', request.user, request.path)
    return render(request, '403.html', {'exception': exception}, status=403)


def custom_404(request, exception):
    # API paths get JSON, HTML pages get the template
    if request.path.startswith('/api/'):
        return JsonResponse({'error': 'not_found', 'path': request.path}, status=404)

    context = {
        'request_path': request.path,
        'exception': str(exception),
        'suggestions': Post.objects.filter(is_published=True)[:5],
    }
    return render(request, '404.html', context, status=404)


def custom_500(request):                 # NOTE: no 'exception' argument
    logger.error('500 error on %s', request.path, exc_info=True)
    return render(request, '500.html', status=500)
```

**`myproject/urls.py` — registration must be at module level in the ROOT URLconf**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
]

# Custom error handlers — string paths to the view functions
handler400 = 'blog.views.custom_400'
handler403 = 'blog.views.custom_403'
handler404 = 'blog.views.custom_404'
handler500 = 'blog.views.custom_500'
```

| Handler | Signature | Status to return |
|---------|-----------|------------------|
| `handler400` | `def view(request, exception)` | 400 |
| `handler403` | `def view(request, exception)` | 403 |
| `handler404` | `def view(request, exception)` | 404 |
| `handler500` | `def view(request)` | 500 |

> Two frequent mistakes: (1) forgetting `status=404` in `render()`, which sends a 404 page with a **200** status and confuses search engines; (2) giving `custom_500` an `exception` parameter, which raises `TypeError` at error time.

### 5.4 Requirements for Custom Error Pages to Appear

Custom templates are used **only when `DEBUG = False`**. To test them on your development machine:

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']     # mandatory once DEBUG is False
```

```bash
# --insecure makes runserver keep serving /static/ even with DEBUG = False
python manage.py runserver --insecure
```

Checklist when a custom page does not show up:

1. `DEBUG = False`?
2. Is the template directly inside a folder listed in `TEMPLATES['DIRS']`?
3. Is the filename exactly `404.html` (not `404.HTML`, not `errors/404.html`)?
4. Was the server restarted?
5. Does `500.html` itself contain an error (`{% extends %}`, `{% url %}`, missing static file)?

### 5.5 Rendering an Error Template Manually with `render(..., status=)`

You do not have to raise an exception at all. This pattern keeps the full context available:

```python
def post_detail(request, pk):
    post = Post.objects.filter(pk=pk).first()

    if post is None:
        return render(request, 'blog/post_not_found.html',
                      {'pk': pk, 'popular': Post.objects.all()[:5]},
                      status=404)

    if not post.is_published and not request.user.is_staff:
        return render(request, 'blog/draft_locked.html', {'post': post}, status=403)

    return render(request, 'blog/post_detail.html', {'post': post})
```

This works **even when `DEBUG = True`**, which makes it convenient during development.

### 5.6 The CSRF Failure Page

A failed CSRF check does **not** go through `handler403`. Django renders `403_csrf.html` if it exists, otherwise a built-in page.

```python
# settings.py — optional custom view
CSRF_FAILURE_VIEW = 'blog.views.csrf_failure'
```

```python
def csrf_failure(request, reason=""):
    return render(request, '403_csrf.html', {'reason': reason}, status=403)
```

```html
<!-- templates/403_csrf.html -->
<h1>403 — CSRF Verification Failed</h1>
<p>Reason: {{ reason }}</p>
<p>Your session may have expired. Please reload the form and submit again.</p>
```

---

## 6. `DEBUG = True` — The Technical Error Page

### 6.1 What `DEBUG = True` Changes

```python
# settings.py
DEBUG = True
ALLOWED_HOSTS = []          # any host is accepted while DEBUG is True
```

| Behaviour | `DEBUG = True` | `DEBUG = False` |
|-----------|----------------|-----------------|
| Uncaught exception | Yellow **technical 500 page** with full traceback | Renders `500.html` |
| `Http404` raised | Technical **404 page** listing every URL pattern tried | Renders `404.html` |
| `PermissionDenied` | Plain 403 page | Renders `403.html` |
| Custom error templates | **Ignored** | Used |
| Static files via `runserver` | Served automatically | Not served (needs `--insecure` or a real web server) |
| SQL queries | Stored in `connection.queries` | Not stored |
| `ALLOWED_HOSTS` | Effectively ignored | **Enforced** — wrong host → 400 |
| Error e-mails to `ADMINS` | Not sent | Sent |
| Sensitive data exposure | **High — settings, secrets, local variables** | None |

> **Security rule:** `DEBUG = True` in production leaks `SECRET_KEY`, database credentials, file paths, environment variables and every local variable at the point of failure. It is the single most common Django security mistake. Always drive it from the environment:
>
> ```python
> import os
> DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'
> ```

### 6.2 Anatomy of the Technical 500 Page

When an exception escapes a view with `DEBUG = True`, Django shows a detailed diagnostic page:

| Section | What it contains |
|---------|------------------|
| **Header** | Exception type (e.g. `ValueError`), exception value, the request URL and the Django version |
| **Traceback** | Every frame from the WSGI entry point down to the failing line; the failing line is highlighted |
| **Local vars** | Click any frame to expand the local variables at that moment — the most useful part |
| **Request information — GET** | All query parameters |
| **Request information — POST** | All submitted form data |
| **FILES** | Uploaded files |
| **COOKIES** | Every cookie, including the session id |
| **META** | All WSGI/HTTP headers |
| **Settings** | Your full settings module, with sensitive keys masked as `********` |
| **"Switch to copy-and-paste view"** | A plain-text traceback you can paste into a bug report |

A typical exception header reads:

```text
ValueError at /blog/archive/2026/13/
month must be in 1..12
Request Method: GET
Request URL:    http://127.0.0.1:8000/blog/archive/2026/13/
Django Version: 5.0.6
Exception Type: ValueError
Exception Value: month must be in 1..12
Exception Location: /myproject/blog/views.py, line 42, in archive
```

### 6.3 The Technical 404 Page

With `DEBUG = True`, an unmatched URL shows which patterns Django tried, in order:

```text
Page not found (404)
Request Method: GET
Request URL: http://127.0.0.1:8000/blog/pst/1/

Using the URLconf defined in myproject.urls, Django tried these URL patterns, in this order:

  1. admin/
  2. blog/ [name='post_list']
  3. blog/ post/<int:pk>/ [name='post_detail']
  4. blog/ category/<str:category>/ [name='by_category']
  5. blog/ search/ [name='search']

The current path, blog/pst/1/, didn't match any of these.
```

This listing is the fastest way to debug a URL typo, a missing trailing slash or a wrong converter.

### 6.4 Hiding Sensitive Data on the Debug Page

Django masks anything whose name looks like a secret. You can extend this:

```python
from django.views.decorators.debug import sensitive_variables, sensitive_post_parameters


@sensitive_variables('password', 'otp', 'card_number')
def process_payment(request, card_number, otp):
    ...


@sensitive_post_parameters('password', 'confirm_password')
def register(request):
    ...
```

Masked values appear as `********************` in the traceback and in error e-mails.

### 6.5 Related Debug Settings

| Setting | Effect |
|---------|--------|
| `DEBUG` | Master switch for the technical error pages |
| `DEBUG_PROPAGATE_EXCEPTIONS = True` | Do not convert exceptions into 500 responses — let them crash upward (useful in tests) |
| `ADMINS` | Recipients of the 500 error e-mails when `DEBUG = False` |
| `MANAGERS` | Recipients of broken-link (404) e-mails |
| `IGNORABLE_404_URLS` | Regexes of 404s not worth reporting (`favicon.ico`, `robots.txt`) |
| `INTERNAL_IPS` | IPs that see extra debug information (and the Debug Toolbar) |
| `SILENCED_SYSTEM_CHECKS` | Suppress specific `manage.py check` warnings |

```python
import re

ADMINS = [('Course Admin', 'admin@example.com')]
MANAGERS = ADMINS
IGNORABLE_404_URLS = [
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/robots\.txt$'),
]
```

---

## 7. Practical Error-Handling Patterns in Views

### 7.1 `try` / `except` / `else` / `finally`

```python
from django.shortcuts import render
from django.http import Http404, HttpResponseBadRequest
from django.db import DatabaseError
import logging

logger = logging.getLogger(__name__)


def archive(request, year, month):
    try:
        year, month = int(year), int(month)
        if not 1 <= month <= 12:
            return HttpResponseBadRequest("Month must be between 1 and 12.")

        posts = Post.objects.filter(published_date__year=year,
                                    published_date__month=month)
        if not posts.exists():
            raise Http404(f"No posts published in {month}/{year}.")

    except ValueError:
        return HttpResponseBadRequest("Year and month must be numbers.")

    except DatabaseError as exc:
        logger.error('DB failure in archive view: %s', exc, exc_info=True)
        return render(request, '500.html', status=500)

    else:
        return render(request, 'blog/archive.html',
                      {'posts': posts, 'year': year, 'month': month})

    finally:
        logger.debug('archive view finished for %s/%s', month, year)
```

**Order matters:** put the most specific exception first. `except Exception` last (or not at all) — a bare `except:` also swallows `KeyboardInterrupt` and `SystemExit`.

### 7.2 Validating Query Parameters Safely

```python
def post_list(request):
    # BAD  — MultiValueDictKeyError if 'page' is absent
    # page = request.GET['page']

    # GOOD — default supplied, then validated
    raw_page = request.GET.get('page', '1')

    if not raw_page.isdigit() or int(raw_page) < 1:
        return HttpResponseBadRequest("'page' must be a positive integer.")

    page = int(raw_page)
    ...
```

### 7.3 Restricting HTTP Methods (405)

```python
from django.views.decorators.http import require_http_methods, require_POST, require_GET


@require_POST                                  # GET → automatic 405
def create_post(request):
    ...


@require_http_methods(["GET", "POST"])         # PUT/DELETE → automatic 405
def edit_post(request, pk):
    ...
```

### 7.4 Permission Checks (403)

```python
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied


@login_required                                  # not logged in → redirect to login
def dashboard(request):
    ...


@permission_required('blog.add_post', raise_exception=True)   # → 403 instead of redirect
def create_post(request):
    ...


def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user.username:
        raise PermissionDenied("You can only delete your own posts.")
    post.delete()
    return redirect('blog:post_list')
```

### 7.5 Form Validation Errors (not HTTP errors)

A failing form is **not** a 404 or 500 — re-render the page with the errors, usually with status 200 (or 400 for APIs).

```python
from django import forms
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise ValidationError("Title must be at least 5 characters long.")
        if Post.objects.filter(title__iexact=title).exists():
            raise ValidationError("A post with this title already exists.")
        return title


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:post_list')
        # invalid → fall through and re-render with form.errors populated
    else:
        form = PostForm()

    return render(request, 'blog/post_form.html', {'form': form})
```

```html
{# blog/post_form.html #}
<form method="post" novalidate>
    {% csrf_token %}

    {% if form.non_field_errors %}
        <div class="alert alert-danger">
            {% for error in form.non_field_errors %}<p>{{ error }}</p>{% endfor %}
        </div>
    {% endif %}

    {% for field in form %}
        <div class="field">
            {{ field.label_tag }}
            {{ field }}
            {% if field.errors %}
                <ul class="errors">
                    {% for error in field.errors %}<li>{{ error }}</li>{% endfor %}
                </ul>
            {% endif %}
            {% if field.help_text %}<small>{{ field.help_text }}</small>{% endif %}
        </div>
    {% endfor %}

    <button type="submit">Save</button>
</form>
```

### 7.6 The Messages Framework for User-Facing Notices

```python
from django.contrib import messages


def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    try:
        post.delete()
        messages.success(request, f'"{post.title}" was deleted.')
    except Exception:
        messages.error(request, 'The post could not be deleted. Please try again.')
    return redirect('blog:post_list')
```

```html
{# in base.html #}
{% if messages %}
    <div class="messages">
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">{{ message }}</div>
        {% endfor %}
    </div>
{% endif %}
```

Levels: `debug`, `info`, `success`, `warning`, `error`.

---

## 8. Logging, Middleware and Admin E-mail Reports

### 8.1 Logging Configuration

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'verbose'},
        'error_file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/errors.log',
            'level': 'ERROR',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            'include_html': True,
        },
    },
    'loggers': {
        'django.request': {                     # 4xx and 5xx responses
            'handlers': ['console', 'error_file', 'mail_admins'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.security': {                    # SuspiciousOperation subclasses
            'handlers': ['error_file'],
            'level': 'WARNING',
        },
        'blog': {
            'handlers': ['console', 'error_file'],
            'level': 'DEBUG',
        },
    },
}
```

| Logger | Logs |
|--------|------|
| `django.request` | 5xx as `ERROR`, 4xx as `WARNING` |
| `django.security.*` | Each `SuspiciousOperation` subclass |
| `django.db.backends` | Every SQL statement (`DEBUG` level) |
| `django.template` | Missing template variables |

### 8.2 Custom Exception Middleware

`process_exception()` runs whenever a view raises an exception. Return a response to handle it, or `None` to let Django continue.

```python
# blog/middleware.py
import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.http import Http404

logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Response-phase hook — log every error status that goes out
        if response.status_code >= 400:
            logger.warning('%s returned %s', request.path, response.status_code)
        return response

    def process_exception(self, request, exception):
        # Let Django's own machinery deal with these two
        if isinstance(exception, (Http404, PermissionDenied)):
            return None

        logger.error('Unhandled %s at %s', type(exception).__name__,
                     request.path, exc_info=True)

        if request.path.startswith('/api/'):
            return JsonResponse({'error': 'server_error'}, status=500)

        return render(request, '500.html', status=500)
```

```python
# settings.py
MIDDLEWARE = [
    # ...
    'blog.middleware.ErrorHandlingMiddleware',      # usually last
]
```

### 8.3 E-mail Reports to Administrators

With `DEBUG = False`, Django e-mails the full traceback of every 500 to `ADMINS`:

```python
DEBUG = False
ADMINS = [('Rabaab', 'admin@example.com')]
SERVER_EMAIL = 'django@example.com'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'you@example.com'
EMAIL_HOST_PASSWORD = 'app-password'

# During development, print e-mails to the console instead of sending them
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Broken-link (404) reports go to `MANAGERS` when `BrokenLinkEmailsMiddleware` is enabled.

---

## 9. Testing Error Handling

```python
from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse
from blog.models import Post


class ErrorStatusTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.post = Post.objects.create(title='Live Post', content='x',
                                       author='A', category='web',
                                       is_published=True)

    # ---------- 404 ----------
    def test_missing_post_returns_404(self):
        response = self.client.get(reverse('blog:post_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_unknown_url_returns_404(self):
        self.assertEqual(self.client.get('/no-such-page/').status_code, 404)

    # ---------- 400 ----------
    def test_non_numeric_age_returns_400(self):
        response = self.client.get('/blog/check-age/', {'age': 'abc'})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'must be a number', status_code=400)

    # ---------- 403 ----------
    def test_draft_post_forbidden_for_anonymous(self):
        draft = Post.objects.create(title='Draft', content='x', author='A',
                                    category='web', is_published=False)
        response = self.client.get(reverse('blog:post_detail', args=[draft.pk]))
        self.assertEqual(response.status_code, 403)

    # ---------- 405 ----------
    def test_get_on_post_only_view_returns_405(self):
        response = self.client.get(reverse('blog:post_create'))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response['Allow'], 'POST')

    # ---------- 302 ----------
    def test_successful_save_redirects(self):
        response = self.client.post(reverse('blog:post_create'),
                                    {'title': 'Valid Title', 'content': 'body',
                                     'category': 'web'})
        self.assertRedirects(response, reverse('blog:post_list'))

    # ---------- JSON errors ----------
    def test_api_404_returns_json(self):
        response = self.client.get('/api/post/9999/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'not_found')

    # ---------- form errors ----------
    def test_short_title_shows_form_error(self):
        response = self.client.post(reverse('blog:post_create'),
                                    {'title': 'Hi', 'content': 'x', 'category': 'web'})
        self.assertEqual(response.status_code, 200)     # re-rendered, not an HTTP error
        self.assertFormError(response.context['form'], 'title',
                             'Title must be at least 5 characters long.')
```

**Testing the custom error templates** (they render only when `DEBUG = False`, which is the default inside tests):

```python
from django.test import SimpleTestCase, override_settings


@override_settings(DEBUG=False, ALLOWED_HOSTS=['testserver'])
class ErrorTemplateTests(SimpleTestCase):

    def test_404_uses_custom_template(self):
        response = self.client.get('/definitely-not-a-real-page/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')
        self.assertContains(response, "couldn't find that page", status_code=404)
```

To let an exception escape so you can assert on it, use `raise_request_exception=False` or a client configured for it:

```python
class ServerErrorTests(SimpleTestCase):

    def test_view_raises_value_error(self):
        client = Client(raise_request_exception=False)
        response = client.get('/blog/crash/')
        self.assertEqual(response.status_code, 500)
```

---

## 10. Summary and Practice Questions

### 10.1 Quick Revision Table

| Situation | Correct response | Code |
|-----------|------------------|------|
| Object not in the database | `raise Http404` / `get_object_or_404` | 404 |
| URL does not match any pattern | Automatic `Resolver404` | 404 |
| Missing/invalid query parameter | `HttpResponseBadRequest` / `BadRequest` | 400 |
| User lacks permission | `PermissionDenied` / `HttpResponseForbidden` | 403 |
| CSRF token missing or wrong | `CSRF_FAILURE_VIEW` → `403_csrf.html` | 403 |
| Wrong HTTP method | `HttpResponseNotAllowed(['POST'])` / `@require_POST` | 405 |
| Duplicate unique value | Catch `IntegrityError` | 409 |
| Resource permanently removed | `HttpResponseGone` | 410 |
| Upload larger than the limit | `RequestDataTooBig` | 413 |
| Rate limit exceeded | `HttpResponse(status=429)` | 429 |
| Uncaught exception in a view | `handler500` → `500.html` | 500 |
| Form validation failed | Re-render the form with `form.errors` | 200 |
| Saved successfully, then redirect | `redirect()` | 302 |
| Permanent URL change | `redirect(..., permanent=True)` | 301 |

### 10.2 Key Rules to Remember

1. `raise Http404` renders `404.html`; `HttpResponseNotFound` returns only the string you wrote.
2. Custom error templates are used **only** when `DEBUG = False`.
3. `404.html`, `403.html`, `400.html` and `500.html` go at the **top level** of a `TEMPLATES['DIRS']` folder.
4. `500.html` receives **no context and no context processors** — keep it self-contained.
5. `handler500` takes only `request`; the other three also take `exception`.
6. Always pass `status=` to `render()` in an error view, or the page goes out as 200.
7. `ALLOWED_HOSTS` must be filled in the moment `DEBUG` becomes `False`, or every request returns 400.
8. `DEBUG = True` in production exposes secrets — drive it from an environment variable.
9. 4xx means the **client** is at fault; 5xx means the **server** is at fault.
10. A failed form is a normal 200 response, not an HTTP error.

### 10.3 Practice Questions

**Short answer (2 marks)**

1. Differentiate between a 4xx and a 5xx status code with one example each.
2. What is the difference between `raise Http404()` and `return HttpResponseNotFound()`?
3. Why must the list of allowed methods be passed to `HttpResponseNotAllowed`?
4. Name the four handler variables set in the root URLconf and the status code each produces.
5. Why should `500.html` not use `{% extends "base.html" %}`?
6. Which exception is raised by `request.POST['title']` when the key is missing, and how do you avoid it?
7. State any two risks of leaving `DEBUG = True` in production.

**Medium answer (5 marks)**

8. List and explain any eight HTTP status codes that a Django application commonly returns.
9. Explain the complete set of steps required to make a custom `404.html` appear on a development machine.
10. Classify Django's exceptions into HTTP-level, model-level and template-level, with two names in each category and the status code they map to.
11. Write a view that validates a `page` query parameter and returns 400, 404 or 200 as appropriate.
12. Compare the technical error page shown with `DEBUG = True` against the behaviour with `DEBUG = False`, in tabular form.

**Long answer (10 marks)**

13. Build a complete error-handling setup for a blog project: four custom handler views, four templates, the URLconf registration, and the settings changes needed.
14. Write a view for `/blog/post/<int:pk>/` that returns 404 for a missing post, 403 for an unpublished post viewed by a non-staff user, 200 otherwise — then write the tests that prove all three paths.
15. Explain Django's exception hierarchy: `SuspiciousOperation` and its subclasses, `ObjectDoesNotExist` and per-model `DoesNotExist`, and database errors such as `IntegrityError`. Give the status code each produces and a code example of catching it.
16. Design an API error-response format using `JsonResponse`, covering 400, 403, 404, 405 and 500, and explain how middleware can enforce this format across every view.

---

*End of Notes — Error Handling in Django*
