from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import (
    Department, Course, Subject, CourseSubject,
    Teacher, TeacherSubject, Student, StudentSubjectEnrollment, Attendance
)

from .serializers import (
    DepartmentSerializer, CourseSerializer, SubjectSerializer,
    CourseSubjectSerializer, TeacherSerializer, TeacherSubjectSerializer,
    StudentSerializer, StudentSubjectEnrollmentSerializer, AttendanceSerializer
)


# -----------------------------------------------------------
# Department CRUD
# -----------------------------------------------------------
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


# -----------------------------------------------------------
# Course CRUD
# -----------------------------------------------------------
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# -----------------------------------------------------------
# Subject CRUD
# -----------------------------------------------------------
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


# -----------------------------------------------------------
# CourseSubject Mapping CRUD
# -----------------------------------------------------------
class CourseSubjectViewSet(viewsets.ModelViewSet):
    queryset = CourseSubject.objects.all()
    serializer_class = CourseSubjectSerializer


# -----------------------------------------------------------
# Teacher CRUD
# -----------------------------------------------------------
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    @action(detail=False, methods=['get'])
    def subjectwise(self, request):
        teacher_id = request.query_params.get('teacher_id')
        if not teacher_id:
            return Response({"error": "teacher_id is required"}, status=400)

        ts_list = TeacherSubject.objects.filter(teacher_id=teacher_id).select_related(
            'subject', 'course', 'course__dept'
        )

        if not ts_list.exists():
            return Response({"message": "No subjects assigned"}, status=404)

        data = []
        for ts in ts_list:
            subject = ts.subject
            course = ts.course
            department = course.dept if course else None

            data.append({
                "subject_id": subject.id,
                "subject_code": subject.subject_code,
                "subject_name": subject.subject_name,
                "course": course.course_name if course else None,
                "department": department.dept_name if department else None,
                "semester": subject.current_semester
            })

        return Response(data)


# -----------------------------------------------------------
# TeacherSubject CRUD
# -----------------------------------------------------------
class TeacherSubjectViewSet(viewsets.ModelViewSet):
    queryset = TeacherSubject.objects.all()
    serializer_class = TeacherSubjectSerializer


# -----------------------------------------------------------
# Student CRUD
# -----------------------------------------------------------
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        course_id = self.request.query_params.get('course_id')
        semester = self.request.query_params.get('semester')
        year = self.request.query_params.get('year')

        if course_id:
            qs = qs.filter(course_id=course_id)
        if semester:
            qs = qs.filter(current_semester=semester)
        if year:
            qs = qs.filter(year_of_study=year)

        return qs

    @action(detail=False, methods=['get'])
    def subjects_teachers(self, request):
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({"error": "student_id is required"}, status=400)

        student = Student.objects.filter(id=student_id).select_related('course', 'user').first()
        if not student:
            return Response({"error": "Student not found"}, status=404)

        enrollments = StudentSubjectEnrollment.objects.filter(student_id=student_id).select_related('subject')

        subjects_data = []
        for e in enrollments:
            subject = e.subject
            ts = TeacherSubject.objects.filter(subject=subject, course=student.course).select_related('teacher', 'teacher__user').first()

            teacher_info = None
            if ts:
                teacher_info = {
                    "id": ts.teacher.id,
                    "name": ts.teacher.user.name if ts.teacher.user else None,
                    "email": ts.teacher.user.email if ts.teacher.user else None,
                    "department": ts.teacher.department.dept_name
                }

            subjects_data.append({
                "subject_id": subject.id,
                "subject_code": subject.subject_code,
                "subject_name": subject.subject_name,
                "teacher": teacher_info
            })

        return Response({
            "student_id": student.id,
            "roll_number": student.roll_number,
            "name": student.user.name,
            "current_semester": student.current_semester,
            "subjects": subjects_data
        })

    @action(detail=False, methods=['get'])
    def subjectwise(self, request):
        subject_id = request.query_params.get('subject_id')
        if not subject_id:
            return Response({"error": "subject_id is required"}, status=400)

        enrollments = StudentSubjectEnrollment.objects.filter(subject_id=subject_id)
        students = [e.student for e in enrollments]
        return Response(StudentSerializer(students, many=True).data)

    @action(detail=False, methods=['get'])
    def contact(self, request):
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({"error": "student_id is required"}, status=400)

        student = Student.objects.filter(id=student_id).select_related('course__dept', 'user').first()
        if not student:
            return Response({"error": "Student not found"}, status=404)

        return Response({
            "id": student.id,
            "roll_number": student.roll_number,
            "name": student.user.name,
            "email": student.user.email,
            "phone_number": student.phone_number,
            "course": student.course.course_name,
            "department": student.course.dept.dept_name,
            "year_of_study": student.year_of_study,
            "semester": student.current_semester
        })


# -----------------------------------------------------------
# StudentSubjectEnrollment CRUD
# -----------------------------------------------------------
class StudentSubjectEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = StudentSubjectEnrollment.objects.all()
    serializer_class = StudentSubjectEnrollmentSerializer


# -----------------------------------------------------------
# Attendance CRUD + Custom Actions
# -----------------------------------------------------------
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    @action(detail=False, methods=['post'])
    def mark(self, request):
        ts_id = request.data.get('ts_id')
        date = request.data.get('attendance_date')
        present = request.data.get('present', [])
        absent = request.data.get('absent', [])
        created_by = request.data.get('created_by')

        if not ts_id or not date:
            return Response({"error": "ts_id and attendance_date required"}, status=400)

        ts = TeacherSubject.objects.filter(id=ts_id).first()
        if not ts:
            return Response({"error": "Invalid teacher-subject"}, status=400)

        teacher = Teacher.objects.filter(id=created_by).first()

        for student_id in present:
            Attendance.objects.update_or_create(
                student_id=student_id,
                ts=ts,
                attendance_date=date,
                defaults={"status": "Present", "created_by": teacher}
            )

        for student_id in absent:
            Attendance.objects.update_or_create(
                student_id=student_id,
                ts=ts,
                attendance_date=date,
                defaults={"status": "Absent", "created_by": teacher}
            )

        return Response({"message": "Attendance updated"}, status=201)

    def get_queryset(self):
        qs = super().get_queryset()
        sid = self.request.query_params.get('student_id')
        tsid = self.request.query_params.get('ts_id')
        date = self.request.query_params.get('date')

        if sid:
            qs = qs.filter(student_id=sid)
        if tsid:
            qs = qs.filter(ts_id=tsid)
        if date:
            qs = qs.filter(attendance_date=date)

        return qs

    @action(detail=False, methods=['get'])
    def subjectwise(self, request):
        subject_id = request.query_params.get('subject_id')
        if not subject_id:
            return Response({"error": "subject_id required"}, status=400)

        enrollments = StudentSubjectEnrollment.objects.filter(subject_id=subject_id)

        output = []
        for e in enrollments:
            student = e.student
            records = Attendance.objects.filter(student=student, ts__subject_id=subject_id)

            total = records.count()
            present = records.filter(status="Present").count()
            percent = round((present / total * 100), 2) if total else 0

            output.append({
                "student_id": student.id,
                "roll_number": student.roll_number,
                "name": student.user.name,
                "total_classes": total,
                "attended_classes": present,
                "percentage": percent
            })

        return Response(output)

    @action(detail=False, methods=['get'])
    def studentwise(self, request):
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({"error": "student_id required"}, status=400)

        enrollments = StudentSubjectEnrollment.objects.filter(student_id=student_id)

        output = []
        for e in enrollments:
            subject = e.subject
            records = Attendance.objects.filter(student_id=student_id, ts__subject_id=subject.id)

            total = records.count()
            present = records.filter(status="Present").count()
            percent = round((present / total * 100), 2) if total else 0

            output.append({
                "subject_id": subject.id,
                "subject_code": subject.subject_code,
                "subject_name": subject.subject_name,
                "total_classes": total,
                "attended_classes": present,
                "percentage": percent
            })

        return Response(output)

    @action(detail=False, methods=['get'])
    def datewise(self, request):
        subject_id = request.query_params.get('subject_id')
        date = request.query_params.get('date')

        if not subject_id or not date:
            return Response({"error": "subject_id and date required"}, status=400)

        enrollments = StudentSubjectEnrollment.objects.filter(subject_id=subject_id)

        output = []
        for e in enrollments:
            student = e.student
            record = Attendance.objects.filter(
                student=student, ts__subject_id=subject_id, attendance_date=date
            ).first()

            output.append({
                "student_id": student.id,
                "roll_number": student.roll_number,
                "name": student.user.name,
                "status": record.status if record else "Not Marked"
            })

        return Response({
            "subject_id": subject_id,
            "date": date,
            "records": output
        })


# -----------------------------------------------------------
# List subjects of a course (optional semester filter)
# -----------------------------------------------------------
class CourseSubjectsView(APIView):
    def get(self, request, course_id):
        semester = request.query_params.get("semester")

        qs = Subject.objects.filter(course_subjects__course_id=course_id)

        if semester:
            qs = qs.filter(current_semester=semester)

        return Response(SubjectSerializer(qs, many=True).data)


# -----------------------------------------------------------
# List all students taught by a teacher
# -----------------------------------------------------------
class TeacherStudentsView(APIView):
    def get(self, request, teacher_id):
        subject_ids = TeacherSubject.objects.filter(teacher_id=teacher_id).values_list('subject_id', flat=True)
        students = Student.objects.filter(enrollments__subject_id__in=subject_ids).distinct()
        return Response(StudentSerializer(students, many=True).data)
