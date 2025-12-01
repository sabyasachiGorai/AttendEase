from rest_framework import serializers
from .models import (
    Department, Course, Subject, CourseSubject,
    Teacher, TeacherSubject, Student, StudentSubjectEnrollment, Attendance
)


# -------------------------
# Department
# -------------------------
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


# -------------------------
# Course
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
# -------------------------
class CourseSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubject
        fields = '__all__'


# -------------------------
# Teacher
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
# -------------------------
class TeacherSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSubject
        fields = '__all__'


# -------------------------
# Student
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
# -------------------------
class StudentSubjectEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSubjectEnrollment
        fields = '__all__'


# -------------------------
# Attendance
# -------------------------
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
