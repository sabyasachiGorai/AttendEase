from rest_framework import serializers
from .models import (
    Department, Course, AcademicYear, Semester, Subject, CourseSubject,
    Teacher, TeacherSubject, Student, StudentSubjectEnrollment, Attendance
)

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    dept = DepartmentSerializer(read_only=True)
    dept_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), write_only=True, source='dept')
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'dept', 'dept_id', 'total_semesters']

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'

class SemesterSerializer(serializers.ModelSerializer):
    academic_year = AcademicYearSerializer(read_only=True)
    academic_year_id = serializers.PrimaryKeyRelatedField(queryset=AcademicYear.objects.all(), write_only=True, source='academic_year')
    class Meta:
        model = Semester
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer(read_only=True)
    semester_id = serializers.PrimaryKeyRelatedField(queryset=Semester.objects.all(), write_only=True, source='semester', required=False, allow_null=True)
    class Meta:
        model = Subject
        fields = ['id', 'subject_code', 'subject_name', 'credits', 'semester', 'semester_id']

class CourseSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubject
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), write_only=True, source='department')
    class Meta:
        model = Teacher
        fields = '__all__'

class TeacherSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSubject
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True, source='course')
    current_semester = SemesterSerializer(read_only=True)
    current_semester_id = serializers.PrimaryKeyRelatedField(queryset=Semester.objects.all(), write_only=True, source='current_semester', required=False, allow_null=True)
    class Meta:
        model = Student
        fields = '__all__'

class StudentSubjectEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSubjectEnrollment
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
