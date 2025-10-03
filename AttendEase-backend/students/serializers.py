# students/serializers.py
from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "name", "email", "roll_number", "attendance_percentage", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
