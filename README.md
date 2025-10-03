# Campus Event & Attendance Portal

A web portal for students and faculty to **view and post events or announcements** with optional admin approval.  
Includes **automated WhatsApp/Telegram reminders**, **real-time attendance tracking**, shortage alerts, and teacher overrides for manual updates.

## ✨ Features
- Centralized feed & calendar for upcoming events and announcements  
- Automated reminders via WhatsApp/Telegram
- Optional admin approval workflow  
- Real-time digital attendance recording (teacher-initiated)  
- Attendance percentage breakdown, forecasting & shortage alerts  

## 🛠 Tech Stack
- Frontend: React  
- Backend: Django  
- Database: PostgreSQL  
- Messaging API: Twilio WhatsApp API (or Telegram Bot API)




# AttendEase - Minimal Django Backend (Student only)

This repository provides a minimal Django backend that exposes Student CRUD endpoints with an `attendance_percentage` field. Uses **SQLite3** for easy local testing.

## Requirements

- Python 3.10+
- pip
- (optional) git

## Setup (local dev)

1. Clone / create project folder and create venv
```bash
git clone <repo-url> AttendEase-backend
cd AttendEase-backend
python -m venv venv
# activate venv:
# macOS / Linux:
source venv/bin/activate
# Windows PowerShell:
venv\Scripts\Activate.ps1


Install dependencies

pip install -r requirements.txt
# or
pip install Django djangorestframework django-cors-headers


Apply migrations

python manage.py makemigrations
python manage.py migrate


(Optional) Create admin user

python manage.py createsuperuser


Run server

python manage.py runserver


Server runs at http://127.0.0.1:8000/. API root prefix is /api/.

API Endpoints

POST /api/students/ — create a student
Request JSON: { "name":"...", "email":"...", "roll_number":"...", "attendance_percentage":"85.50" }

GET /api/students/ — list all students

GET /api/students/<id>/ — fetch a single student

PUT /api/students/<id>/ or PATCH /api/students/<id>/ — update a student (PUT requires all fields; PATCH can update only attendance)

Frontend testing

See test-front.html (example file). Use fetch from your frontend to call http://127.0.0.1:8000/api/students/.

