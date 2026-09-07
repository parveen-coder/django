# 🐍 Unit I — Introduction to Django

> **Course:** Full Stack Web Development (B.Tech, 4th Year)
> **Duration:** 5 Lectures × 50 minutes
> **Prerequisite:** Basic Python programming

---

## 🗺️ Unit Roadmap

```mermaid
flowchart LR
    L1["📖 Lecture 1<br/>What is Django?<br/>+ Installation"] --> L2["🛠️ Lecture 2<br/>Editor Setup<br/>+ Projects vs Apps"]
    L2 --> L3["🏗️ Lecture 3<br/>First Project<br/>+ Project Structure"]
    L3 --> L4["⚙️ Lecture 4<br/>django-admin &<br/>manage.py Commands"]
    L4 --> L5["📦 Lecture 5<br/>App Structure<br/>+ Creating an App"]

    style L1 fill:#e8f5e9,stroke:#2e7d32
    style L2 fill:#e3f2fd,stroke:#1565c0
    style L3 fill:#fff3e0,stroke:#ef6c00
    style L4 fill:#f3e5f5,stroke:#7b1fa2
    style L5 fill:#fce4ec,stroke:#c2185b
```

| # | Lecture | Topics Covered | Outcome |
|---|---------|---------------|---------|
| 1 | Introduction & Installation | What is Django, Why Django, MVT, Installing Python & Django | Working Django installation |
| 2 | Environment & Concepts | Editor setup (VS Code), venv, Projects vs Apps | Ready dev environment |
| 3 | First Project | `startproject`, project structure file-by-file, dev server | Running website on localhost |
| 4 | Command-line Tools | `django-admin` vs `manage.py`, all key commands | Command-line fluency |
| 5 | Apps | App structure file-by-file, creating & registering an app, first view | First working page |

---
---

# 📖 LECTURE 1 — Introduction to Django & Installation

### 🎯 Learning Objectives
By the end of this lecture, students will be able to:
1. Explain **what Django is** and where it is used
2. Describe the **MVT architecture**
3. **Install Python and Django** on their own machines
4. Verify the installation

---

## 1.1 What is Django? 🤔

**Django** is a **free, open-source, high-level web framework written in Python** that enables rapid development of secure and maintainable websites.

> 💬 **One-line definition for exams:**
> *"Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design."* — Official Django tagline

### 🧩 What is a "Web Framework"?

Think of building a house 🏠:

| Without Framework | With Framework |
|---|---|
| Make your own bricks, cement, pipes | Bricks, cement & pipes are ready-made |
| Handle user login code from scratch | Login system built-in |
| Write SQL queries manually | Database handled by ORM |
| Worry about security attacks yourself | Security protections built-in |

A framework gives you the **skeleton + tools**; you focus only on **what makes your website unique**.

### 🌍 Who uses Django?

| Company | Use |
|---|---|
| 📷 **Instagram** | Entire backend |
| 🎵 **Spotify** | Backend services |
| 📌 **Pinterest** | Web platform |
| 🚀 **NASA** | Official website |
| 💬 **Disqus** | Comment system |

> 🗣️ **Fun fact:** Django is named after jazz guitarist **Django Reinhardt**. It's pronounced **"JANG-oh"** (the D is silent!).

---

## 1.2 History of Django 📜 (Who, When, Where, Why & How)

### 🗞️ The Newspaper Origin Story

Django was **not** born in a big tech company — it was born in a **newspaper office**!

| ❓ Question | ✅ Answer |
|---|---|
| **Where?** 🌎 | *Lawrence Journal-World* newspaper, Lawrence, **Kansas, USA** |
| **When?** 📅 | Development began in **Autumn 2003**; released publicly in **July 2005** |
| **By Whom?** 👨‍💻 | Web programmers **Adrian Holovaty** and **Simon Willison** (later joined by **Jacob Kaplan-Moss**) |
| **Why?** 🎯 | Journalism runs on **tight deadlines** — the team had to build complete web applications (news sites, event calendars, local portals) in **days or hours**, not months |
| **How?** 🛠️ | They kept rebuilding the same pieces (admin interfaces, forms, database code) for every news site — so they **extracted the common patterns into one reusable framework** |
| **Named after?** 🎸 | Jazz guitarist **Django Reinhardt** (a favorite of the creators) |
| **License?** 📄 | Open-sourced under the **BSD license** in July 2005 — free for everyone, forever |
| **Maintained by?** 🏛️ | The **Django Software Foundation (DSF)**, a non-profit established in **June 2008** |

```mermaid
timeline
    title 🕰️ The Django Journey
    2003 : 🗞️ Adrian & Simon start building it at Lawrence Journal-World
    2005 : 🌍 Open-sourced (July 2005, BSD license)
    2008 : 🏛️ Django Software Foundation formed : 🚩 Django 1.0 released (Sept 2008)
    2015 : 📈 Django 1.8 — first LTS-labelled release era
    2019 : 3️⃣ Django 3.0 — async (ASGI) support begins
    2023 : 4️⃣ Django 4.2 LTS — psycopg3, async ORM improvements
    2025 : 5️⃣ Django 5.2 LTS (Apr) : 6️⃣ Django 6.0 released (Dec)
    2026 : 🚀 Django 6.0.x current, 6.1 in development
```

> 💬 **Exam-ready line:** *"Django was created in 2003 by Adrian Holovaty and Simon Willison at the Lawrence Journal-World newspaper in Kansas to meet the fast deadlines of news journalism, and was released as open-source software in July 2005. That deadline-driven origin is why its motto is 'The web framework for perfectionists with deadlines.'"*

> 💡 **Why the origin matters:** Django's most-loved features — the instant **admin panel**, rapid **forms**, and the **ORM** — all exist because journalists needed working websites *yesterday*. The framework's DNA is speed + reliability.

---

## 1.3 Django Versions 🔢

### How Django releases work

- 📦 **Feature releases** (5.2, 6.0, 6.1 …) arrive roughly **every 8 months** — new features, improvements
- 🩹 **Patch releases** (6.0.1, 6.0.2 …) — bug/security fixes only, always safe to upgrade
- 🛡️ **LTS (Long-Term Support)** — the *last* feature release of a major series gets **~3 years of support** — the version companies prefer for production

### 📋 Major version milestones

| Version | Released | Highlights | Status |
|---|---|---|---|
| 1.0 | Sept 2008 | First stable API | 🪦 EOL |
| 2.0 | Dec 2017 | Dropped Python 2, simplified URL routing (`path()`) | 🪦 EOL |
| 3.0 | Dec 2019 | **ASGI / async support begins** | 🪦 EOL |
| 4.0 | Dec 2021 | Redis cache, zoneinfo timezones | 🪦 EOL |
| 4.2 **LTS** | Apr 2023 | psycopg3, async ORM interfaces | ⏳ Support ended Apr 2026 |
| 5.0 | Dec 2023 | Facet filters in admin, form field groups | 🪦 EOL |
| 5.2 **LTS** | Apr 2025 | Composite primary keys, auto model imports in shell | ✅ **Supported until Apr 2028** |
| **6.0** | **Dec 2025** | 🆕 **Content Security Policy (CSP) support, built-in Background Tasks, Template Partials, modern email API** | ✅ **Current series** |
| 6.1 | Expected 2026 | In development (release candidate stage) | 🔬 Preview |

### 🏷️ So what's the LATEST version?

> ✅ As of **July 2026**, the latest official release is **Django 6.0.7** (in the Django 6.0 series, first released December 2025).
> 🛡️ The current **LTS** choice for long-lived production projects is **Django 5.2** (supported until April 2028).
> 🔬 **Django 6.1** is around the corner — its release candidate is already out for testing.

```bash
# Check YOUR installed version:
python -m django --version

# Install a specific version (e.g., the LTS):
pip install "django==5.2.*"

# Upgrade to the latest:
pip install --upgrade django
```

> ⚠️ **Note for students:** version numbers move fast — always verify the latest at **djangoproject.com/download** before starting a new project. Concepts in this unit apply to *all* modern versions (4.x, 5.x, 6.x).

---

## 1.4 Why Django? ✨ (Key Features)

```mermaid
mindmap
  root((🐍 Django))
    🚀 Rapid Development
      "Batteries included"
      Admin panel free
    🔒 Secure by Default
      SQL Injection protection
      XSS & CSRF protection
    📈 Scalable
      Instagram-level traffic
    🗄️ ORM
      No raw SQL needed
      Python classes = DB tables
    🌐 Versatile
      Websites, APIs, CMS
```

**The 5 features to remember (exam-friendly):**

1. **🔋 Batteries Included** — authentication, admin panel, forms, ORM all come pre-built
2. **🔒 Secure** — protects against SQL injection, XSS, CSRF out of the box
3. **📈 Scalable** — handles small blogs to Instagram-scale traffic
4. **⚡ Fast Development** — "The web framework for perfectionists with deadlines"
5. **🐍 Pythonic** — clean, readable code following DRY (*Don't Repeat Yourself*) principle

---

## 1.5 MVT Architecture 🏛️

Django follows **MVT = Model – View – Template** (a variant of the famous MVC pattern).

```mermaid
flowchart TB
    U["🧑‍💻 User / Browser"] -->|"1️⃣ Request (URL)"| URLS["🔀 URL Dispatcher<br/>(urls.py)"]
    URLS -->|"2️⃣ Routes to"| V["🧠 VIEW (views.py)<br/>Business Logic"]
    V <-->|"3️⃣ Fetch/Save data"| M["🗄️ MODEL (models.py)<br/>Database Layer"]
    V -->|"4️⃣ Sends data to"| T["🎨 TEMPLATE (.html)<br/>Presentation Layer"]
    T -->|"5️⃣ Rendered HTML"| U

    style M fill:#e8f5e9,stroke:#2e7d32
    style V fill:#e3f2fd,stroke:#1565c0
    style T fill:#fff3e0,stroke:#ef6c00
```

| Component | File | Responsibility | Analogy 🍽️ (Restaurant) |
|---|---|---|---|
| **Model** | `models.py` | Data & database structure | 🥬 Kitchen storage (ingredients) |
| **View** | `views.py` | Logic: what to do with a request | 👨‍🍳 Chef (prepares the dish) |
| **Template** | `.html` files | How the page looks | 🍽️ Plating & presentation |

> ⚠️ **Common confusion:** Django's **View** = MVC's **Controller**, and Django's **Template** = MVC's **View**. Interviewers love this question!

---

## 1.6 Installing Python 🐍

### Step 1 — Check if Python is already installed

```bash
python --version
# or on Mac/Linux:
python3 --version
```

✅ If you see `Python 3.10+` → skip to section 1.5
❌ If not → install:

### Step 2 — Install Python

| OS | Method |
|---|---|
| 🪟 **Windows** | Download from [python.org/downloads](https://python.org/downloads) → Run installer → ✅ **CHECK "Add Python to PATH"** (most common mistake if skipped!) |
| 🍎 **macOS** | `brew install python3` (or download from python.org) |
| 🐧 **Linux** | `sudo apt update && sudo apt install python3 python3-pip` |

### Step 3 — Verify pip (Python's package installer)

```bash
pip --version
# or
pip3 --version
```

> 📦 **What is pip?** *Pip Installs Packages* — it downloads Python libraries (like Django) from the internet (PyPI repository).

---

## 1.7 Installing Django 🎯

```bash
pip install django
```

That's it! ✨ Verify:

```bash
python -m django --version
# Output: 5.x.x  (your installed version)
```

```mermaid
flowchart LR
    A["🐍 Install Python 3.10+"] --> B["📦 Verify pip"]
    B --> C["⬇️ pip install django"]
    C --> D["✅ python -m django --version"]
    style D fill:#e8f5e9,stroke:#2e7d32
```

### 🛠️ Troubleshooting Corner

| Error | Fix |
|---|---|
| `'python' is not recognized` | Python not in PATH → reinstall with "Add to PATH" checked |
| `'pip' is not recognized` | Use `python -m pip install django` |
| Permission denied (Mac/Linux) | Use `pip install --user django` |

---

## ✅ CHECKPOINT — Lecture 1

**🧠 Quick Recap:**
- Django = high-level Python web framework, "batteries included"
- Born at **Lawrence Journal-World newspaper (Kansas, 2003)** by **Adrian Holovaty & Simon Willison** to beat journalism deadlines; open-sourced **July 2005**; maintained by the **DSF** since 2008
- Latest series: **Django 6.0** (Dec 2025); production LTS: **5.2** (supported to Apr 2028); feature releases every ~8 months
- Follows **MVT**: Model (data) → View (logic) → Template (presentation)
- Install: `pip install django`, verify: `python -m django --version`

**❓ Quiz yourself:**
1. Who created Django, where, and in which year? Why was it created?
2. What is an LTS release, and which Django LTS is currently supported the longest?
3. Django's View corresponds to which component of MVC? *(Controller)*
4. Name three security threats Django protects against by default.
5. What does the "D" in DRY stand for?

**🏠 Homework:** Install Python + Django on your laptop and bring a screenshot of `python -m django --version` output to the next class.

---
---

# 🛠️ LECTURE 2 — Editor Setup, Virtual Environments & Projects vs Apps

### 🎯 Learning Objectives
1. Set up **VS Code** for Django development
2. Create and use a **virtual environment**
3. Clearly distinguish a **Project** from an **App**

---

## 2.1 Setting Up the Editor (VS Code) 📝

**Why VS Code?** Free, lightweight, best Python/Django extension ecosystem.

### Step-by-step setup:

1. **Download** VS Code → [code.visualstudio.com](https://code.visualstudio.com)
2. **Install these extensions** (Ctrl+Shift+X):

| Extension | Why |
|---|---|
| 🐍 **Python** (Microsoft) | IntelliSense, debugging, linting |
| 🎨 **Django** (Baptiste Darthenay) | Django template syntax highlighting |
| ✨ **Pylance** | Fast, smart autocomplete |

3. **Open integrated terminal:** `` Ctrl + ` `` (backtick) — you'll run all Django commands here.

> 💡 **Pro tip:** `File → Open Folder` and open your *project folder* — VS Code works best folder-based, not file-based.

---

## 2.2 Virtual Environments 🧪 (Very Important!)

### The Problem 😰

Imagine two projects on one laptop:
- **Project A** needs Django 4.2
- **Project B** needs Django 5.0

Installing globally = 💥 conflict! Only one version can exist globally.

### The Solution ✅

A **virtual environment** = an **isolated Python box 📦 per project**, each with its own packages.

```mermaid
flowchart TB
    subgraph PC ["💻 Your Computer"]
        subgraph V1 ["📦 venv — Project A"]
            D1["Django 4.2"]
        end
        subgraph V2 ["📦 venv — Project B"]
            D2["Django 5.0"]
        end
        G["🌍 Global Python<br/>(kept clean!)"]
    end
    style V1 fill:#e8f5e9,stroke:#2e7d32
    style V2 fill:#e3f2fd,stroke:#1565c0
```

### Commands (memorize these!) 🧠

```bash
# 1️⃣ Create a virtual environment named "venv"
python -m venv venv

# 2️⃣ Activate it
venv\Scripts\activate        # 🪟 Windows
source venv/bin/activate     # 🍎🐧 Mac / Linux

# ✅ Your prompt changes to show (venv):
# (venv) C:\Users\you\myproject>

# 3️⃣ Install Django INSIDE the environment
pip install django

# 4️⃣ Deactivate when done
deactivate
```

> ⚠️ **Golden Rule:** *Always activate your venv before running any Django command.* If you see `ModuleNotFoundError: No module named 'django'` — 90% chance your venv is not activated!

---

## 2.3 Projects vs Apps 🏗️ (Core Concept!)

This is **the most important conceptual distinction** in Django.

> 🏢 **Analogy — A Shopping Mall:**
> - **Project** = The entire mall 🏬 (building, electricity, security, parking — shared infrastructure)
> - **Apps** = Individual shops inside 🛍️ (each does ONE thing: food court 🍔, cinema 🎬, clothing store 👕)

```mermaid
flowchart TB
    subgraph P ["🏬 PROJECT: E-commerce Website"]
        direction LR
        A1["🛍️ App: products"]
        A2["🛒 App: cart"]
        A3["👤 App: accounts"]
        A4["💳 App: payments"]
    end
    style P fill:#fff3e0,stroke:#ef6c00
    style A1 fill:#e8f5e9,stroke:#2e7d32
    style A2 fill:#e3f2fd,stroke:#1565c0
    style A3 fill:#f3e5f5,stroke:#7b1fa2
    style A4 fill:#fce4ec,stroke:#c2185b
```

| | 🏬 Project | 🛍️ App |
|---|---|---|
| **What** | The whole website + configuration | One functional module |
| **Contains** | Settings, main URLs, deployment config | Models, views, templates for ONE feature |
| **Quantity** | ONE per website | MANY per project |
| **Command** | `django-admin startproject` | `python manage.py startapp` |
| **Reusable?** | ❌ No | ✅ Yes! An app can be plugged into other projects |
| **Example** | "AmazonClone" | "cart", "reviews", "orders" |

> 💬 **Exam-ready line:** *"A project is a collection of configuration and apps for a particular website. An app is a self-contained module that does one thing well and can be reused across projects."*

**✍️ Class Activity (5 min):** For a "University Portal" project, list 4 apps you would create. *(e.g., students, courses, results, library)*

---

## ✅ CHECKPOINT — Lecture 2

**🧠 Quick Recap:**
- VS Code + Python extension + integrated terminal = your Django workshop
- Virtual environment = isolated package box per project (`python -m venv venv` → activate)
- **1 Project : Many Apps**; apps are reusable, projects are not

**❓ Quiz yourself:**
1. What error usually appears when you forget to activate your venv?
2. Can one Django project have zero apps? Can an app exist without a project?
3. Give the activation command for venv on Windows vs Linux.

**🏠 Homework:** Create a folder `myfirstsite`, set up a venv inside it, activate it, and install Django in it.

---
---

# 🏗️ LECTURE 3 — Creating Your First Project & Project Structure

### 🎯 Learning Objectives
1. Create a Django project using `startproject`
2. Explain **every file** in the generated project
3. Run the **development server** and view the site

---

## 3.1 Creating Your First Project 🚀

With your venv **activated**:

```bash
django-admin startproject mysite
cd mysite
```

> 📌 **Naming rules:** letters, numbers, underscores only. No hyphens, no spaces. Avoid names like `django` or `test` (they clash with built-ins).

---

## 3.2 Project Structure — File by File 🗂️

```
mysite/                  ← 📁 Outer folder (just a container — rename freely)
│
├── manage.py            ← 🎮 Command-line utility (your remote control)
│
└── mysite/              ← 📁 Inner folder (the actual Python package — DON'T rename)
    ├── __init__.py      ← 🏷️ Marks this folder as a Python package
    ├── settings.py      ← ⚙️ All configuration (the brain 🧠)
    ├── urls.py          ← 🔀 URL routing table (the receptionist)
    ├── asgi.py          ← 🔌 Async server entry point (deployment)
    └── wsgi.py          ← 🔌 Sync server entry point (deployment)
```

> 😵 **"Why two folders with the same name?!"** — Every student asks this!
> The **outer** `mysite/` is just a container (you can rename it to anything).
> The **inner** `mysite/` is the real Python package that holds settings (renaming it breaks imports).

### 📋 Every file at a glance (revision table)

| File | Nickname | Purpose | Do you edit it? |
|---|---|---|---|
| `manage.py` | 🎮 Remote control | Runs every project command | ❌ Never |
| `__init__.py` | 🏷️ Package marker | Tells Python "this folder is importable" | ❌ Never (stays empty) |
| `settings.py` | ⚙️ The brain | ALL configuration: apps, DB, timezone, security | ✅ Constantly |
| `urls.py` | 🔀 Receptionist | Master URL → view routing table | ✅ Often |
| `wsgi.py` | 🔌 Sync door | Production entry (synchronous servers: Gunicorn) | ⚠️ Only at deployment |
| `asgi.py` | 🔌 Async door | Production entry (async servers: WebSockets, Daphne) | ⚠️ Only at deployment |

### 🔍 Deep-dive into each file:

#### 🎮 `manage.py`
Your project's **remote control**. You'll type `python manage.py <command>` hundreds of times. Internally it does just one thing: sets the environment variable `DJANGO_SETTINGS_MODULE = "mysite.settings"` and forwards your command to Django — that's why it always "knows" your project. Never edit this file.

#### 🏷️ `__init__.py`
An **empty file** with an important job: its presence makes Python treat the folder as an importable **package**, enabling statements like `from mysite import settings`. Delete it and imports across the project break. (Every app also has one — same reason.)

#### ⚙️ `settings.py` — the brain 🧠
The most-edited file. Key settings to know:

```python
# settings.py (important excerpts)

BASE_DIR = Path(__file__).resolve().parent.parent
                        # 📍 Absolute path to your project folder —
                        #    used to build other paths (DB file, templates, static)

SECRET_KEY = 'django-insecure-...'
                        # 🔑 Cryptographic key for sessions/passwords.
                        #    Keep it SECRET in production (env variable)!

DEBUG = True            # 🐛 Show detailed errors (True in dev, MUST be False in production!)

ALLOWED_HOSTS = []      # 🌐 Domains allowed to serve this site (add your domain in production)

INSTALLED_APPS = [      # 📦 List of active apps (you'll add yours here!)
    'django.contrib.admin',          # 🎛️ the admin panel
    'django.contrib.auth',           # 👤 users & permissions
    'django.contrib.contenttypes',   # 🔗 framework for model metadata
    'django.contrib.sessions',       # 🍪 session management
    'django.contrib.messages',       # 💬 one-time flash messages
    'django.contrib.staticfiles',    # 🎨 CSS/JS/image handling
]

ROOT_URLCONF = 'mysite.urls'
                        # 🔀 Which urls.py is the MASTER routing file

DATABASES = {           # 🗄️ Database config (SQLite by default — zero setup!)
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

TIME_ZONE = 'UTC'       # 🕐 Change to 'Asia/Kolkata' for IST

STATIC_URL = 'static/'  # 🎨 URL prefix for CSS/JS/images
```

#### 🔀 `urls.py` — the receptionist
Maps URLs → views. Like a receptionist directing visitors: *"Admin panel? Go to counter `/admin/`."* Django reads `urlpatterns` **top to bottom** and uses the **first match**.

```python
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),   # yoursite.com/admin/ → admin panel
]
```

#### 🔌 `wsgi.py` & `asgi.py`
Entry points for **production web servers**:
- **WSGI** (*Web Server Gateway Interface*) — the traditional, **synchronous** standard; used by servers like Gunicorn/uWSGI
- **ASGI** (*Asynchronous Server Gateway Interface*) — the modern, **async-capable** standard; needed for WebSockets/real-time features; used by Daphne/Uvicorn

You won't touch these until deployment — the dev server ignores them.

```mermaid
flowchart LR
    R["🌐 Request"] --> W["🔌 wsgi.py / asgi.py"] --> S["⚙️ settings.py"] --> U["🔀 urls.py"] --> RESP["📄 Response"]
```

---

## 3.3 Running the Development Server ▶️

```bash
python manage.py runserver
```

Expected output:

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). ...   ← ⚠️ Ignore for now (Lecture 4!)

Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

🌐 Open **http://127.0.0.1:8000/** in your browser → You'll see the 🚀 **rocket page**: *"The install worked successfully! Congratulations!"*

> 🎉 This moment = your first running Django website!

### Useful variations:

```bash
python manage.py runserver 9000          # 🔢 Different port
python manage.py runserver 0.0.0.0:8000  # 📱 Accessible from other devices on your Wi-Fi
```

### 🧠 Know-hows:
- **127.0.0.1** = `localhost` = "this same computer"
- **:8000** = port number (like a door number in a building)
- Server **auto-reloads** on every file save — no need to restart! 🔄
- Stop the server: `Ctrl + C`
- ⚠️ This server is for **development only** — never use it in production

---

## ✅ CHECKPOINT — Lecture 3

**🧠 Quick Recap:**
- `django-admin startproject mysite` → creates outer container + inner package
- `manage.py` = remote control | `settings.py` = brain | `urls.py` = receptionist | `wsgi/asgi.py` = deployment doors
- `python manage.py runserver` → 🚀 rocket page at `127.0.0.1:8000`

**❓ Quiz yourself:**
1. Which of the two `mysite` folders can be safely renamed?
2. Where would you add `'Asia/Kolkata'` and where would you register a new app?
3. What's the difference between WSGI and ASGI?

**🏠 Homework:** Create a project named `campusportal`, run the server on port **7000**, and screenshot the rocket page.

---
---

# ⚙️ LECTURE 4 — django-admin & manage.py Commands

### 🎯 Learning Objectives
1. Differentiate `django-admin` and `manage.py`
2. Use all essential day-to-day commands
3. Understand migrations at a basic level & create a superuser

---

## 4.1 django-admin vs manage.py 🥊

Both run the **same commands** — the difference is *context*:

| | 🌍 `django-admin` | 🎮 `python manage.py` |
|---|---|---|
| **What is it?** | Global command (installed with Django) | Script inside YOUR project |
| **Knows your settings?** | ❌ No | ✅ Yes (auto-points to your `settings.py`) |
| **Use it for** | Creating a project (before a project exists!) | Everything else afterwards |

> 💬 **Exam-ready line:** *"`manage.py` is a thin wrapper around `django-admin` that automatically sets the `DJANGO_SETTINGS_MODULE` environment variable to point to the current project's settings."*

```mermaid
flowchart LR
    A["🌍 django-admin startproject mysite"] -->|"creates project"| B["📁 mysite/ with manage.py"]
    B -->|"from now on use"| C["🎮 python manage.py &lt;command&gt;"]
    style A fill:#f3e5f5,stroke:#7b1fa2
    style C fill:#e8f5e9,stroke:#2e7d32
```

---

## 4.2 The Essential Commands Toolbox 🧰

### 📋 Master Table (keep this handy!)

| Command | Emoji | What it does |
|---|---|---|
| `startproject <name>` | 🏗️ | Creates a new project |
| `startapp <name>` | 📦 | Creates a new app |
| `runserver` | ▶️ | Starts the development server |
| `makemigrations` | 📝 | Writes DB change instructions from your models |
| `migrate` | 🗄️ | Applies those instructions to the database |
| `createsuperuser` | 👑 | Creates an admin account |
| `shell` | 🐚 | Opens interactive Python shell with Django loaded |
| `check` | ✅ | Checks project for problems (no DB touch) |
| `showmigrations` | 📜 | Lists migrations and their status ([X] = applied) |
| `collectstatic` | 🎨 | Gathers static files for deployment |
| `test` | 🧪 | Runs your test suite |
| `flush` | 🧹 | Empties database (⚠️ careful!) |
| `dbshell` | 💾 | Opens the database's own CLI |
| `--version` / `help` | ℹ️ | Version / list all commands |

### 🔬 Detailed Command Reference (with syntax, examples & output)

#### 🏗️ 1. `startproject` — create a project
```bash
django-admin startproject <projectname>            # creates outer + inner folder
django-admin startproject mysite                   # example
django-admin startproject mysite .                 # 💡 the DOT: create in CURRENT folder (no outer folder)
```
*Only command run with `django-admin` — because no `manage.py` exists yet!*

#### 📦 2. `startapp` — create an app
```bash
python manage.py startapp <appname>
python manage.py startapp blog                     # → creates blog/ with models.py, views.py, etc.
```
⚠️ Run from the folder containing `manage.py`. Don't forget to register the app in `INSTALLED_APPS`!

#### ▶️ 3. `runserver` — start the development server
```bash
python manage.py runserver                         # default → http://127.0.0.1:8000
python manage.py runserver 9000                    # custom port → 127.0.0.1:9000
python manage.py runserver 0.0.0.0:8000            # visible to other devices on your Wi-Fi
```
Auto-reloads on file save 🔄 | Stop with `Ctrl+C` | Development ONLY — never production.

#### 📝 4. `makemigrations` — write DB change plans
```bash
python manage.py makemigrations                    # scan ALL apps for model changes
python manage.py makemigrations blog               # only the blog app
```
Output: `Migrations for 'blog': blog/migrations/0001_initial.py - Create model Post`
Creates a numbered Python file describing changes — **nothing touches the DB yet.**

#### 🗄️ 5. `migrate` — apply plans to the database
```bash
python manage.py migrate                           # apply ALL pending migrations
python manage.py migrate blog                      # only blog's migrations
python manage.py migrate blog 0001                 # ⏪ roll BACK to migration 0001
```
This is the step that actually **creates/alters tables** in the database.

#### 📜 6. `showmigrations` — see migration status
```bash
python manage.py showmigrations
```
```
blog
 [X] 0001_initial      ← [X] = applied
 [ ] 0002_add_author   ← [ ] = pending (run migrate!)
```

#### 👑 7. `createsuperuser` — make an admin account
```bash
python manage.py createsuperuser
# prompts: Username → Email → Password (typing is invisible!)
```
Then log in at `http://127.0.0.1:8000/admin/` 🎛️

#### 🐚 8. `shell` — interactive Python + Django
```bash
python manage.py shell
```
```python
>>> from blog.models import Post
>>> Post.objects.count()        # experiment with your data live!
```

#### ✅ 9. `check` — health check without touching the DB
```bash
python manage.py check
# System check identified no issues (0 silenced).  ← what you want to see
```

#### 🧪 10. `test` — run the test suite
```bash
python manage.py test                              # all tests
python manage.py test blog                         # only blog app's tests
```

#### 🎨 11. `collectstatic` — gather static files (deployment)
```bash
python manage.py collectstatic
```
Copies all CSS/JS/images from every app into one `STATIC_ROOT` folder for the production server.

#### 🧹 12. `flush` — empty the database ⚠️
```bash
python manage.py flush
# Asks for confirmation — deletes ALL DATA, keeps tables. There is NO undo!
```

#### 💾 13. `dbshell` — open the database's own console
```bash
python manage.py dbshell           # e.g., opens the sqlite3 prompt for db.sqlite3
```

#### ℹ️ 14. Help & version
```bash
python manage.py help              # 📋 list every available command
python manage.py help migrate     # 📖 detailed help for ONE command
python -m django --version         # 🔢 installed Django version
```

> 🧠 **Memory aid — the Daily Five:** in real work, 90% of your typing is just:
> `runserver` ▶️ → `startapp` 📦 → `makemigrations` 📝 → `migrate` 🗄️ → `createsuperuser` 👑

---

## 4.3 Migrations — the 2-step dance 💃 (Intro)

**Migrations** = version control for your database structure.

```mermaid
flowchart LR
    M["🧱 models.py<br/>(Python classes)"] -->|"1️⃣ makemigrations<br/>📝 write the plan"| F["📄 0001_initial.py<br/>(migration file)"]
    F -->|"2️⃣ migrate<br/>🗄️ execute the plan"| DB[("💾 Database<br/>tables created")]
    style M fill:#e3f2fd,stroke:#1565c0
    style DB fill:#e8f5e9,stroke:#2e7d32
```

> 🍳 **Analogy:** `makemigrations` = writing the recipe 📝, `migrate` = actually cooking the dish 🍳.

Remember the warning `You have 18 unapplied migrations` from Lecture 3? Django's built-in apps (auth, admin, sessions) need database tables. Fix it:

```bash
python manage.py migrate
```

```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

✨ This creates `db.sqlite3` in your project folder — your database is born!

---

## 4.4 Creating a Superuser 👑

Django's **killer feature**: a free, full-featured admin panel!

```bash
python manage.py createsuperuser
```

```
Username: admin
Email address: admin@example.com
Password: ********        ← ⌨️ typing is invisible — that's normal!
Password (again): ********
Superuser created successfully. ✅
```

Now: `runserver` → visit **http://127.0.0.1:8000/admin/** → log in → 🎛️ full admin dashboard (Users & Groups manageable already — with ZERO code written!)

---

## 4.5 The Django Shell 🐚 (quick taste)

```bash
python manage.py shell
```

```python
>>> from django.contrib.auth.models import User
>>> User.objects.all()
<QuerySet [<User: admin>]>       # 👀 your superuser, queried with pure Python!
>>> exit()
```

> 💡 The shell is your **experiment lab** — test queries here before writing them in views.

---

## ✅ CHECKPOINT — Lecture 4

**🧠 Quick Recap:**
- `django-admin` = global (use once, to create project); `manage.py` = project-aware (use always after)
- The sacred workflow: `makemigrations` (write plan 📝) → `migrate` (apply plan 🗄️)
- `createsuperuser` → free admin panel at `/admin/` 👑

**❓ Quiz yourself:**
1. Why can't you use `manage.py` to create a brand-new project?
2. What is the difference between `makemigrations` and `migrate`?
3. Which command lists all migrations and shows which are applied?

**🏠 Homework:** In your `campusportal` project: run `migrate`, create a superuser, log into the admin panel, and add 2 new users through the admin UI.

---
---

# 📦 LECTURE 5 — App Structure & Creating Your First App

### 🎯 Learning Objectives
1. Create an app with `startapp`
2. Explain **every file** inside an app
3. **Register** the app in settings
4. Write your **first view** and map a URL to it → see your own page! 🎉

---

## 5.1 Creating an App 🛠️

Inside your project folder (venv active!):

```bash
python manage.py startapp blog
```

> 📛 **Naming convention:** apps are named after **what they do**, usually plural or functional: `blog`, `products`, `accounts`, `orders`.

---

## 5.2 App Structure — File by File 🗂️

```
blog/                        ← 📦 Your new app
├── __init__.py              ← 🏷️ Makes it a Python package
├── admin.py                 ← 🎛️ Register models to appear in admin panel
├── apps.py                  ← ⚙️ App configuration (name, settings)
├── models.py                ← 🗄️ M of MVT → database tables as Python classes
├── views.py                 ← 🧠 V of MVT → request-handling logic
├── tests.py                 ← 🧪 Your unit tests
└── migrations/              ← 📜 Folder storing DB change history
    └── __init__.py
```

### 🔍 Role of each file (mapped to MVT):

| File | MVT Role | One-liner |
|---|---|---|
| `models.py` | **M** 🗄️ | "What data do we store?" — DB tables as classes |
| `views.py` | **V** 🧠 | "What happens on a request?" — the logic |
| *(templates/)* | **T** 🎨 | "How does it look?" — you create this folder yourself |
| `admin.py` | — 🎛️ | "Show my models in the admin panel" |
| `apps.py` | — ⚙️ | "App's identity card" |
| `tests.py` | — 🧪 | "Prove the app works" |
| `migrations/` | — 📜 | "History of every DB change" |

### 👀 A peek inside each file (what's actually there)

#### ⚙️ `apps.py` — the app's identity card
```python
from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # default primary key type
    name = 'blog'                                          # the app's official name
```
You'll rarely edit this — but it's what Django reads when the app is registered.

#### 🗄️ `models.py` — starts empty, becomes your database
```python
from django.db import models

# Example of what goes here (covered in the Models unit):
class Post(models.Model):
    title = models.CharField(max_length=100)   # → a column in the DB table!
    body = models.TextField()
```
Each class = one database table; each attribute = one column.

#### 🎛️ `admin.py` — one line to unlock the admin panel
```python
from django.contrib import admin
from .models import Post

admin.site.register(Post)    # ✨ Post now fully manageable at /admin/ — zero extra code!
```

#### 📜 `migrations/` folder
Starts with only `__init__.py`. Every time you run `makemigrations`, a new numbered file appears (`0001_initial.py`, `0002_add_author.py`…) — a **complete, replayable history** of your database's evolution. Never edit these by hand; never delete them casually (teammates' databases depend on them!).

### 🆚 Project package vs App — side-by-side

| | ⚙️ Project package (`mysite/`) | 📦 App (`blog/`) |
|---|---|---|
| `settings.py` | ✅ (configuration hub) | ❌ |
| `urls.py` | ✅ (master routes) | 🔧 you create it yourself |
| `wsgi.py` / `asgi.py` | ✅ (deployment doors) | ❌ |
| `models.py` | ❌ | ✅ (the data) |
| `views.py` | ❌ | ✅ (the logic) |
| `admin.py` | ❌ | ✅ (admin registration) |
| `migrations/` | ❌ | ✅ (DB history) |
| **Job** | 🏬 Configure the whole site | 🛍️ Implement ONE feature |

> 🆚 **Notice:** an app has `models.py` & `views.py` but **no** `settings.py` (project-level) — while the project package has settings but no models. The structures perfectly mirror the Project-vs-App division of labour!

---

## 5.3 Registering the App ✍️ (Don't skip this!)

Django doesn't know your app exists until you **register** it.

Open `mysite/settings.py` → add your app to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',                    # 👈 YOUR APP — added here!
]
```

> ⚠️ **Top-3 beginner bug:** creating an app but forgetting to register it → models won't migrate, templates won't load. When something "mysteriously doesn't work," check `INSTALLED_APPS` first!

---

## 5.4 Your First View + URL 🎉 (The Payoff!)

Let's make the browser show **our own page** instead of the rocket.

### Step 1 — Write a view (`blog/views.py`):

```python
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>🎉 Hello from the Blog app!</h1>")
```

*A view = a Python function that takes a `request` and returns a `response`. That's it!*

### Step 2 — Give the app its own URLs (create new file `blog/urls.py`):

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),   # '' = app's root URL
]
```

### Step 3 — Connect app URLs to the project (`mysite/urls.py`):

```python
from django.contrib import admin
from django.urls import path, include          # 👈 add include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),            # 👈 hand over to blog app
]
```

### Step 4 — Run & marvel ✨

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** → 🎉 **"Hello from the Blog app!"**

### 🔄 The full request journey you just built:

```mermaid
flowchart LR
    B["🌐 Browser<br/>127.0.0.1:8000/"] --> P["🔀 mysite/urls.py<br/>include('blog.urls')"]
    P --> A["🔀 blog/urls.py<br/>path('', views.home)"]
    A --> V["🧠 blog/views.py<br/>home(request)"]
    V --> R["📄 HttpResponse<br/>'Hello from the Blog app!'"]
    R --> B
    style B fill:#e3f2fd,stroke:#1565c0
    style V fill:#e8f5e9,stroke:#2e7d32
```

> 💡 **Why give each app its own `urls.py`?** Reusability! The `blog` app carries its URLs with it — plug it into any project with one `include()` line. (Mall analogy: each shop manages its own internal layout 🛍️.)

---

## 5.5 The Complete Picture 🖼️

```mermaid
flowchart TB
    subgraph PROJECT ["🏬 PROJECT: mysite"]
        MG["🎮 manage.py"]
        subgraph CONF ["⚙️ mysite/ (config package)"]
            S["settings.py<br/>(blog registered ✅)"]
            PU["urls.py<br/>(includes blog.urls)"]
        end
        subgraph APP ["📦 APP: blog"]
            AU["urls.py"] --> AV["views.py"]
            AM["models.py"]
            AA["admin.py"]
        end
    end
    PU -.->|include| AU
    style PROJECT fill:#fff8e1,stroke:#ef6c00
    style APP fill:#e8f5e9,stroke:#2e7d32
```

---

## ✅ CHECKPOINT — Lecture 5 (Unit Complete! 🏁)

**🧠 Quick Recap:**
- `python manage.py startapp blog` → app skeleton
- `models.py`=data, `views.py`=logic, `admin.py`=admin registration, `migrations/`=DB history
- **Register in `INSTALLED_APPS`** — the step everyone forgets!
- View function + app `urls.py` + project `include()` = your first custom page 🎉

**❓ Quiz yourself:**
1. Which file is present in a project package but NOT in an app? *(settings.py)*
2. What happens if you skip registering the app in `INSTALLED_APPS`?
3. Trace the journey of a request from browser to `HttpResponse` in 4 steps.

**🏠 Homework (mini-project):** In `campusportal`, create an app `students`, register it, and create two pages: `/` showing "Welcome to Campus Portal 🎓" and `/about/` showing your name and section.

---

## 🧾 Unit I — One-Page Revision Sheet

| Concept | Key Command / Fact |
|---|---|
| History | Created **2003** by **Adrian Holovaty & Simon Willison** at *Lawrence Journal-World* newspaper (Kansas, USA); open-sourced **July 2005** (BSD); DSF since 2008 |
| Latest version | **Django 6.0.x** (series since Dec 2025); **5.2 LTS** for production (→ Apr 2028); new feature release every ~8 months |
| Install Django | `pip install django` |
| Virtual env | `python -m venv venv` → activate → then install |
| New project | `django-admin startproject mysite` |
| New app | `python manage.py startapp blog` |
| Run server | `python manage.py runserver` → 127.0.0.1:8000 |
| Apply DB changes | `makemigrations` → `migrate` |
| Admin account | `createsuperuser` → `/admin/` |
| Architecture | **MVT**: Model=data, View=logic, Template=look |
| Project vs App | 1 project = many apps; apps are reusable |
| #1 beginner bug | Forgetting app in `INSTALLED_APPS` ⚠️ |

> 🎓 **Next Unit Preview:** URLs in depth, Views (function & class-based), and Templates — making pages that actually look good! 🎨
