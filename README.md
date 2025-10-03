# 📚 Campus Event & Attendance Portal

A web portal for students and faculty to **view and post events or announcements** with optional admin approval.
Includes **automated WhatsApp/Telegram reminders**, **real-time attendance tracking**, shortage alerts, and teacher overrides for manual updates.

---

## ✨ Features

* 📅 Centralized feed & calendar for upcoming events and announcements
* 🔔 Automated reminders via WhatsApp/Telegram
* ✅ Optional admin approval workflow
* 📝 Real-time digital attendance recording (teacher-initiated)
* 📊 Attendance percentage breakdown, forecasting & shortage alerts

---

## 🛠 Tech Stack

* **Frontend:** React
* **Backend:** Django
* **Database:** PostgreSQL, Sqlite3
* **Messaging API:** Twilio WhatsApp API / Telegram Bot API

---

# ⚡ AttendEase - Minimal Django Backend (Student Only)

This repository provides a **minimal Django backend** that exposes **Student CRUD endpoints** with an `attendance_percentage` field.
👉 Uses **SQLite3** for easy local testing.

---

## 📦 Requirements

* Python **3.10+**
* pip
* (optional) git

---

## ⚙️ Setup (Local Development)

### 1. Clone project & create virtual environment

```bash
git clone <repo-url> AttendEase-backend
cd AttendEase-backend
python -m venv venv
```

Activate venv:

* **macOS / Linux**

  ```bash
  source venv/bin/activate
  ```
* **Windows (PowerShell)**

  ```powershell
  venv\Scripts\Activate.ps1
  ```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
# or manually:
pip install Django djangorestframework django-cors-headers
```

---

### 3. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 4. (Optional) Create admin user

```bash
python manage.py createsuperuser
```

---

### 5. Run development server

```bash
python manage.py runserver
```

Server runs at 👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**
API root prefix 👉 **/api/**

---

## 🔗 API Endpoints

### ➕ Create Student

**POST** `/api/students/`

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "roll_number": "CSE001",
  "attendance_percentage": "85.50"
}
```

### 📜 List Students

**GET** `/api/students/`

### 🔍 Get Student by ID

**GET** `/api/students/<id>/`

### ✏️ Update Student

**PUT** `/api/students/<id>/` — update all fields
**PATCH** `/api/students/<id>/` — update partial fields (e.g., only attendance)

---

## 🖥️ Frontend Testing

Use the sample `test-front.html` file.
From your frontend, call:

```http
http://127.0.0.1:8000/api/students/
```

---
