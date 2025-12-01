
# 🚀 **STUDENT API DOCUMENTATION ()**

Version: **AttendEase Backend v1**
Auth Type: **JWT Bearer Token**
Role Required: **Student**
Base URL: `{{base_url}}/api/`

---

# 📌 **AUTH REQUIRED FOR ALL STUDENT APIs**

Students must log in first:

### **POST /api/user/login/**

Body:

```json
{
  "email": "student@example.com",
  "password": "password123"
}
```

Success Response:

```json
{
  "user_id": 23,
  "user_name": "Aman Singh",
  "context": {
    "role": "student",
    "id": 11,
    "empCode_RollNo": "MCA2025001"
  },
  "token": {
    "access": "JWT_ACCESS_TOKEN"
  }
}
```

Save:

* `access_token`
* `student_id` (optional, since endpoints use `/me/`)

---

# 🟩 **1. GET ALL SUBJECTS + ATTENDANCE SUMMARY**

### 📘 **GET /students/me/subjects-attendance/**

**Role:** Student
**Purpose:** Student sees all subjects enrolled + attendance summary for EACH subject.

---

### 🔐 Headers:

```
Authorization: Bearer <access_token>
```

---

### 🔽 Response Example:

```json
[
  {
    "subject_id": 3,
    "subject_name": "Data Structures",
    "subject_code": "DSC102",
    "credits": 4,
    "teacher_name": "Prof. Ajay",
    "total_classes": 40,
    "attended_classes": 32,
    "percentage": 80.0
  },
  {
    "subject_id": 5,
    "subject_name": "OOP",
    "subject_code": "OOP101",
    "credits": 4,
    "teacher_name": "Prof. Shweta",
    "total_classes": 38,
    "attended_classes": 36,
    "percentage": 94.7
  }
]
```

---

### ✔ Data Included:

* All subjects student is enrolled in
* Subject code
* Subject credits
* Teacher name
* Total classes
* Attended classes
* Attendance percentage

---

### ✔ Use Cases:

* Student dashboard
* Attendance donut charts
* Subject list page

---

# 🟦 **2. GET DATE-WISE ATTENDANCE FOR ONE SUBJECT**

### 📘 **GET /students/me/attendance/?subject_id={id}**

**Role:** Student
**Purpose:** Shows all attendance entries for one subject.

---

### 📌 Required Query Param:

```
subject_id = <subject_id_from_previous_api>
```

---

### 🔐 Headers:

```
Authorization: Bearer <access_token>
```

---

### 🔽 Response Example:

```json
[
  {
    "date": "2025-01-21",
    "status": "Present",
    "subject_name": "Data Structures",
    "teacher_name": "Prof. Ajay"
  },
  {
    "date": "2025-01-20",
    "status": "Absent",
    "subject_name": "Data Structures",
    "teacher_name": "Prof. Ajay"
  }
]
```

---

### ✔ Data Included:

* Class date
* Attendance status
* Subject name
* Teacher name

---

### ✔ Use Cases:

* When student clicks a subject
* Build a detailed attendance table
* Date sorting (newest → oldest)

---

# 🟧 **3. GET SUBJECTS UNDER A COURSE**

### 📘 **GET /courses/{course_id}/subjects/?semester={n}**

**Role:** Student OR Teacher
**Purpose:** Show all subjects available in a course/semester.

---

### 🔐 Headers:

```
Authorization: Bearer <access_token>
```

---

### 🔽 Example:

```
GET /courses/2/subjects/?semester=1
```

Response:

```json
[
    {
        "id": 16,
        "subject_code": "MCSC101",
        "subject_name": "Design and Analysis of Algorithms",
        "credits": 4,
        "current_semester": 1,
        "teacher_name": "Prof. Design"
    },
    {
        "id": 17,
        "subject_code": "MCSC102",
        "subject_name": "Artificial Intelligence",
        "credits": 4,
        "current_semester": 1,
        "teacher_name": "Prof. Artificial"
    },
    {
        "id": 18,
        "subject_code": "MCSC103",
        "subject_name": "Information Security",
        "credits": 4,
        "current_semester": 1,
        "teacher_name": "Prof. Information"
    },
    {
        "id": 19,
        "subject_code": "MCSC104",
        "subject_name": "Mathematical Foundations of Computer Science",
        "credits": 4,
        "current_semester": 1,
        "teacher_name": "Prof. Mathematical"
    },
    {
        "id": 20,
        "subject_code": "MCSC105",
        "subject_name": "Data Mining",
        "credits": 4,
        "current_semester": 1,
        "teacher_name": "Prof. Data"
    }
]
```

---

### ✔ Use Cases:

* Student course curriculum page
* Subject selection dropdown
* My course page

---

# 🟨 **4. STUDENT PROFILE API (Optional but Common)**

### 📘 **GET /api/student/profile/**

(From account app)

**Role:** Student

### Response:

```json
{
  "id": 11,
  "name": "Aman Singh",
  "email": "aman@example.com",
  "roll_number": "MCA2025001",
  "course": "MCA",
  "semester": 1
}
```

---

# 🎯 **STUDENT API SUMMARY TABLE**

| Feature                   | Method | Endpoint                               | Body | Who             | Notes               |
| ------------------------- | ------ | -------------------------------------- | ---- | --------------- | ------------------- |
| All subjects + attendance | GET    | `/students/me/subjects-attendance/`    | ❌    | Student         | Shows summary       |
| Date-wise attendance      | GET    | `/students/me/attendance/?subject_id=` | ❌    | Student         | Requires subject_id |
| Course subjects           | GET    | `/courses/{course_id}/subjects/`       | ❌    | Student/Teacher | Semester optional   |
| Student profile           | GET    | `/student/profile/`                    | ❌    | Student         | (Account API)       |

---

# 🟢 **Student Flow (Frontend Sequence)**

### Step 1

Student logs in → receives token + student_id

### Step 2

Call:

```
/students/me/subjects-attendance/
```

Show list of subjects + attendance %

### Step 3

When student clicks a subject:

```
/students/me/attendance/?subject_id=3
```

Show date-wise attendance

### Step 4

Show course subjects (optional):

```
/courses/2/subjects/?semester=1
```

---

