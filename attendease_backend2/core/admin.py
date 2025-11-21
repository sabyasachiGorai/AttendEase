from django.contrib import admin
from .models import (
    Department, Course, AcademicYear, Semester,
    Subject, CourseSubject, Teacher, TeacherSubject,
    Student, StudentSubjectEnrollment, Attendance
)

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(AcademicYear)
# admin.site.register(Semester)
admin.site.register(Subject)
admin.site.register(CourseSubject)
admin.site.register(Teacher)
admin.site.register(TeacherSubject)
# admin.site.register(Student)
admin.site.register(StudentSubjectEnrollment)
admin.site.register(Attendance)




class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_name",          # <-- shows student's user name
        "roll_number",
        "course",
        "current_semester",
        "year_of_study",
    )

    search_fields = (
        "User__email",
        "User__name",
        "roll_number",
        "phone_number",
    )

    list_filter = (
        "course",
        "current_semester",
        "year_of_study",
    )

    ordering = ("id",)

    def user_name(self, obj):
        return obj.User.name   # Access the name field from related User

    user_name.short_description = "Student Name"

    # Optional: show dropdown search instead of huge list
    # autocomplete_fields = ("User", "course", "current_semester")

admin.site.register(Student, StudentAdmin)