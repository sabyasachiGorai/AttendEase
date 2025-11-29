from django.contrib.auth import get_user_model
from core.models import (
    Department, Course, Subject, CourseSubject,
    Teacher, TeacherSubject, Student, StudentSubjectEnrollment, Attendance
)
from django.utils.timezone import now

User = get_user_model()

def run():
    print("🌱 Seeding database with sample data...")

    # ------------------------
    # 1. Department
    # ------------------------
    cse = Department.objects.create(dept_name="Computer Science")
    maths = Department.objects.create(dept_name="Mathematics")

    # ------------------------
    # 2. Courses
    # ------------------------
    mca = Course.objects.create(course_name="MCA", dept=cse, total_semesters=4)
    bsc = Course.objects.create(course_name="BSc Mathematics", dept=maths, total_semesters=6)

    # ------------------------
    # 3. Subjects
    # ------------------------
    sub1 = Subject.objects.create(subject_code="MCA101", subject_name="Data Structures", credits=4, current_semester=1)
    sub2 = Subject.objects.create(subject_code="MCA102", subject_name="DBMS", credits=3, current_semester=1)
    sub3 = Subject.objects.create(subject_code="MCA201", subject_name="Operating Systems", credits=4, current_semester=2)

    # Link subjects to course (CourseSubject)
    CourseSubject.objects.create(course=mca, subject=sub1)
    CourseSubject.objects.create(course=mca, subject=sub2)
    CourseSubject.objects.create(course=mca, subject=sub3)

    # ------------------------
    # 4. Teacher Users
    # ------------------------
    tuser1 = User.objects.create_user(email="t1@example.com", name="Mr. Sharma", role="teacher", password="123456")
    tuser2 = User.objects.create_user(email="t2@example.com", name="Ms. Neha", role="teacher", password="123456")

    # Teacher profiles
    teacher1 = Teacher.objects.create(user=tuser1, employee_code="EMP001", department=cse)
    teacher2 = Teacher.objects.create(user=tuser2, employee_code="EMP002", department=cse)

    # ------------------------
    # 5. TeacherSubject
    # ------------------------
    TeacherSubject.objects.create(teacher=teacher1, subject=sub1, course=mca)
    TeacherSubject.objects.create(teacher=teacher1, subject=sub2, course=mca)
    TeacherSubject.objects.create(teacher=teacher2, subject=sub3, course=mca)

    # ------------------------
    # 6. Student Users
    # ------------------------
    suser1 = User.objects.create_user(email="s1@example.com", name="Rahul Kumar", role="student", password="123456")
    suser2 = User.objects.create_user(email="s2@example.com", name="Priya Singh", role="student", password="123456")

    # Student profiles
    student1 = Student.objects.create(user=suser1, roll_number="MCA001", course=mca, current_semester=1, year_of_study=1)
    student2 = Student.objects.create(user=suser2, roll_number="MCA002", course=mca, current_semester=1, year_of_study=1)

    # ------------------------
    # 7. Enroll subjects for students
    # ------------------------
    StudentSubjectEnrollment.objects.create(student=student1, subject=sub1, current_semester=1)
    StudentSubjectEnrollment.objects.create(student=student1, subject=sub2, current_semester=1)
    StudentSubjectEnrollment.objects.create(student=student2, subject=sub1, current_semester=1)

    # ------------------------
    # 8. Attendance for demo
    # ------------------------
    Attendance.objects.create(student=student1, ts=TeacherSubject.objects.first(), attendance_date=now(), status="Present")
    Attendance.objects.create(student=student2, ts=TeacherSubject.objects.first(), attendance_date=now(), status="Absent")

    print("🌱 DONE — Sample Data Inserted Successfully!")
