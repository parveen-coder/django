# Unit 3 — Templates, Debugging and Testing (Django)

> **Scope:** Introduction to templates, creating templates, Django Template Language (DTL), template tags and filters, variables, loops and conditionals, dynamic templates using URL and query parameters, template inheritance (`include`, `extends`, `load`, `static`, `block`, `url`), debugging with `breakpoint()` and Django Debug Toolbar, and testing URLs, view functions, context variables and templates.
>
> **Tested on:** Django 4.2 / 5.x, Python 3.10+

---

## Table of Contents

1. [Introduction to Templates in Django](#1-introduction-to-templates-in-django)
2. [Creating Templates](#2-creating-templates)
3. [Working with Django Template Language (DTL)](#3-working-with-django-template-language-dtl)
4. [Template Tags and Filters](#4-template-tags-and-filters)
5. [Django Variables, `for` Loop and `if-else` Statements](#5-django-variables-for-loop-and-if-else-statements)
6. [Dynamic Templates — URL Parameters and Query Parameters](#6-dynamic-templates--url-parameters-and-query-parameters)
7. [Template Inheritance — `extends`, `include`, `load`, `static`, `block`, `url`](#7-template-inheritance)
8. [Debugging Django Applications](#8-debugging-django-applications)
9. [Testing in Django](#9-testing-in-django)
10. [Summary and Practice Questions](#10-summary-and-practice-questions)

---

## Running Example Used Throughout This Unit

All examples in this unit use a single project so that the code builds up gradually.

```text
myproject/
├── manage.py
├── myproject/
│   ├── settings.py
│   └── urls.py
├── blog/                       # our application
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   ├── templatetags/
│   │   ├── __init__.py
│   │   └── blog_extras.py
│   └── templates/
│       └── blog/
│           ├── post_list.html
│           └── post_detail.html
├── templates/                  # project-level templates
│   ├── base.html
│   └── partials/
│       └── navbar.html
└── static/
    ├── css/
    │   └── style.css
    └── images/
        └── logo.png
```

**Model used in the examples (`blog/models.py`):**

```python
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

---

## 1. Introduction to Templates in Django

### 1.1 What is a Template?

A **template** is a text file (usually HTML) that contains:

* **Static parts** — the HTML markup that never changes, and
* **Special placeholders** — the dynamic parts filled in by Django at run time.

A template is *not* a Python file. It is rendered into a plain HTML string and that string is sent to the browser.

```text
Template (HTML + placeholders)  +  Context (Python dictionary)  →  Rendered HTML → Browser
```

### 1.2 Templates in the MVT Architecture

Django follows the **MVT (Model – View – Template)** pattern:

| Component | Responsibility | File |
|-----------|----------------|------|
| **Model** | Data and database structure | `models.py` |
| **View** | Business logic; fetches data and selects a template | `views.py` |
| **Template** | Presentation layer; how the data looks | `*.html` |

The **URLconf** (`urls.py`) maps a requested URL to a view, the view builds a **context**, and the **template engine** renders the template with that context.

### 1.3 Why use Templates?

* **Separation of concerns** — designers work on HTML, developers on Python.
* **Reusability** — one base layout is inherited by every page.
* **Security** — DTL auto-escapes variables, preventing XSS attacks.
* **Restricted logic by design** — DTL deliberately does *not* allow arbitrary Python, which keeps business logic inside views where it belongs.

### 1.4 Template Engine Configuration (`settings.py`)

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES = [
    {
        # 1. The template engine to use
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # 2. Project-level template directories (searched FIRST)
        'DIRS': [BASE_DIR / 'templates'],

        # 3. If True, also search <app>/templates/ of every installed app
        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

| Key | Meaning |
|-----|---------|
| `BACKEND` | Which engine renders the template (`DjangoTemplates` or `Jinja2`) |
| `DIRS` | List of project-wide template folders, searched in order |
| `APP_DIRS` | If `True`, Django searches `appname/templates/` for every app in `INSTALLED_APPS` |
| `context_processors` | Functions that inject extra variables (e.g. `request`, `user`) into **every** template automatically |

### 1.5 Template Search Order

When a view asks for `blog/post_list.html`, Django looks:

1. In each folder listed in `DIRS`, in order → `templates/blog/post_list.html`
2. Then in each app's `templates/` folder, in `INSTALLED_APPS` order → `blog/templates/blog/post_list.html`

The **first match wins**. This is why templates are namespaced inside a folder named after the app (`blog/templates/blog/...`) — two apps may both have a `post_list.html`, and the extra folder prevents a name clash.

---

## 2. Creating Templates

### 2.1 Step 1 — Create the folder

**App-level (recommended for app-specific pages):**

```bash
mkdir -p blog/templates/blog
```

**Project-level (recommended for shared pages such as `base.html`, `404.html`):**

```bash
mkdir -p templates/partials
```

Remember to register the project folder in `TEMPLATES['DIRS']` as shown in §1.4.

### 2.2 Step 2 — Write the template

`blog/templates/blog/post_list.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ page_title }}</title>
</head>
<body>
    <h1>{{ page_title }}</h1>
    <p>Total posts: {{ posts|length }}</p>

    <ul>
        {% for post in posts %}
            <li>{{ post.title }} — by {{ post.author }}</li>
        {% empty %}
            <li>No posts published yet.</li>
        {% endfor %}
    </ul>
</body>
</html>
```

### 2.3 Step 3 — Render it from a view

`blog/views.py`

```python
from django.shortcuts import render
from .models import Post


def post_list(request):
    posts = Post.objects.filter(is_published=True)

    context = {                       # the "context" dictionary
        'page_title': 'All Blog Posts',
        'posts': posts,
    }
    return render(request, 'blog/post_list.html', context)
```

`render(request, template_name, context)` is a shortcut that:

1. loads the template,
2. renders it with the context and the current request, and
3. returns an `HttpResponse` containing the resulting HTML.

### 2.4 Step 4 — Map a URL to the view

`blog/urls.py`

```python
from django.urls import path
from . import views

app_name = 'blog'                     # namespace, used later by the {% url %} tag

urlpatterns = [
    path('', views.post_list, name='post_list'),
]
```

`myproject/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
]
```

### 2.5 The Longer Form (without `render`)

Useful to understand what `render()` actually does:

```python
from django.http import HttpResponse
from django.template import loader


def post_list_manual(request):
    template = loader.get_template('blog/post_list.html')
    context = {'page_title': 'All Posts', 'posts': Post.objects.all()}
    html = template.render(context, request)       # returns a string
    return HttpResponse(html)
```

`render_to_string()` is the same idea and is very handy for generating HTML e-mail bodies:

```python
from django.template.loader import render_to_string

body = render_to_string('blog/email_body.html', {'name': 'Aman'})
```

---

## 3. Working with Django Template Language (DTL)

DTL has exactly **four** constructs.

| Construct | Syntax | Purpose | Example |
|-----------|--------|---------|---------|
| **Variable** | `{{ ... }}` | Output a value | `{{ post.title }}` |
| **Tag** | `{% ... %}` | Logic / control flow | `{% if user.is_staff %}` |
| **Filter** | `{{ var\|filter }}` | Transform a value before printing | `{{ name\|upper }}` |
| **Comment** | `{# ... #}` | Ignored by the engine | `{# TODO: add pagination #}` |

### 3.1 Variables and the Dot Lookup

`{{ post.title }}` — the dot is **not** only attribute access. Django tries, **in this order**:

1. **Dictionary lookup** — `post['title']`
2. **Attribute lookup** — `post.title`
3. **Method call** (no arguments allowed) — `post.title()`
4. **Numeric index lookup** — `post[0]`

The first one that succeeds is used.

```python
# views.py
context = {
    'student': {'name': 'Simran', 'roll': 21},         # dict  → student.name
    'post': Post.objects.first(),                      # object→ post.title
    'marks': [88, 76, 91],                             # list  → marks.0
}
```

```html
{{ student.name }}      {# Simran — dictionary lookup       #}
{{ post.title }}        {# Django Basics — attribute lookup #}
{{ post.get_absolute_url }}  {# method call, no () allowed   #}
{{ marks.0 }}           {# 88 — index lookup, NOT marks[0]  #}
```

> **Important:** You cannot call a method with arguments from a template — `{{ post.filter(x) }}` is invalid. Do such work in the view or in a custom template tag.

### 3.2 Silent Failure

If a variable does not exist, DTL inserts the value of `TEMPLATE_STRING_IF_INVALID` — an **empty string** by default — instead of raising an error.

```html
{{ non_existent_variable }}   {# prints nothing, no crash #}
```

Use the `default` filter to make the intent explicit:

```html
{{ post.subtitle|default:"No subtitle available" }}
```

### 3.3 Auto-escaping (Security)

Every variable is HTML-escaped automatically. If `comment = "<script>alert('hi')</script>"`:

```html
{{ comment }}
{# Renders as: &lt;script&gt;alert(&#x27;hi&#x27;)&lt;/script&gt; — harmless text #}
```

To render trusted HTML deliberately:

```html
{{ article_body|safe }}

{% autoescape off %}
    {{ article_body }}
{% endautoescape %}
```

> Only use `|safe` on content you control. Marking user input as safe re-opens the XSS hole.

### 3.4 Comments

```html
{# single line comment #}

{% comment "Optional note" %}
    Everything here is ignored,
    including {{ variables }} and {% tags %}.
{% endcomment %}
```

---

## 4. Template Tags and Filters

### 4.1 Built-in Template Tags — Quick Reference

| Tag | Purpose |
|-----|---------|
| `{% if %} {% elif %} {% else %} {% endif %}` | Conditional rendering |
| `{% for %} {% empty %} {% endfor %}` | Iterate over a sequence |
| `{% block %} {% endblock %}` | Define a replaceable region (inheritance) |
| `{% extends %}` | Inherit from a parent template |
| `{% include %}` | Insert another template |
| `{% load %}` | Load a tag/filter library (`static`, custom libs) |
| `{% static %}` | Build a URL for a static file |
| `{% url %}` | Reverse a named URL pattern |
| `{% csrf_token %}` | Insert the CSRF hidden field inside a form |
| `{% with %}` | Cache an expensive value under a short name |
| `{% cycle %}` | Alternate between values on each loop pass |
| `{% now %}` | Print the current date/time |
| `{% lorem %}` | Generate placeholder text |
| `{% comment %}` | Multi-line comment |
| `{% debug %}` | Dump the entire context for debugging |

**Examples**

```html
{# with — evaluates the query only once #}
{% with total=post.comments.count %}
    <p>{{ total }} comment{{ total|pluralize }}</p>
{% endwith %}

{# cycle — zebra striped table rows #}
{% for post in posts %}
    <tr class="{% cycle 'row-light' 'row-dark' %}">
        <td>{{ post.title }}</td>
    </tr>
{% endfor %}

{# now — current server time #}
<footer>&copy; {% now "Y" %} My Blog</footer>

{# csrf_token — mandatory in every POST form #}
<form method="post">
    {% csrf_token %}
    <input type="text" name="q">
    <button type="submit">Search</button>
</form>
```

### 4.2 Built-in Filters — Quick Reference

A filter transforms a value: `{{ value|filter_name:"argument" }}`. Filters can be chained.

| Filter | Example | Output (if `value = "django framework"`) |
|--------|---------|------------------------------------------|
| `upper` | `{{ value\|upper }}` | `DJANGO FRAMEWORK` |
| `lower` | `{{ value\|lower }}` | `django framework` |
| `title` | `{{ value\|title }}` | `Django Framework` |
| `capfirst` | `{{ value\|capfirst }}` | `Django framework` |
| `length` | `{{ value\|length }}` | `17` |
| `truncatewords:1` | `{{ value\|truncatewords:1 }}` | `django …` |
| `truncatechars:7` | `{{ value\|truncatechars:7 }}` | `django…` |
| `slice:":6"` | `{{ value\|slice:":6" }}` | `django` |
| `default:"N/A"` | `{{ empty_var\|default:"N/A" }}` | `N/A` |
| `default_if_none` | `{{ none_var\|default_if_none:"-" }}` | `-` |
| `wordcount` | `{{ value\|wordcount }}` | `2` |

**Numeric and date filters**

| Filter | Example | Output |
|--------|---------|--------|
| `add` | `{{ 5\|add:3 }}` | `8` |
| `floatformat:2` | `{{ 3.14159\|floatformat:2 }}` | `3.14` |
| `divisibleby:2` | `{{ 10\|divisibleby:2 }}` | `True` |
| `pluralize` | `{{ count }} item{{ count\|pluralize }}` | `3 items` / `1 item` |
| `date:"d M Y"` | `{{ post.published_date\|date:"d M Y" }}` | `12 Sep 2026` |
| `time:"H:i"` | `{{ post.published_date\|time:"H:i" }}` | `14:30` |
| `timesince` | `{{ post.published_date\|timesince }}` | `3 days, 2 hours` |
| `join:", "` | `{{ tags\|join:", " }}` | `django, python` |
| `first` / `last` | `{{ marks\|first }}` | `88` |
| `linebreaks` | `{{ text\|linebreaks }}` | wraps text in `<p>` tags |
| `striptags` | `{{ html\|striptags }}` | removes all HTML tags |
| `yesno:"Yes,No"` | `{{ post.is_published\|yesno:"Yes,No" }}` | `Yes` |

**Chaining filters**

```html
<h2>{{ post.title|lower|title|truncatechars:40 }}</h2>
<p>{{ post.content|striptags|truncatewords:25 }}</p>
<span>&#8377; {{ post.price|floatformat:2 }}</span>
```

### 4.3 Custom Template Filters and Tags

When the built-ins are not enough, create your own. DTL looks for a `templatetags` package inside the app.

**Step 1 — create the package**

```bash
mkdir blog/templatetags
touch blog/templatetags/__init__.py      # this file is mandatory
```

**Step 2 — write the library** (`blog/templatetags/blog_extras.py`)

```python
from django import template

register = template.Library()


# ---------- CUSTOM FILTER ----------
@register.filter(name='gst')
def gst(value, rate=18):
    """Usage: {{ post.price|gst:18 }} — adds GST to a price."""
    try:
        return round(float(value) * (1 + rate / 100), 2)
    except (ValueError, TypeError):
        return value


@register.filter
def reading_time(text, wpm=200):
    """Usage: {{ post.content|reading_time }} — minutes to read."""
    words = len(str(text).split())
    return max(1, round(words / wpm))


# ---------- SIMPLE TAG ----------
@register.simple_tag
def multiply(a, b):
    """Usage: {% multiply 4 5 %} → 20"""
    return a * b


# ---------- INCLUSION TAG (renders a small template) ----------
@register.inclusion_tag('blog/partials/post_card.html')
def post_card(post):
    """Usage: {% post_card post %}"""
    return {'post': post}
```

**Step 3 — load and use it in a template**

```html
{% load blog_extras %}

<p>Price with GST: &#8377; {{ post.price|gst:18 }}</p>
<p>{{ post.content|reading_time }} min read</p>
<p>Result: {% multiply 4 5 %}</p>

{% for post in posts %}
    {% post_card post %}
{% endfor %}
```

> Restart the development server after creating a new `templatetags` module — Django discovers these libraries at start-up.

---

## 5. Django Variables, `for` Loop and `if-else` Statements

### 5.1 Passing Variables from View to Template

```python
# blog/views.py
from django.shortcuts import render
from .models import Post


def dashboard(request):
    context = {
        'college': 'Lovely Professional University',
        'semester': 7,
        'subjects': ['Django', 'DSA', 'DBMS', 'OS'],
        'topper': {'name': 'Harleen', 'marks': 96},
        'posts': Post.objects.all(),
        'is_admin': request.user.is_staff,
    }
    return render(request, 'blog/dashboard.html', context)
```

```html
<h1>{{ college }}</h1>
<p>Semester: {{ semester }}</p>
<p>First subject: {{ subjects.0 }}</p>
<p>Topper: {{ topper.name }} ({{ topper.marks }}%)</p>
```

### 5.2 The `for` Loop

**Basic syntax**

```html
<ul>
{% for subject in subjects %}
    <li>{{ subject }}</li>
{% empty %}
    <li>No subjects allotted.</li>
{% endfor %}
</ul>
```

`{% empty %}` runs when the sequence is empty or does not exist — it replaces the usual `{% if subjects %}` wrapper.

**The `forloop` variable**

Inside a loop Django provides a special `forloop` object:

| Attribute | Meaning |
|-----------|---------|
| `forloop.counter` | Current iteration, **1-indexed** |
| `forloop.counter0` | Current iteration, **0-indexed** |
| `forloop.revcounter` | Iterations remaining, 1-indexed |
| `forloop.revcounter0` | Iterations remaining, 0-indexed |
| `forloop.first` | `True` on the first pass |
| `forloop.last` | `True` on the last pass |
| `forloop.parentloop` | The `forloop` object of the enclosing loop |

```html
<table border="1">
    <tr><th>S.No</th><th>Title</th><th>Author</th></tr>
{% for post in posts %}
    <tr class="{% if forloop.first %}top-row{% endif %}">
        <td>{{ forloop.counter }}</td>
        <td>{{ post.title }}</td>
        <td>{{ post.author }}</td>
    </tr>
{% endfor %}
</table>
```

**Looping over a dictionary**

```python
context = {'result': {'Django': 85, 'DSA': 92, 'DBMS': 78}}
```

```html
{% for subject, marks in result.items %}
    <p>{{ subject }} : {{ marks }}</p>
{% endfor %}
```

**Nested loops and `parentloop`**

```html
{% for unit in units %}
    <h3>Unit {{ forloop.counter }}</h3>
    <ul>
    {% for topic in unit.topics %}
        <li>{{ forloop.parentloop.counter }}.{{ forloop.counter }} {{ topic }}</li>
    {% endfor %}
    </ul>
{% endfor %}
```

**Reverse iteration**

```html
{% for post in posts reversed %}
    <p>{{ post.title }}</p>
{% endfor %}
```

> DTL has **no `break` and no `continue`**. Filter the data in the view (`Post.objects.filter(...)[:5]`) instead of trying to break out of a loop.

### 5.3 `if` / `elif` / `else`

```html
{% if semester > 6 %}
    <p>Final year — placement drive active.</p>
{% elif semester > 4 %}
    <p>Third year — start preparing.</p>
{% else %}
    <p>Junior batch.</p>
{% endif %}
```

**Supported operators**

| Type | Operators |
|------|-----------|
| Comparison | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| Membership | `in`, `not in` |
| Identity | `is`, `is not` |
| Boolean | `and`, `or`, `not` |

```html
{% if 'Django' in subjects and is_admin %}
    <a href="{% url 'blog:post_create' %}">Add Post</a>
{% endif %}

{% if post.author != request.user.username %}
    <p>Read-only view</p>
{% endif %}

{% if post.published_date is not None %}
    <small>{{ post.published_date|date:"d M Y" }}</small>
{% endif %}
```

**Truthiness** — empty strings, empty lists, empty querysets, `0` and `None` are all false:

```html
{% if posts %}
    <p>{{ posts|length }} post(s) found.</p>
{% else %}
    <p>Nothing to show.</p>
{% endif %}
```

**`if` with filters**

```html
{% if post.content|length > 500 %}
    <span class="badge">Long read</span>
{% endif %}

{% if forloop.counter|divisibleby:2 %}
    <tr class="even">
{% endif %}
```

> Arithmetic is **not** supported: `{% if a + b > 10 %}` is invalid. Compute it in the view, or use the `add` filter: `{% if a|add:b > 10 %}`.

### 5.4 `ifchanged` and `regroup`

```html
{# print a heading only when the category changes #}
{% for post in posts %}
    {% ifchanged post.category %}<h3>{{ post.category }}</h3>{% endifchanged %}
    <p>{{ post.title }}</p>
{% endfor %}

{# group a flat list by an attribute (list must be sorted by that key) #}
{% regroup posts by category as category_list %}
{% for group in category_list %}
    <h3>{{ group.grouper }}</h3>
    <ul>
        {% for post in group.list %}<li>{{ post.title }}</li>{% endfor %}
    </ul>
{% endfor %}
```

---

## 6. Dynamic Templates — URL Parameters and Query Parameters

A *dynamic template* is one whose output changes according to data supplied in the request. Data reaches a view in two different ways:

| | **URL (path) parameter** | **Query (GET) parameter** |
|---|---|---|
| Example URL | `/blog/post/5/` | `/blog/search/?q=django&sort=new` |
| Defined in | `urls.py` path converter | Not defined in `urls.py` at all |
| Received as | A named **function argument** | `request.GET` dictionary |
| Missing value | URL does not match → 404 | `None` / default value |
| Typical use | Identifying **one** resource | Filtering, searching, sorting, pagination |

### 6.1 URL Parameters (Path Converters)

**Available converters**

| Converter | Matches | Example |
|-----------|---------|---------|
| `int` | Zero or positive integers | `<int:pk>` |
| `str` | Any text except `/` (default) | `<str:username>` |
| `slug` | Letters, digits, hyphen, underscore | `<slug:slug>` |
| `uuid` | A formatted UUID | `<uuid:id>` |
| `path` | Any text **including** `/` | `<path:file>` |

**`blog/urls.py`**

```python
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('category/<str:category>/', views.posts_by_category, name='by_category'),
    path('archive/<int:year>/<int:month>/', views.archive, name='archive'),
    path('search/', views.search, name='search'),          # uses query params
]
```

**`blog/views.py`**

```python
from django.shortcuts import render, get_object_or_404
from .models import Post


def post_detail(request, pk):                 # pk comes from <int:pk>
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def posts_by_category(request, category):     # category comes from <str:category>
    posts = Post.objects.filter(category__iexact=category)
    context = {
        'category': category,
        'posts': posts,
        'found': posts.exists(),              # used for conditional rendering
    }
    return render(request, 'blog/by_category.html', context)


def archive(request, year, month):            # two URL parameters
    posts = Post.objects.filter(
        published_date__year=year,
        published_date__month=month,
    )
    return render(request, 'blog/archive.html',
                  {'posts': posts, 'year': year, 'month': month})
```

**`blog/templates/blog/by_category.html` — rendering conditionally on the URL value**

```html
{% extends "base.html" %}

{% block content %}
    <h1>Category: {{ category|title }}</h1>

    {% if found %}
        <p>{{ posts|length }} post(s) in this category.</p>
        <ul>
            {% for post in posts %}
                <li><a href="{% url 'blog:post_detail' post.pk %}">{{ post.title }}</a></li>
            {% endfor %}
        </ul>
    {% else %}
        <p class="warning">No posts found under "{{ category }}".</p>
        <a href="{% url 'blog:post_list' %}">Back to all posts</a>
    {% endif %}
{% endblock %}
```

**Optional URL parameter using a default argument**

```python
# urls.py
path('posts/', views.post_list, name='post_list'),
path('posts/<int:page>/', views.post_list, name='post_list_paged'),

# views.py
def post_list(request, page=1):
    ...
```

### 6.2 Query Parameters (`request.GET`)

Query parameters come after `?` in the URL and are **not** declared in `urls.py`.

```text
/blog/search/?q=django&category=web&sort=old
              └──┬───┘ └────┬─────┘ └──┬──┘
               key=value   key=value  key=value
```

**View**

```python
def search(request):
    query    = request.GET.get('q', '')                 # '' if not supplied
    category = request.GET.get('category', 'all')
    sort     = request.GET.get('sort', 'new')
    tags     = request.GET.getlist('tag')               # ?tag=a&tag=b → ['a', 'b']

    posts = Post.objects.filter(is_published=True)

    if query:
        posts = posts.filter(title__icontains=query)
    if category != 'all':
        posts = posts.filter(category__iexact=category)

    posts = posts.order_by('published_date' if sort == 'old' else '-published_date')

    context = {
        'query': query,
        'category': category,
        'sort': sort,
        'posts': posts,
        'result_count': posts.count(),
        'has_query': bool(query),
    }
    return render(request, 'blog/search.html', context)
```

| Method | Behaviour |
|--------|-----------|
| `request.GET['q']` | Raises `MultiValueDictKeyError` if the key is absent |
| `request.GET.get('q')` | Returns `None` if absent — **safe** |
| `request.GET.get('q', '')` | Returns a default if absent — **preferred** |
| `request.GET.getlist('tag')` | Returns a list for repeated keys |

**Template — conditional output driven by query parameters**

```html
{% extends "base.html" %}

{% block content %}
<form method="get" action="{% url 'blog:search' %}">
    <input type="text" name="q" value="{{ query }}" placeholder="Search posts…">
    <select name="sort">
        <option value="new" {% if sort == 'new' %}selected{% endif %}>Newest first</option>
        <option value="old" {% if sort == 'old' %}selected{% endif %}>Oldest first</option>
    </select>
    <button type="submit">Search</button>
</form>

{% if not has_query %}
    <p>Type something above to begin searching.</p>

{% elif result_count == 0 %}
    <p>No results for "<strong>{{ query }}</strong>".</p>

{% else %}
    <h2>{{ result_count }} result{{ result_count|pluralize }} for "{{ query }}"</h2>
    <ul>
    {% for post in posts %}
        <li>
            <a href="{% url 'blog:post_detail' post.pk %}">{{ post.title }}</a>
            <small>{{ post.category }} · {{ post.published_date|date:"d M Y" }}</small>
        </li>
    {% endfor %}
    </ul>
{% endif %}
{% endblock %}
```

### 6.3 Reading Query Parameters Directly in a Template

Because `django.template.context_processors.request` is enabled, `request` is available in every template:

```html
<p>Current page: {{ request.GET.page|default:"1" }}</p>
<p>Full path with query string: {{ request.get_full_path }}</p>

{% if request.GET.category == 'web' %}
    <span class="badge">Web Development</span>
{% endif %}
```

### 6.4 Building URLs with Both Parameter Types

```html
{# URL parameter passed positionally #}
<a href="{% url 'blog:post_detail' post.pk %}">Read more</a>

{# URL parameter passed by keyword #}
<a href="{% url 'blog:archive' year=2026 month=9 %}">Sep 2026</a>

{# Query string is simply appended after the url tag #}
<a href="{% url 'blog:search' %}?q={{ query|urlencode }}&sort=old">Oldest first</a>

{# Pagination that preserves the existing search term #}
<a href="?q={{ query|urlencode }}&page={{ page_obj.next_page_number }}">Next &raquo;</a>
```

---

## 7. Template Inheritance

Template inheritance lets you define a **skeleton** page once and override only the parts that change. It eliminates duplicated markup across pages.

### 7.1 `{% block %}` and `{% extends %}`

**Parent — `templates/base.html`**

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>{% block title %}My Blog{% endblock %}</title>

    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    {% block extra_css %}{% endblock %}
</head>
<body>

    {% include "partials/navbar.html" %}

    <main class="container">
        {% block content %}
            <p>Default content — child templates override this.</p>
        {% endblock %}
    </main>

    <footer>
        {% block footer %}
            <p>&copy; {% now "Y" %} My Blog. All rights reserved.</p>
        {% endblock %}
    </footer>

    <script src="{% static 'js/main.js' %}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

**Child — `blog/templates/blog/post_detail.html`**

```html
{% extends "base.html" %}
{% load static %}

{% block title %}{{ post.title }} — My Blog{% endblock %}

{% block extra_css %}
    <link rel="stylesheet" href="{% static 'css/detail.css' %}">
{% endblock %}

{% block content %}
    <article>
        <h1>{{ post.title }}</h1>
        <p class="meta">
            By {{ post.author }} ·
            {{ post.published_date|date:"d M Y" }} ·
            {{ post.content|wordcount }} words
        </p>
        <div>{{ post.content|linebreaks }}</div>
    </article>

    <a href="{% url 'blog:post_list' %}">&laquo; Back to all posts</a>
{% endblock %}

{% block footer %}
    {{ block.super }}          {# keeps the parent footer AND adds to it #}
    <p>Category: {{ post.category }}</p>
{% endblock %}
```

**Rules for `{% extends %}`**

1. It must be the **very first tag** in the child template.
2. A template can extend only **one** parent.
3. Anything written outside a `{% block %}` in a child template is **ignored**.
4. Block names must be **unique** inside a template.
5. `{{ block.super }}` outputs whatever the parent block contained.

**Multi-level inheritance** is allowed and common:

```text
base.html  →  blog/base_blog.html  →  blog/post_detail.html
```

```html
{# blog/base_blog.html #}
{% extends "base.html" %}
{% block content %}
    <div class="blog-layout">
        <section class="main">{% block blog_content %}{% endblock %}</section>
        <aside>{% include "blog/partials/sidebar.html" %}</aside>
    </div>
{% endblock %}
```

### 7.2 `{% include %}` — Reusable Fragments

`{% include %}` inserts and renders another template **at that point**, using the current context.

```html
{% include "partials/navbar.html" %}

{# pass extra variables #}
{% include "blog/partials/post_card.html" with post=item show_author=True %}

{# isolate the context — the included file sees ONLY what is passed #}
{% include "blog/partials/post_card.html" with post=item only %}

{# template name can itself be a variable #}
{% include card_template %}
```

**`extends` vs `include`**

| | `{% extends %}` | `{% include %}` |
|---|---|---|
| Direction | Child **inherits** parent skeleton | Current template **pulls in** a fragment |
| Position | Must be the first tag | Anywhere in the body |
| Count per file | Only one | Any number |
| Typical use | Page layout (`base.html`) | Navbar, footer, cards, form snippets |

### 7.3 `{% load %}`

`{% load %}` makes a tag/filter library available **in that file only** — it is *not* inherited from a parent template.

```html
{% load static %}                 {# built-in staticfiles library      #}
{% load blog_extras %}            {# our custom library from §4.3      #}
{% load static blog_extras %}     {# several libraries in one tag      #}
{% load gst from blog_extras %}   {# import a single filter            #}
```

> A very common exam/lab error: using `{% static %}` in a child template without writing `{% load static %}` in **that** child. `{% load %}` does not cross template boundaries.

### 7.4 The `static` Folder and `{% static %}`

**`settings.py`**

```python
STATIC_URL = 'static/'                       # public URL prefix

STATICFILES_DIRS = [                         # extra project-level folders (development)
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'       # collectstatic destination (production)
```

**Folder layout**

```text
static/                    ← project-wide assets (listed in STATICFILES_DIRS)
├── css/style.css
├── js/main.js
└── images/logo.png

blog/static/blog/          ← app-specific assets (found because APP_DIRS-style discovery)
└── css/blog.css
```

**Usage**

```html
{% load static %}

<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script src="{% static 'js/main.js' %}"></script>
<img src="{% static 'images/logo.png' %}" alt="Logo" width="120">

{# app-namespaced asset #}
<link rel="stylesheet" href="{% static 'blog/css/blog.css' %}">

{# store the URL in a variable #}
{% static 'images/banner.jpg' as banner %}
<div style="background-image: url('{{ banner }}');"></div>
```

Serving uploaded **media** during development (`myproject/urls.py`):

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your patterns
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

> Never hard-code `/static/css/style.css`. `{% static %}` respects `STATIC_URL`, CDN storage backends, and cache-busting hashes.

### 7.5 The `{% url %}` Tag and a Reusable Navbar

`{% url %}` performs **reverse URL resolution**: it turns a URL *name* into a path. Change the path in `urls.py` and every template updates automatically.

```html
{% url 'blog:post_list' %}                     {# /blog/                 #}
{% url 'blog:post_detail' post.pk %}           {# /blog/post/5/          #}
{% url 'blog:archive' year=2026 month=9 %}     {# /blog/archive/2026/9/  #}
{% url 'blog:post_list' as list_url %}         {# store, no error if missing #}
```

**`templates/partials/navbar.html` — with an "active link" highlight**

```html
{% load static %}

<nav class="navbar">
    <a class="brand" href="{% url 'blog:post_list' %}">
        <img src="{% static 'images/logo.png' %}" alt="Logo" height="32">
    </a>

    <ul class="nav-links">
        <li>
            <a href="{% url 'blog:post_list' %}"
               class="{% if request.resolver_match.url_name == 'post_list' %}active{% endif %}">
               Home
            </a>
        </li>
        <li>
            <a href="{% url 'blog:by_category' 'django' %}"
               class="{% if request.path == '/blog/category/django/' %}active{% endif %}">
               Django
            </a>
        </li>
        <li>
            <a href="{% url 'blog:archive' 2026 9 %}">Archive</a>
        </li>
        <li>
            <a href="{% url 'blog:search' %}">Search</a>
        </li>
    </ul>

    <div class="nav-right">
        {% if user.is_authenticated %}
            <span>Hi, {{ user.username }}</span>
            <a href="{% url 'logout' %}">Logout</a>
        {% else %}
            <a href="{% url 'login' %}">Login</a>
        {% endif %}
    </div>
</nav>
```

Two ways to detect the current page:

| Expression | Notes |
|------------|-------|
| `request.path` | Compares the literal path string |
| `request.resolver_match.url_name` | Compares the URL **name** — refactor-safe, preferred |
| `request.resolver_match.namespace` | The app namespace, e.g. `blog` |

Matching CSS (`static/css/style.css`):

```css
.navbar { display: flex; align-items: center; gap: 1rem; padding: .75rem 1.5rem; background: #212529; }
.nav-links { display: flex; list-style: none; gap: 1rem; margin: 0; }
.nav-links a { color: #ced4da; text-decoration: none; }
.nav-links a.active { color: #fff; border-bottom: 2px solid #0d6efd; }
```

---

## 8. Debugging Django Applications

### 8.1 The `DEBUG` Setting and the Yellow Error Page

```python
# settings.py
DEBUG = True                       # development ONLY
ALLOWED_HOSTS = []                 # must be filled in when DEBUG = False
```

With `DEBUG = True`, an unhandled exception produces Django's technical error page showing the traceback, the local variables at each frame, the request `GET`/`POST`/`COOKIES`/`META` data and the full settings.

> **Never deploy with `DEBUG = True`.** It leaks settings, secret keys and database details to anyone who can trigger an error.

For template errors specifically, the error page highlights the exact line in the template and shows the template search path that failed (`TemplateDoesNotExist`).

### 8.2 Debugging with `breakpoint()`

Python 3.7+ provides the built-in `breakpoint()` function, which starts **pdb** (the Python debugger) at that line. Django's development server runs in the foreground, so the debugger prompt appears in the same terminal.

```python
# blog/views.py
from django.shortcuts import render, get_object_or_404
from .models import Post


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    breakpoint()            # ← execution pauses here; terminal becomes a pdb prompt

    related = Post.objects.filter(category=post.category).exclude(pk=pk)[:3]
    return render(request, 'blog/post_detail.html',
                  {'post': post, 'related': related})
```

Run the server **without** the auto-reloader so the debugger is not interrupted:

```bash
python manage.py runserver --noreload
```

Now open `/blog/post/1/` in the browser — the request hangs and the terminal shows `(Pdb)`.

**Essential pdb commands**

| Command | Short | Action |
|---------|-------|--------|
| `next` | `n` | Execute the current line, stay in this function |
| `step` | `s` | Step **into** the function being called |
| `continue` | `c` | Resume until the next breakpoint |
| `list` | `l` | Show source around the current line |
| `print expr` | `p` | Print the value of an expression |
| `pp expr` | | Pretty-print (useful for dicts and querysets) |
| `args` | `a` | Print the arguments of the current function |
| `where` | `w` | Show the call stack (traceback) |
| `until` | `unt` | Run until a line greater than the current one |
| `quit` | `q` | Abort execution |
| `help` | `h` | List all commands |

**A sample debugging session**

```text
> /myproject/blog/views.py(11)post_detail()
-> related = Post.objects.filter(category=post.category).exclude(pk=pk)[:3]
(Pdb) p pk
1
(Pdb) p post.title
'Getting Started with Django'
(Pdb) p post.category
'web'
(Pdb) pp Post.objects.filter(category='web').count()
4
(Pdb) n
> /myproject/blog/views.py(12)post_detail()
(Pdb) p list(related)
[<Post: Django Templates>, <Post: Django ORM>]
(Pdb) c
```

Other options:

```python
import pdb; pdb.set_trace()      # classic form, identical behaviour to breakpoint()
```

```bash
# Use a nicer debugger without changing any code
pip install ipdb
PYTHONBREAKPOINT=ipdb.set_trace python manage.py runserver --noreload

# Disable every breakpoint() call without deleting them
PYTHONBREAKPOINT=0 python manage.py runserver
```

> A `breakpoint()` left in committed code will freeze the production server. Always remove them before pushing.

### 8.3 Debugging inside Templates

```html
{% load static %}

{# Dump the whole context and all available tags #}
{% debug %}

{# Quick, targeted checks #}
<pre>
posts type/length : {{ posts|length }}
first post        : {{ posts.0 }}
user              : {{ user }}
path              : {{ request.path }}
GET params        : {{ request.GET }}
</pre>
```

You can also raise an invalid-variable error deliberately during development:

```python
TEMPLATES = [{
    # ...
    'OPTIONS': {
        'string_if_invalid': 'INVALID VARIABLE: %s',   # development aid only
    },
}]
```

### 8.4 Logging Instead of Printing

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',
        },
    },
    'loggers': {
        'django': {'handlers': ['console'], 'level': 'INFO'},
        'blog': {'handlers': ['console', 'file'], 'level': 'DEBUG'},
    },
}
```

```python
# blog/views.py
import logging

logger = logging.getLogger(__name__)


def post_detail(request, pk):
    logger.debug('post_detail called with pk=%s by %s', pk, request.user)
    post = get_object_or_404(Post, pk=pk)
    logger.info('Rendering post "%s"', post.title)
    return render(request, 'blog/post_detail.html', {'post': post})
```

To see every SQL query Django executes, add:

```python
'loggers': {
    'django.db.backends': {'handlers': ['console'], 'level': 'DEBUG'},
}
```

### 8.5 Django Debug Toolbar

The Debug Toolbar adds a collapsible panel to every HTML page showing SQL queries, template rendering details, the context of each template, static files, signals, cache usage and request timing.

**Step 1 — install**

```bash
pip install django-debug-toolbar
```

**Step 2 — `settings.py`**

```python
INSTALLED_APPS = [
    # ...
    'django.contrib.staticfiles',      # required by the toolbar
    'debug_toolbar',
    'blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',   # as early as possible
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# The toolbar renders only for these IPs
INTERNAL_IPS = [
    '127.0.0.1',
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,   # optional custom rule
}
```

**Step 3 — `myproject/urls.py`**

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
```

**Requirements for the toolbar to appear**

1. `DEBUG = True`
2. The client IP is listed in `INTERNAL_IPS`
3. The response is HTML and contains a closing `</body>` tag
4. The response is not an AJAX/JSON response

**The panels and what they are used for**

| Panel | What it tells you |
|-------|-------------------|
| **SQL** | Every query, its duration, duplicates, and an `EXPLAIN` link — the fastest way to spot **N+1 query** problems |
| **Templates** | Which templates rendered, their paths, and the full **context** of each |
| **Time** | CPU and total time spent on the request |
| **Static files** | Which static assets were used and where they were found |
| **Request** | `GET`, `POST`, cookies, session, and the matched **view name and URL kwargs** |
| **Headers** | Request and response headers |
| **Signals** | Which Django signals fired |
| **Cache** | Cache hits and misses |

**Fixing an N+1 problem discovered through the SQL panel**

```python
# Before: 1 query for posts + 1 query per post for its author → N+1
posts = Post.objects.all()

# After: a single JOIN
posts = Post.objects.select_related('author')        # ForeignKey / OneToOne
posts = Post.objects.prefetch_related('tags')        # ManyToMany / reverse FK
```

---

## 9. Testing in Django

Django's test framework extends Python's `unittest`. Tests live in `tests.py` (or a `tests/` package) inside each app, must be in a class derived from a Django test case, and every test method name must start with `test_`.

### 9.1 Test Case Classes

| Class | Database access | Use for |
|-------|-----------------|---------|
| `SimpleTestCase` | ❌ Not allowed | URL resolution, template rendering, pure functions |
| `TestCase` | ✅ Wrapped in a rolled-back transaction | Views, models, forms (most common) |
| `TransactionTestCase` | ✅ Real commits | Testing transactions, `select_for_update` |
| `LiveServerTestCase` | ✅ Runs a real server | Selenium / browser tests |

### 9.2 Running Tests

```bash
python manage.py test                        # every app
python manage.py test blog                   # one app
python manage.py test blog.tests             # one module
python manage.py test blog.tests.PostViewTests               # one class
python manage.py test blog.tests.PostViewTests.test_status   # one method

python manage.py test -v 2                   # verbose output
python manage.py test --keepdb               # reuse the test DB (faster)
python manage.py test --failfast             # stop at the first failure
```

Django creates a **separate test database** (`test_<dbname>`), runs migrations on it, and destroys it afterwards — your development data is never touched.

### 9.3 Testing URLs — `reverse()` and `resolve()`

* `reverse('name', args=[...])` → **name to path** (`'blog:post_detail'` → `/blog/post/1/`)
* `resolve('/path/')` → **path to view**, returning `func`, `url_name`, `args`, `kwargs`

```python
# blog/tests.py
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from blog.views import post_list, post_detail, search


class UrlTests(SimpleTestCase):

    def test_post_list_url_resolves_to_correct_view(self):
        url = reverse('blog:post_list')
        self.assertEqual(url, '/blog/')
        self.assertEqual(resolve(url).func, post_list)          # view FUNCTION
        self.assertEqual(resolve(url).func.__name__, 'post_list')  # view NAME

    def test_post_detail_url_builds_and_resolves(self):
        url = reverse('blog:post_detail', args=[5])
        self.assertEqual(url, '/blog/post/5/')

        match = resolve('/blog/post/5/')
        self.assertEqual(match.func, post_detail)
        self.assertEqual(match.url_name, 'post_detail')         # URL name
        self.assertEqual(match.namespace, 'blog')               # app namespace
        self.assertEqual(match.kwargs, {'pk': 5})               # captured params

    def test_archive_url_with_kwargs(self):
        url = reverse('blog:archive', kwargs={'year': 2026, 'month': 9})
        self.assertEqual(url, '/blog/archive/2026/9/')

    def test_search_url(self):
        self.assertEqual(reverse('blog:search'), '/blog/search/')
        self.assertEqual(resolve('/blog/search/').func.__name__, 'search')

    def test_invalid_url_returns_404(self):
        response = self.client.get('/blog/no-such-page/')
        self.assertEqual(response.status_code, 404)
```

For a **class-based view**, compare `func.view_class` instead:

```python
from blog.views import PostListView

def test_cbv_url(self):
    match = resolve('/blog/')
    self.assertEqual(match.func.view_class, PostListView)
```

### 9.4 Testing Views — the Test `Client`

`self.client` is a dummy browser: it issues requests through the full URLconf–middleware–view–template stack without a running server.

```python
from django.test import TestCase
from django.urls import reverse
from blog.models import Post


class PostViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Runs ONCE for the whole class — read-only shared fixtures."""
        cls.published = Post.objects.create(
            title='Django Templates', content='DTL basics ' * 30,
            author='Rabaab', category='web', is_published=True,
        )
        cls.draft = Post.objects.create(
            title='Unfinished Draft', content='WIP',
            author='Rabaab', category='web', is_published=False,
        )

    def setUp(self):
        """Runs before EVERY test method."""
        self.list_url = reverse('blog:post_list')
        self.detail_url = reverse('blog:post_detail', args=[self.published.pk])

    # ---------- status codes ----------
    def test_post_list_returns_200(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_detail_of_missing_post_returns_404(self):
        response = self.client.get(reverse('blog:post_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)

    # ---------- content ----------
    def test_list_shows_published_and_hides_drafts(self):
        response = self.client.get(self.list_url)
        self.assertContains(response, 'Django Templates')
        self.assertNotContains(response, 'Unfinished Draft')

    # ---------- redirect ----------
    def test_old_url_redirects(self):
        response = self.client.get('/blog/posts/')          # legacy path
        self.assertRedirects(response, self.list_url,
                             status_code=301, target_status_code=200)
```

**HTTP methods on the client**

```python
self.client.get(url)
self.client.get(url, {'q': 'django', 'sort': 'old'})       # query parameters
self.client.post(url, {'title': 'New Post', 'content': '...'})
self.client.login(username='admin', password='secret')      # authenticated tests
self.client.get(url, follow=True)                           # follow redirects
```

### 9.5 Testing the Template Used

```python
class TemplateTests(TestCase):

    def test_list_view_uses_correct_templates(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertTemplateUsed(response, 'blog/post_list.html')
        self.assertTemplateUsed(response, 'base.html')            # parent template
        self.assertTemplateUsed(response, 'partials/navbar.html') # included file
        self.assertTemplateNotUsed(response, 'blog/post_detail.html')

    def test_all_rendered_template_names(self):
        response = self.client.get(reverse('blog:post_list'))
        names = [t.name for t in response.templates]
        self.assertIn('blog/post_list.html', names)

    def test_navbar_contains_working_links(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertContains(response, f'href="{reverse("blog:search")}"')
```

Rendering a template directly, without any view:

```python
from django.template.loader import render_to_string
from django.test import SimpleTestCase


class DirectRenderTests(SimpleTestCase):

    def test_card_partial_renders_title(self):
        html = render_to_string('blog/partials/post_card.html',
                                {'post': {'title': 'Hello', 'author': 'Amit'}})
        self.assertIn('Hello', html)
        self.assertIn('Amit', html)
```

### 9.6 Testing Context Variables

`response.context` holds the context the template was rendered with.

```python
class ContextTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        for i in range(5):
            Post.objects.create(title=f'Post {i}', content='x', author='A',
                                category='web' if i % 2 else 'dsa',
                                is_published=True)

    def test_context_keys_exist(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertIn('posts', response.context)
        self.assertIn('page_title', response.context)

    def test_context_variable_values(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.context['page_title'], 'All Blog Posts')
        self.assertEqual(len(response.context['posts']), 5)

    def test_queryset_contents(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertQuerySetEqual(                       # assertQuerysetEqual < Django 4.2
            response.context['posts'].order_by('title'),
            Post.objects.filter(is_published=True).order_by('title'),
        )

    # ---------- query parameters ----------
    def test_search_context_reflects_query_params(self):
        response = self.client.get(reverse('blog:search'), {'q': 'Post 1', 'sort': 'old'})
        self.assertEqual(response.context['query'], 'Post 1')
        self.assertEqual(response.context['sort'], 'old')
        self.assertEqual(response.context['result_count'], 1)
        self.assertTrue(response.context['has_query'])

    def test_search_without_query_shows_prompt(self):
        response = self.client.get(reverse('blog:search'))
        self.assertFalse(response.context['has_query'])
        self.assertContains(response, 'Type something above')

    # ---------- url parameters ----------
    def test_category_url_parameter_filters_context(self):
        response = self.client.get(reverse('blog:by_category', args=['dsa']))
        self.assertEqual(response.context['category'], 'dsa')
        self.assertTrue(response.context['found'])
        for post in response.context['posts']:
            self.assertEqual(post.category, 'dsa')

    def test_unknown_category_renders_empty_message(self):
        response = self.client.get(reverse('blog:by_category', args=['cloud']))
        self.assertFalse(response.context['found'])
        self.assertContains(response, 'No posts found')
```

### 9.7 Testing Custom Template Filters

```python
from django.test import SimpleTestCase
from django.template import Context, Template
from blog.templatetags.blog_extras import gst, reading_time


class TemplateTagTests(SimpleTestCase):

    def test_gst_filter_function(self):
        self.assertEqual(gst(100, 18), 118.0)

    def test_reading_time_minimum_is_one(self):
        self.assertEqual(reading_time('short text'), 1)

    def test_filter_inside_a_rendered_template(self):
        template = Template('{% load blog_extras %}{{ price|gst:18 }}')
        rendered = template.render(Context({'price': 200}))
        self.assertEqual(rendered.strip(), '236.0')
```

### 9.8 Common Assertions — Quick Reference

| Assertion | Checks |
|-----------|--------|
| `assertEqual(a, b)` | `a == b` |
| `assertTrue(x)` / `assertFalse(x)` | Truthiness |
| `assertIn(a, b)` / `assertNotIn(a, b)` | Membership |
| `assertIsNone(x)` | `x is None` |
| `assertContains(response, text)` | Status 200 **and** `text` appears in the HTML |
| `assertNotContains(response, text)` | `text` does not appear |
| `assertTemplateUsed(response, name)` | The template was rendered |
| `assertTemplateNotUsed(response, name)` | The template was not rendered |
| `assertRedirects(response, url)` | Redirect target and final status |
| `assertQuerySetEqual(qs, values)` | QuerySet contents match |
| `assertFormError(response, form, field, errors)` | A form validation error is present |
| `assertNumQueries(n)` | Exactly `n` SQL queries run (performance) |
| `assertRaises(Error)` | The block raises the given exception |

### 9.9 A Complete `tests.py` Skeleton

```python
from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve

from blog.models import Post
from blog.views import post_list, post_detail


class BlogUrlTests(SimpleTestCase):
    """Layer 1 — URL name ↔ path ↔ view function."""

    def test_list_url(self):
        self.assertEqual(resolve(reverse('blog:post_list')).func, post_list)

    def test_detail_url(self):
        self.assertEqual(resolve(reverse('blog:post_detail', args=[1])).func, post_detail)


class BlogViewTests(TestCase):
    """Layer 2 — status codes, context variables and templates."""

    @classmethod
    def setUpTestData(cls):
        cls.post = Post.objects.create(
            title='Django Testing', content='How to test Django apps.',
            author='Rabaab', category='web', is_published=True,
        )

    def test_list_view(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')
        self.assertContains(response, 'Django Testing')
        self.assertEqual(len(response.context['posts']), 1)

    def test_detail_view(self):
        response = self.client.get(reverse('blog:post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertEqual(response.context['post'].title, 'Django Testing')


class BlogModelTests(TestCase):
    """Layer 3 — model behaviour."""

    def test_str_returns_title(self):
        post = Post.objects.create(title='ORM Basics', content='...',
                                   author='A', category='db')
        self.assertEqual(str(post), 'ORM Basics')
```

**Sample output**

```text
$ python manage.py test blog -v 2
Creating test database for alias 'default'...
test_detail_url (blog.tests.BlogUrlTests) ... ok
test_list_url (blog.tests.BlogUrlTests) ... ok
test_detail_view (blog.tests.BlogViewTests) ... ok
test_list_view (blog.tests.BlogViewTests) ... ok
test_str_returns_title (blog.tests.BlogModelTests) ... ok
----------------------------------------------------------------------
Ran 5 tests in 0.412s

OK
Destroying test database for alias 'default'...
```

### 9.10 Measuring Test Coverage

```bash
pip install coverage
coverage run --source='.' manage.py test blog
coverage report          # table in the terminal
coverage html            # detailed report in htmlcov/index.html
```

---

## 10. Summary and Practice Questions

### 10.1 Unit Summary

| Concept | Key Point |
|---------|-----------|
| Template | HTML + placeholders, rendered with a context dictionary |
| `render()` | Shortcut for load + render + `HttpResponse` |
| DTL | `{{ variable }}`, `{% tag %}`, `\|filter`, `{# comment #}` |
| Dot lookup | dictionary → attribute → method → index |
| Auto-escaping | On by default; `\|safe` to disable for trusted HTML |
| `for` loop | `{% empty %}` for the empty case, `forloop.counter` for numbering, no `break` |
| `if` | Comparison, `in`, `and/or/not`; no arithmetic |
| URL parameter | Declared in `urls.py` (`<int:pk>`), arrives as a view argument |
| Query parameter | Not declared; read via `request.GET.get('key', default)` |
| `extends` | First tag, one parent, overrides `{% block %}`s, `{{ block.super }}` |
| `include` | Inserts a fragment anywhere, optional `with ... only` |
| `load` | Per-file; required for `static` and custom libraries |
| `static` | Builds asset URLs from `STATIC_URL` / `STATICFILES_DIRS` |
| `url` | Reverse resolution by URL name; refactor-safe links |
| `breakpoint()` | Starts pdb; run `runserver --noreload` |
| Debug Toolbar | SQL, templates, context, timing; needs `DEBUG`, `INTERNAL_IPS`, middleware, URLs |
| Testing | `SimpleTestCase` for URLs, `TestCase` for views; `reverse`, `resolve`, `assertTemplateUsed`, `response.context` |

### 10.2 Practice Questions

**Short answer (2 marks)**

1. Differentiate between `{{ }}` and `{% %}` in DTL.
2. State the order in which Django resolves `{{ obj.attr }}`.
3. Why is `{% load static %}` required in a child template that already extends a parent using `{% static %}`?
4. What does `{{ block.super }}` output?
5. Give one difference between `{% include %}` and `{% extends %}`.
6. Why does `request.GET.get('q', '')` fail less often than `request.GET['q']`?
7. Which test case class should be used for URL tests that need no database, and why?

**Medium answer (5 marks)**

8. Explain the template loading order when `DIRS` and `APP_DIRS` are both configured.
9. Write a template snippet that lists all posts with serial numbers, alternates row colours, and prints a message when the list is empty.
10. Compare URL parameters and query parameters with one example each.
11. Explain the steps to create and use a custom template filter that converts marks into a grade.
12. Describe any five panels of the Django Debug Toolbar and what each helps you find.

**Long answer (10 marks)**

13. Design a `base.html` with blocks for title, content and footer, plus a navbar partial that highlights the active link using `{% url %}`. Write a child template that overrides all three blocks.
14. A view must show posts filtered by a category supplied in the URL and further sorted by a query parameter. Write the URLconf, view and template, handling the "no results" case.
15. Write a complete `tests.py` for a `post_detail` view that verifies: the URL resolves to the correct view function, a valid pk returns 200, an invalid pk returns 404, the correct template is used, and the `post` context variable holds the right object.
16. Explain how you would locate and fix an N+1 query problem in a list page using the Debug Toolbar and `assertNumQueries`.

---

*End of Unit 3 — Templates, Debugging and Testing*
