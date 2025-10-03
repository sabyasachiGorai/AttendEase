# students/admin.py
from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "roll_number", "email", "attendance_percentage", "created_at")
    search_fields = ("name", "roll_number", "email")
