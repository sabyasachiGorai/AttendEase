from django.contrib import admin
from .models import Department, Course, Subject, Teacher, TeacherSubject, Student, Attendance, Event, StudentSubjectEnrollment, SubjectOffering

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(TeacherSubject)
admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(Event)
admin.site.register(StudentSubjectEnrollment)
admin.site.register(SubjectOffering)
