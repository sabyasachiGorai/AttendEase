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

    # --------------------------
    # GET /api/teachers/subjectwise/?teacher_id=
    # --------------------------
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
            dept = course.dept if course else None

            data.append({
                "subject_id": subject.id,
                "subject_code": subject.subject_code,
                "subject_name": subject.subject_name,
                "course": course.course_name if course else None,
                "department": dept.dept_name if dept else None,
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

    # --------------------------
    # Filters applied to GET /api/students/
    # --------------------------
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

    # --------------------------
    # GET /api/students/subjects_teachers/?student_id=
    # --------------------------
    @action(detail=False, methods=['get'])
    def subjects_teachers(self, request):
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({"error": "student_id is required"}, status=400)

        student = Student.objects.filter(id=student_id).select_related('course').first()
        if not student:
            return Response({"error": "Student not found"}, status=404)

        enrollments = StudentSubjectEnrollment.objects.filter(student_id=student_id).select_related('subject')

        data = []
        for enroll in enrollments:
            subject = enroll.subject

            # find teacher for this (subject + student's course)
            ts = TeacherSubject.objects.filter(subject=subject, course=student.course).select_related('teacher').first()

            teacher_data = None
            if ts:
                t = ts.teacher
                teacher_data = {
                    "id": t.id,
                    "email": t.user.email if t.user else None,
                    "department": t.department.dept_name
                }

            data.append({
                "subject_id": subject.id,
                "subject_code": subject.subject_code,
                "subject_name": subject.subject_name,
                "teacher": teacher_data
            })

        return Response({
            "student_id": student.id,
            "roll_number": student.roll_number,
            "current_semester": student.current_semester,
            "subjects": data
        })

    # --------------------------
    # GET /api/students/subjectwise/?subject_id=
    # --------------------------
    @action(detail=False, methods=['get'])
    def subjectwise(self, request):
        subject_id = request.query_params.get('subject_id')
        if not subject_id:
            return Response({"error": "subject_id is required"}, status=400)

        enrolls = StudentSubjectEnrollment.objects.filter(subject_id=subject_id)
        students = [e.student for e in enrolls]
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)

    # --------------------------
    # GET /api/students/contact/?student_id=
    # --------------------------
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
            "email": student.user.email if student.user else None,
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
# Attendance CRUD + custom actions
# -----------------------------------------------------------
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    # --------------------------
    # POST /api/attendance/mark/
    # --------------------------
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
            return Response({"error": "Invalid ts_id"}, status=400)

        teacher = Teacher.objects.filter(id=created_by).first()

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

    # --------------------------
    # Filters in list
    # --------------------------
    def get_queryset(self):
        qs = super().get_queryset()
        student = self.request.query_params.get("student_id")
        ts = self.request.query_params.get("ts_id")
        date = self.request.query_params.get("date")

        if student:
            qs = qs.filter(student_id=student)
        if ts:
            qs = qs.filter(ts_id=ts)
        if date:
            qs = qs.filter(attendance_date=date)
        return qs

    # --------------------------
    # GET /api/attendance/subjectwise/
    # --------------------------
    @action(detail=False, methods=['get'])
    def subjectwise(self, request):
        subject_id = request.query_params.get('subject_id')
        if not subject_id:
            return Response({"error": "subject_id required"}, status=400)

        enrolls = StudentSubjectEnrollment.objects.filter(subject_id=subject_id)

        output = []
        for e in enrolls:
            student = e.student
            records = Attendance.objects.filter(student=student, ts__subject_id=subject_id)
            total = records.count()
            attended = records.filter(status='Present').count()
            percent = round((attended / total * 100), 2) if total else 0

            output.append({
                "student_id": student.id,
                "roll_number": student.roll_number,
                "total_classes": total,
                "attended_classes": attended,
                "percentage": percent
            })

        return Response(output)

    # --------------------------
    # GET /api/attendance/studentwise/
    # --------------------------
    @action(detail=False, methods=['get'])
    def studentwise(self, request):
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({"error": "student_id required"}, status=400)

        enrolls = StudentSubjectEnrollment.objects.filter(student_id=student_id)

        output = []
        for e in enrolls:
            subject = e.subject
            records = Attendance.objects.filter(student_id=student_id, ts__subject_id=subject.id)
            total = records.count()
            attended = records.filter(status='Present').count()
            percent = round((attended / total * 100), 2) if total else 0

            output.append({
                "subject_id": subject.id,
                "subject_code": subject.subject_code,
                "subject_name": subject.subject_name,
                "total_classes": total,
                "attended_classes": attended,
                "percentage": percent
            })

        return Response(output)

    # --------------------------
    # GET /api/attendance/datewise/
    # --------------------------
    @action(detail=False, methods=['get'])
    def datewise(self, request):
        subject_id = request.query_params.get('subject_id')
        date = request.query_params.get('date')

        if not subject_id or not date:
            return Response({"error": "subject_id and date required"}, status=400)

        enrolls = StudentSubjectEnrollment.objects.filter(subject_id=subject_id)
        output = []

        for e in enrolls:
            student = e.student
            record = Attendance.objects.filter(
                student=student,
                ts__subject_id=subject_id,
                attendance_date=date
            ).first()

            output.append({
                "student_id": student.id,
                "roll_number": student.roll_number,
                "status": record.status if record else "Not Marked"
            })

        return Response({
            "subject_id": subject_id,
            "date": date,
            "records": output
        })


# -----------------------------------------------------------
# GET /api/courses/<id>/subjects/?semester=<int>
# -----------------------------------------------------------
class CourseSubjectsView(APIView):
    def get(self, request, course_id):
        semester = request.query_params.get("semester")

        # list all subjects mapped to this course
        qs = Subject.objects.filter(course_subjects__course_id=course_id)

        # filter by integer semester
        if semester:
            qs = qs.filter(current_semester=semester)

        serializer = SubjectSerializer(qs, many=True)
        return Response(serializer.data)


# -----------------------------------------------------------
# GET /api/teachers/<id>/students/
# -----------------------------------------------------------
class TeacherStudentsView(APIView):
    def get(self, request, teacher_id):
        # find all subjects taught by this teacher
        subjects = TeacherSubject.objects.filter(teacher_id=teacher_id).values_list("subject_id", flat=True)

        # all students enrolled in those subjects
        students = Student.objects.filter(enrollments__subject_id__in=subjects).distinct()

        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
