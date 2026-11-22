# Unit 5 — Models and Migrations and Django Admin

> **Scope:** Creating models, working with migrations, using the Django shell to explore models (insert, update and delete), using Object Relational Mapping (ORM), models using foreign keys, the `auth_user` table and its CRUD from the shell, Django admin, adding groups and users, users and permissions, and database configuration — configuring and setting up a database connection.
>
> **Code source:** `Wednesday` project → `student` app (`models.py`, `migrations/0001_initial.py`, `admin.py`, `views.py`) and `Wednesday/settings.py` in the class repository.
>
> **Tested on:** Django 6.x, Python 3.12+, **PostgreSQL 16** using the exact `DATABASES` setting from the class project. Every shell session in this file is a real transcript.

---

## Table of Contents

1. [Introduction to Models and the ORM](#1-introduction-to-models-and-the-orm)
2. [Creating Models](#2-creating-models)
3. [Working with Migrations](#3-working-with-migrations)
4. [Using the Django Shell — CRUD on Normal Models](#4-using-the-django-shell--crud-on-normal-models)
5. [Using Object Relational Mapping (ORM)](#5-using-object-relational-mapping-orm)
6. [Models using Foreign Keys](#6-models-using-foreign-keys)
7. [The `auth_user` Table — CRUD from the Shell](#7-the-auth_user-table--crud-from-the-shell)
8. [Django Admin](#8-django-admin)
9. [Adding Groups and Users](#9-adding-groups-and-users)
10. [Users and Permissions](#10-users-and-permissions)
11. [Database Configuration — Setting Up a Database Connection](#11-database-configuration--setting-up-a-database-connection)
12. [Testing Models](#12-testing-models)
13. [Issues Found in the Class Code (and Fixes)](#13-issues-found-in-the-class-code-and-fixes)
14. [Summary and Practice Questions](#14-summary-and-practice-questions)

---

## Project Files Used in This Unit

```text
Wednesday/
├── manage.py
├── Wednesday/
│   └── settings.py                 # DATABASES → PostgreSQL "jot"
└── student/
    ├── models.py                   # Student, User, Car, Cloth, Stud, Department, Employee
    ├── migrations/
    │   ├── __init__.py
    │   └── 0001_initial.py         # creates all 7 tables
    ├── admin.py                    # registers Car, User, Cloth, Department, Employee
    ├── forms.py                    # CarForm, StudentFormNew, ClothForm (ModelForms — Unit 4)
    ├── views.py                    # car_*, stud_*, cloth_* CRUD views
    │                               # createuser, showusers, updateuser, deleteuser (auth User)
    └── templates/student/
        ├── car_list.html  car_detail.html  car_form.html  car_confirm_delete.html
        ├── stud_list.html stud_detail.html stud_form.html stud_confirm_delete.html
        ├── cloth_list.html cloth_details.html cloth_add.html cloth_confirm_delete.html
        └── users.html
```

---

## 1. Introduction to Models and the ORM

### 1.1 What is a Model?

A **model** is a Python class that describes **one database table**.

| Python (model) | Database |
|----------------|----------|
| Class `Car` | Table `student_car` |
| Attribute `brand = models.CharField()` | Column `brand varchar` |
| One object `Car(brand="Honda", ...)` | One row |
| `Car.objects` | The whole table (for queries) |

### 1.2 Models in the MVT Architecture

```text
Browser ──▶ urls.py ──▶ View ──▶ Model ──▶ Database (PostgreSQL)
                         │         ◀── rows as Python objects
                         ▼
                      Template ──▶ HTML ──▶ Browser
```

Until Unit 4 our data lived in Python lists and dictionaries inside views and disappeared on restart. From this unit, data is stored **permanently** in a database.

### 1.3 What is an ORM?

**ORM — Object Relational Mapping** — lets us work with database tables using Python objects instead of writing SQL.

| Task | SQL | Django ORM |
|------|-----|-----------|
| Insert | `INSERT INTO student_student (roll_no, name, marks) VALUES (102, 'Priya', 91);` | `Student.objects.create(roll_no=102, name="Priya", marks=91)` |
| Read all | `SELECT * FROM student_student;` | `Student.objects.all()` |
| Filter | `SELECT * FROM student_student WHERE marks >= 80;` | `Student.objects.filter(marks__gte=80)` |
| Update | `UPDATE student_student SET marks = 82 WHERE roll_no = 101;` | `Student.objects.filter(roll_no=101).update(marks=82)` |
| Delete | `DELETE FROM student_student WHERE roll_no = 105;` | `Student.objects.filter(roll_no=105).delete()` |

**Advantages of the ORM:**

- Same Python code works on SQLite, PostgreSQL, MySQL, Oracle — only `settings.py` changes
- Protection against **SQL injection** (values are always sent as parameters)
- Results come back as Python objects with attributes (`student.name`)
- Table structure is kept in sync through **migrations**

---

## 2. Creating Models

### 2.1 Steps

1. App must be in `INSTALLED_APPS` (`'student'` is already there).
2. Write the class in `student/models.py`, inheriting from `models.Model`.
3. Run `python manage.py makemigrations` → creates the migration file.
4. Run `python manage.py migrate` → creates the table.
5. (Optional) Register it in `admin.py`.

### 2.2 The Models in `student/models.py`

```python
from django.db import models

# Create your models here.

class Student(models.Model):
    roll_no=models.IntegerField()
    name=models.CharField(max_length=100)
    marks=models.FloatField()

    def __str__(self):
        return self.name


class  User(models.Model):
    name=models.CharField(max_length=100)
    price=models.FloatField()

    def __str__(self):
        return self.name


class Car(models.Model):
    brand=models.CharField()
    price=models.IntegerField()
    color=models.CharField()
    model=models.IntegerField()

    def __str__(self):
        return self.brand


class Cloth(models.Model):
    name=models.CharField()
    color=models.CharField()
    price=models.IntegerField()

    def __str__(self):
        return self.name

class Stud(models.Model):
    roll_no=models.IntegerField()
    name=models.CharField(max_length=100)
    marks=models.FloatField()

    def __str__(self):
        return self.name

class Department(models.Model):
    dept_name = models.CharField(max_length=100)

    def __str__(self):
        return self.dept_name


class Employee(models.Model):
    emp_name = models.CharField(max_length=100)
    email = models.EmailField()
    dept = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.emp_name
```

### 2.3 Things Django Adds Automatically

| Automatic | Detail |
|-----------|--------|
| Primary key `id` | `BigAutoField` — 1, 2, 3 ... (set by `DEFAULT_AUTO_FIELD`) |
| Table name | `<app_label>_<model name in lower case>` → `student_car`, `student_employee` |
| Manager `objects` | `Car.objects` — the entry point for all queries |
| 4 permissions | `add_car`, `change_car`, `delete_car`, `view_car` (Section 10) |

### 2.4 Why `__str__()`?

```python
>>> Student.objects.all()
<QuerySet [<Student: Rahul>, <Student: Priya>]>          # with __str__ returning self.name
<QuerySet [<Student: Student object (1)>, ...]>         # without __str__
```

`__str__` controls how an object is printed — in the shell, in templates (`{{ car }}` in `car_list.html` shows the brand), and in the admin.

### 2.5 Common Field Types

| Field | Database column (PostgreSQL) | Python value | Notes |
|-------|------------------------------|--------------|-------|
| `CharField(max_length=100)` | `varchar(100)` | `str` | `max_length` may be skipped **only** on PostgreSQL/SQLite |
| `TextField()` | `text` | `str` | Long text, no length limit |
| `IntegerField()` | `integer` | `int` | |
| `BigIntegerField()` | `bigint` | `int` | |
| `PositiveIntegerField()` | `integer` + check ≥ 0 | `int` | |
| `FloatField()` | `double precision` | `float` | `marks` in `Student` |
| `DecimalField(max_digits=8, decimal_places=2)` | `numeric(8,2)` | `Decimal` | Use for money |
| `BooleanField(default=False)` | `boolean` | `bool` | |
| `DateField()` / `DateTimeField()` | `date` / `timestamp with time zone` | `date` / `datetime` | `auto_now_add=True`, `auto_now=True` |
| `EmailField()` | `varchar(254)` | `str` | Validates email format in forms |
| `URLField()`, `SlugField()` | `varchar` | `str` | |
| `ImageField(upload_to="images/")` | `varchar(100)` (stores the path) | file | Needs Pillow |
| `FileField(upload_to="files/")` | `varchar(100)` | file | |
| `ForeignKey(Model, on_delete=...)` | `bigint` + FK constraint | object | Section 6 |
| `ManyToManyField(Model)` | extra join table | manager | |
| `OneToOneField(Model, on_delete=...)` | unique FK | object | |

### 2.6 Common Field Options

| Option | Effect | Example |
|--------|--------|---------|
| `max_length` | Maximum characters | `CharField(max_length=100)` |
| `null=True` | Database allows `NULL` | `DateField(null=True)` |
| `blank=True` | Forms / admin allow empty | `CharField(blank=True)` |
| `default` | Value when none given | `BooleanField(default=True)` |
| `unique=True` | No duplicates (DB constraint) | `IntegerField(unique=True)` for `roll_no` |
| `choices` | Fixed list of allowed values | `choices=[("P","Petrol"),("D","Diesel")]` |
| `verbose_name` | Human label in admin/forms | `CharField("Car brand", ...)` |
| `db_index=True` | Create an index for faster search | |
| `help_text` | Hint under the field in forms/admin | |

> `null` is about the **database**, `blank` is about **validation**. For an optional text field use `blank=True` only; for an optional number/date use `null=True, blank=True`.

### 2.7 `class Meta` — Model-Level Options

```python
class Student(models.Model):
    roll_no = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    marks = models.FloatField()

    class Meta:
        ordering = ["roll_no"]              # default order for every query
        db_table = "students"               # custom table name
        verbose_name_plural = "Students"    # name shown in admin
```

---

## 3. Working with Migrations

### 3.1 What is a Migration?

A **migration** is a Python file that records a **change to the database structure** (create table, add column, rename, delete). Migrations are Django's **version control for the database**.

```text
models.py  ──makemigrations──▶  migrations/0001_initial.py  ──migrate──▶  tables in PostgreSQL
 (what you want)                  (the plan, saved in git)                 (the real database)
```

### 3.2 Migration Commands

| Command | What it does |
|---------|--------------|
| `python manage.py makemigrations` | Compares `models.py` with existing migrations and writes a new migration file |
| `python manage.py makemigrations student` | Same, only for the `student` app |
| `python manage.py migrate` | Runs all unapplied migrations on the database |
| `python manage.py migrate student 0001` | Moves the `student` app to migration 0001 (rollback) |
| `python manage.py migrate student zero` | Unapplies every migration of `student` (drops its tables) |
| `python manage.py showmigrations` | Lists migrations — `[X]` applied, `[ ]` not applied |
| `python manage.py sqlmigrate student 0001` | Prints the SQL a migration will run (does not run it) |
| `python manage.py makemigrations --check --dry-run` | Reports whether models and migrations are out of sync |

### 3.3 The First `migrate` on a New Database (verified, PostgreSQL)

```text
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, student
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  ...
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
  Applying student.0001_initial... OK
```

Built-in apps (`auth`, `admin`, `sessions`, `contenttypes`) also have migrations — that is where `auth_user`, `django_session` and the other tables come from.

**Tables now in the `jot` database:**

```text
jot=> \dt
 public | auth_group                 | table | django_jot
 public | auth_group_permissions     | table | django_jot
 public | auth_permission            | table | django_jot
 public | auth_user                  | table | django_jot
 public | auth_user_groups           | table | django_jot
 public | auth_user_user_permissions | table | django_jot
 public | django_admin_log           | table | django_jot
 public | django_content_type        | table | django_jot
 public | django_migrations          | table | django_jot
 public | django_session             | table | django_jot
 public | student_car                | table | django_jot
 public | student_cloth              | table | django_jot
 public | student_department         | table | django_jot
 public | student_employee           | table | django_jot
 public | student_stud               | table | django_jot
 public | student_student            | table | django_jot
 public | student_user               | table | django_jot
(17 rows)
```

| Table | Created by | Holds |
|-------|-----------|-------|
| `student_*` | our `student` app | our models |
| `auth_user` | `django.contrib.auth` | login users (Section 7) |
| `auth_group`, `auth_permission` + link tables | `django.contrib.auth` | groups and permissions (Sections 9–10) |
| `django_session` | `django.contrib.sessions` | session data (Unit 6) |
| `django_admin_log` | `django.contrib.admin` | history of admin actions |
| `django_content_type` | `django.contrib.contenttypes` | one row per model — permissions point to it |
| `django_migrations` | Django | which migrations have been applied |

### 3.4 Anatomy of `0001_initial.py` (class project)

```python
# Generated by Django 6.0.7 on 2026-11-16 06:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField()),
                ('price', models.IntegerField()),
                ('color', models.CharField()),
                ('model', models.IntegerField()),
            ],
        ),
        # ... Cloth, Department, Stud, Student, User ...
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.department')),
            ],
        ),
    ]
```

| Part | Meaning |
|------|---------|
| `initial = True` | First migration of the app |
| `dependencies` | Migrations that must run before this one |
| `operations` | List of changes: `CreateModel`, `AddField`, `AlterField`, `RemoveField`, `DeleteModel`, `RenameField` ... |

### 3.5 The SQL Behind a Migration — `sqlmigrate` (PostgreSQL)

```text
$ python manage.py sqlmigrate student 0001
BEGIN;
-- Create model Car
CREATE TABLE "student_car" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
  "brand" varchar NOT NULL, "price" integer NOT NULL, "color" varchar NOT NULL, "model" integer NOT NULL);
-- Create model Cloth
CREATE TABLE "student_cloth" (... "name" varchar NOT NULL, "color" varchar NOT NULL, "price" integer NOT NULL);
-- Create model Department
CREATE TABLE "student_department" (... "dept_name" varchar(100) NOT NULL);
-- Create model Stud
CREATE TABLE "student_stud" (... "roll_no" integer NOT NULL, "name" varchar(100) NOT NULL, "marks" double precision NOT NULL);
-- Create model Student
CREATE TABLE "student_student" (... "roll_no" integer NOT NULL, "name" varchar(100) NOT NULL, "marks" double precision NOT NULL);
-- Create model User
CREATE TABLE "student_user" (... "name" varchar(100) NOT NULL, "price" double precision NOT NULL);
-- Create model Employee
CREATE TABLE "student_employee" (... "emp_name" varchar(100) NOT NULL, "email" varchar(254) NOT NULL, "dept_id" bigint NOT NULL);
ALTER TABLE "student_employee" ADD CONSTRAINT "student_employee_dept_id_0ab6109a_fk_student_department_id"
  FOREIGN KEY ("dept_id") REFERENCES "student_department" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "student_employee_dept_id_0ab6109a" ON "student_employee" ("dept_id");
COMMIT;
```

Notice: every column is `NOT NULL` by default; `CharField()` without `max_length` became plain `varchar`; the `ForeignKey` named `dept` became the column **`dept_id`** with a foreign-key constraint and an index.

### 3.6 Changing a Model — Add a Column (verified)

Add a field to `Car`:

```python
class Car(models.Model):
    brand=models.CharField()
    price=models.IntegerField()
    color=models.CharField()
    model=models.IntegerField()
    fuel=models.CharField(max_length=20, default="Petrol")      # NEW
```

```text
$ python manage.py makemigrations student
Migrations for 'student':
  student/migrations/0002_car_fuel.py
    + Add field fuel to car

$ python manage.py sqlmigrate student 0002
BEGIN;
-- Add field fuel to car
ALTER TABLE "student_car" ADD COLUMN "fuel" varchar(20) DEFAULT 'Petrol' NOT NULL;
ALTER TABLE "student_car" ALTER COLUMN "fuel" DROP DEFAULT;
COMMIT;

$ python manage.py migrate student
Running migrations:
  Applying student.0002_car_fuel... OK

$ python manage.py showmigrations student
student
 [X] 0001_initial
 [X] 0002_car_fuel
```

Generated file `0002_car_fuel.py`:

```python
class Migration(migrations.Migration):

    dependencies = [
        ("student", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="car",
            name="fuel",
            field=models.CharField(default="Petrol", max_length=20),
        ),
    ]
```

### 3.7 Adding a Required Field to a Table That Already Has Rows

Without a `default`, Django cannot fill the new column for existing rows and asks (verified):

```text
It is impossible to add a non-nullable field 'fuel' to car without specifying a default.
This is because the database needs something to populate existing rows.
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit and manually define a default value in models.py.
Select an option:
```

Fixes: give `default="Petrol"`, or make it optional with `null=True, blank=True`, or choose option 1 and type a value.

### 3.8 Rolling Back (verified)

```text
$ python manage.py migrate student 0001
Running migrations:
  Rendering model states... DONE
  Unapplying student.0002_car_fuel... OK

$ python manage.py showmigrations student
student
 [X] 0001_initial
 [ ] 0002_car_fuel
```

The column `fuel` is dropped from the table, but the file `0002_car_fuel.py` stays. Delete the file **and** remove the field from `models.py` if you no longer want it.

### 3.9 Rules for Working with Migrations

1. Run `makemigrations` **every time** you change `models.py`, then `migrate`.
2. **Commit migration files to git** — every student / server builds the same tables from them.
3. Don't edit or delete a migration that has already been applied on another machine.
4. Changing `max_length`, adding `unique=True`, renaming a field — all need a new migration.
5. Changing only `__str__`, methods, or `Meta.ordering` does not change the table (ordering still creates a small migration — it is harmless).
6. `django_migrations` table records what has been applied:

```sql
SELECT app, name, applied FROM django_migrations WHERE app = 'student';
```

---

## 4. Using the Django Shell — CRUD on Normal Models

### 4.1 Opening the Shell

```bash
python manage.py shell
```

It is a normal Python prompt with your project's settings and database already loaded. (Django 5.2+ also auto-imports all models — it prints e.g. *"15 objects imported automatically"*. The `import` lines below are still shown so the code also works in older versions and in `views.py`.)

Exit with `exit()` or `Ctrl + D` (Mac/Linux) / `Ctrl + Z` then Enter (Windows).

### 4.2 CREATE — Inserting Records

**Way 1 — create an object, then `save()`:**

```python
>>> from student.models import Student
>>> s = Student(roll_no=101, name="Rahul", marks=78.5)
>>> s.id                     # None — nothing is in the database yet
>>> s.save()                 # INSERT runs here
>>> s.id
1
```

**Way 2 — `objects.create()` (create + save in one step):**

```python
>>> Student.objects.create(roll_no=102, name="Priya", marks=91.0)
<Student: Priya>
```

**Way 3 — `bulk_create()` (many rows in one query):**

```python
>>> Student.objects.bulk_create([Student(roll_no=103, name="Aman", marks=65.0), Student(roll_no=104, name="Neha", marks=88.0), Student(roll_no=105, name="Ankit", marks=42.5)])
[<Student: Aman>, <Student: Neha>, <Student: Ankit>]
```

| Method | Queries | Returns |
|--------|---------|---------|
| `obj.save()` | 1 | `None` (object now has an `id`) |
| `Model.objects.create(...)` | 1 | the new object |
| `Model.objects.bulk_create([...])` | 1 for all | list of objects |
| `Model.objects.get_or_create(roll_no=101, defaults={...})` | 1–2 | `(object, created_bool)` |

### 4.3 READ — Fetching Records

```python
>>> Student.objects.all()
<QuerySet [<Student: Rahul>, <Student: Priya>, <Student: Aman>, <Student: Neha>, <Student: Ankit>]>
>>> Student.objects.count()
5
>>> Student.objects.get(roll_no=102)
<Student: Priya>
>>> Student.objects.get(id=1).name
'Rahul'
>>> Student.objects.filter(marks__gte=80)
<QuerySet [<Student: Priya>, <Student: Neha>]>
>>> Student.objects.exclude(marks__gte=80)
<QuerySet [<Student: Rahul>, <Student: Aman>, <Student: Ankit>]>
>>> Student.objects.order_by("-marks")
<QuerySet [<Student: Priya>, <Student: Neha>, <Student: Rahul>, <Student: Aman>, <Student: Ankit>]>
>>> Student.objects.order_by("-marks")[:3]
<QuerySet [<Student: Priya>, <Student: Neha>, <Student: Rahul>]>
>>> Student.objects.values("name", "marks")
<QuerySet [{'name': 'Rahul', 'marks': 78.5}, {'name': 'Priya', 'marks': 91.0}, {'name': 'Aman', 'marks': 65.0}, {'name': 'Neha', 'marks': 88.0}, {'name': 'Ankit', 'marks': 42.5}]>
>>> Student.objects.values_list("name", flat=True)
<QuerySet ['Rahul', 'Priya', 'Aman', 'Neha', 'Ankit']>
>>> Student.objects.first()
<Student: Rahul>
>>> Student.objects.last()
<Student: Ankit>
>>> Student.objects.filter(roll_no=999).exists()
False
```

**`get()` must match exactly one row:**

```python
>>> Student.objects.get(roll_no=999)
Traceback (most recent call last):
  ...
student.models.Student.DoesNotExist: Student matching query does not exist.

>>> Student.objects.get(marks__gt=50)
Traceback (most recent call last):
  ...
student.models.Student.MultipleObjectsReturned: get() returned more than one Student -- it returned 4!
```

| Method | Returns | When nothing matches | When many match |
|--------|---------|----------------------|-----------------|
| `get()` | one object | `DoesNotExist` error | `MultipleObjectsReturned` error |
| `filter()` | QuerySet | empty QuerySet `[]` | QuerySet of all |
| `first()` / `last()` | one object | `None` | first / last one |
| `exists()` | `bool` | `False` | `True` |

In views use `get_object_or_404(Car, id=id)` — it turns `DoesNotExist` into a **404 page** (as in `car_detail`, `car_update`, `car_delete`).

### 4.4 UPDATE — Changing Records

**Way 1 — fetch, change, `save()` (one object):**

```python
>>> s = Student.objects.get(roll_no=101)
>>> s.marks = 82.0
>>> s.save()                       # UPDATE runs here — forget this and nothing changes
>>> Student.objects.get(roll_no=101).marks
82.0
```

**Way 2 — `update()` on a QuerySet (many rows, one query, no `save()`):**

```python
>>> Student.objects.filter(marks__lt=50).update(marks=50)
1                                   # number of rows changed
>>> Student.objects.get(roll_no=105).marks
50.0
```

| | `obj.save()` | `queryset.update()` |
|---|---|---|
| Rows | one | any number |
| Queries | SELECT + UPDATE | one UPDATE |
| Returns | `None` | number of rows updated |
| Runs model `save()` logic / `auto_now` | Yes | No |

### 4.5 DELETE — Removing Records

```python
>>> s = Student.objects.get(roll_no=105)
>>> s.delete()
(1, {'student.Student': 1})              # (total deleted, per model)

>>> Student.objects.filter(marks__lt=70).delete()
(1, {'student.Student': 1})

>>> Student.objects.count()
3
```

```python
Student.objects.all().delete()         # ⚠ deletes EVERY row of the table
```

### 4.6 The Same CRUD on `Car` and `Cloth`

```python
>>> from student.models import Car, Cloth
>>> Car.objects.create(brand="Honda", price=800000, color="Red", model=2024)
>>> Car.objects.create(brand="Kia", price=1200000, color="White", model=2023)
>>> Car.objects.filter(price__lt=1000000)               # cheaper than 10 lakh
>>> Car.objects.filter(color="Red").update(price=850000)
>>> Car.objects.get(brand="Kia").delete()

>>> Cloth.objects.create(name="Shirt", color="Blue", price=799)
>>> Cloth.objects.order_by("price").values_list("name", "price")
```

### 4.7 CRUD Cheat Sheet

| Operation | Shell / view code |
|-----------|-------------------|
| **C**reate | `Model.objects.create(**fields)` or `obj = Model(...); obj.save()` |
| **R**ead all | `Model.objects.all()` |
| **R**ead one | `Model.objects.get(id=1)` / `get_object_or_404(Model, id=1)` |
| **R**ead some | `Model.objects.filter(...)`, `.exclude(...)`, `.order_by(...)` |
| **U**pdate one | `obj = Model.objects.get(...); obj.field = x; obj.save()` |
| **U**pdate many | `Model.objects.filter(...).update(field=x)` |
| **D**elete one | `Model.objects.get(...).delete()` |
| **D**elete many | `Model.objects.filter(...).delete()` |

### 4.8 The Same CRUD from Views — `car_*` in the Class Code

The shell commands above are exactly what the class views run, wrapped in forms and templates:

```python
# READ: Display all cars
def car_list(request):
    cars = Car.objects.all()
    return render(request, 'student/car_list.html', {'cars': cars})

# CREATE: Add a new car
def car_create(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()                                  # INSERT
            return redirect('car_list')
    else:
        form = CarForm()
    return render(request, 'student/car_form.html', {'form': form})

# VIEW: Display complete details of a car
def car_detail(request, id):
    car = get_object_or_404(Car, id=id)                  # SELECT ... WHERE id = ...
    return render(request, 'student/car_detail.html', {'car': car})

# UPDATE: Edit an existing car
def car_update(request, id):
    car = get_object_or_404(Car, id=id)
    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()                                  # UPDATE
            return redirect('car_list')
    else:
        form = CarForm(instance=car)
    return render(request, 'student/car_form.html', {'form': form})

# DELETE: Delete an existing car
def car_delete(request, id):
    car = get_object_or_404(Car, id=id)
    if request.method == 'POST':
        car.delete()                                     # DELETE
        return redirect('car_list')
    return render(request, 'student/car_confirm_delete.html', {'car': car})
```

| URL | Name | Operation |
|-----|------|-----------|
| `/student/cars/` | `car_list` | Read all |
| `/student/cars/add/` | `car_create` | Create |
| `/student/cars/details/<id>/` | `car_detail` | Read one |
| `/student/cars/edit/<id>/` | `car_update` | Update |
| `/student/cars/delete/<id>/` | `car_delete` | Delete (confirm on GET, delete on POST) |

`stud_*` (model `Student`) and `cloth_*` (model `Cloth`) follow the same five-view pattern.

---

## 5. Using Object Relational Mapping (ORM)

### 5.1 Managers and QuerySets

- **Manager** — `Model.objects`, the gateway to the table.
- **QuerySet** — the result of `all()`, `filter()`, `exclude()`, `order_by()` ... — a list-like collection of objects that can be **chained**:

```python
Student.objects.filter(marks__gte=60).exclude(name="Rahul").order_by("-marks")[:5]
```

### 5.2 QuerySets Are Lazy — See the SQL

Building a QuerySet does **not** hit the database; it runs only when the data is needed (loop, `print`, `len()`, `list()`, slicing with a step, template `{% for %}`).

```python
>>> qs = Student.objects.filter(marks__gte=70)        # no query yet
>>> print(qs.query)                                    # the SQL Django will send
SELECT "student_student"."id", "student_student"."roll_no", "student_student"."name", "student_student"."marks" FROM "student_student" WHERE "student_student"."marks" >= 70.0
```

### 5.3 Field Lookups (`field__lookup=value`)

| Lookup | SQL | Example |
|--------|-----|---------|
| `exact` (default) | `=` | `filter(name="Rahul")` |
| `iexact` | case-insensitive `=` | `filter(name__iexact="rahul")` |
| `gt`, `gte`, `lt`, `lte` | `>`, `>=`, `<`, `<=` | `filter(marks__gte=80)` |
| `contains` / `icontains` | `LIKE '%x%'` | `filter(name__icontains="an")` |
| `startswith` / `endswith` | `LIKE 'x%'` / `'%x'` | `filter(name__startswith="A")` |
| `in` | `IN (...)` | `filter(roll_no__in=[101, 105])` |
| `range` | `BETWEEN` | `filter(marks__range=(60, 90))` |
| `isnull` | `IS NULL` | `filter(email__isnull=True)` |
| `year`, `month`, `day` | date parts | `filter(date_joined__year=2026)` |
| `fk__field` | JOIN | `filter(dept__dept_name="CSE")` (Section 6) |

**Verified on the class data:**

```python
>>> Student.objects.filter(name__startswith="A")
<QuerySet [<Student: Aman>, <Student: Ankit>]>
>>> Student.objects.filter(name__icontains="an")
<QuerySet [<Student: Aman>, <Student: Ankit>]>
>>> Student.objects.filter(roll_no__in=[101, 105])
<QuerySet [<Student: Rahul>, <Student: Ankit>]>
>>> Student.objects.filter(marks__range=(60, 90))
<QuerySet [<Student: Rahul>, <Student: Aman>, <Student: Neha>]>
```

### 5.4 AND, OR, NOT — `Q` Objects

```python
>>> from django.db.models import Q, F, Avg, Max, Min, Sum, Count

>>> Student.objects.filter(marks__gte=60, name__startswith="S")            # AND
<QuerySet [<Student: Sonia>]>
>>> Student.objects.filter(Q(marks__gte=90) | Q(name__startswith="R"))     # OR
<QuerySet [<Student: Priya>, <Student: Rahul>, <Student: Ravi>]>
>>> Student.objects.filter(~Q(name="Rahul"))                               # NOT
<QuerySet [<Student: Priya>, <Student: Neha>, <Student: Ravi>, <Student: Sonia>]>
```

### 5.5 `F` Expressions — Use a Column's Own Value

```python
>>> Student.objects.filter(roll_no=106).update(marks=F("marks") + 5)    # grace marks
1
>>> Student.objects.get(roll_no=106).marks
60.0                                                                   # was 55
```

The addition happens **inside the database** (`SET marks = marks + 5`), so it is safe even if two users update at the same time.

### 5.6 Aggregation and Annotation

```python
>>> Student.objects.aggregate(Avg("marks"), Max("marks"), Min("marks"))
{'marks__avg': 77.8, 'marks__max': 91.0, 'marks__min': 55.0}
>>> Student.objects.aggregate(total=Sum("marks"))
{'total': 389.0}
```

- `aggregate()` → **one dictionary** for the whole table.
- `annotate()` → adds a calculated value **to every row** (example with foreign keys in Section 6.6).

### 5.7 Ordering in PostgreSQL — Always Use `order_by()`

```python
>>> Student.objects.all()        # after some updates (verified)
<QuerySet [<Student: Priya>, <Student: Neha>, <Student: Rahul>, <Student: Ravi>, <Student: Sonia>]>
```

Rahul (id 1) is no longer first. SQL databases — PostgreSQL especially — return rows in **no guaranteed order** unless you ask for one. Use `order_by("roll_no")` in the query or `ordering = ["roll_no"]` in `class Meta`. (`first()` and `last()` order by `id` automatically when no order is set.)

### 5.8 Useful QuerySet Methods

| Method | Returns |
|--------|---------|
| `all()`, `filter()`, `exclude()`, `order_by()`, `distinct()` | QuerySet |
| `values("a", "b")` | QuerySet of dictionaries |
| `values_list("a", flat=True)` | QuerySet of plain values |
| `select_related("fk")` | QuerySet with the FK loaded by a JOIN |
| `get()`, `first()`, `last()`, `latest("field")` | one object |
| `count()`, `exists()`, `aggregate()` | number / bool / dict |
| `create()`, `bulk_create()`, `get_or_create()`, `update_or_create()` | object(s) |
| `update()`, `delete()` | rows changed / deleted |

---

## 6. Models using Foreign Keys

### 6.1 One-to-Many Relationship

**One department has many employees; each employee belongs to one department.**

```python
class Department(models.Model):
    dept_name = models.CharField(max_length=100)

    def __str__(self):
        return self.dept_name


class Employee(models.Model):
    emp_name = models.CharField(max_length=100)
    email = models.EmailField()
    dept = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.emp_name
```

The `ForeignKey` is written on the **"many"** side (`Employee`).

### 6.2 How It Looks in PostgreSQL (verified)

```text
jot=> \d student_employee
  Column  |          Type          | Nullable |             Default
----------+------------------------+----------+----------------------------------
 id       | bigint                 | not null | generated by default as identity
 emp_name | character varying(100) | not null |
 email    | character varying(254) | not null |
 dept_id  | bigint                 | not null |
Indexes:
    "student_employee_pkey" PRIMARY KEY, btree (id)
    "student_employee_dept_id_0ab6109a" btree (dept_id)
Foreign-key constraints:
    "student_employee_dept_id_0ab6109a_fk_student_department_id"
        FOREIGN KEY (dept_id) REFERENCES student_department(id) DEFERRABLE INITIALLY DEFERRED
```

```text
 student_department            student_employee
 ┌────┬───────────┐            ┌────┬──────────┬────────────────┬─────────┐
 │ id │ dept_name │            │ id │ emp_name │ email          │ dept_id │
 ├────┼───────────┤            ├────┼──────────┼────────────────┼─────────┤
 │ 1  │ CSE       │◀───────────│ 1  │ Rohit    │ rohit@lpu.in   │ 1       │
 │ 2  │ ECE       │◀──┐        │ 2  │ Simran   │ simran@lpu.in  │ 1       │
 └────┴───────────┘   └────────│ 3  │ Karan    │ karan@lpu.in   │ 2       │
                               └────┴──────────┴────────────────┴─────────┘
```

### 6.3 Foreign Keys in the Shell (verified)

**Create — pass the object, or its id:**

```python
>>> from student.models import Department, Employee
>>> cse = Department.objects.create(dept_name="CSE")
>>> ece = Department.objects.create(dept_name="ECE")
>>> e1 = Employee.objects.create(emp_name="Rohit", email="rohit@lpu.in", dept=cse)
>>> Employee.objects.create(emp_name="Simran", email="simran@lpu.in", dept=cse)
<Employee: Simran>
>>> Employee.objects.create(emp_name="Karan", email="karan@lpu.in", dept_id=ece.id)
<Employee: Karan>
```

**Forward access — employee → department:**

```python
>>> e1.dept
<Department: CSE>
>>> e1.dept.dept_name
'CSE'
>>> e1.dept_id
1
```

**Reverse access — department → employees (`<model>_set`):**

```python
>>> cse.employee_set.all()
<QuerySet [<Employee: Rohit>, <Employee: Simran>]>
>>> cse.employee_set.count()
2
>>> cse.employee_set.create(emp_name="Meena", email="meena@lpu.in")    # dept filled automatically
<Employee: Meena>
```

**Filtering across the relationship (double underscore = JOIN):**

```python
>>> Employee.objects.filter(dept__dept_name="CSE")
<QuerySet [<Employee: Rohit>, <Employee: Simran>, <Employee: Meena>]>
>>> Department.objects.filter(employee__emp_name="Karan")
<QuerySet [<Department: ECE>]>
```

**Update — move an employee to another department:**

```python
>>> e = Employee.objects.get(emp_name="Karan")
>>> e.dept = cse
>>> e.save()
>>> cse.employee_set.count()
4
```

**The database refuses a department that doesn't exist:**

```python
>>> Employee.objects.create(emp_name="Ghost", email="g@lpu.in", dept_id=999)
django.db.utils.IntegrityError: insert or update on table "student_employee" violates foreign key constraint
"student_employee_dept_id_0ab6109a_fk_student_department_id"
DETAIL:  Key (dept_id)=(999) is not present in table "student_department".
```

**Delete with `CASCADE`:**

```python
>>> cse.delete()
(5, {'student.Employee': 4, 'student.Department': 1})    # 1 department + its 4 employees
>>> Employee.objects.all()
<QuerySet []>
```

### 6.4 `on_delete` Options

What happens to employees when their department is deleted?

| Option | Effect |
|--------|--------|
| `models.CASCADE` | Delete the employees too *(class code)* |
| `models.PROTECT` | Refuse to delete the department (`ProtectedError`) while employees exist |
| `models.RESTRICT` | Like PROTECT, but allows deletion if it is part of a bigger cascade |
| `models.SET_NULL` | Set `dept` to `NULL` (field needs `null=True`) |
| `models.SET_DEFAULT` | Set `dept` to its `default` |
| `models.DO_NOTHING` | Do nothing in Django (database may raise an error) |

### 6.5 `related_name` — A Better Name for the Reverse Side

```python
dept = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="employees")
```

```python
cse.employees.all()          # instead of cse.employee_set.all()
```

### 6.6 Counting Per Department — `annotate()`

```python
>>> Department.objects.annotate(total=Count("employee")).values("dept_name", "total")
<QuerySet [{'dept_name': 'ECE', 'total': 0}]>          # (after CSE was deleted above)
```

### 6.7 `select_related()` — Avoid Extra Queries

```python
>>> Employee.objects.select_related("dept").get(emp_name="Karan").dept.dept_name
'ECE'
```

Without `select_related`, a loop over 100 employees printing `e.dept.dept_name` runs **101 queries** (the N+1 problem from the Unit 3 Debug Toolbar section). With it — **1 query** using a JOIN.

### 6.8 Foreign Keys in Templates

```html
{% for e in employees %}
    <p>{{ e.emp_name }} — {{ e.dept.dept_name }}</p>
{% endfor %}

<h3>{{ department.dept_name }}</h3>
{% for e in department.employee_set.all %}      {# no () in templates #}
    <li>{{ e.emp_name }}</li>
{% endfor %}
```

### 6.9 Other Relationships (Overview)

| Relationship | Field | Example |
|--------------|-------|---------|
| One-to-many | `ForeignKey` | many employees → one department |
| Many-to-many | `ManyToManyField` | students ↔ courses (Django makes a link table) |
| One-to-one | `OneToOneField` | one `User` ↔ one `Profile` |

---

## 7. The `auth_user` Table — CRUD from the Shell

### 7.1 Django's Built-in `User` Model

`django.contrib.auth` (already in `INSTALLED_APPS`) provides a ready-made **`User`** model stored in the **`auth_user`** table. It is used for login, admin access, groups and permissions.

```python
from django.contrib.auth.models import User
```

**Structure (verified on PostgreSQL):**

```text
jot=> \d auth_user
    Column    |           Type           | Nullable |             Default
--------------+--------------------------+----------+----------------------------------
 id           | integer                  | not null | generated by default as identity
 password     | character varying(128)   | not null |
 last_login   | timestamp with time zone |          |
 is_superuser | boolean                  | not null |
 username     | character varying(150)   | not null |
 first_name   | character varying(150)   | not null |
 last_name    | character varying(150)   | not null |
 email        | character varying(254)   | not null |
 is_staff     | boolean                  | not null |
 is_active    | boolean                  | not null |
 date_joined  | timestamp with time zone | not null |
Indexes:
    "auth_user_pkey" PRIMARY KEY, btree (id)
    "auth_user_username_key" UNIQUE CONSTRAINT, btree (username)
```

| Column | Meaning |
|--------|---------|
| `username` | **Unique**, case-sensitive login name (`Navjot` ≠ `navjot`) |
| `password` | **Hashed** password — never plain text |
| `is_active` | `False` = account disabled, cannot log in |
| `is_staff` | `True` = can log in to `/admin/` |
| `is_superuser` | `True` = has **every** permission |
| `last_login` | Updated automatically on login |
| `date_joined` | Set automatically when created |

Related tables:

| Table | Holds |
|-------|-------|
| `auth_group` | Groups (`Faculty`, `Viewer`) |
| `auth_permission` | All permissions (`add_car`, ...) |
| `auth_user_groups` | Which user is in which group |
| `auth_group_permissions` | Which permission each group has |
| `auth_user_user_permissions` | Permissions given directly to a user |

### 7.2 CREATE — Users

```python
>>> from django.contrib.auth.models import User
>>> u = User.objects.create_user(username="navjot", email="navjot@lpu.in", password="Navjot@123")
>>> u
<User: navjot>
>>> u.id, u.username, u.email
(1, 'navjot', 'navjot@lpu.in')
>>> u.password
'pbkdf2_sha256$1500000$BHmTiw5a7FvoX8S21KgRMT$RR3QL4WA2hfU9TSfllXAW2lG0X8B9uqCaTcCYt9MycM='
>>> u.is_staff, u.is_superuser, u.is_active
(False, False, True)
>>> u.date_joined
datetime.datetime(2026, 11, 22, 16, 16, 9, 547544, tzinfo=datetime.timezone.utc)
```

The stored password is `algorithm$iterations$salt$hash` — the original `Navjot@123` cannot be read back.

**Superuser and extra fields:**

```python
>>> User.objects.create_superuser(username="admin", email="admin@lpu.in", password="Admin@123")
<User: admin>
>>> User.objects.create_user("rahul", "rahul@lpu.in", "Rahul@123", first_name="Rahul", last_name="Sharma")
<User: rahul>
```

**⚠ Wrong way — `create()` stores the password as plain text:**

```python
>>> User.objects.create(username="plain", password="plain123")
<User: plain>
>>> User.objects.get(username="plain").password
'plain123'                                  # not hashed → this user can never log in
```

| Method | Password | Flags set |
|--------|----------|-----------|
| `User.objects.create_user(username, email, password)` | hashed ✔ | `is_staff=False`, `is_superuser=False` |
| `User.objects.create_superuser(username, email, password)` | hashed ✔ | `is_staff=True`, `is_superuser=True` |
| `User.objects.create(...)` | **plain text ✘** | — |

**`username` is unique:**

```python
>>> User.objects.create_user(username="navjot", password="x")
django.db.utils.IntegrityError: duplicate key value violates unique constraint "auth_user_username_key"
DETAIL:  Key (username)=(navjot) already exists.
```

### 7.3 READ — Users

```python
>>> User.objects.all()
<QuerySet [<User: navjot>, <User: admin>, <User: rahul>, <User: plain>]>
>>> User.objects.count()
4
>>> User.objects.get(username="rahul").get_full_name()
'Rahul Sharma'
>>> User.objects.filter(is_superuser=True)
<QuerySet [<User: admin>]>
>>> User.objects.filter(email__endswith="@lpu.in").values_list("username", flat=True)
<QuerySet ['navjot', 'admin', 'rahul']>
>>> User.objects.filter(username="nobody").exists()
False
```

**Checking a password:**

```python
>>> u = User.objects.get(username="navjot")
>>> u.check_password("Navjot@123")
True
>>> u.check_password("wrong")
False
```

### 7.4 UPDATE — Users

**Profile fields — change and `save()`:**

```python
>>> u.email = "navjot@gmail.com"
>>> u.first_name = "Navjot"
>>> u.save()
>>> User.objects.get(username="navjot").email
'navjot@gmail.com'
```

**Password — always with `set_password()` (it hashes), then `save()`:**

```python
>>> u.set_password("NewPass@456")
>>> u.save()
>>> u.check_password("NewPass@456")
True
```

> `u.password = "NewPass@456"` would store plain text — never assign `password` directly.

**Flags for many users at once:**

```python
>>> User.objects.filter(username="rahul").update(is_staff=True)
1
>>> User.objects.get(username="rahul").is_staff
True
```

**Deactivate instead of delete (keeps history, blocks login):**

```python
>>> u.is_active = False
>>> u.save()
>>> from django.contrib.auth import authenticate
>>> authenticate(username="navjot", password="NewPass@456")        # None — inactive user
>>> u.is_active = True
>>> u.save()
>>> authenticate(username="navjot", password="NewPass@456")
<User: navjot>
>>> authenticate(username="navjot", password="wrong")              # None — wrong password
```

### 7.5 DELETE — Users

```python
>>> User.objects.get(username="plain").delete()
(1, {'auth.User': 1})
>>> User.objects.values_list("username", flat=True)
<QuerySet ['admin', 'rahul', 'navjot']>
```

Deleting a user also removes its rows in `auth_user_groups`, `auth_user_user_permissions` and `django_admin_log` (cascade).

### 7.6 What the `auth_user` Table Looks Like Now (verified)

```text
jot=> SELECT id, username, email, is_staff, is_superuser, is_active, left(password,30)||'...' AS password FROM auth_user ORDER BY id;
 id | username |      email       | is_staff | is_superuser | is_active |             password
----+----------+------------------+----------+--------------+-----------+-----------------------------------
  1 | navjot   | navjot@gmail.com | f        | f            | t         | pbkdf2_sha256$1500000$1Alxg2at...
  2 | admin    | admin@lpu.in     | t        | t            | t         | pbkdf2_sha256$1500000$3CNw1g6K...
  3 | rahul    | rahul@lpu.in     | t        | f            | t         | pbkdf2_sha256$1500000$cPXz6xLW...
```

### 7.7 `auth_user` CRUD Cheat Sheet

| Operation | Code |
|-----------|------|
| Create user | `User.objects.create_user("name", "mail", "pass")` |
| Create superuser | `User.objects.create_superuser(...)` or `python manage.py createsuperuser` |
| Read | `User.objects.all()`, `get(username=...)`, `filter(is_staff=True)` |
| Check password | `user.check_password("pass")` / `authenticate(username=..., password=...)` |
| Update details | `user.email = ...; user.save()` |
| Change password | `user.set_password("new"); user.save()` or `python manage.py changepassword name` |
| Make staff / admin | `user.is_staff = True` / `user.is_superuser = True`, then `save()` |
| Disable | `user.is_active = False; user.save()` |
| Delete | `User.objects.get(username=...).delete()` |

### 7.8 `auth_user` CRUD from Views — Class Code

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
    return render(request, 'student/users.html', {'users': users})

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

```html
<!-- users.html -->
<h2>Registered Users</h2>
{% for user in users %}
    <p>{{ user.username }}</p>
    <p>{{ user.email }}</p>
{% endfor %}
```

| URL | Name | Operation |
|-----|------|-----------|
| `/student/createuser/` | `createuser` | Create `Parveen` |
| `/student/alluser/` | `alluser` | Read all users |
| `/student/updateuser/` | `updateuser` | Update `Navjot`'s email |
| `/student/deleteuser/` | `deleteuser` | Delete `Navjot` |

These views work as a first demo, but they break in real use (opening `createuser` twice, or `Navjot` not existing) — see Issues 3 and 4 in Section 13 for verified improved versions.

### 7.9 Two Different `User` Models in This Project

The `student` app also defines its own `class User(models.Model)` with `name` and `price`. It is a **different table** (`student_user`) and has nothing to do with login:

```python
>>> from student.models import User
>>> User
<class 'student.models.User'>
>>> User.objects.all()
<QuerySet []>                                 # student_user table

>>> from django.contrib.auth.models import User as AuthUser
>>> AuthUser.objects.count()
3                                             # auth_user table
```

Whichever `User` was imported **last** wins. `views.py` imports `from django.contrib.auth.models import User`, so the views use `auth_user`. In the admin both appear as **"Users"** (one under *Authentication and Authorization*, one under *Student*). See Issue 1.

---

## 8. Django Admin

### 8.1 What is the Django Admin?

A ready-made, password-protected website at **`/admin/`** for managing the data of every registered model — list, search, filter, add, edit and delete — without writing any views or templates. It is meant for **staff**, not the public.

It is enabled by default:

```python
# settings.py
INSTALLED_APPS = ['django.contrib.admin', 'django.contrib.auth', ...]

# Wednesday/urls.py
path('admin/', admin.site.urls),
```

### 8.2 Creating a Superuser

```bash
python manage.py createsuperuser
```

```text
Username (leave blank to use 'pritpalsingh'): admin
Email address: admin@lpu.in
Password:
Password (again):
Superuser created successfully.
```

Non-interactive version (useful for scripts):

```bash
DJANGO_SUPERUSER_PASSWORD=Teacher@123 python manage.py createsuperuser --noinput --username teacher --email teacher@lpu.in
```

Then run `python manage.py runserver` and open `http://127.0.0.1:8000/admin/`.

> If you forget a password: `python manage.py changepassword admin`

### 8.3 Registering Models — Class Code

```python
from django.contrib import admin
from .models import  Car, User, Cloth, Department, Employee

# Register your models here.
# admin.site.register(Student)
admin.site.register(Car)
admin.site.register(User)
admin.site.register(Cloth)
admin.site.register(Department)
admin.site.register(Employee)
```

**Admin home page (verified):**

```text
Site administration
  AUTHENTICATION AND AUTHORIZATION
      Groups        + Add   Change
      Users         + Add   Change
  STUDENT
      Cars          + Add   Change
      Cloths        + Add   Change
      Departments   + Add   Change
      Employees     + Add   Change
      Users         + Add   Change      ← student.User, not the login users
```

`Student` is commented out, so it does not appear.

For an `Employee`, the **Dept** field automatically appears as a drop-down of departments (because it is a `ForeignKey`), with a **+** button to add a new department.

### 8.4 Customising the Admin with `ModelAdmin`

The class `admin.py` already contains (commented) the next step. Verified working version:

```python
from django.contrib import admin
from .models import Car, User, Cloth, Department, Employee, Student

admin.site.register(User)
admin.site.register(Cloth)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'model', 'color', 'price')   # columns in the list
    list_filter = ('brand', 'color')                             # filter sidebar
    search_fields = ('brand', 'color')                           # search box
    ordering = ('-price',)                                       # default sort
    list_per_page = 10                                           # pagination


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'name', 'marks')
    search_fields = ('name',)
    list_editable = ('marks',)                                   # edit marks directly in the list
    ordering = ('roll_no',)


class EmployeeInline(admin.TabularInline):                       # employees inside the department page
    model = Employee
    extra = 1


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'dept_name')
    search_fields = ('dept_name',)
    inlines = [EmployeeInline]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'emp_name', 'email', 'dept')
    search_fields = ('emp_name', 'email')
    list_filter = ('dept',)
```

> A model can be registered **only once**. Uncommenting `@admin.register(Department)` while `admin.site.register(Department)` is still active gives `AlreadyRegistered` — remove the plain `register()` line for any model you customise.

| `ModelAdmin` option | Effect |
|---------------------|--------|
| `list_display` | Columns shown in the list page |
| `list_filter` | Right-side filter panel |
| `search_fields` | Search box (`'dept__dept_name'` searches across the FK) |
| `ordering` | Default sort order |
| `list_editable` | Edit fields directly in the list (must also be in `list_display`, not the first column) |
| `list_per_page` | Rows per page |
| `readonly_fields` | Shown but not editable |
| `fields` / `fieldsets` | Which fields appear on the edit page and how they are grouped |
| `inlines` | Edit related (FK) rows on the parent's page |
| `date_hierarchy` | Date drill-down bar (needs a date field) |

### 8.5 Admin and the Model

- Labels come from field names (`emp_name` → *Emp name*) or `verbose_name`.
- `blank=True` makes a field optional in the admin form; otherwise it is required.
- `__str__` is used in drop-downs and list pages — without it you see *"Employee object (3)"*.
- Every add/change/delete is recorded in `django_admin_log` and shown under **Recent actions** and **History**.

---

## 9. Adding Groups and Users

### 9.1 Why Groups?

Instead of giving 10 permissions to each of 50 faculty members one by one, create a **group** (`Faculty`), give the permissions **to the group**, then add users to it. Changing the group changes everyone in it.

### 9.2 Using the Admin

**Add a user:**

1. `/admin/` → *Authentication and Authorization* → **Users** → **Add user**
2. Enter username and password twice → **Save** (password is hashed automatically)
3. On the next page fill first name, last name, email
4. **Permissions** section:
   - ☑ **Active** — can log in
   - ☑ **Staff status** — can log in to the admin
   - ☐ **Superuser status** — all permissions (only for administrators)
5. Choose **Groups** and/or individual **User permissions** → **Save**

**Add a group:**

1. **Groups** → **Add group**
2. Name: `Faculty`
3. Move permissions from *Available* to *Chosen*, e.g. `student | car | Can add car`, `Can change car`, `Can view car`
4. **Save**
5. Open a user → **Groups** → choose `Faculty` → **Save**

> A user with **Staff status** but **no permissions** can log in to `/admin/` but sees *"You don't have permission to view or edit anything."*

### 9.3 Using the Shell (verified)

```python
>>> from django.contrib.auth.models import User, Group, Permission

>>> faculty = Group.objects.create(name="Faculty")
>>> viewer = Group.objects.create(name="Viewer")

>>> faculty.permissions.add(*Permission.objects.filter(codename__in=["view_car", "add_car", "change_car"]))
>>> viewer.permissions.add(Permission.objects.get(codename="view_car"))
>>> faculty.permissions.values_list("codename", flat=True)
<QuerySet ['add_car', 'change_car', 'view_car']>

>>> rahul = User.objects.get(username="rahul")
>>> rahul.groups.add(faculty)
>>> rahul.groups.all()
<QuerySet [<Group: Faculty>]>
>>> faculty.user_set.all()                    # reverse: users in a group
<QuerySet [<User: rahul>]>

>>> rahul.groups.remove(faculty)              # take the user out
```

| Task | Code |
|------|------|
| Create group | `Group.objects.create(name="Faculty")` or `get_or_create(...)` |
| Add permissions | `group.permissions.add(p1, p2)` / `.set([...])` / `.remove(p)` / `.clear()` |
| Add user to group | `user.groups.add(group)` |
| Remove user | `user.groups.remove(group)` |
| Users in a group | `group.user_set.all()` |
| Groups of a user | `user.groups.all()` |

**Group permissions in the database (verified):**

```text
jot=> SELECT g.name, p.codename FROM auth_group_permissions gp
      JOIN auth_group g ON g.id = gp.group_id
      JOIN auth_permission p ON p.id = gp.permission_id ORDER BY 1, 2;
  name   |  codename
---------+------------
 Faculty | add_car
 Faculty | change_car
 Faculty | view_car
 Viewer  | view_car
```

---

## 10. Users and Permissions

### 10.1 Default Permissions

For **every model**, `migrate` automatically creates four permissions:

```python
>>> Permission.objects.filter(content_type__app_label="student", content_type__model="car").values_list("codename", "name")
<QuerySet [('add_car', 'Can add car'), ('change_car', 'Can change car'), ('delete_car', 'Can delete car'), ('view_car', 'Can view car')]>
>>> Permission.objects.filter(content_type__app_label="student").count()
28                                   # 7 models × 4
```

A permission is written as **`<app_label>.<action>_<model>`** — e.g. `student.add_car`, `student.delete_employee`.

### 10.2 Three Kinds of Access

| Flag / source | Gives |
|---------------|-------|
| `is_superuser=True` | **Every** permission, always |
| Group permissions | Every permission of every group the user is in |
| User permissions | Permissions assigned directly to that user |

A user's final permissions = **group permissions + user permissions** (or everything, for a superuser).

`is_staff` is **not** a permission — it only lets the user *enter* `/admin/`. What they can do there depends on their permissions.

### 10.3 Checking Permissions (verified)

```python
>>> rahul = User.objects.get(username="rahul")
>>> rahul.groups.add(faculty)
>>> rahul.has_perm("student.add_car")
True
>>> rahul.has_perm("student.delete_car")
False
>>> rahul.get_group_permissions()
{'student.view_car', 'student.add_car', 'student.change_car'}

>>> rahul.user_permissions.add(Permission.objects.get(codename="delete_car"))   # direct permission
>>> rahul.has_perm("student.delete_car")
False                                       # ⚠ still False — permissions are cached on this object
>>> rahul = User.objects.get(username="rahul")                                  # fetch again
>>> rahul.has_perm("student.delete_car")
True
>>> sorted(rahul.get_all_permissions())
['student.add_car', 'student.change_car', 'student.delete_car', 'student.view_car']

>>> admin = User.objects.get(username="admin")
>>> admin.has_perm("student.delete_car")
True
>>> admin.has_perm("anything.at_all")
True                                        # superuser passes every check
```

| Method | Returns |
|--------|---------|
| `user.has_perm("app.codename")` | `True` / `False` |
| `user.has_perms(["app.a", "app.b"])` | `True` only if all |
| `user.get_all_permissions()` | set of all permission strings |
| `user.get_group_permissions()` | set from groups only |
| `user.user_permissions.add(p)` / `.remove(p)` | give / take a direct permission |

> **Permission cache:** after changing a user's groups or permissions, fetch the user again (`User.objects.get(...)`) before calling `has_perm()`. In a web request this happens automatically on the next request.

### 10.4 Protecting Views with Permissions

```python
from django.contrib.auth.decorators import login_required, permission_required


@permission_required('student.delete_car', raise_exception=True)
def car_delete_protected(request, id):
    car = get_object_or_404(Car, id=id)
    if request.method == 'POST':
        car.delete()
        return redirect('car_list')
    return render(request, 'student/car_confirm_delete.html', {'car': car})
```

**Verified:**

```text
navjot (no permission) → 403 Forbidden
admin  (superuser)     → 200 confirm page
```

| Decorator | If the check fails |
|-----------|--------------------|
| `@login_required` | Redirect to `LOGIN_URL` (`/login/` in the class settings) |
| `@permission_required('app.perm')` | Redirect to login |
| `@permission_required('app.perm', raise_exception=True)` | **403 Forbidden** |

Inside a view without a decorator:

```python
if not request.user.has_perm('student.change_car'):
    return HttpResponse("You are not allowed", status=403)
```

### 10.5 Permissions in Templates

The `auth` context processor gives every template `user` and `perms`:

```html
{% if perms.student.add_car %}
    <a href="{% url 'car_create' %}">Add New Car</a>
{% endif %}

{% if perms.student.delete_car %}
    <a href="{% url 'car_delete' car.id %}">Delete</a>
{% endif %}
```

Hiding a link is only cosmetic — always protect the **view** too.

### 10.6 Custom Permissions

```python
class Car(models.Model):
    ...
    class Meta:
        permissions = [
            ("approve_car", "Can approve car listing"),
        ]
```

After `makemigrations` + `migrate`: `user.has_perm("student.approve_car")`.

---

## 11. Database Configuration — Setting Up a Database Connection

### 11.1 The `DATABASES` Setting

All database details live in **one place** — `settings.py`. Models, views and the ORM code never change when the database changes.

| Key | Meaning |
|-----|---------|
| `ENGINE` | Which database backend |
| `NAME` | Database name (for SQLite: the file path) |
| `USER`, `PASSWORD` | Login for the database server |
| `HOST`, `PORT` | Where the server runs |

| Database | `ENGINE` | Python driver | Default port |
|----------|----------|---------------|--------------|
| SQLite | `django.db.backends.sqlite3` | built in | — (a file) |
| PostgreSQL | `django.db.backends.postgresql` | `psycopg` (or `psycopg2`) | 5432 |
| MySQL / MariaDB | `django.db.backends.mysql` | `mysqlclient` | 3306 |
| Oracle | `django.db.backends.oracle` | `oracledb` | 1521 |

### 11.2 SQLite — the Default

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

A single file, nothing to install — perfect for learning. Not suitable for many simultaneous users in production.

### 11.3 PostgreSQL — Class Configuration

**`Wednesday/settings.py` (class project):**

```python
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
       'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'jot',
        'USER': 'django_jot',
        'PASSWORD': 'jot123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**Step-by-step setup:**

**Step 1 — Install PostgreSQL** (and keep the server running)

| OS | Command / installer |
|----|--------------------|
| macOS | `brew install postgresql@16` then `brew services start postgresql@16` (or Postgres.app) |
| Windows | Installer from postgresql.org (includes pgAdmin) |
| Ubuntu | `sudo apt install postgresql` |

**Step 2 — Create the database and user** (in `psql` or pgAdmin's Query Tool)

```sql
CREATE USER django_jot WITH PASSWORD 'jot123';
CREATE DATABASE jot OWNER django_jot;
ALTER USER django_jot CREATEDB;          -- needed only for "python manage.py test"
```

**Step 3 — Install the Python driver** (inside your virtual environment)

```bash
pip install "psycopg[binary]"
```

Without it (verified):

```text
django.core.exceptions.ImproperlyConfigured: Error loading psycopg2 or psycopg module
```

**Step 4 — Update `DATABASES`** as above.

**Step 5 — Create the tables and an admin user**

```bash
python manage.py migrate
python manage.py createsuperuser
```

**Step 6 — Check the connection**

```bash
python manage.py dbshell            # opens psql connected to "jot"
```

```sql
\dt                                  -- list tables
\d student_car                       -- structure of one table
SELECT * FROM student_car;
\q                                   -- quit
```

Common errors:

| Error | Cause |
|-------|-------|
| `Error loading psycopg2 or psycopg module` | Driver not installed (Step 3) |
| `connection to server at "localhost", port 5432 failed: Connection refused` | PostgreSQL server not running |
| `password authentication failed for user "django_jot"` | Wrong `USER` / `PASSWORD` |
| `database "jot" does not exist` | Step 2 not done |
| `Got an error creating the test database: permission denied to create database` | Run `ALTER USER django_jot CREATEDB;` (verified) |
| `relation "student_car" does not exist` | `migrate` not run on the new database |

### 11.4 MySQL Configuration

```sql
CREATE DATABASE jot CHARACTER SET utf8mb4;
CREATE USER 'django_jot'@'localhost' IDENTIFIED BY 'jot123';
GRANT ALL PRIVILEGES ON jot.* TO 'django_jot'@'localhost';
```

```bash
pip install mysqlclient
```

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jot',
        'USER': 'django_jot',
        'PASSWORD': 'jot123',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
```

> ⚠ **For the class models:** `Car.brand`, `Car.color`, `Cloth.name` and `Cloth.color` are `CharField()` **without `max_length`**. That is allowed only on PostgreSQL and SQLite. On MySQL or Oracle the system check fails (`fields.E120: CharFields must define a 'max_length' attribute`). Add `max_length=100` before switching.

### 11.5 Keeping the Password out of `settings.py`

`settings.py` is pushed to GitHub, so a password written there becomes public. Read it from **environment variables** instead:

```python
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'jot'),
        'USER': os.environ.get('DB_USER', 'django_jot'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

```bash
export DB_PASSWORD=jot123            # macOS / Linux
set DB_PASSWORD=jot123               # Windows CMD
python manage.py runserver
```

(The `python-decouple` or `django-environ` packages do the same using a `.env` file — add `.env` to `.gitignore`.)

### 11.6 Moving Data from SQLite to PostgreSQL

```bash
# 1. while settings still point to SQLite
python manage.py dumpdata student auth.user --indent 2 -o backup.json

# 2. switch DATABASES to PostgreSQL, then
python manage.py migrate
python manage.py loaddata backup.json
```

`dumpdata` output (verified):

```json
[
{
  "model": "student.student",
  "pk": 1,
  "fields": {
    "roll_no": 101,
    "name": "Rahul",
    "marks": 82.0
  }
},
...
```

### 11.7 Same Code, Different Databases

Every shell session in this file ran on PostgreSQL. The only visible differences from SQLite are in generated SQL — e.g. `bigint ... GENERATED BY DEFAULT AS IDENTITY` (PostgreSQL) vs `integer ... AUTOINCREMENT` (SQLite), and `double precision` vs `real`. The Python code is identical.

---

## 12. Testing Models

Django creates a **separate test database** (`test_jot`), runs the tests, then deletes it — your real data is never touched. All six tests below pass on PostgreSQL.

**`student/test_unit5.py`**

```python
from django.contrib.auth.models import Group, Permission, User
from django.test import TestCase

from .models import Car, Department, Employee, Student


class StudentModelTests(TestCase):
    def setUp(self):
        Student.objects.create(roll_no=101, name="Rahul", marks=78.5)
        Student.objects.create(roll_no=102, name="Priya", marks=91.0)

    def test_str_returns_name(self):
        self.assertEqual(str(Student.objects.get(roll_no=101)), "Rahul")

    def test_update_and_delete(self):
        Student.objects.filter(roll_no=101).update(marks=80)
        self.assertEqual(Student.objects.get(roll_no=101).marks, 80)
        Student.objects.get(roll_no=102).delete()
        self.assertEqual(Student.objects.count(), 1)


class ForeignKeyTests(TestCase):
    def test_cascade_delete(self):
        cse = Department.objects.create(dept_name="CSE")
        Employee.objects.create(emp_name="Rohit", email="rohit@lpu.in", dept=cse)
        self.assertEqual(cse.employee_set.count(), 1)
        cse.delete()
        self.assertEqual(Employee.objects.count(), 0)


class AuthUserTests(TestCase):
    def test_create_user_hashes_password(self):
        user = User.objects.create_user("navjot", "navjot@lpu.in", "Navjot@123")
        self.assertNotEqual(user.password, "Navjot@123")
        self.assertTrue(user.check_password("Navjot@123"))

    def test_group_permission(self):
        user = User.objects.create_user("rahul", password="Rahul@123")
        faculty = Group.objects.create(name="Faculty")
        faculty.permissions.add(Permission.objects.get(codename="add_car"))
        user.groups.add(faculty)
        self.assertTrue(user.has_perm("student.add_car"))
        self.assertFalse(user.has_perm("student.delete_car"))


class CarViewTests(TestCase):
    def test_car_list_shows_records(self):
        Car.objects.create(brand="Honda", price=800000, color="Red", model=2024)
        response = self.client.get("/student/cars/")
        self.assertContains(response, "Honda")
```

```text
$ python manage.py test student.test_unit5
Found 6 test(s).
Creating test database for alias 'default'...
......
----------------------------------------------------------------------
Ran 6 tests in 0.875s
OK
```

---

## 13. Issues Found in the Class Code (and Fixes)

### Issue 1 — A model named `User` clashes with Django's `User`

`student/models.py` has `class User(models.Model)` with `name` and `price` (looks like a product). The admin then shows **two** "Users" entries, and `from student.models import User` hides the login `User` in the shell (Section 7.9).

**Fix:** rename it (e.g. `Product`), then `makemigrations` (Django asks *"Was the model student.User renamed to Product? [y/N]"* → `y`) and `migrate`.

### Issue 2 — Duplicate models `Student` and `Stud`

Both have `roll_no`, `name`, `marks`. The `stud_*` views use `Student`; `Stud` is unused. Remove `Stud` (and migrate) or use it.

### Issue 3 — `createuser` crashes the second time

The username `Parveen` is fixed, and usernames are unique. Opening `/student/createuser/` twice (verified):

```text
django.db.utils.IntegrityError: duplicate key value violates unique constraint "auth_user_username_key"
DETAIL:  Key (username)=(Parveen) already exists.
→ 500 Internal Server Error
```

**Fix (verified):**

```python
def createuser2(request):
    username = request.GET.get('username', 'Parveen')
    if User.objects.filter(username=username).exists():
        return render(request, 'student/home.html', {"c": f"{username} already exists"})
    User.objects.create_user(username=username, email=f'{username.lower()}@gmail.com', password='parveen123')
    return render(request, 'student/home.html', {"c": "user created"})
```

### Issue 4 — `updateuser` / `deleteuser` crash when `Navjot` doesn't exist, and delete runs on GET

`User.objects.get(username='Navjot')` → `DoesNotExist` → **500** (verified). Usernames are case-sensitive, so a user created as `navjot` is not found either. Deleting on a plain GET link is also unsafe (Unit 4 — CSRF).

**Fix (verified — 404 for unknown users, 405 for GET delete, 302 after POST delete):**

```python
from django.views.decorators.http import require_POST

def updateuser2(request, username):
    user = get_object_or_404(User, username=username)
    user.email = request.GET.get('email', user.email)
    user.save()
    return redirect('alluser')

@require_POST
def deleteuser2(request, username):
    user = get_object_or_404(User, username=username)
    user.delete()
    return redirect('alluser')
```

```python
path('updateuser2/<str:username>/', views.updateuser2, name='updateuser2'),
path('deleteuser2/<str:username>/', views.deleteuser2, name='deleteuser2'),
```

### Issue 5 — `CharField()` without `max_length` in `Car` and `Cloth`

Works on PostgreSQL/SQLite, fails on MySQL/Oracle (Section 11.4). Add `max_length=100`.

### Issue 6 — Database password committed to GitHub

`settings.py` in the public repository contains `'PASSWORD': 'jot123'`. Use environment variables (Section 11.5).

### Issue 7 — `stud_confirm_delete.html` shows nothing for the student

```html
<p>{{Stud }}</p>
```

The view passes `{'stud': stud}` (lower case). Template variables are case-sensitive, so `{{ Stud }}` is empty. **Fix:** `{{ stud }}`.

### Issue 8 — Small template issues in `stud_list.html`

`<a href=" {% url 'stud_update' stud.id %}" >` has a leading space inside `href`, and the last `<td>` is not closed. Write `href="{% url 'stud_update' stud.id %}"` and add `</td>`.

---

## 14. Summary and Practice Questions

### 14.1 Unit Summary

| Concept | Key Point |
|---------|-----------|
| Model | Python class = table; attribute = column; object = row |
| Table name | `app_model` → `student_car` |
| `id` | Added automatically (`BigAutoField`) |
| `__str__` | How the object is displayed (shell, admin, templates) |
| `makemigrations` | Writes the migration file from model changes |
| `migrate` | Applies migrations to the database |
| `sqlmigrate` / `showmigrations` | See the SQL / see what's applied |
| Rollback | `migrate app 000X` |
| Shell | `python manage.py shell` — CRUD with `create`, `get`, `filter`, `save`, `update`, `delete` |
| `get()` vs `filter()` | One object (errors if 0 or many) vs QuerySet |
| Lookups | `field__gte`, `__icontains`, `__in`, `__range`, `fk__field` |
| `Q` / `F` | OR/NOT conditions / use a column's own value |
| `aggregate` / `annotate` | One summary / value per row |
| `ForeignKey` | On the "many" side; column `<name>_id`; `on_delete` required |
| Reverse access | `department.employee_set.all()` or `related_name` |
| `auth_user` | Built-in login users; `create_user()` hashes passwords |
| Password | `set_password()` + `save()`; `check_password()`; never assign `password` |
| Admin | `createsuperuser`, `admin.site.register`, `ModelAdmin` options |
| Groups | Permissions given to a group apply to all its users |
| Permissions | `app.action_model`; 4 per model; `has_perm()`; superuser has all |
| `is_staff` | Can enter `/admin/` — not a permission by itself |
| `@permission_required` | Protects a view (`raise_exception=True` → 403) |
| `DATABASES` | Only place to change the database; driver must be installed |
| Secrets | Read DB password from environment variables |

### 14.2 Practice Questions

**Short answer (2 marks)**

1. What is an ORM? Give two advantages.
2. Differentiate between `makemigrations` and `migrate`.
3. What will be the table name and the FK column name for `dept = models.ForeignKey(Department, ...)` in model `Employee` of app `student`?
4. Differentiate between `get()` and `filter()`.
5. Why must `create_user()` be used instead of `User.objects.create()`?
6. Differentiate between `null=True` and `blank=True`.
7. Name the four default permissions Django creates for model `Car`.
8. What is the difference between `is_staff` and `is_superuser`?
9. Which package must be installed to connect Django to PostgreSQL?

**Medium answer (5 marks)**

10. Write shell commands to insert three students, display students with marks above 75 in descending order, increase every student's marks by 5 using an `F` expression, and delete students with marks below 40.
11. Explain `CASCADE`, `PROTECT` and `SET_NULL` with the `Department`/`Employee` example.
12. Write shell commands to create a user, change the user's email and password, deactivate the account, and finally delete it.
13. Explain the steps to configure a Django project with PostgreSQL, including the SQL to create the database and user.
14. Write a `ModelAdmin` for `Employee` that shows name, email and department, allows searching by name and email, and filters by department.

**Long answer (10 marks)**

15. Design models `Course` and `Enrollment` (an enrollment belongs to one course and has `student_name`, `email`, `date`). Write the models, the migration commands, the SQL generated (`sqlmigrate`), and shell commands for: adding a course with three enrollments, listing all enrollments of a course using reverse access, counting enrollments per course with `annotate`, and deleting a course.
16. Create two groups — **Editors** (view, add, change `Car`) and **Viewers** (view `Car`) — and two users, one in each group, using the **shell**. Show how to check each user's permissions, and write a view protected with `@permission_required` that only Editors can open.
17. Explain the complete flow from writing a model to seeing it in the admin: model → `makemigrations` → `migrate` → `createsuperuser` → `admin.py` registration → `ModelAdmin` customisation. Mention the tables created and what each built-in table stores.
18. A project currently uses SQLite with real data. Describe how to move it to PostgreSQL without losing data, how to keep the database password out of GitHub, and how to verify the new connection.

---

*End of Unit 5 — Models and Migrations and Django Admin*
