from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import (
    Department, Course, Subject, CourseSubject,
    Teacher, TeacherSubject, Student, StudentSubjectEnrollment, Attendance
)

from .serializers import (
    DepartmentSerializer, CourseSerializer, SubjectSerializer,
    CourseSubjectSerializer, TeacherSerializer, TeacherSubjectSerializer,
    StudentSerializer, StudentSubjectEnrollmentSerializer, AttendanceSerializer
)

from core.permissions import IsAdmin, IsTeacher, IsStudent


# ===========================================================
# 1. DEPARTMENT CRUD  (Admin = full CRUD, Teacher/Student = Read)
# ===========================================================
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return [IsAdmin()]
        return [IsAuthenticated()]


# ===========================================================
# 2. COURSE CRUD (Admin full CRUD, Teacher/Student read-only)
# ===========================================================
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return [IsAdmin()]
        return [IsAuthenticated()]


# ===========================================================
# 3. SUBJECT CRUD (Admin full CRUD, Teacher/Student read-only)
# ===========================================================
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return [IsAdmin()]
        return [IsAuthenticated()]


# ===========================================================
# 4. COURSE-SUBJECT CRUD (Admin only)
# ===========================================================
class CourseSubjectViewSet(viewsets.ModelViewSet):
    queryset = CourseSubject.objects.all()
    serializer_class = CourseSubjectSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


# ===========================================================
# 5. TEACHER VIEWSET
# - Admin: full CRUD
# - Teacher: can only see THEIR OWN profile
# - Student: cannot access teachers
# ===========================================================
class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'admin':
            return Teacher.objects.all()

        if user.role == 'teacher':
            return Teacher.objects.filter(user=user)

        return Teacher.objects.none()

    def get_permissions(self):
        user = self.request.user

        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return [IsAdmin()]

        return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def subjectwise(self, request):
        user = request.user

        if user.role != 'teacher':
            return Response({"error": "Only teachers allowed"}, status=403)

        teacher = Teacher.objects.filter(user=user).first()

        if not teacher:
            return Response({"error": "Teacher profile not found"}, status=404)

        ts_list = TeacherSubject.objects.filter(teacher=teacher).select_related(
            'subject', 'course', 'course__dept'
        )

        data = []
        for ts in ts_list:
            data.append({
                "subject_id": ts.subject.id,
                "subject_code": ts.subject.subject_code,
                "subject_name": ts.subject.subject_name,
                "course": ts.course.course_name,
                "department": ts.course.dept.dept_name,
                "semester": ts.subject.current_semester
            })

        return Response(data)


# ===========================================================
# 6. TEACHER-SUBJECT CRUD (Admin only)
# ===========================================================
class TeacherSubjectViewSet(viewsets.ModelViewSet):
    queryset = TeacherSubject.objects.all()
    serializer_class = TeacherSubjectSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


# ===========================================================
# 7. STUDENT VIEWSET
# - Admin: full access
# - Student: only themselves
# - Teacher: only students enrolled in their subjects
# ===========================================================
class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'admin':
            return Student.objects.all()

        if user.role == 'student':
            return Student.objects.filter(user=user)

        if user.role == 'teacher':
            subjects = TeacherSubject.objects.filter(
                teacher__user=user
            ).values_list('subject_id', flat=True)

            return Student.objects.filter(
                enrollments__subject_id__in=subjects
            ).distinct()

        return Student.objects.none()

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return [IsAdmin()]
        return [IsAuthenticated()]


    # --------------------------
    # student → view own subjects + teacher info
    # --------------------------
    @action(detail=False, methods=['get'])
    def subjects_teachers(self, request):
        user = request.user
        student_id = request.query_params.get('student_id')

        if user.role == 'student' and student_id and str(user.student_profile.id) != student_id:
            return Response({"error": "Not allowed"}, status=403)

        if user.role == 'teacher':
            # teacher can only view if student is in their subject
            pass  # (optional extended rule)

        student = Student.objects.filter(id=student_id).first()
        if not student:
            return Response({"error": "Student not found"}, status=404)

        enrollments = StudentSubjectEnrollment.objects.filter(student=student)

        data = []
        for enroll in enrollments:
            subject = enroll.subject
            ts = TeacherSubject.objects.filter(
                subject=subject,
                course=student.course
            ).first()

            teacher_info = None
            if ts:
                teacher_info = {
                    "id": ts.teacher.id,
                    "email": ts.teacher.user.email,
                    "department": ts.teacher.department.dept_name
                }

            data.append({
                "subject_id": subject.id,
                "subject_code": subject.subject_code,
                "subject_name": subject.subject_name,
                "teacher": teacher_info
            })

        return Response(data)


# ===========================================================
# 8. ENROLLMENT CRUD (Admin only)
# ===========================================================
class StudentSubjectEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = StudentSubjectEnrollment.objects.all()
    serializer_class = StudentSubjectEnrollmentSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


# ===========================================================
# 9. ATTENDANCE VIEWSET
# - Teacher: only their classes
# - Student: only their attendance
# - Admin: full access
# ===========================================================
class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'admin':
            return Attendance.objects.all()

        if user.role == 'student':
            return Attendance.objects.filter(student__user=user)

        if user.role == 'teacher':
            teacher = Teacher.objects.filter(user=user).first()
            return Attendance.objects.filter(ts__teacher=teacher)

        return Attendance.objects.none()

    # --------------------------
    # MARK ATTENDANCE (TEACHERS ONLY)
    # --------------------------
    @action(detail=False, methods=['post'])
    def mark(self, request):
        user = request.user

        if user.role != 'teacher':
            return Response({"error": "Only teachers can mark attendance"}, status=403)

        teacher = Teacher.objects.filter(user=user).first()

        ts_id = request.data.get('ts_id')
        ts = TeacherSubject.objects.filter(id=ts_id, teacher=teacher).first()

        if not ts:
            return Response({"error": "You are not assigned to this class"}, status=403)

        date = request.data.get('attendance_date')
        present = request.data.get('present', [])
        absent = request.data.get('absent', [])

        for sid in present:
            Attendance.objects.update_or_create(
                student_id=sid, ts=ts, attendance_date=date,
                defaults={"status": "Present", "created_by": teacher}
            )

        for sid in absent:
            Attendance.objects.update_or_create(
                student_id=sid, ts=ts, attendance_date=date,
                defaults={"status": "Absent", "created_by": teacher}
            )

        return Response({"message": "Attendance updated"}, status=201)


# ===========================================================
# 10. COURSE SUBJECT LIST VIEW
# ===========================================================
class CourseSubjectsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        semester = request.query_params.get("semester")
        qs = Subject.objects.filter(course_subjects__course_id=course_id)

        if semester:
            qs = qs.filter(current_semester=semester)

        return Response(SubjectSerializer(qs, many=True).data)


# ===========================================================
# 11. TEACHER STUDENTS VIEW
# ===========================================================
class TeacherStudentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, teacher_id):
        user = request.user

        if user.role != 'teacher' or user.teacher_profile.id != teacher_id:
            return Response({"error": "Not allowed"}, status=403)

        subjects = TeacherSubject.objects.filter(
            teacher_id=teacher_id
        ).values_list("subject_id", flat=True)

        students = Student.objects.filter(
            enrollments__subject_id__in=subjects
        ).distinct()

        return Response(StudentSerializer(students, many=True).data)
