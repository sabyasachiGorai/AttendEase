from django.db import models

class Department(models.Model):
    dept_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.dept_name


class Course(models.Model):
    course_name = models.CharField(max_length=100, unique=True)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return self.course_name

class Subject(models.Model):
    subject_code = models.CharField(max_length=50, unique=True)
    subject_name = models.CharField(max_length=100)
    credits = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.subject_code} - {self.subject_name}"

class Course(models.Model):
    course_name = models.CharField(max_length=100, unique=True)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    subjects = models.ManyToManyField(Subject, through='CourseSubject')

    def __str__(self):
        return self.course_name


class CourseSubject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course', 'subject')

    def __str__(self):
        return f"{self.course} - {self.subject}"

class Teacher(models.Model):
    employee_code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='teachers')
    designation = models.CharField(max_length=50, blank=True, null=True)
    joining_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Teacher(models.Model):
    # ... fields as above ...
    subjects = models.ManyToManyField(Subject, through='TeacherSubject')

class TeacherSubject(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('teacher', 'subject')

    def __str__(self):
        return f"{self.teacher} teaches {self.subject}"


class Student(models.Model):
    roll_number = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')
    year_of_study = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.roll_number} - {self.first_name} {self.last_name}"


from django.core.validators import MinValueValidator, MaxValueValidator

year_of_study = models.PositiveSmallIntegerField(
    validators=[MinValueValidator(1), MaxValueValidator(5)]
)


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    teacher_subject = models.ForeignKey('TeacherSubject', on_delete=models.CASCADE, related_name='attendances')
    attendance_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'teacher_subject', 'attendance_date')

    def __str__(self):
        return f"{self.student} - {self.attendance_date} - {self.status}"



class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    event_date = models.DateField()
    event_time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    created_by_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    created_by_student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    approval_status = models.CharField(max_length=20, default='Pending')

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.created_by_teacher and self.created_by_student:
            raise ValidationError('Event cannot be created by both teacher and student.')

    def __str__(self):
        return self.title



class StudentSubjectEnrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.PositiveSmallIntegerField()
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'subject', 'semester')

    def __str__(self):
        return f"{self.student} enrolled in {self.subject} (Semester {self.semester})"



class SubjectOffering(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('subject', 'semester')
        constraints = [
            models.CheckConstraint(check=models.Q(semester__gte=1) & models.Q(semester__lte=8), name='valid_semester')
        ]

    def __str__(self):
        return f"{self.subject} offered in semester {self.semester}"
