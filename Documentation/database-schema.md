
# AttendEase Database Schema
-----

### 1. Departments Table

```sql
CREATE TABLE departments (
    dept_id SERIAL PRIMARY KEY,
    dept_name VARCHAR(100) UNIQUE NOT NULL
);
```

  * *Purpose:* This is a foundational *lookup table* that stores a unique list of all academic departments in the institution, such as "Computer Science" or "Mathematics". It acts as a central reference for departments.
  * *Relationships:*
      * It is the *parent table* for courses and teachers.
      * courses.dept_id references departments.dept_id (A course belongs to one department).
      * teachers.department_id references departments.dept_id (A teacher belongs to one department).

-----

###  2. Courses Table

```sql
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) UNIQUE NOT NULL,
    dept_id INT NOT NULL REFERENCES departments(dept_id) ON DELETE CASCADE
);

```

  * *Purpose:* This table holds the list of academic programs or degrees offered by the institution, like "Master of Computer Applications (MCA)" or "MSc in Physics".
  * *Relationships:*
      * **departments**: Has a many-to-one relationship. Many courses can belong to a single department.
      * **students**: Has a one-to-many relationship. A single course can have many students enrolled in it.
      * **course_subject**: Has a one-to-many relationship with this junction table to define its curriculum.

-----

###  3. Subjects Table

```sql

CREATE TABLE subjects (
    subject_id SERIAL PRIMARY KEY,
    subject_code VARCHAR(50) UNIQUE NOT NULL,
    subject_name VARCHAR(100) NOT NULL,
    credits INT DEFAULT 3
);

```

  * *Purpose:* This table is a master list of all individual subjects or papers that can be taught, such as "Data Structures," "Quantum Mechanics," or "Database Management Systems." Crucially, a subject here is an independent entity, not tied to any single course.
  * *Relationships:*
      * This table is a central hub and is referenced by many other tables to specify a particular subject. It has relationships with course_subject, teacher_subject, student_subject_enrollments, and subject_offerings.

-----

###  4. Course_Subject Table

```sql
CREATE TABLE course_subject (
    cs_id SERIAL PRIMARY KEY,
    course_id INT NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
    subject_id INT NOT NULL REFERENCES subjects(subject_id) ON DELETE CASCADE,
    UNIQUE(course_id, subject_id)
);
```

  * *Purpose:* This is a *junction table* (or mapping table). Its sole purpose is to create a *many-to-many relationship* between courses and subjects. It allows you to define the curriculum for each course.
  * *Relationships:*
      * It links the courses and subjects tables.
      * This allows a single subject (e.g., "Programming 101") to be part of multiple courses (e.g., "MCA" and "MSc CS"), and a single course to contain many subjects.

-----

###  5. Teachers Table

```sql
CREATE TABLE teachers (
    teacher_id SERIAL PRIMARY KEY,
    employee_code VARCHAR(50) UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    department_id INT NOT NULL REFERENCES departments(dept_id) ON DELETE CASCADE,
    designation VARCHAR(50),
    joining_date DATE,
    status VARCHAR(20) DEFAULT 'Active'
);
```

  * *Purpose:* This table stores the profile information for all teachers, faculty members, and professors. It includes details like their name, employee code, email, and designation.
  * *Relationships:*
      * **departments**: Has a many-to-one relationship. Many teachers can belong to the same department.
      * **teacher_subject**: Has a one-to-many relationship with this junction table to define which subjects they teach.
      * **events**: A teacher can be the creator of an event (created_by_teacher).

-----

###  6. Teacher_Subject Table

```sql
CREATE TABLE teacher_subject (
    ts_id SERIAL PRIMARY KEY,
    teacher_id INT NOT NULL REFERENCES teachers(teacher_id) ON DELETE CASCADE,
    subject_id INT NOT NULL REFERENCES subjects(subject_id) ON DELETE CASCADE,
    UNIQUE(teacher_id, subject_id)
);
```

  * *Purpose:* This is another *junction table. It maps which teachers are assigned to or are qualified to teach which subjects, creating a **many-to-many relationship* between them. Each row represents a specific class offering (e.g., Dr. Smith teaching Data Structures).
  * *Relationships:*
      * It links the teachers and subjects tables.
      * **attendance**: The primary key (ts_id) is now referenced by the attendance table to ensure that attendance is marked against a valid teacher-subject pairing.

-----

###  7. Students Table

```sql
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    roll_number VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone_number VARCHAR(20),
    course_id INT NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
    // add in which semester
    year_of_study INT NOT NULL CHECK (year_of_study BETWEEN 1 AND 5)
);
```

  * *Purpose:* This table contains all the necessary profile information for each student, including their roll number, name, and the course they are enrolled in.
  * *Relationships:*
      * **courses**: Has a many-to-one relationship. Many students can be enrolled in the same course.
      * It is referenced by attendance, events, and student_subject_enrollments.

-----

###  8. Attendance Table

```sql
CREATE TABLE attendance (
    attendance_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    ts_id INT NOT NULL REFERENCES teacher_subject(ts_id) ON DELETE CASCADE,
    attendance_date DATE NOT NULL,
    status VARCHAR(10) CHECK (status IN ('Present','Absent')) NOT NULL,
    UNIQUE(student_id, ts_id, attendance_date)
);
```

  * *Purpose:* This is a *transactional table*. It is used to record the attendance status ('Present', 'Absent', 'Late') of a student for a specific class on a specific date. Each row is a single attendance record.
  * *Relationships:*
      * **students**: Identifies which student the record belongs to.
      * **teacher_subject**: Identifies the specific class (the combination of a teacher and a subject) for which attendance is being taken. This provides strong data integrity.

-----


###  10. student_subject_enrollments Table

```sql
CREATE TABLE student_subject_enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    subject_id INT NOT NULL REFERENCES subjects(subject_id) ON DELETE CASCADE,
    semester INT NOT NULL,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    UNIQUE(student_id, subject_id, semester)
);
```

  * *Purpose:* This *junction table* tracks the enrollment of students in various subjects for a specific semester. This table answers the question, "Which subjects is this student taking this semester?"
  * *Relationships:*
      * It creates a *many-to-many relationship* between students and subjects.

-----
