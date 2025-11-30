
# 🚀 **TEACHER API DOCUMENTATION **

Version: **AttendEase Backend v1**
Auth Type: **JWT Bearer Token**
Role Required: **Teacher**
Base URL: `{{base_url}}/api/`

---

# 📌 **AUTHENTICATION REQUIRED FOR ALL TEACHER APIs**

Teachers must log in via:

### **POST /api/login/**

Headers:

```
Content-Type: application/json
```

Body:

```json
{
  "email": "teacher@example.com",
  "password": "password123"
}
```

Response:

```json
{
  "user_id": 23,
  "user_name": "Prof. John",
  "context": {
    "role": "teacher",
    "id": 7,
    "empCode_RollNo": "TCH001"
  },
  "token": {
    "access": "JWT_ACCESS_TOKEN",
    "refresh": "JWT_REFRESH_TOKEN"
  },
  "msg": "Login Success"
}
```

Save:

* `access` → `Authorization: Bearer <TOKEN>`
* `teacher_id` → for APIs requiring teacher_id

---

# 🟦 **1. GET TEACHER'S OWN SUBJECTS**

### 📘 **GET /teachers/subjectwise/**

**Who can call:** Teacher
**Purpose:** Get all subjects the teacher teaches

### Headers:

```
Authorization: Bearer <access_token>
```

### Response:

```json
[
  {
    "subject_id": 3,
    "subject_code": "DSC102",
    "subject_name": "Data Structures",
    "course": "M.Sc",
    "department": "Computer Science",
    "semester": 1
  }
]
```

### Notes:

✔ Useful for subject dropdown
✔ Use subject_id to filter students later

---

# 🟦 **2. GET TEACHER SUBJECT IDs (ts_id) FOR ATTENDANCE MARKING**

### 📘 **GET /teachers/me/teacher-subject-ids/**

**Who can call:** Teacher
**Purpose:** Teacher gets list of all **TeacherSubject IDs (`ts_id`)** required to mark attendance

### Response:

```json
[
  {
    "ts_id": 12,
    "subject_id": 3,
    "subject_code": "DSC102",
    "subject_name": "Data Structures",
    "current_semester": 1,
    "credits": 4,
    "course_id": 2,
    "course_name": "M.Sc",
    "department_name": "Computer Science"
  }
]
```

### Notes:

✔ `ts_id` is *required* for attendance marking
✔ Each subject teacher teaches will appear here

---

# 🟪 **3. GET STUDENTS TAUGHT BY TEACHER**

### 📘 **GET /teachers/{teacher_id}/students/**

**Who can call:** Teacher
**Purpose:** Get all the students of all subjects the teacher teaches

### URL Example:

```
/teachers/7/students/
```

### Optional Filter:

```
/teachers/7/students/?subject_id=3
```

### Response:

```json
[
  {
    "id": 11,
    "student_name": "Rahul",
    "email": "rahul@du.ac.in",
    "roll_number": "MCA2025001",
    "phone_number": "9876543210",
    "course": {
      "id": 2,
      "course_name": "MCA",
      "dept": "Computer Science",
      "total_semesters": 4
    },
    "current_semester": 1,
    "year_of_study": 1,
    "subject_id": 3,
    "subject_name": "Data Structures",
    "attendance_percentage": 82.5
  }
]
```

### Notes:

✔ This API gives **student_id**
✔ Use these IDs in attendance marking
✔ Attendance % is pre-calculated

---

# 🟥 **4. MARK ATTENDANCE (Bulk)**

### 📘 **POST /attendance/mark/**

**Who can call:** Teacher
**Purpose:** Mark attendance for ALL students of a subject/date in one API call

### Headers:

```
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Body:

```json
{
  "ts_id": 12,
  "attendance_date": "2025-01-20",
  "present": [11, 12, 13],
  "absent": [14, 15]
}
```

### Response:

```json
{
  "message": "Attendance marked",
  "created": 5,
  "updated": 0
}
```

### Notes:

✔ `present` and `absent` = list of **student table IDs**
✔ Backend automatically validates allowed students
✔ One-shot bulk attendance marking

---

# 🟩 **5. TEACHER ATTENDANCE HISTORY (All classes teacher taught)**

### 📘 **GET /attendance/teacherwise/?teacher_id={teacher_id}**

**Who can call:** Teacher
**Purpose:** Get all attendance marked by teacher + filters

### Example:

```
/attendance/teacherwise/?teacher_id=7
```

### Filters:

| Filter         | Query Param  | Example            |
| -------------- | ------------ | ------------------ |
| By subject     | `subject_id` | `&subject_id=3`    |
| By date        | `date`       | `&date=2025-01-20` |
| By status      | `status`     | `&status=Present`  |
| Search student | `search`     | `&search=rahul`    |
| By course      | `course_id`  | `&course_id=2`     |
| By semester    | `semester`   | `&semester=1`      |

### Response:

```json
[
  {
    "date": "2025-01-20",
    "status": "Present",
    "student_name": "Rahul",
    "roll_number": "MCA2025001",
    "subject_name": "Data Structures",
    "subject_code": "DSC102",
    "course_name": "M.Sc"
  }
]
```

### Notes:

✔ Perfect for Teacher Dashboard
✔ Supports searching, filtering, sorting
✔ Gives subject, course, student details

---

# 🟧 **6. COURSE SUBJECTS FOR TEACHERS**

### 📘 **GET /courses/{course_id}/subjects/?semester=1**

**Who can call:** Teacher
**Purpose:** Get all subjects mapped to a course

### Example:

```
GET /courses/2/subjects/?semester=1
```

### Response:

```json
[
  {
    "id": 3,
    "subject_name": "Data Structures",
    "subject_code": "DSC102",
    "current_semester": 1,
    "credits": 4
  }
]
```

---

# 🎯 **TEACHER API SUMMARY TABLE**

| Feature             | URL                                 | Method | Body Required | Role    |
| ------------------- | ----------------------------------- | ------ | ------------- | ------- |
| Get subjects taught | `/teachers/subjectwise/`            | GET    | No            | Teacher |
| Get ts_id list      | `/teachers/me/teacher-subject-ids/` | GET    | No            | Teacher |
| Get students taught | `/teachers/{id}/students/`          | GET    | No            | Teacher |
| Bulk attendance     | `/attendance/mark/`                 | POST   | YES           | Teacher |
| Attendance history  | `/attendance/teacherwise/`          | GET    | No            | Teacher |
| Course subjects     | `/courses/{id}/subjects/`           | GET    | No            | Teacher |

---
