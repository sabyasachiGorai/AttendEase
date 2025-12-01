from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q

from account.permissions import IsTeacher, IsStudent, IsAdmin
from rest_framework_simplejwt.tokens import AccessToken

from .models import (
    Department, Course, Subject, CourseSubject,
    Teacher, TeacherSubject, Student, StudentSubjectEnrollment, Attendance
)

from .serializers import (
    DepartmentSerializer, CourseSerializer, SubjectSerializer,
    CourseSubjectSerializer, TeacherSerializer, TeacherSubjectSerializer,
    StudentSerializer, StudentSubjectEnrollmentSerializer, AttendanceSerializer
)

# Utility: Extract user-id from token (optional use)
def get_user_id_from_token(token):
    access_token = AccessToken(token)
    return access_token['user_id']

# ============================================================
# ADMIN CRUD (Optional Admin-only)
# ============================================================

class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class CourseSubjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = CourseSubject.objects.all()
    serializer_class = CourseSubjectSerializer


# ============================================================
# TEACHER VIEWS
# ============================================================

class TeacherViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsTeacher]
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsTeacher])
    def subjectwise(self, request):
        teacher_id = request.user.teacher_profile.id

        ts_list = TeacherSubject.objects.filter(teacher_id=teacher_id).select_related(
            'subject', 'course', 'course__dept'
        )

        if not ts_list.exists():
            return Response({"message": "No subjects assigned"}, status=404)

        data = []
        for ts in ts_list:
            subject = ts.subject
            course = ts.course

            data.append({
                "subject_id": subject.id,
                "subject_code": subject.subject_code,
                "subject_name": subject.subject_name,
                "course": course.course_name,
                "department": course.dept.dept_name,
                "semester": subject.current_semester
            })

        return Response(data)


class TeacherSubjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = TeacherSubject.objects.all()
    serializer_class = TeacherSubjectSerializer



# ============================================================
# STUDENT CRUD (Admin only)
# ============================================================

class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# ============================================================
# STUDENT-TEACHER RELATED VIEWS
# ============================================================

class TeacherStudentsView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request, teacher_id):
        if request.user.teacher_profile.id != teacher_id:
            return Response({"error": "Access denied"}, status=403)

        subject_id = request.query_params.get("subject_id")

        teacher_subjects = TeacherSubject.objects.filter(teacher_id=teacher_id)

        if subject_id:
            teacher_subjects = teacher_subjects.filter(subject_id=subject_id)

        if not teacher_subjects.exists():
            return Response({"error": "No subjects found"}, status=404)

        subject_ids = teacher_subjects.values_list("subject_id", flat=True)
        course_ids = teacher_subjects.values_list("course_id", flat=True)

        enrollments = StudentSubjectEnrollment.objects.filter(
            subject_id__in=subject_ids,
            student__course_id__in=course_ids
        ).select_related("student", "subject", "student__user")

        output = []

        for enroll in enrollments:
            student = enroll.student
            subject = enroll.subject

            # records = Attendance.objects.filter(student=student, ts__subject_id=subject.id)
            # total = records.count()
            # attended = records.filter(status="Present").count()
            # percent = round((attended / total * 100), 2) if total else 0

            stats = Attendance.objects.filter(
                    student=student,
                    ts__subject_id=subject.id
                ).aggregate(
                    total=Count('id'),
                    attended=Count('id', filter=Q(status="Present"))
                )

            total = stats['total'] or 0
            attended = stats['attended'] or 0
            percent = round((attended / total * 100), 2) if total else 0

            output.append({
                "id": student.id,
                "student_name": student.user.name,
                "email": student.user.email,
                "roll_number": student.roll_number,
                "phone_number": student.phone_number,
                "course": {
                    "id": student.course.id,
                    "course_name": student.course.course_name,
                    "dept": student.course.dept.dept_name,
                    "total_semesters": student.course.total_semesters
                },
                "current_semester": student.current_semester,
                "year_of_study": student.year_of_study,
                "subject_id": subject.id,
                "subject_name": subject.subject_name,
                "attendance_percentage": percent
            })

        return Response(output)

class TeacherSubjectIDs(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        teacher = request.user.teacher_profile

        # Fetch all TeacherSubject mappings for this teacher
        ts_list = TeacherSubject.objects.filter(
            teacher=teacher
        ).select_related("subject", "course")

        if not ts_list.exists():
            return Response({"error": "No subjects assigned to this teacher"}, status=404)

        output = []

        for ts in ts_list:
            subject = ts.subject
            course = ts.course

            output.append({
                "ts_id": ts.id,                          # 
                "subject_id": subject.id,
                "subject_code": subject.subject_code,
                "subject_name": subject.subject_name,
                "current_semester": subject.current_semester,
                "credits": subject.credits,
                "course_id": course.id,
                "course_name": course.course_name,
                "department_name": course.dept.dept_name
            })

        return Response(output, status=200)

# ============================================================
# ENROLLMENT CRUD (Admin-only)
# ============================================================

class StudentSubjectEnrollmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = StudentSubjectEnrollment.objects.all()
    serializer_class = StudentSubjectEnrollmentSerializer



# ============================================================
# ATTENDANCE VIEWS
# ============================================================

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    # Teacher-only: Mark attendance
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, IsTeacher])
    def mark(self, request):
        teacher = request.user.teacher_profile
        ts_id = request.data.get('ts_id')
        date = request.data.get('attendance_date')
        present = request.data.get('present', [])
        absent = request.data.get('absent', [])

        if not ts_id or not date:
            return Response({"error": "Missing parameters"}, status=400)

        ts = TeacherSubject.objects.filter(id=ts_id).first()
        if not ts or ts.teacher != teacher:
            return Response({"error": "Unauthorized or invalid ts_id"}, status=403)

        valid_ids = set(
            StudentSubjectEnrollment.objects.filter(
                subject_id=ts.subject.id,
                student__course_id=ts.course.id
            ).values_list("student_id", flat=True)
        )

        present = [sid for sid in present if sid in valid_ids]
        absent = [sid for sid in absent if sid in valid_ids]

        created_count = 0
        updated_count = 0

        for sid in present:
            _, created = Attendance.objects.update_or_create(
                student_id=sid,
                ts=ts,
                attendance_date=date,
                defaults={"status": "Present", "created_by": teacher}
            )
            created_count += created

        for sid in absent:
            _, created = Attendance.objects.update_or_create(
                student_id=sid,
                ts=ts,
                attendance_date=date,
                defaults={"status": "Absent", "created_by": teacher}
            )
            created_count += created

        return Response({
            "message": "Attendance marked",
            "created": created_count,
            "updated": updated_count
        })


    # Teacher-only: Attendance history
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsTeacher])
    def teacherwise(self, request):
        teacher = request.user.teacher_profile
        subject_id = request.query_params.get("subject_id")
        date = request.query_params.get("date")
        course_id = request.query_params.get("course_id")
        status_filter = request.query_params.get("status")
        search = request.query_params.get("search")
        semester = request.query_params.get("semester")

        ts_qs = TeacherSubject.objects.filter(teacher=teacher)

        if subject_id:
            ts_qs = ts_qs.filter(subject_id=subject_id)
        if course_id:
            ts_qs = ts_qs.filter(course_id=course_id)

        ts_ids = ts_qs.values_list("id", flat=True)
        records = Attendance.objects.filter(ts_id__in=ts_ids).select_related(
            "student", "student__user", "ts", "ts__course", "ts__subject"
        )

        if date:
            records = records.filter(attendance_date=date)
        if status_filter in ["Present", "Absent"]:
            records = records.filter(status=status_filter)

        output = []

        for rec in records:
            student = rec.student
            subject = rec.ts.subject
            course = rec.ts.course

            if semester and str(subject.current_semester) != str(semester):
                continue

            if search and search.lower() not in student.user.name.lower() and search.lower() not in student.roll_number.lower():
                continue

            output.append({
                "date": rec.attendance_date,
                "status": rec.status,
                "student_name": student.user.name,
                "roll_number": student.roll_number,
                "subject_name": subject.subject_name,
                "subject_code": subject.subject_code,
                "course_name": course.course_name,
                "created_at": rec.created_at,
                "updated_at": rec.updated_at
            })


        return Response(sorted(output, key=lambda x: x["date"], reverse=True))



# ============================================================
# COURSE SUBJECTS (Admin + Teacher)
# ============================================================

class CourseSubjectsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        semester = request.query_params.get("semester")

        qs = Subject.objects.filter(course_subjects__course_id=course_id)

        if semester:
            qs = qs.filter(current_semester=semester)

        serializer = SubjectSerializer(qs, many=True)
        return Response(serializer.data)



# ============================================================
# STUDENT APIs (SAFE /me/)
# ============================================================

class StudentSubjectsAttendance(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        student = request.user.student_profile

        enrolls = StudentSubjectEnrollment.objects.filter(student=student).select_related(
            "subject", "student", "student__user"
        )

        output = []

        for e in enrolls:
            subject = e.subject

            ts = TeacherSubject.objects.filter(
                subject_id=subject.id,
                course_id=student.course.id
            ).select_related("teacher", "teacher__user").first()

            teacher_name = ts.teacher.user.name if ts else None

            records = Attendance.objects.filter(
                student=student, ts__subject_id=subject.id
            )

            total = records.count()
            attended = records.filter(status="Present").count()
            percent = round(attended / total * 100, 2) if total else 0

            output.append({
                "subject_id": subject.id,
                "subject_name": subject.subject_name,
                "subject_code": subject.subject_code,
                "credits": subject.credits,
                "teacher_name": teacher_name,
                "total_classes": total,
                "attended_classes": attended,
                "percentage": percent,
            })

        return Response(output)


class StudentSubjectWiseAttendance(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        student = request.user.student_profile
        subject_id = request.query_params.get("subject_id")

        if not subject_id:
            return Response({"error": "subject_id is required"}, status=400)

        records = Attendance.objects.filter(
            student=student, ts__subject_id=subject_id
        ).select_related("ts", "ts__teacher", "ts__teacher__user", "ts__subject")

        if not records.exists():
            return Response({"error": "No attendance found"}, status=404)

        output = []

        for rec in records:
            output.append({
                "date": rec.attendance_date,
                "status": rec.status,
                "subject_name": rec.ts.subject.subject_name,
                "teacher_name": rec.ts.teacher.user.name
            })

        return Response(sorted(output, key=lambda x: x["date"], reverse=True))
