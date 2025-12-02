# ⚡ AttendEase – Smart Attendance & Campus Management Backend

AttendEase is a modern, scalable **Django + DRF backend** powering a complete system for **student attendance tracking, teacher–student interaction, course management, authentication, and admin operations**.

Designed to integrate seamlessly with your **React frontend**, AttendEase supports:

* ✔ Real-time attendance tracking
* ✔ Secure JWT authentication
* ✔ Teacher & student dashboards
* ✔ Clean REST APIs
* ✔ PostgreSQL deployment on Railway
* ✔ CORS-enabled public API for Vercel frontend

---

## 🌍 Live Production URLs

| Service                   | URL                                                                                          |
| ------------------------- | -------------------------------------------------------------------------------------------- |
| **Frontend (Vercel)**     | [https://attend-ease-frontend-chi.vercel.app/](https://attend-ease-frontend-chi.vercel.app/) |
| **Backend API (Railway)** | [https://web-production-4f452.up.railway.app/](https://web-production-4f452.up.railway.app/) |
| **API Base URL**          | `https://web-production-4f452.up.railway.app/api/`                                           |

Your frontend directly communicates with Railway through this base URL.

---

# ✨ Key Features

* 🔐 **Secure JWT Authentication** (Login, Register, Logout)
* 🎓 **Teacher & Student Roles** with permission-based access
* 📚 **Courses, Subjects, Assignments & Enrollments**
* ⏱️ **Attendance Marking & Easy Filtering**
* 📊 **Attendance Percentage Calculation**
* 👤 **/me APIs** — no student/teacher ID exposure
* 🌐 **CORS Enabled** for frontend integration
* 🛠️ **Clean REST Architecture** using Django REST Framework
* ☁️ **Production-ready on Railway with PostgreSQL**

---

# 🛠️ Tech Stack

| Layer    | Technology                            |
| -------- | ------------------------------------- |
| Backend  | Django, DRF                           |
| Auth     | JWT (SimpleJWT)                       |
| Database | SQLite (dev), PostgreSQL (production) |
| Hosting  | Railway                               |
| Frontend | React (Vite)                        |

---

# ⚙️ Local Development Setup

Follow these steps to run the backend locally for development.

---

## 1️⃣ Clone the Repository

```bash
git clone <repo-url> attendease-backend
cd attendease-backend
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### Activate (One of the following)

**Windows PowerShell**

```powershell
venv\Scripts\Activate.ps1
```

**Windows CMD**

```cmd
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Database Setup (Local)

By default, your project uses **SQLite3** (configured in `settings.py` ).

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 5️⃣ Create Admin (Optional)

```bash
python manage.py createsuperuser
```

---

## 6️⃣ Run Local Server

```bash
python manage.py runserver
```

API will be available at:

👉 [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)

---

# 🚀 Production Deployment on Railway

### ✔ Backend URL

Your backend is live here:

```
https://web-production-4f452.up.railway.app/
```

### ✔ PostgreSQL Setup

In Railway, set the environment variables:

```
DATABASE_URL=<Railway PostgreSQL URL>
DJANGO_SECRET_KEY=<your-secret>
DEBUG=False
```

Update your database config when deploying:

```python
# settings.py
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get("DATABASE_URL"))
}
```

---

# 🔗 Connecting Backend With Frontend

Your React frontend calls APIs like:

```
https://web-production-4f452.up.railway.app/api/login/
https://web-production-4f452.up.railway.app/api/students/me/subjects-attendance/
https://web-production-4f452.up.railway.app/api/teachers/<id>/students/
```

### CORS

CORS is already enabled globally in your settings:

```python
CORS_ALLOW_ALL_ORIGINS = True
```

So Vercel frontend can communicate without issues.

---

# 📁 Project Structure

```
attendease-backend/
│
├── attendease_backend2/        # Project config
│   ├── settings.py             # DRF, JWT, CORS, DB config
│   ├── urls.py                 # Project routes
│
├── core/                       # Main logic (students, attendance, subjects)
│   ├── models.py               # Database models (Dept, Course, Student…)  :contentReference[oaicite:1]{index=1}
│   ├── serializers.py          # Serializers for APIs                     :contentReference[oaicite:2]{index=2}
│   ├── views.py                # Major API logic (attendance, teacher)    :contentReference[oaicite:3]{index=3}
│   ├── urls.py                 # All API endpoints                        :contentReference[oaicite:4]{index=4}
│
├── account/                    # Authentication system
│   ├── models.py               # Custom User model                         :contentReference[oaicite:5]{index=5}
│   ├── serializers.py          # Auth serializers                          :contentReference[oaicite:6]{index=6}
│   ├── views.py                # Register, login, logout, profile          :contentReference[oaicite:7]{index=7}
│   ├── permissions.py          # Role-based access                          :contentReference[oaicite:8]{index=8}
│
├── requirements.txt
└── manage.py
```

---

# 🔑 Important API Routes

Below are some key endpoints:

### **Auth**

| Method | Endpoint         | Description              |
| ------ | ---------------- | ------------------------ |
| POST   | `/api/register/` | Register user            |
| POST   | `/api/login/`    | Login user               |
| POST   | `/api/logout/`   | Logout (blacklist token) |

---

### **Student**

| Method | Endpoint                                   | Description                       |
| ------ | ------------------------------------------ | --------------------------------- |
| GET    | `/api/students/me/subjects-attendance/`    | All subjects + attendance summary |
| GET    | `/api/students/me/attendance/?subject_id=` | Date-wise attendance              |

---
### **Teacher**

| Method | Endpoint                                   | Description                       |
| ------ | ------------------------------------------ | --------------------------------- |
| GET    | `/api/teachers/me/teacher-subject-ids/`    | Subjects assigned |
| GET    | `/api/teachers/<id>/students/?subject_id=` | All students for that subject |
| POST | `/api/attendance/mark/` | Mark attendance |


### **Admin CRUD**

Uses ModelViewSet:

```
/api/departments/
/api/courses/
/api/subjects/
/api/students/
/api/teachers/
```

---

# 🗄 PostgreSQL Notes (Railway)

You **must** set these env variables in Railway:

```
DATABASE_URL
DJANGO_SECRET_KEY
DEBUG=False
```

Static files & migrations run automatically during deployment.

---

