# Unit 4 — Forms in Django

> **Scope:** Introduction to forms, using GET, POST and HTTP, building forms using Django (`forms.Form`, `ModelForm`, rendering, file uploads), introduction to Cross Site Request Forgery (CSRF), CSRF support in Django, implementing POST/Redirect/GET, and data validation with Django forms (built-in, `error_messages`, `clean_<field>()`, `clean()`).
>
> **Code source:** `Wednesday` project → `student` app (`forms.py`, `views.py`, `urls.py`, `templates/student/`) in the class repository.
>
> **Tested on:** Django 6.x, Python 3.12+ — every output shown in this file was produced by running the class code.

---

## Table of Contents

1. [Introduction to Forms](#1-introduction-to-forms)
2. [Using GET, POST and HTTP](#2-using-get-post-and-http)
3. [Building Forms using Django](#3-building-forms-using-django)
4. [Rendering a Django Form in a Template](#4-rendering-a-django-form-in-a-template)
5. [Uploading Images and Files with a Form](#5-uploading-images-and-files-with-a-form)
6. [ModelForm — Forms Generated from Models](#6-modelform--forms-generated-from-models)
7. [Introduction to Cross Site Request Forgery (CSRF)](#7-introduction-to-cross-site-request-forgery-csrf)
8. [CSRF Support in Django](#8-csrf-support-in-django)
9. [Implementing POST/Redirect/GET in Django](#9-implementing-postredirectget-in-django)
10. [Data Validation with Django Forms](#10-data-validation-with-django-forms)
11. [Testing Forms](#11-testing-forms)
12. [Issues Found in the Class Code (and Fixes)](#12-issues-found-in-the-class-code-and-fixes)
13. [URL → View → Template Map for Unit 4](#13-url--view--template-map-for-unit-4)
14. [Summary and Practice Questions](#14-summary-and-practice-questions)

---

## Project Files Used in This Unit

All Unit 4 code lives in the `student` app of the `Wednesday` project.

```text
Wednesday/
├── manage.py
├── media/                          # uploaded images and files are stored here
│   ├── images/
│   └── files/
├── Wednesday/
│   ├── settings.py                 # MEDIA_URL, MEDIA_ROOT, CSRF middleware
│   └── urls.py                     # serves /media/ during development
└── student/
    ├── forms.py                    # ExamForm, Newform, StudentForm, RegisterStudent,
    │                               # CarForm, StudentFormNew, ClothForm
    ├── models.py                   # Car, Student, Cloth (used by ModelForms)
    ├── views.py                    # studentadd, student_form, newform, form23,
    │                               # studentform, car_* / stud_* / cloth_* views
    ├── urls.py
    └── templates/student/
        ├── studentrecord.html      # plain HTML form
        ├── showrecord.html         # shows submitted data
        ├── formstudent.html        # ExamForm with {{ form.as_p }}
        ├── detailsstudent.html
        ├── formnew.html            # Newform
        ├── form2student.html       # StudentForm (with files)
        ├── studentform.html        # RegisterStudent, fields rendered manually
        ├── Registeredstudent.html  # shows uploaded image + file
        ├── car_form.html / car_list.html / car_detail.html / car_confirm_delete.html
        ├── stud_form.html / stud_list.html / ...
        └── cloth_add.html / cloth_list.html / ...
```

**Unit 4 views in this project, from simplest to most complete:**

| Step | URL | View | Shows |
|------|-----|------|-------|
| 1 | `/student/addstudent/` | `studentadd` | Plain HTML form, read with `request.POST.get()` |
| 2 | `/student/formnew/` | `student_form` | Django form displayed, but data still read manually |
| 3 | `/student/newform/` | `newform` | Django form + a POST branch |
| 4 | `/student/form23/` | `form23` | `is_valid()`, `cleaned_data`, file upload |
| 5 | `/student/studentform/` | `studentform` | Custom validation, manual rendering, image + file upload |
| 6 | `/student/cars/add/` | `car_create` | `ModelForm` + **POST/Redirect/GET** |

---

## 1. Introduction to Forms

### 1.1 What is a Form?

A **form** is the part of a web page that lets the user **send data to the server** — a login box, a registration page, a search bar, a feedback page.

Every web form has three jobs:

| Job | Who does it |
|-----|-------------|
| **Display** the input boxes | HTML (`<form>`, `<input>`, `<select>`, `<textarea>`) |
| **Send** the typed data | The browser, using a GET or POST request |
| **Receive and check** the data | The server — in our case a Django view |

### 1.2 Anatomy of an HTML Form

```html
<form method="post" action="/student/addstudent/">
    {% csrf_token %}
    <label>Name</label>
    <input type="text" name="name">
    <button type="submit">Add Student</button>
</form>
```

| Part | Meaning |
|------|---------|
| `<form>` | Container for all inputs that are sent together |
| `method` | `get` or `post` — how the data travels (Section 2) |
| `action` | URL that receives the data. **Empty or missing = the same URL the page came from** |
| `name="name"` | The **key** the server uses to read the value. An input with no `name` is **never sent** |
| `type="submit"` | The button that sends the form |
| `{% csrf_token %}` | Django security token, required for POST (Section 8) |

### 1.3 Our First Form — a Plain HTML Form (`studentadd`)

**Template — `student/templates/student/studentrecord.html`**

```html
<form method="post">
   {% csrf_token %}
    <label>Name</label>
    <input type="text" name="name"><br>

    <label>Email</label>
    <input type="email" name="email"><br>

    <label>Age</label>
    <input type="number" name="age"><br>

    <button type="submit">Add Student</button>
</form>
```

**View — `student/views.py`**

```python
#  function to return the student form
def studentadd(req):

    if req.method=="GET":
         return render(req,'student/studentrecord.html')

    if req.method=="POST":
            name=req.POST.get('name')
            email=req.POST.get('email')
            age=req.POST.get('age')

            print(name)
            print(email)
            print(age)

            return render(req,'student/showrecord.html',{'n':name, 'e':email, 'a':age})
```

**Result template — `showrecord.html`**

```html
<h1>Student name is : {{n}}</h1>
<h3>Student email is : {{e}}</h3>
<p>Student age is : {{a}}</p>
```

**URL:** `path('addstudent/', views.studentadd)` → `http://127.0.0.1:8000/student/addstudent/`

**What happens (verified):**

```text
GET  /student/addstudent/   → 200, empty form (studentrecord.html)
POST /student/addstudent/   → 200, "Student name is : Rahul  Student email is : r@x.com  Student age is : 20"
Terminal: Rahul
          r@x.com
          20
```

> **Note:** The parameter is called `req` here instead of `request`. The name does not matter to Django — it always passes the request object as the **first** argument.

### 1.4 Problems with Plain HTML Forms

The view above works, but it has no protection:

| Problem | Example |
|---------|---------|
| No validation | `age = "abc"` or an empty name is accepted |
| Everything is a string | `req.POST.get('age')` returns `"20"`, not `20` |
| HTML and Python can disagree | Rename the input to `student_name` and the view silently gets `None` |
| Errors must be shown by hand | No built-in way to tell the user what went wrong |

Django's **forms library** (Section 3) fixes every one of these.

---

## 2. Using GET, POST and HTTP

### 2.1 HTTP Request Methods

The browser talks to Django using **HTTP requests**. Each request has a **method** that says what it wants to do.

| Method | Purpose | Used for |
|--------|---------|----------|
| **GET** | *Read* — ask for a page | Opening a page, search, filters |
| **POST** | *Send / change* data | Register, login, add, edit, delete |
| PUT / PATCH | Update (mostly REST APIs) | — |
| DELETE | Delete (mostly REST APIs) | — |

> HTML forms only support **GET** and **POST**.

### 2.2 GET vs POST

| | GET | POST |
|---|-----|------|
| Where the data goes | In the **URL**: `/student/home3/?name=Rahul` | In the **request body** (not visible in the URL) |
| Read in Django with | `request.GET.get('name')` | `request.POST.get('name')` |
| Bookmark / share the URL | Yes | No |
| Browser history / server logs | Data is saved there | Not saved |
| Size limit | Limited by URL length | Large (files allowed) |
| Safe to repeat? | Yes — it only reads | No — it may add a record twice |
| CSRF token needed? | No | **Yes** |
| Use for | Search, filter, pagination | Passwords, registration, add/edit/delete, file upload |

**GET example from Unit 2/3 — `home3`:**

```python
def home3(request):
    name=request.GET.get('name')
    return render(request,'home.html',{"name":name})
```

`http://127.0.0.1:8000/student/home3/?name=Rahul` → the value travels **in the URL**.

**A GET form** simply uses `method="get"`; the browser builds the query string for you:

```html
<form method="get" action="/student/home3/">
    <input type="text" name="name">
    <button type="submit">Go</button>
</form>
<!-- submitting "Rahul" opens  /student/home3/?name=Rahul -->
```

### 2.3 `request.method`, `request.GET`, `request.POST`

| Attribute | Type | Contains |
|-----------|------|----------|
| `request.method` | `str` | `"GET"` or `"POST"` (always upper case) |
| `request.GET` | `QueryDict` | Values from the URL query string |
| `request.POST` | `QueryDict` | Values from a submitted POST form |
| `request.FILES` | `MultiValueDict` | Uploaded files (Section 5) |

Ways to read a value:

```python
name = request.POST.get("name")        # None if the key is missing  (safe)
name = request.POST.get("name", "")    # "" if missing               (safe, with default)
name = request.POST["name"]            # MultiValueDictKeyError if missing (crash → 500)
```

The class code uses `.get()` — the safe version. The `request.POST["name"]` line is left commented in `student_form` to show the alternative.

### 2.4 One View, Two Methods

Every form view follows the same shape: **GET shows the form, POST processes it** — both on the *same URL*.

```python
def student_form(request):
    form = ExamForm()
    if request.method=="GET":
       return render(request,"student/formstudent.html", {"form": form})

    elif request.method == "POST":
        # Process submitted form here

        name = request.POST.get("name")
        # name = request.POST["name"]
        email = request.POST.get("email")
        age = request.POST.get("age")

        print("Name:", name)
        print("Email:", email)
        print("Age", age)

        return render(request,"student/detailsstudent.html",{ "name": name, "email": email,"age": age})
```

```text
First visit           GET  /student/formnew/  →  empty form
User clicks Register  POST /student/formnew/  →  details page
```

> ⚠️ This view **displays** a Django form but reads the data **manually** with `request.POST.get()`. The form's validation never runs, so bad data gets through (verified: `name="a"`, `email="notanemail"`, `age="abc"` are all accepted). Section 3.5 shows the correct way, and Section 12 lists this as an issue.

### 2.5 The Request–Response Cycle of a Form

```text
 Browser                                   Django
 ───────                                   ──────
 1. GET /student/form23/      ───────────▶ view: request.method == "GET"
                              ◀─────────── empty form + csrftoken cookie
 2. user fills the form
 3. POST /student/form23/     ───────────▶ CsrfViewMiddleware checks the token
    (name, email, age, files,              view: form = StudentForm(request.POST, request.FILES)
     csrfmiddlewaretoken)                  form.is_valid()?
                              ◀─────────── valid   → result page / redirect
                              ◀─────────── invalid → same form + error messages
```

---

## 3. Building Forms using Django

### 3.1 Why Use Django Forms?

A Django form is a **Python class** that describes the fields once. From that one class Django:

1. **Generates the HTML** input boxes (`{{ form.as_p }}`)
2. **Validates** the submitted data (`form.is_valid()`)
3. **Converts** strings to Python types (`"21"` → `21`)
4. **Collects error messages** and shows them next to the fields
5. **Keeps the user's input** in the boxes when the form is shown again with errors

### 3.2 Steps to Build a Django Form

1. Create `forms.py` inside the app.
2. Write a class that inherits from `forms.Form`.
3. Add one **field** per input.
4. Create the form in the view and pass it to the template.
5. Show it with `{{ form.as_p }}` inside `<form>` with `{% csrf_token %}`.
6. On POST, bind it to `request.POST`, call `is_valid()`, use `cleaned_data`.

### 3.3 The Forms in `student/forms.py`

```python
import re
from django import forms

from .models import Car, Student, Cloth


class ExamForm(forms.Form):
      name = forms.CharField(required=True, min_length=3, max_length=20, error_messages={ 'min_length':'Minimum 3 characters required'})
      age = forms.IntegerField(required=False)
      email = forms.EmailField()


class Newform(forms.Form):
       name=forms.CharField()
       email=forms.EmailField()
       roll=forms.IntegerField()


class StudentForm(forms.Form):

    name = forms.CharField(required=True, max_length=100)

    email = forms.EmailField(required=True)

    age = forms.IntegerField(required=True, min_value=18, max_value=60)

    image = forms.ImageField()

    file = forms.FileField()
```

(`RegisterStudent` is covered in Section 10; `CarForm`, `StudentFormNew`, `ClothForm` in Section 6.)

### 3.4 Common Form Fields

| Field | HTML rendered | `cleaned_data` type | Useful arguments |
|-------|---------------|---------------------|------------------|
| `CharField` | `<input type="text">` | `str` | `max_length`, `min_length`, `strip` |
| `EmailField` | `<input type="email">` | `str` | checks `user@domain.tld` format |
| `IntegerField` | `<input type="number">` | `int` | `min_value`, `max_value` |
| `FloatField` / `DecimalField` | `<input type="number">` | `float` / `Decimal` | `min_value`, `max_value`, `decimal_places` |
| `BooleanField` | checkbox | `bool` | use `required=False` for an optional tick |
| `ChoiceField` | `<select>` | `str` | `choices=[("btech","B.Tech"), ...]` |
| `DateField` | `<input type="text">` | `datetime.date` | `widget=forms.DateInput(attrs={"type": "date"})` |
| `URLField` | `<input type="url">` | `str` | |
| `ImageField` | `<input type="file">` | `UploadedFile` | needs **Pillow**; checks it really is an image |
| `FileField` | `<input type="file">` | `UploadedFile` | any file |

Arguments that work on **every** field:

| Argument | Meaning | Default |
|----------|---------|---------|
| `required` | Empty value is an error | `True` |
| `label` | Text of the `<label>` | Field name, capitalised (`roll` → `Roll`) |
| `initial` | Value shown in an empty form | — |
| `help_text` | Small hint under the input | — |
| `widget` | Change the HTML element | depends on field |
| `error_messages` | Your own error text | Django's text |

**Widgets** change *how* a field looks, not what it accepts:

```python
password = forms.CharField(widget=forms.PasswordInput)               # ●●●●●
address  = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))  # multi-line box
gender   = forms.ChoiceField(choices=[("M","Male"),("F","Female")],
                             widget=forms.RadioSelect)                  # radio buttons
```

### 3.5 Unbound vs Bound Forms

| | Unbound form | Bound form |
|---|---|---|
| Created as | `ExamForm()` | `ExamForm(request.POST)` |
| Has data? | No | Yes |
| Used for | Showing an **empty** form (GET) | **Checking** submitted data (POST) |
| `form.is_bound` | `False` | `True` |
| Can call `is_valid()`? | Always returns `False` | Yes |

**Verified in the Django shell:**

```python
>>> from student.forms import ExamForm
>>> f = ExamForm()
>>> f.is_bound
False

>>> f = ExamForm(data={"name": "Rahul", "age": "21", "email": "r@lpu.in"})
>>> f.is_bound, f.is_valid()
(True, True)
>>> f.cleaned_data
{'name': 'Rahul', 'age': 21, 'email': 'r@lpu.in'}
>>> type(f.cleaned_data["age"])
<class 'int'>                     # "21" (string) became 21 (int)
```

### 3.6 `is_valid()`, `cleaned_data` and `errors`

```python
>>> f = ExamForm(data={"name": "Ra", "age": "x", "email": "bad"})
>>> f.is_valid()
False
>>> dict(f.errors)
{'name': ['Minimum 3 characters required'],        # our own error_messages text
 'age': ['Enter a whole number.'],
 'email': ['Enter a valid email address.']}

>>> f = ExamForm(data={"name": "Rahul", "email": "r@lpu.in"})   # age not sent
>>> f.is_valid(); f.cleaned_data
True
{'name': 'Rahul', 'age': None, 'email': 'r@lpu.in'}             # required=False → None
```

| Attribute / method | Meaning |
|--------------------|---------|
| `form.is_valid()` | Runs **all** validation, returns `True` / `False` |
| `form.cleaned_data` | Dictionary of **validated, converted** values (exists only after `is_valid()`) |
| `form.errors` | Dictionary `{field: [messages]}` |
| `form.non_field_errors()` | Errors not tied to one field (raised in `clean()`) |
| `form["name"].value()` | The raw value the user typed |
| `form.errors.as_json()` | Errors as JSON — handy for AJAX/APIs |

> **Golden rule:** after `is_valid()` read data from `form.cleaned_data[...]`, **never** from `request.POST[...]`.

### 3.7 The Standard Form View Pattern (`form23`)

```python
def form23(request):
    if request.method == "POST":

        form = StudentForm(request.POST, request.FILES)       # bound form
        if form.is_valid():

            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            age = form.cleaned_data["age"]
            image = form.cleaned_data["image"]
            file = form.cleaned_data["file"]

            fs=FileSystemStorage()
            if(image):
                fs.save(image.name, image)

            if(image):                       # ⚠ should be  if(file):  — see Section 12
                fs.save(file.name, file)

            return render(request, "student/detailsstudent.html",
                          {"name": name, "email": email, "age": age})

    else:

        form = StudentFormNew()              # ⚠ should be  StudentForm()  — see Section 12

    return render(request, "student/form2student.html", {"form": form})
```

The **shape** to remember:

```python
def my_view(request):
    if request.method == "POST":
        form = MyForm(request.POST)          # 1. bind
        if form.is_valid():                  # 2. validate
            data = form.cleaned_data         # 3. use clean data
            ...                              # 4. save / process
            return redirect("success")       # 5. redirect (Section 9)
    else:
        form = MyForm()                      # empty form for GET
    return render(request, "my_form.html", {"form": form})   # GET  or  invalid POST
```

The last `render()` is **outside** the `if/else` on purpose. It runs in two cases:
- a **GET** request → empty form
- an **invalid POST** → the *same bound form*, now carrying error messages and the user's typed values

**Verified — invalid POST to `/student/form23/`:**

```text
POST name="R", email="x", age="10"  →  200, form2student.html shown again with:
  Email: Enter a valid email address.
  Age:   Ensure this value is greater than or equal to 18.
  Image: This field is required.
  File:  This field is required.
```

### 3.8 A View That Skips Validation (`newform`)

```python
def newform(request):
    if(request.method=="POST"):
        return HttpResponse("Data added successfully")
    else:
        form = Newform()
        return render(request,'student/formnew.html',{'form':form})
```

`formnew.html` uses `novalidate`, so the browser does not check anything either. Result: submitting an **empty** form still prints *"Data added successfully"*. Compare it with `form23` — the missing `form = Newform(request.POST)` + `is_valid()` is the whole difference.

---

## 4. Rendering a Django Form in a Template

### 4.1 Quick Rendering Methods

| Template code | Output |
|---------------|--------|
| `{{ form }}` / `{{ form.as_div }}` | each field in a `<div>` (default since Django 5) |
| `{{ form.as_p }}` | each field in a `<p>` — **used in the class templates** |
| `{{ form.as_table }}` | `<tr>` rows (you write `<table>` yourself) |
| `{{ form.as_ul }}` | `<li>` items (you write `<ul>` yourself) |

> These print **only the fields**. You still write `<form>`, `{% csrf_token %}` and the submit button.

**`formstudent.html` (used by `student_form`):**

```html
<form method="POST">
   {% csrf_token %}
   {{form.as_p}}
   <button type="submit">Register</button>
</form>
```

**HTML that `{{ form.as_p }}` produced for `ExamForm` (verified):**

```html
<p>
    <label for="id_name">Name:</label>
    <input type="text" name="name" maxlength="20" minlength="3" required id="id_name">
</p>
<p>
    <label for="id_age">Age:</label>
    <input type="number" name="age" id="id_age">
</p>
<p>
    <label for="id_email">Email:</label>
    <input type="email" name="email" maxlength="320" required id="id_email">
</p>
```

See how the Python arguments became HTML attributes:

| Python | HTML |
|--------|------|
| `CharField(min_length=3, max_length=20)` | `minlength="3" maxlength="20"` |
| `required=True` (default) | `required` |
| `required=False` (age) | no `required` |
| `EmailField()` | `type="email"` |
| `IntegerField()` | `type="number"` |
| field name `name` | `name="name"` and `id="id_name"` |

### 4.2 Rendering Each Field Manually (`studentform.html`)

When you need your own layout, render the fields one by one:

```html
<form method="POST" enctype="multipart/form-data" novalidate>
    {% csrf_token %}

    <label>Name:</label>
    {{ form.name }}
    {% for error in form.name.errors %}
        <span style="color:red;">
            {{ error }}
        </span>
    {% endfor %}
    <br><br>

    <label>Email:</label>
    {{ form.email }}
    {% for error in form.email.errors %}
        <span style="color:red;">
            {{ error }}
        </span>
    {% endfor %}
    <br><br>

    <!-- age, country, image and file follow the same pattern -->

    <button type="submit">Register Student</button>
</form>
```

| Template code | Gives |
|---------------|-------|
| `{{ form.name }}` | only the `<input>` |
| `{{ form.name.label_tag }}` | `<label for="id_name">Name:</label>` |
| `{{ form.name.errors }}` | `<ul class="errorlist">` with the messages |
| `{% for error in form.name.errors %}` | each message, so you can style it |
| `{{ form.name.value }}` | the value currently in the box |
| `{{ form.non_field_errors }}` | errors from `clean()` |

**A shorter loop that works for any form:**

```html
{% for field in form %}
    <p>
        {{ field.label_tag }} {{ field }}
        {% for error in field.errors %}<span style="color:red;">{{ error }}</span>{% endfor %}
    </p>
{% endfor %}
```

### 4.3 Showing All Errors at the Top

Kept (commented) in `formstudent.html` and `form2student.html`:

```html
{% if form.errors %}
    <h3>There are errors:</h3>
    {{ form.errors }}
{% endif %}
```

### 4.4 `novalidate` — Browser Checks vs Server Checks

Because Django adds `required`, `minlength`, `type="email"`, the **browser** checks the form before sending it. To *see Django's* messages during class, the templates add `novalidate`:

```html
<form method="POST" novalidate>
```

| Without `novalidate` | With `novalidate` |
|----------------------|-------------------|
| Browser pop-up: "Please fill out this field" | Form is sent; Django returns its own red messages |

> Browser validation is only for convenience — anyone can switch it off. **Server-side validation (`is_valid()`) is the real protection.**

---

## 5. Uploading Images and Files with a Form

### 5.1 Three Things Are Required

| # | Where | What |
|---|-------|------|
| 1 | Template | `<form method="POST" enctype="multipart/form-data">` |
| 2 | View | Pass **both** `request.POST` **and** `request.FILES` to the form |
| 3 | Form | `forms.ImageField()` / `forms.FileField()` (ImageField needs `pip install Pillow`) |

Forget #1 or #2 and the file field is always **"This field is required."** even when a file was chosen.

### 5.2 Settings and URLs for Media Files

**`Wednesday/settings.py`**

```python
MEDIA_URL = '/media/'                 # URL prefix for uploaded files
MEDIA_ROOT = BASE_DIR / 'media'       # folder on disk where they are saved
```

**`Wednesday/urls.py`**

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ...
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
```

> `static()` serves uploaded files **only while `DEBUG = True`** (development). In production the web server (Nginx) or cloud storage serves them.

### 5.3 The Registration View with Uploads (`studentform`)

```python
def studentform(request):
    if(request.method=="POST"):

        # fetch the data from django form
        form=RegisterStudent(request.POST, request.FILES)
        if form.is_valid():
            name=form.cleaned_data['name']
            age=form.cleaned_data['age']
            email = form.cleaned_data['email']
            country = form.cleaned_data['country']
            image = form.cleaned_data['image']
            file = form.cleaned_data['file']

            fs=FileSystemStorage()

            # Save image
            if image:
                image_path = fs.save( 'images/' + image.name,image)
                image_url = fs.url(image_path)
            else:
                image_url = None

            # Save file
            if file:
                file_path = fs.save('files/' + file.name,file)
                file_url = fs.url(file_path)
            else:
                file_url = None

            print("IMAGE URL:", image_url)
            print("FILE URL:", file_url)

            return render(request, 'student/Registeredstudent.html', {'n':name, 'a':age, 'e':email, 'c':country, 'image_url': image_url,
                     'file_url': file_url})
        else:
             # FORM IS INVALID
            print(form.errors)
            return render(request,'student/studentform.html',{'form': form})

    else:
            form=RegisterStudent()
            return render(request, 'student/studentform.html',{'form':form})
```

| Code | Meaning |
|------|---------|
| `FileSystemStorage()` | Saves files inside `MEDIA_ROOT` |
| `fs.save('images/' + image.name, image)` | Writes `media/images/a.png`; returns the path actually used |
| `fs.url(path)` | Turns the path into a URL: `/media/images/a.png` |

If a file with the same name already exists, `fs.save()` adds a random suffix (`a_k3J9xQz.png`) instead of overwriting.

**Verified terminal output for a valid submission:**

```text
IMAGE URL: /media/images/a.png
FILE URL: /media/files/notes.txt
```

**`Registeredstudent.html` — showing the upload:**

```html
<h1>Student name is {{n}}</h1>
<h3>Student age is {{a}}</h3>
<h6>Student email is {{e}}</h6>
<p>Student country is {{c}}</p>

<h2>Uploaded Image</h2>
<img src="{{ image_url }}" width="300" alt="Student Image">

<h2>Uploaded File</h2>
<a href="{{ file_url }}" target="_blank">  Open Uploaded File</a>
```

### 5.4 Useful Properties of an Uploaded File

```python
image = form.cleaned_data["image"]
image.name            # "a.png"
image.size            # bytes
image.content_type    # "image/png"  (sent by the browser)
```

---

## 6. ModelForm — Forms Generated from Models

### 6.1 Why `ModelForm`?

When a form only saves a model, writing every field again is repetition. A `ModelForm` **reads the fields from the model**.

**Model — `student/models.py`**

```python
class Car(models.Model):
    brand=models.CharField()
    price=models.IntegerField()
    color=models.CharField()
    model=models.IntegerField()

    def __str__(self):
        return self.brand
```

**ModelForms — `student/forms.py`**

```python
class CarForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = '__all__'


class StudentFormNew(forms.ModelForm):
       class Meta:
            model= Student
            fields = '__all__'


class ClothForm(forms.ModelForm):
       class Meta:
              model=Cloth
              fields = '__all__'
```

**Generated by `{{ form.as_p }}` for `CarForm` (verified):** `Brand` (text), `Price` (number), `Color` (text), `Model` (number) — all `required`.

### 6.2 `forms.Form` vs `forms.ModelForm`

| | `forms.Form` | `forms.ModelForm` |
|---|---|---|
| Fields | Written by hand | Taken from the model |
| Saves to DB | You write the code | `form.save()` |
| Edit an existing row | Manual | `CarForm(request.POST, instance=car)` |
| Use when | Search, contact, login, data not stored as-is | Add / edit a model record |
| Class examples | `ExamForm`, `RegisterStudent` | `CarForm`, `StudentFormNew`, `ClothForm` |

`Meta` options:

```python
class Meta:
    model = Car
    fields = '__all__'                 # every field
    # fields = ['brand', 'price']      # only these
    # exclude = ['color']              # all except these
    # labels = {'brand': 'Car brand'}
    # widgets = {'color': forms.TextInput(attrs={'placeholder': 'Red'})}
```

### 6.3 Create and Update with a ModelForm

```python
# CREATE: Add a new car
def car_create(request):
    if request.method == 'POST':
        form = CarForm(request.POST)

        if form.is_valid():
            form.save()                       # INSERT into the table
            return redirect('car_list')       # POST/Redirect/GET (Section 9)
    else:
        form = CarForm()

    return render(request, 'student/car_form.html', {'form': form})


# UPDATE: Edit an existing car
def car_update(request, id):
    car = get_object_or_404(Car, id=id)

    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)   # change THIS car

        if form.is_valid():
            form.save()                               # UPDATE
            return redirect('car_list')
    else:
        form = CarForm(instance=car)                  # boxes pre-filled with current values

    return render(request, 'student/car_form.html', {'form': form})
```

`instance=car` is the only difference between **add** and **edit** — and both views share `car_form.html`.

> Full CRUD (list, detail, delete) and models/migrations are Unit 5. In Unit 4 the important parts are the **form**, `is_valid()`, `save()` and the **redirect**.

---

## 7. Introduction to Cross Site Request Forgery (CSRF)

### 7.1 What is CSRF?

**Cross Site Request Forgery** is an attack where a **malicious website** makes **your browser** send a request to **another website where you are logged in** — without you knowing.

It works because the browser **automatically attaches cookies** (including the login/session cookie) to every request it sends to a site.

### 7.2 The Attack, Step by Step

```text
1. You log in to  college-portal.com          → browser stores sessionid cookie
2. In another tab you open  evil-site.com
3. evil-site.com contains a hidden form:

      <form action="https://college-portal.com/student/cars/delete/5/" method="POST">
      </form>
      <script>document.forms[0].submit();</script>

4. Your browser sends the POST to college-portal.com
   AND attaches your sessionid cookie automatically
5. college-portal.com sees a valid logged-in user → record 5 is deleted
```

You never clicked anything on college-portal.com, yet the action happened **as you**.

### 7.3 What an Attacker Can Do

- change your email or password
- delete or edit records (cars, students, marks)
- submit forms, make payments, transfer money
- post content in your name

### 7.4 Why GET Is Not Protected

CSRF protection is applied to **POST, PUT, PATCH, DELETE** — methods that *change* data. GET must only *read*. That is why:

> **Rule:** never change data on a GET request. Delete/update must use POST (as `car_delete`, `stud_delete`, `cloth_delete` do).

### 7.5 How a Token Stops It

The server gives the real page a **secret token** and refuses any POST that does not send it back. The evil site cannot read that token (browsers block cross-site reading), so its forged form has no valid token → **rejected**.

---

## 8. CSRF Support in Django

### 8.1 The Middleware

CSRF protection is **on by default** through this line in `settings.py`:

```python
MIDDLEWARE = [
    ...
    'django.middleware.csrf.CsrfViewMiddleware',
    ...
]
```

It checks **every POST request** before the view runs.

### 8.2 `{% csrf_token %}`

Every POST form in the class templates contains it:

```html
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
</form>
```

It renders a **hidden input**:

```html
<input type="hidden" name="csrfmiddlewaretoken" value="6sG0x...k1Lq">
```

### 8.3 How Django Checks the Token

```text
GET page     → Django sets cookie  csrftoken=SECRET
               and puts a masked version of SECRET in the hidden input
POST submit  → browser sends  cookie csrftoken  +  field csrfmiddlewaretoken
               CsrfViewMiddleware: do they match?
                  yes → view runs
                  no / missing → 403 Forbidden, view NEVER runs
```

The evil site can make the browser send the cookie, but it cannot know the value to put in the hidden field.

### 8.4 What Happens When the Token Is Missing (verified)

```python
client = Client(enforce_csrf_checks=True)
client.post("/student/cars/add/", {...})       # no csrfmiddlewaretoken
```

```text
Forbidden (CSRF cookie not set.): /student/cars/add/
→ 403 Forbidden   "CSRF verification failed. Request aborted."

The same POST with the token from the GET page → 302 /student/cars/   (saved)
```

Common reasons for a CSRF 403 in class:

| Cause | Fix |
|-------|-----|
| Forgot `{% csrf_token %}` inside a POST form | Add it inside `<form>` |
| Token placed **outside** the `<form>` | Move it inside |
| Page opened from a file (`file://`) or cookies blocked | Open it through `runserver` |
| Used `HttpResponse` with hand-written HTML for a POST form | Use `render()` so the template tag can produce the token |

### 8.5 Exempting a View (Only When Necessary)

```python
from django.views.decorators.csrf import csrf_exempt, csrf_protect

@csrf_exempt                 # turns protection OFF for this view (e.g. a payment gateway webhook)
def webhook(request):
    ...

@csrf_protect                # forces protection ON (used when the middleware is disabled)
def my_view(request):
    ...
```

> Never use `@csrf_exempt` just to "make the 403 go away" — add the token instead.

### 8.6 CSRF with JavaScript (AJAX)

For `fetch()` POST requests, send the token in a header:

```html
<script>
fetch("/student/cars/add/", {
    method: "POST",
    headers: { "X-CSRFToken": "{{ csrf_token }}" },
    body: new FormData(document.querySelector("form"))
});
</script>
```

### 8.7 Related Settings

| Setting | Purpose |
|---------|---------|
| `CSRF_COOKIE_SECURE = True` | Send the cookie only over HTTPS (production) |
| `CSRF_TRUSTED_ORIGINS = ["https://mysite.com"]` | Allowed origins when behind a proxy / different domain |
| `CSRF_FAILURE_VIEW` | Custom page instead of the default 403 |

---

## 9. Implementing POST/Redirect/GET in Django

### 9.1 The Double-Submit Problem

`studentform` and `form23` finish a successful POST with `render(...)`. The page shown is the **result of a POST**, so when the user presses **Refresh (F5)** the browser asks:

> *"Confirm Form Resubmission — The page that you're looking for used information that you entered..."*

Clicking *Continue* sends the POST **again**. In `studentform` that means the image and file are uploaded and saved a **second** time (`a.png`, then `a_k3J9xQz.png`). In a shop it means paying twice.

### 9.2 The PRG Pattern

```text
  Browser                         Django
  POST /student/cars/add/   ──▶  form valid → save
                            ◀──  302 Found   Location: /student/cars/
  GET  /student/cars/       ──▶
                            ◀──  200 list page
  user presses F5           ──▶  repeats only the harmless GET
```

After a **successful POST**, return a **redirect**, never a page.

### 9.3 PRG in the Class Code — `car_create`

```python
def car_create(request):
    if request.method == 'POST':
        form = CarForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('car_list')      # ← POST / Redirect / GET
    else:
        form = CarForm()

    return render(request, 'student/car_form.html', {'form': form})
```

**Verified:**

```text
POST /student/cars/add/  (valid)    → 302  Location: /student/cars/
GET  /student/cars/                 → 200  "1  Honda  View Details | Edit | Delete"
POST /student/cars/add/  (invalid)  → 200  car_form.html again: "Enter a whole number."
```

The same pattern is used in `car_update`, `car_delete`, `stud_create`, `stud_update`, `stud_delete`, `cloth_add`, `cloth_update`, `cloth_delete`.

> **Only redirect when the form is valid.** An invalid POST must `render()` the same form so the errors are shown.

### 9.4 `redirect()` Accepts Three Kinds of Targets

```python
from django.shortcuts import redirect

return redirect('car_list')                      # URL name  (best — from urls.py name=...)
return redirect('car_detail', id=car.id)         # URL name + arguments
return redirect('/student/cars/')                # hard-coded path
return redirect(car)                             # a model object (needs get_absolute_url)
```

`redirect()` returns `HttpResponseRedirect` (status **302**). It is a shortcut for:

```python
from django.http import HttpResponseRedirect
from django.urls import reverse
return HttpResponseRedirect(reverse('car_list'))
```

### 9.5 Showing Submitted Data After a Redirect

A redirect starts a **new request**, so local variables are lost. To show "Registered: Rahul" on the next page, store it in the **session** (Unit 6) or use the **messages framework**.

**`studentform` rewritten with PRG (verified):**

```python
def studentform_prg(request):
    if request.method == "POST":
        form = RegisterStudent(request.POST, request.FILES)
        if form.is_valid():
            fs = FileSystemStorage()
            image_path = fs.save('images/' + form.cleaned_data['image'].name, form.cleaned_data['image'])
            file_path = fs.save('files/' + form.cleaned_data['file'].name, form.cleaned_data['file'])
            request.session['registered'] = {
                'n': form.cleaned_data['name'], 'a': form.cleaned_data['age'],
                'e': form.cleaned_data['email'], 'c': form.cleaned_data['country'],
                'image_url': fs.url(image_path), 'file_url': fs.url(file_path),
            }
            return redirect('registered')                 # POST → Redirect
    else:
        form = RegisterStudent()
    return render(request, 'student/studentform.html', {'form': form})


def registered(request):                                  # → GET
    data = request.session.pop('registered', None)        # read once, then remove
    if data is None:
        return redirect('studentform_prg')
    return render(request, 'student/Registeredstudent.html', data)
```

```python
# urls.py
path('studentform2/', views.studentform_prg, name='studentform_prg'),
path('registered/', views.registered, name='registered'),
```

```text
POST /student/studentform2/  → 302  /student/registered/
GET  /student/registered/    → 200  details + image + file link
F5 on /student/registered/   → 302  back to the empty form — nothing is uploaded again
```

**Alternative with the messages framework (already enabled in `settings.py`):**

```python
from django.contrib import messages

if form.is_valid():
    form.save()
    messages.success(request, "Car added successfully")
    return redirect('car_list')
```

```html
<!-- car_list.html -->
{% for m in messages %}
    <p style="color:green;">{{ m }}</p>
{% endfor %}
```

---

## 10. Data Validation with Django Forms

### 10.1 Why Validate on the Server?

- Browser checks (`required`, `type="email"`) can be removed with DevTools, `novalidate`, or tools like Postman.
- Bad data can break the database, crash views or create security holes.
- **Never trust `request.POST`.** Validate with `form.is_valid()` and use `form.cleaned_data`.

### 10.2 The Order in Which Django Validates

When you call `form.is_valid()`, for **each field** in order:

```text
1. field.to_python()        "21" → 21, "abc" → error "Enter a whole number."
2. field.validate()         required? choice in list?
3. field.run_validators()   min_length, max_length, min_value, email format, validators=[...]
4. form.clean_<field>()     YOUR per-field rule             (only if 1–3 passed)
then once for the whole form:
5. form.clean()             YOUR rule that uses several fields
```

If any step raises `ValidationError`, the message is stored in `form.errors` and that field is **not** put in `cleaned_data`.

### 10.3 Built-in Validation

Free with each field — no extra code (from `StudentForm` and `ExamForm`):

| Field definition | Invalid input | Message (verified) |
|------------------|---------------|--------------------|
| `CharField(required=True)` | empty | This field is required. |
| `CharField(min_length=3)` | `"Ra"` | Ensure this value has at least 3 characters (it has 2). |
| `CharField(max_length=15)` | 17 letters | Ensure this value has at most 15 characters (it has 17). |
| `EmailField()` | `"bad"` | Enter a valid email address. |
| `IntegerField()` | `"abc"` | Enter a whole number. |
| `IntegerField(min_value=18)` | `10` | Ensure this value is greater than or equal to 18. |
| `ImageField()` | a non-image file | Upload a valid image. The file you uploaded was either not an image or a corrupted image. |

### 10.4 Custom Error Messages — `error_messages`

```python
class RegisterStudent(forms.Form):
    name= forms.CharField(required=True, min_length=3, max_length=15,  error_messages={'required': 'Please enter your name.',
            'max_length': 'Name cannot contain more than 15 characters.'})
    email= forms.EmailField(error_messages={
            'required': 'Email is required.',
            'invalid': 'Please enter a valid email address.'
        })
    age=forms.IntegerField(required=False)
    country=forms.CharField()
    image=forms.ImageField()
    file=forms.FileField()
```

The **key** is the error code:

| Key | Raised when |
|-----|-------------|
| `required` | Field is empty |
| `invalid` | Wrong format (email, number, date, image) |
| `min_length` / `max_length` | Text too short / long |
| `min_value` / `max_value` | Number too small / large |
| `invalid_choice` | Value not in `choices` |

**Verified:** a 17-letter name → *"Name cannot contain more than 15 characters."*; `email="bad"` → *"Please enter a valid email address."*

### 10.5 Field-Level Custom Validation — `clean_<fieldname>()`

For a rule Django does not have, add a method named **`clean_` + field name**.

```python
    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(r'^[A-Za-z ]+$',name):
            raise forms.ValidationError(
                "Name should contain only letters and spaces."
            )
        return name

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError(
                 "Only Gmail addresses are allowed."
            )

        return email
```

Three rules for every `clean_<field>()`:

1. **Name** must match the field exactly: `clean_name` for `name`, `clean_email` for `email`.
2. **Read** the value from `self.cleaned_data['field']` (already converted and checked by built-ins).
3. **Raise** `forms.ValidationError("message")` to reject, or **return** the value to accept. Whatever you return is what ends up in `cleaned_data` — forgetting `return` makes the value `None`.

`r'^[A-Za-z ]+$'` means: from start (`^`) to end (`$`), one or more (`+`) letters or spaces.

**Verified** — POST `name="Rahul123"`, `email="rahul@yahoo.com"`, `country=""`:

```text
Name:    Name should contain only letters and spaces.
Email:   Only Gmail addresses are allowed.
Country: This field is required.
Image:   This field is required.
File:    This field is required.
```

### 10.6 Validating Uploaded Files — `clean_image()`

```python
    def clean_image(self):
        image = self.cleaned_data['image']

        if image.size > 2 * 1024 * 1024:

            raise forms.ValidationError(
                "Image must be smaller than 2 MB."
            )

        allowed_types = [
            'image/jpeg',
            'image/png'
        ]

        if image.content_type not in allowed_types:

            raise forms.ValidationError(
                "Only JPG and PNG images are allowed."
            )

        return image
```

| Check | How |
|-------|-----|
| Size limit | `image.size` is in bytes; `2 * 1024 * 1024` = 2 MB |
| Type | `image.content_type` (`image/jpeg`, `image/png`, `image/gif` ...) |

> `content_type` is reported by the **browser**, so it can be faked. `ImageField` itself already opens the file with Pillow and rejects anything that is not a real image — the two checks work together.

### 10.7 Form-Level Validation — `clean()`

Use `clean()` when the rule needs **two or more fields** (e.g. password and confirm password):

```python
class SignupForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()                 # keep the built-in checks
        p1 = cleaned_data.get("password")              # .get() — the field may have failed
        p2 = cleaned_data.get("confirm_password")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
```

The message goes into `form.non_field_errors` — show it with `{{ form.non_field_errors }}`.

To attach a form-level error to a specific field:

```python
self.add_error("confirm_password", "Passwords do not match.")
```

### 10.8 Reusable Validator Functions

When the same rule is needed on many fields or forms, write a function and pass it in `validators=[...]`:

```python
from django.core.exceptions import ValidationError

def validate_gmail(value):
    if not value.lower().endswith("@gmail.com"):
        raise ValidationError("Only Gmail addresses are allowed.")

class RegisterStudent(forms.Form):
    email = forms.EmailField(validators=[validate_gmail])
```

Django also ships ready-made validators:

```python
from django.core.validators import RegexValidator, MinLengthValidator, FileExtensionValidator

phone = forms.CharField(validators=[RegexValidator(r'^[0-9]{10}$', "Enter a 10-digit phone number.")])
file  = forms.FileField(validators=[FileExtensionValidator(['pdf', 'docx'])])
```

### 10.9 `clean_<field>()` vs `clean()` vs validator function

| | `clean_<field>()` | `clean()` | `validators=[func]` |
|---|---|---|---|
| Checks | One field | Several fields together | One field |
| Reusable in other forms | No | No | **Yes** |
| Error appears | Next to that field | `non_field_errors` (or `add_error`) | Next to that field |
| Class example | `clean_name`, `clean_email`, `clean_image` | — | — |

### 10.10 ModelForm Validation

A `ModelForm` validates automatically against the **model**: an `IntegerField` column rejects `"abc"`, a `CharField(max_length=100)` rejects long text, `unique=True` rejects duplicates. `clean_<field>()` and `clean()` can be added to a `ModelForm` in exactly the same way.

**Verified** — `POST /student/cars/add/` with `price="abc"` and no colour/model → form shown again with *"Enter a whole number."* and *"This field is required."*; nothing saved.

---

## 11. Testing Forms

All ten tests below were run against the class code and **pass**.

**`student/test_unit4.py`**

```python
import shutil, tempfile
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .forms import ExamForm, RegisterStudent
from .models import Car


def make_image(name="photo.png"):
    buffer = BytesIO()
    Image.new("RGB", (10, 10)).save(buffer, "PNG")
    return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/png")


class ExamFormTests(TestCase):
    def test_valid_data(self):
        form = ExamForm(data={"name": "Rahul", "age": "21", "email": "rahul@lpu.in"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["age"], 21)          # string "21" -> int 21

    def test_short_name_uses_custom_message(self):
        form = ExamForm(data={"name": "Ra", "email": "rahul@lpu.in"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["name"], ["Minimum 3 characters required"])

    def test_age_is_optional(self):
        form = ExamForm(data={"name": "Rahul", "email": "rahul@lpu.in"})
        self.assertTrue(form.is_valid())
        self.assertIsNone(form.cleaned_data["age"])


class RegisterStudentValidationTests(TestCase):
    def test_clean_name_rejects_digits(self):
        form = RegisterStudent(data={"name": "Rahul123"})
        form.is_valid()
        self.assertIn("Name should contain only letters and spaces.", form.errors["name"])

    def test_clean_email_allows_only_gmail(self):
        form = RegisterStudent(data={"email": "rahul@yahoo.com"})
        form.is_valid()
        self.assertIn("Only Gmail addresses are allowed.", form.errors["email"])


class CarPostRedirectTests(TestCase):
    def test_valid_post_redirects_to_list(self):
        response = self.client.post(reverse("car_create"),
                                    {"brand": "Honda", "price": 800000, "color": "Red", "model": 2024})
        self.assertRedirects(response, reverse("car_list"))
        self.assertEqual(Car.objects.count(), 1)

    def test_invalid_post_shows_form_again(self):
        response = self.client.post(reverse("car_create"), {"brand": "Honda", "price": "abc"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "student/car_form.html")
        self.assertContains(response, "Enter a whole number.")
        self.assertEqual(Car.objects.count(), 0)


class CsrfTests(TestCase):
    def test_post_without_token_is_rejected(self):
        client = Client(enforce_csrf_checks=True)       # the test client skips CSRF unless told
        response = client.post(reverse("car_create"),
                               {"brand": "Kia", "price": 1, "color": "Red", "model": 2024})
        self.assertEqual(response.status_code, 403)

    def test_form_page_contains_token(self):
        response = self.client.get(reverse("car_create"))
        self.assertContains(response, "csrfmiddlewaretoken")


MEDIA = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA)                    # don't fill the real media/ folder
class FileUploadTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA, ignore_errors=True)
        super().tearDownClass()

    def test_valid_registration_with_files(self):
        response = self.client.post("/student/studentform/", {
            "name": "Rahul Kumar", "email": "rahul@gmail.com", "age": 20, "country": "India",
            "image": make_image(), "file": SimpleUploadedFile("notes.txt", b"hello"),
        })
        self.assertTemplateUsed(response, "student/Registeredstudent.html")
        self.assertEqual(response.context["n"], "Rahul Kumar")
        self.assertTrue(response.context["image_url"].startswith("/media/images/"))
```

```bash
python manage.py test student.test_unit4
```

```text
Ran 10 tests in 0.113s
OK
```

| What to test | How |
|--------------|-----|
| Valid data accepted | `form.is_valid()` is `True`, check `cleaned_data` types |
| Each rule rejects bad data | `form.errors["field"]` contains your message |
| Successful POST redirects | `assertRedirects(response, url)` |
| Invalid POST re-shows form | status 200 + `assertTemplateUsed` + `assertContains(error)` |
| CSRF | `Client(enforce_csrf_checks=True)` → 403 |
| Uploads | `SimpleUploadedFile` + `override_settings(MEDIA_ROOT=tmp)` |

---

## 12. Issues Found in the Class Code (and Fixes)

These were found by running the project. They make good discussion points — each one maps to a Unit 4 concept.

### Issue 1 — Project does not start: URLs point to views that do not exist ❗

`student/urls.py` contains:

```python
path('djangoform/', views.djangoform),
path('register/', views.registration),
path('examform/', views.examform),
path('examreg/', views.examreg),
path('clothes/', views.clothes_list, name="clothes_list"),
path('clothes/add/', views.clothes_add, name="clothes_add"),
path('clothes/detail/<int:id>/', views.clothes_details, name="clothes_details"),
path('clothes/update/<int:id>/', views.clothes_update, name="clothes_update"),
path('clothes/deleye/<int:id>/', views.clothes_delete, name="clothes_delete"),
```

but `views.py` has no `djangoform`, `registration`, `examform`, `examreg` or `clothes_*` functions. Python reads `urls.py` when the server starts, so **every page fails**:

```text
AttributeError: module 'student.views' has no attribute 'djangoform'
```

**Fix:** delete (or comment out) those nine lines, or write the missing views. The working equivalents already exist: `studentform`, `newform`, and the `cloth_*` views.

### Issue 2 — `form23` shows the wrong form on GET

```python
    else:
        form = StudentFormNew()          # ModelForm for Student: roll_no, name, marks
```

GET shows *Roll no / Name / Marks*, but POST validates `StudentForm` (*name, email, age, image, file*). The user can never submit successfully from the first page.

**Fix:** `form = StudentForm()` — verified: GET now shows name, email, age, image, file.

### Issue 3 — `form23` checks `image` before saving `file`

```python
            if(image):
                fs.save(file.name, file)     # condition checks the wrong variable
```

**Fix:** `if(file):`

### Issue 4 — `cloth_add` and `cloth_update` crash on invalid data

```python
def cloth_add(request):
    if(request.method=="POST"):
        form=ClothForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('cloth_list')
    else:
        form=ClothForm()
        return render(request, 'student/cloth_add.html', {'form':form})   # only inside else
```

An invalid POST reaches the end of the function and returns nothing (verified):

```text
ValueError: The view student.views.cloth_add didn't return an HttpResponse object. It returned None instead.
→ 500 Internal Server Error
```

`cloth_update` has the same problem.

**Fix — move the final `render()` out of the `else` (as `car_create` does):**

```python
def cloth_add(request):
    if request.method == "POST":
        form = ClothForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cloth_list')
    else:
        form = ClothForm()
    return render(request, 'student/cloth_add.html', {'form': form})   # outside if/else
```

Verified after the fix: invalid POST → 200 with error messages, for both add and update.

### Issue 5 — `student_form` shows a Django form but skips validation

It reads `request.POST.get(...)` directly, so `ExamForm`'s rules never run (verified: `name="a"`, `email="notanemail"`, `age="abc"` are all accepted).

**Fix:**

```python
def student_form(request):
    if request.method == "POST":
        form = ExamForm(request.POST)
        if form.is_valid():
            return render(request, "student/detailsstudent.html", form.cleaned_data)
    else:
        form = ExamForm()
    return render(request, "student/formstudent.html", {"form": form})
```

### Issue 6 — `newform` accepts anything

The POST branch returns *"Data added successfully"* without creating `Newform(request.POST)` or calling `is_valid()`. Fix it the same way as Issue 5.

### Issue 7 — `studentform` and `form23` don't follow POST/Redirect/GET

A successful POST ends with `render()`, so refreshing the page resubmits the form and **uploads the files again**. See the verified `studentform_prg` / `registered` version in Section 9.5.

### Issue 8 — `clean_email` is case-sensitive

`rahul@GMAIL.com` is rejected with *"Only Gmail addresses are allowed."* (verified).

**Fix:** `if not email.lower().endswith('@gmail.com'):`

### Issue 9 — Small template issues

| File | Issue |
|------|-------|
| `formstudent.html` | Two `<title>` tags (one empty) |
| `formstudent.html` | Title text "Regsitration" (spelling) |
| `stud_form.html`, `car_form.html`, `cloth_add.html` | Do not extend `base.html` from Unit 3 — no navbar/footer |

---

## 13. URL → View → Template Map for Unit 4

All URLs start with `/student/`.

| URL | Name | View | Form class | Template(s) | Topic |
|-----|------|------|------------|-------------|-------|
| `addstudent/` | — | `studentadd` | none (plain HTML) | `studentrecord.html` → `showrecord.html` | Intro, GET/POST |
| `formnew/` | — | `student_form` | `ExamForm` | `formstudent.html` → `detailsstudent.html` | Django form display |
| `newform/` | — | `newform` | `Newform` | `formnew.html` | Building forms |
| `form23/` | — | `form23` | `StudentForm` | `form2student.html` → `detailsstudent.html` | `is_valid`, uploads |
| `studentform/` | — | `studentform` | `RegisterStudent` | `studentform.html` → `Registeredstudent.html` | Validation, uploads, manual rendering |
| `cars/` | `car_list` | `car_list` | — | `car_list.html` | PRG target |
| `cars/add/` | `car_create` | `car_create` | `CarForm` | `car_form.html` | ModelForm, PRG, CSRF |
| `cars/edit/<int:id>/` | `car_update` | `car_update` | `CarForm` | `car_form.html` | `instance=` |
| `cars/delete/<int:id>/` | `car_delete` | `car_delete` | — | `car_confirm_delete.html` | Delete via POST |
| `studs/add/` | `stud_create` | `stud_create` | `StudentFormNew` | `stud_form.html` | ModelForm, PRG |
| `cloths/add/` | `cloth_add` | `cloth_add` | `ClothForm` | `cloth_add.html` | ModelForm (see Issue 4) |

---

## 14. Summary and Practice Questions

### 14.1 Unit Summary

| Concept | Key Point |
|---------|-----------|
| HTML form | `method`, `action`, inputs with `name=`; empty `action` = same URL |
| GET | Data in URL, `request.GET`, safe to repeat — search/filter |
| POST | Data in body, `request.POST`, changes data — needs CSRF token |
| One view, two methods | `if request.method == "POST": ... else: ...` |
| `forms.Form` | Python class → HTML + validation + type conversion |
| Unbound / bound | `Form()` for display, `Form(request.POST)` for checking |
| `is_valid()` | Runs all validation; then read `cleaned_data` |
| Rendering | `{{ form.as_p }}` or field by field with `{{ form.name.errors }}` |
| `novalidate` | Skip browser checks to see Django's messages |
| File upload | `enctype="multipart/form-data"` + `request.FILES` + `MEDIA_ROOT` |
| `ModelForm` | Fields from the model, `form.save()`, `instance=` for edit |
| CSRF | Evil site uses your logged-in cookies to send a forged POST |
| `{% csrf_token %}` | Hidden token checked by `CsrfViewMiddleware`; missing → 403 |
| PRG | Successful POST → `redirect()` (302) → GET; refresh is harmless |
| Built-in validation | `required`, `min/max_length`, `min/max_value`, email/number format |
| `error_messages` | Replace Django's message per error code |
| `clean_<field>()` | One-field rule; raise `ValidationError` or return the value |
| `clean()` | Multi-field rule; error in `non_field_errors` |
| Validator function | Reusable rule via `validators=[...]` |

### 14.2 Practice Questions

**Short answer (2 marks)**

1. Write two differences between GET and POST.
2. What happens if an `<input>` has no `name` attribute?
3. Differentiate between a bound and an unbound form.
4. Why should data be read from `cleaned_data` and not from `request.POST` after validation?
5. What is the purpose of `enctype="multipart/form-data"`?
6. What status code does Django return when the CSRF token is missing?
7. Why is `{% csrf_token %}` not needed in a GET form?
8. What does `instance=car` do in `CarForm(request.POST, instance=car)`?
9. Write the naming rule for a field-level validation method.

**Medium answer (5 marks)**

10. Explain the CSRF attack with a step-by-step example and how Django's token prevents it.
11. Explain the POST/Redirect/GET pattern. Why should an invalid form **not** be redirected?
12. Write a Django form `FeedbackForm` with `name` (3–30 characters), `email`, `rating` (1–5) and `comments` (textarea), with a custom message for a missing name.
13. Compare `forms.Form` and `forms.ModelForm` with one use case each.
14. List the steps required to upload an image through a Django form and display it on the next page.
15. Explain the order in which Django runs validation when `is_valid()` is called.

**Long answer (10 marks)**

16. Write `forms.py`, the view, the URL and the template for a **student registration** page with: name (letters only), email (must end with `@lpu.in`), age (17–30), password and confirm password (must match). Show errors next to each field and redirect to a success page after a valid submission.
17. The `cloth_add` view in the class code returns a 500 error for invalid data. Explain why, rewrite the view correctly, and write two test cases: one proving that valid data redirects and one proving that invalid data shows the form again with status 200.
18. Build a **car add/edit** feature using one `ModelForm`, one template and two views (`car_create`, `car_update`), using PRG and CSRF protection. Explain how the same template works for both.
19. Write `clean_image()` that accepts only JPG/PNG files under 2 MB, and a `clean()` method that ensures `start_date` is before `end_date`. Explain where each error appears in the template.

---

*End of Unit 4 — Forms in Django*
