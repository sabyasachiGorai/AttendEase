from django.contrib import admin
from .models import (
    Department, Course, AcademicYear, Semester,
    Subject, CourseSubject, Teacher, TeacherSubject,
    Student, StudentSubjectEnrollment, Attendance
)

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(AcademicYear)
admin.site.register(Semester)
admin.site.register(Subject)
admin.site.register(CourseSubject)
admin.site.register(Teacher)
admin.site.register(TeacherSubject)
admin.site.register(Student)
admin.site.register(StudentSubjectEnrollment)
admin.site.register(Attendance)
