from django.db import models
from django.conf import settings

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
    total_semesters = models.IntegerField(default=4)

    def __str__(self):
        return self.course_name


# -------------------------
# Subject
# -------------------------
class Subject(models.Model):
    subject_code = models.CharField(max_length=50, unique=True)
    subject_name = models.CharField(max_length=100)
    credits = models.IntegerField(default=3)
    current_semester = models.IntegerField(null=True, blank=True)

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
    # FIXED → use settings.AUTH_USER_MODEL
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        null=True,
        blank=True
    )
    employee_code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='teachers')
    designation = models.CharField(max_length=50, null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return f"{self.employee_code or ''} - {self.user}"


# -------------------------
# TeacherSubject (junction)
# -------------------------
class TeacherSubject(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='teacher_subjects')
    course = models.ForeignKey(
    Course,
    on_delete=models.CASCADE,
    related_name='teacher_subjects'
    )

    class Meta:
        unique_together = ('teacher', 'subject', 'course')

    def __str__(self):
        return f"{self.teacher} - {self.subject}"


# -------------------------
# Student
# -------------------------
class Student(models.Model):
    # FIXED → use settings.AUTH_USER_MODEL
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    roll_number = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')
    current_semester = models.IntegerField(null=True, blank=True)
    year_of_study = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.roll_number} - {self.user}"


# -------------------------
# StudentSubjectEnrollment
# -------------------------
class StudentSubjectEnrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='enrollments')
    current_semester = models.IntegerField(null=True, blank=True)
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'subject', 'current_semester')

    def __str__(self):
        return f"{self.student} - {self.subject}"


# -------------------------
# Attendance
# -------------------------
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    ts = models.ForeignKey(TeacherSubject, on_delete=models.CASCADE, related_name='attendance_records')
    attendance_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_by = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='marked_attendance'
    )
    created_at = models.DateTimeField(auto_now_add=True) # first time only
    updated_at = models.DateTimeField(auto_now=True) # changes on every update

    class Meta:
        unique_together = ('student', 'ts', 'attendance_date')

    def __str__(self):
        return f"{self.student} - {self.ts.subject.subject_name} - {self.attendance_date}"
