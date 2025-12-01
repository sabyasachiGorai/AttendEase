"""
-----------------------------------------------------------------------
Project     : AttendEase – Smart Attendance Management System
Module      : serializers.py
Author      : Sabyasachi Gorai
Description :
    This file contains all serializer classes used for converting
    Django ORM model instances into JSON format, and validating incoming
    API request data. These serializers bridge the communication between
    database models and API endpoints.
-----------------------------------------------------------------------
"""

from rest_framework import serializers
from .models import (
    Department, Course, Subject, CourseSubject,
    Teacher, TeacherSubject, Student, StudentSubjectEnrollment, Attendance
)


# -------------------------
# Department
# Serializes Department model for CRUD operations.
# -------------------------
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


# -------------------------
# Course
# Includes:
#   - dept (nested read-only serializer)
#   - dept_id (write-only field for creating/updating)
# This keeps API clean and avoids nested POST issues.
# -------------------------
class CourseSerializer(serializers.ModelSerializer):
    dept = DepartmentSerializer(read_only=True)
    dept_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        write_only=True,
        source='dept'
    )

    class Meta:
        model = Course
        fields = ['id', 'course_name', 'dept', 'dept_id', 'total_semesters']


# -------------------------
# Subject
# Adds teacher_name using SerializerMethodField for dynamic computed data.
# Does NOT include teacher relationship directly to avoid circular nesting.
# -------------------------
class SubjectSerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = [
            'id',
            'subject_code',
            'subject_name',
            'credits',
            'current_semester',
            'teacher_name'
        ]

    def get_teacher_name(self, obj):
        ts = obj.teacher_subjects.first()
        if ts and ts.teacher and ts.teacher.user:
            return ts.teacher.user.name
        return None


# -------------------------
# CourseSubject
# Simple serializer for the junction table.
# -------------------------
class CourseSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubject
        fields = '__all__'


# -------------------------
# Teacher
# Uses read-only user field because teachers are linked to user accounts.
# department_id is the write-only version of department.
# -------------------------
class TeacherSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # FIXED
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        write_only=True,
        source='department'
    )

    class Meta:
        model = Teacher
        fields = '__all__'


# -------------------------
# TeacherSubject
# Used for assigning a teacher to teach a specific subject in a course.
# -------------------------
class TeacherSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSubject
        fields = '__all__'


# -------------------------
# Student
# Contains nested course details (read)
# but accepts course_id (write) for clean API requests.
# -------------------------
class StudentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)   # FIXED
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        write_only=True,
        source='course'
    )


    class Meta:
        model = Student
        fields = [
            'id',
            'user',
            'roll_number',
            'phone_number',
            'course', 'course_id',
            'current_semester',
            'year_of_study'
        ]


# -------------------------
# Student Subject Enrollment
# Handles storing which student is enrolled in which subject.
# -------------------------
class StudentSubjectEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSubjectEnrollment
        fields = '__all__'


# -------------------------
# Attendance
# Straightforward serializer for attendance records.
# No custom fields needed.
# -------------------------
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
