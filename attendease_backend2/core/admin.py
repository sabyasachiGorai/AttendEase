from django.contrib import admin
from .models import (
    Department,
    Course,
    Subject,
    CourseSubject,
    Teacher,
    TeacherSubject,
    Student,
    StudentSubjectEnrollment,
    Attendance
)

# Register simple models
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(CourseSubject)
admin.site.register(Teacher)
admin.site.register(TeacherSubject)
admin.site.register(StudentSubjectEnrollment)
admin.site.register(Attendance)


# -------------------------
# Student Admin (Customized)
# -------------------------
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_name",        
        "roll_number",
        "course",
        "current_semester",
        "year_of_study",
    )

    search_fields = (
        "user__email",
        "user__name",
        "roll_number",
        "phone_number",
    )

    list_filter = (
        "course",
        "current_semester",
        "year_of_study",
    )

    ordering = ("id",)

    # Corrected function
    def user_name(self, obj):
        return obj.user.name

    user_name.short_description = "Student Name"


# Register Student using the custom admin
admin.site.register(Student, StudentAdmin)
