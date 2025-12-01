from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
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


# -------------------------
# Teacher Admin (Customized)
# -------------------------
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_name",        
        "employee_code",
        "department",
        "designation",
    )

    search_fields = (
        "user__email",
        "user__name",
        "employee_code",
        "phone_number",
    )

    list_filter = (
        "department",
        "designation",
        "status",
    )

    ordering = ("id",)

    # Corrected function
    def user_name(self, obj):
        return obj.user.name

    user_name.short_description = "Teacher Name"

# Register Student using the custom admin
admin.site.register(Teacher, TeacherAdmin)


# -------------------------
# Attendance Admin (Customized)
# -------------------------

class SubjectFilter(admin.SimpleListFilter):
    title = "Subject"
    parameter_name = "subject"

    def lookups(self, request, model_admin):
        subjects = TeacherSubject.objects.values_list(
            "subject_id", "subject__subject_name"
        ).distinct()
        return subjects

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(ts__subject_id=self.value())
        return queryset

class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student_name",
        "subject_name",
        "attendance_date",
        "status",
        "created_by_name",
        "created_at",
        "updated_at",
    )


    search_fields = (
        "student__user__name",
        "student__roll_number",
        "ts__subject__subject_name",
        "created_by__user__name",
        "attendance_date",
    )

    list_filter = (
        "status",
        "attendance_date",
        # "ts__subject__subject_name",
        SubjectFilter,
    )

    ordering = ("attendance_date",)

    # --- Custom Display Functions ---

    def student_name(self, obj):
        return obj.student.user.name
    student_name.short_description = "Student"

    def subject_name(self, obj):
        return obj.ts.subject.subject_name
    subject_name.short_description = "Subject"

    def created_by_name(self, obj):
        return obj.created_by.user.name if obj.created_by else "—"
    created_by_name.short_description = "Marked By"

# Register Attendance model with the custom admin
admin.site.register(Attendance, AttendanceAdmin)

# -------------------------
# Teacher-Subject Admin (Customized)
# -------------------------
class TeacherSubjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "teacher_name",
        "subject_name",
        "course_name",
    )

    search_fields = (
        "teacher__user__name",
        "teacher__employee_code",
        "subject__subject_name",
        "course__course_name",
    )

    list_filter = (
        "subject__subject_name",
        "course__course_name",
        "teacher__department",
    )

    ordering = ("id",)

    # ----- Custom Display Methods -----

    def teacher_name(self, obj):
        return obj.teacher.user.name
    teacher_name.short_description = "Teacher"

    def subject_name(self, obj):
        return obj.subject.subject_name
    subject_name.short_description = "Subject"

    def course_name(self, obj):
        return obj.course.course_name
    course_name.short_description = "Course"


# Register TeacherSubject in admin
admin.site.register(TeacherSubject, TeacherSubjectAdmin)


# -------------------------
# Student-Subject Admin (Customized)
# -------------------------
class StudentSubjectEnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student_name",
        "subject_name",
        "current_semester",
        "enrollment_date",
    )

    search_fields = (
        "student__user__name",
        "student__roll_number",
        "subject__subject_name",
        "current_semester",
    )

    list_filter = (
        "current_semester",
        "subject__subject_name",
        "enrollment_date",
    )

    ordering = ("id",)

    # ----- Custom Display Methods -----

    def student_name(self, obj):
        return obj.student.user.name
    student_name.short_description = "Student"

    def subject_name(self, obj):
        return obj.subject.subject_name
    subject_name.short_description = "Subject"

# Register StudentSubjectEnrollment in admin
admin.site.register(StudentSubjectEnrollment, StudentSubjectEnrollmentAdmin)

# -------------------------
#Subject Admin (Customized)
# -------------------------
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subject_code",
        "subject_name",
        "credits",
        "current_semester",
        "courses_list",
    )

    search_fields = (
        "subject_code",
        "subject_name",
        "current_semester",
        "course_subjects__course__course_name",
    )

    list_filter = (
        "current_semester",
        "credits",
        "course_subjects__course__course_name",
    )

    ordering = ("id",)

    # Custom Function: Show Course(s) that the Subject belongs to
    def courses_list(self, obj):
        courses = obj.course_subjects.values_list("course__course_name", flat=True)
        return ", ".join(courses) if courses else "—"
    courses_list.short_description = "Courses"

# Register Subject model
admin.site.register(Subject, SubjectAdmin)

# -------------------------
# Course-Subject Admin (Customized)
# -------------------------
class CourseSubjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "course_name",
        "subject_name",
        "assigned_teachers",
    )

    search_fields = (
        "course__course_name",
        "subject__subject_code",
        "subject__subject_name",
        "subject__teacher_subjects__teacher__user__name",
    )

    list_filter = (
        "course__course_name",
        "subject__subject_name",
        "subject__teacher_subjects__teacher__user__name",
    )

    ordering = ("id",)

    # ---- Custom Display Methods ----

    def course_name(self, obj):
        return obj.course.course_name
    course_name.short_description = "Course"

    def subject_name(self, obj):
        return obj.subject.subject_name
    subject_name.short_description = "Subject"

    def assigned_teachers(self, obj):
        teachers = obj.subject.teacher_subjects.values_list(
            "teacher__user__name", flat=True
        )
        return ", ".join(teachers) if teachers else "—"
    assigned_teachers.short_description = "Assigned Teacher(s)"


admin.site.register(CourseSubject, CourseSubjectAdmin)

