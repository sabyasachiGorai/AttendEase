# ⚡ AttendEase – Campus Attendance & Event Management Backend

A lightweight **Django backend** powering the AttendEase platform —
a modern system for **event management, automated reminders, and real-time attendance tracking** for students and faculty.

This backend provides the foundation for handling **students, attendance, routing, and data modeling**, designed to integrate smoothly with a React frontend.

---

## ✨ Key Capabilities

* 🔐 **Modular Django app structure**
* 📊 **Attendance tracking logic** & percentage calculations
* 👥 **Student management**
* 🔄 **REST API architecture** using Django REST Framework
* 🔗 **CORS-enabled backend** for easy frontend integration
* 💾 **SQLite database** for local development
* 📦 Clean project layout following industry best practices
* 🚀 Ready for expansion into events, reminders, teachers, and more

---

## 🛠 Tech Stack

| Layer    | Technology                    |
| -------- | ----------------------------- |
| Backend  | Django, Django REST Framework |
| Database | SQLite3 (local development)   |
| Frontend | React (separate repository)   |
| Tools    | Virtual Environment, Git      |

---

# ⚙️ Local Setup Guide

Follow these steps to set up the backend locally in a clean, professional workflow.

---

## 1️⃣ Clone the Project
clone the whole repo first then move to the ```local-testing``` branch
```bash
git clone <repo-url> attendease-backend
cd attendease-backend
```
then move to ```attendease_backend2``` folder

---

## 2️⃣ Create & Activate Virtual Environment

```bash
python -m venv venv
```

### Activate venv

**Windows (PowerShell):**

```powershell
venv\Scripts\Activate.ps1
```

**Windows (cmd):**

```cmd
venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If you add new packages, don’t forget:

```bash
pip freeze > requirements.txt
```

---

## 4️⃣ Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 5️⃣ (Optional) Create Admin User

```bash
python manage.py createsuperuser
```

---

## 6️⃣ Start Development Server

```bash
python manage.py runserver
```

Server will run at:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

Your API will be accessible under:
👉 **/api/**

---

# 📁 Project Structure

```
attendease-backend/
│
├── attendease_backend2/        # Project config (settings, urls, wsgi)
├── core/                       # Student app (models, views, serializers)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
│
├── venv/                       # Virtual environment (ignored)
├── db.sqlite3                  # Local dev DB (ignored)
├── .gitignore                  # Ignore rules
├── requirements.txt            # Dependencies
└── manage.py
```

---

# 🔗 Connecting With Frontend

Your React frontend can access backend data directly using:

```
http://127.0.0.1:8000/api/
```

Make sure **CORS is enabled** in your Django settings (already configured in this repo).

---
