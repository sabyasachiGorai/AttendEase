# core/models.py
from django.db import models

# -------------------------
# Department
# -------------------------
class Department(models.Model):
    dept_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.dept_name


# -------------------------
# Course
# -------------------------
class Course(models.Model):
    course_name = models.CharField(max_length=100, unique=True)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    total_semesters = models.IntegerField(default=4)  # set default as needed (MCA=4 sem? change to 6 if you want)

    def __str__(self):
        return self.course_name


# -------------------------
# AcademicYear (NEW)
# -------------------------
class AcademicYear(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='academic_years')
    year_number = models.IntegerField()  # 1, 2, ...
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('course', 'year_number')

    def __str__(self):
        return f"{self.course.course_name} - Year {self.year_number}"


# -------------------------
# Semester (NEW)
# -------------------------
class Semester(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='semesters')
    semester_number = models.IntegerField()  # 1 or 2 within that academic year
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('academic_year', 'semester_number')

    def __str__(self):
        global_index = (self.academic_year.year_number - 1) * 2 + self.semester_number
        return f"{self.academic_year.course.course_name} - Sem {global_index} (Y{self.academic_year.year_number}S{self.semester_number})"


# -------------------------
# Subject
# -------------------------
class Subject(models.Model):
    subject_code = models.CharField(max_length=50, unique=True)
    subject_name = models.CharField(max_length=100)
    credits = models.IntegerField(default=3)
    # link subject to specific Semester
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subjects', null=True, blank=True)

    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"


# -------------------------
# CourseSubject (junction)
# -------------------------
class CourseSubject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='course_subjects')

    class Meta:
        unique_together = ('course', 'subject')

    def __str__(self):
        return f"{self.course.course_name} - {self.subject.subject_name}"


# -------------------------
# Teacher
# -------------------------
class Teacher(models.Model):
    employee_code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='teachers')
    designation = models.CharField(max_length=50, null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# -------------------------
# TeacherSubject (junction)
# -------------------------
class TeacherSubject(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='teacher_subjects')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='teacher_subjects', null=True, blank=True)

    class Meta:
        unique_together = ('teacher', 'subject', 'course')

    def __str__(self):
        return f"{self.teacher} - {self.subject}"


# -------------------------
# Student
# -------------------------
class Student(models.Model):
    roll_number = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')
    # now link student to a Semester
    current_semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    year_of_study = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.roll_number} - {self.first_name} {self.last_name}"


# -------------------------
# StudentSubjectEnrollment
# -------------------------
class StudentSubjectEnrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='enrollments')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True, blank=True, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'subject', 'semester')

    def __str__(self):
        return f"{self.student} - {self.subject}"


# -------------------------
# Attendance
# -------------------------
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    ts = models.ForeignKey(TeacherSubject, on_delete=models.CASCADE, related_name='attendance_records')
    attendance_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='marked_attendance')

    class Meta:
        unique_together = ('student', 'ts', 'attendance_date')

    def __str__(self):
        return f"{self.student} - {self.ts.subject.subject_name} - {self.attendance_date}"
