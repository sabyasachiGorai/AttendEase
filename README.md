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


## 📦 Getting Started (Frontend & Backend Separately)

Currently, the frontend and backend are **not fully linked**. The integrations (e.g. API routing, authentication flow) are under development and will come soon.

You can still run the frontend and backend independently for development and testing.

### Backend Setup

1. **Go to the backend folder**  
   ```bash
   cd backend


2. **Install dependencies**
   (assuming you’re using a virtual environment)

   ```bash
   python -m venv venv
   source venv/bin/activate   # on Linux/macOS  
   venv\Scripts\activate      # on Windows  
   pip install -r requirements.txt
   ```

3. **Set up environment variables / config**
   Copy `.env.example` to `.env` (or otherwise configure your settings: database, SECRET_KEY, etc.)

4. **Run database migrations & seed (if any)**

   ```bash
   python manage.py migrate
   ```

5. **Start backend server**

   ```bash
   python manage.py runserver
   ```

   By default, this will run on `http://127.0.0.1:8000` (unless configured otherwise).

### Frontend Setup

1. **Go to the frontend folder**

   ```bash
   cd frontend
   ```

2. **Install Node dependencies**

   ```bash
   npm install
   # or if you use yarn:
   # yarn install
   ```


3. **Start frontend dev server**

   ```bash
   npm start
   ```

   This will run the React app (often on `http://localhost:3000`).

### Notes & Future Work

* The **linking between frontend and backend** (actual API calls, authentication, token passing, etc.) is under development and will be added soon.
* Once linking is done, you will be able to run both together and the frontend will communicate with the backend seamlessly.


