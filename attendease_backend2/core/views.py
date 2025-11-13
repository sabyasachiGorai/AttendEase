from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count

from .models import (
    Department, Course, AcademicYear, Semester, Subject, CourseSubject,
    Teacher, TeacherSubject, Student, StudentSubjectEnrollment, Attendance
)
from .serializers import (
    DepartmentSerializer, CourseSerializer, AcademicYearSerializer, SemesterSerializer,
    SubjectSerializer, CourseSubjectSerializer, TeacherSerializer, TeacherSubjectSerializer,
    StudentSerializer, StudentSubjectEnrollmentSerializer, AttendanceSerializer
)

"""
================================================================================
1) BASIC CRUD VIEWSETS (Auto-routed by DRF Router)
--------------------------------------------------------------------------------
These ModelViewSets expose standard REST endpoints automatically:

- LIST     GET     /api/<resource>/
- CREATE   POST    /api/<resource>/
- RETRIEVE GET     /api/<resource>/<id>/
- UPDATE   PUT     /api/<resource>/<id>/
- PARTIAL  PATCH   /api/<resource>/<id>/
- DELETE   DELETE  /api/<resource>/<id>/

The `router.register()` calls in urls.py generate these routes.
"""

# -----------------------------------------------------------------------------
# Department CRUD
# API Base: /api/departments/
# Purpose: Manage departments in the institute.
# Works: Standard DRF ModelViewSet wired by DefaultRouter.
# -----------------------------------------------------------------------------
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


# -----------------------------------------------------------------------------
# Course CRUD
# API Base: /api/courses/
# Purpose: Manage courses (e.g., B.Tech CSE).
# -----------------------------------------------------------------------------
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# -----------------------------------------------------------------------------
# Academic Year CRUD
# API Base: /api/academic-years/
# Purpose: Define year groupings within a course (Year 1, Year 2, ...).
# -----------------------------------------------------------------------------
class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer


# -----------------------------------------------------------------------------
# Semester CRUD
# API Base: /api/semesters/
# Purpose: Manage semesters that belong to academic years.
# -----------------------------------------------------------------------------
class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer


# -----------------------------------------------------------------------------
# Subject CRUD
# API Base: /api/subjects/
# Purpose: Manage subjects offered by the institute.
# -----------------------------------------------------------------------------
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


# -----------------------------------------------------------------------------
# CourseSubject CRUD (Mapping: Course ↔ Subjects)
# API Base: /api/course-subjects/
# Purpose: Stores which subjects belong to which course.
# -----------------------------------------------------------------------------
class CourseSubjectViewSet(viewsets.ModelViewSet):
    queryset = CourseSubject.objects.all()
    serializer_class = CourseSubjectSerializer


# -----------------------------------------------------------------------------
# Teacher CRUD + Subjectwise listing
# API Base: /api/teachers/
# Purpose: Manage teachers. Also provides subject-wise listing for a teacher.
# -----------------------------------------------------------------------------
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    # -------------------------------------------------------------------------
    # GET /api/teachers/subjectwise/?teacher_id=<id>
    # Purpose: Return all subjects assigned to the given teacher.
    # How it works: Looks up TeacherSubject rows by teacher_id and returns
    #               subject, course, department, and semester info.
    # -------------------------------------------------------------------------
    @action(detail=False, methods=['get'])
    def subjectwise(self, request):
        teacher_id = request.query_params.get('teacher_id')
        if not teacher_id:
            return Response({"error": "teacher_id is required"}, status=400)

        teacher_subjects = TeacherSubject.objects.filter(teacher_id=teacher_id).select_related(
            'subject', 'course', 'course__dept'
        )

        if not teacher_subjects.exists():
            return Response({"message": "No subjects assigned to this teacher."}, status=404)

        data = []
        for ts in teacher_subjects:
            subject = ts.subject
            course = ts.course
            department = course.dept if course else None

            # Semester if available (str() to leverage __str__ of Semester)
            semester_display = None
            subject_sem = getattr(subject, 'semester', None)
            if subject_sem:
                semester_display = str(subject_sem)

            data.append({
                "subject_id": subject.id,
                "subject_code": subject.subject_code,
                "subject_name": subject.subject_name,
                "course": course.course_name if course else None,
                "department": department.dept_name if department else None,
                "semester": semester_display
            })

        return Response(data)


# -----------------------------------------------------------------------------
# TeacherSubject CRUD (Mapping: Teacher ↔ Subject ↔ Course)
# API Base: /api/teacher-subjects/
# Purpose: Assigns teachers to teach specific subjects in a course.
# -----------------------------------------------------------------------------
class TeacherSubjectViewSet(viewsets.ModelViewSet):
    queryset = TeacherSubject.objects.all()
    serializer_class = TeacherSubjectSerializer


# -----------------------------------------------------------------------------
# Student CRUD + utilities
# API Base: /api/students/
# Purpose: Manage students with support for filtering and utility endpoints.
# Filters:
#   - /api/students/?course_id=<id>
#   - /api/students/?semester_id=<id>
#   - /api/students/?year=<int>
# -----------------------------------------------------------------------------
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    # How it works: overrides the base queryset to apply query-param filters.
    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.request.query_params.get('course_id')
        semester_id = self.request.query_params.get('semester_id')
        year = self.request.query_params.get('year')

        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if semester_id:
            queryset = queryset.filter(current_semester_id=semester_id)
        if year:
            queryset = queryset.filter(year_of_study=year)
        return queryset

    # -------------------------------------------------------------------------
    # GET /api/students/subjects_teachers/?student_id=<id>
    # Purpose: For a student, list all enrolled subjects plus the teacher
    #          (within the student's course) teaching each subject.
    # How it works: Pulls enrollments, then finds TeacherSubject for (subject, course).
    # -------------------------------------------------------------------------
    @action(detail=False, methods=['get'])
    def subjects_teachers(self, request):
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({"error": "student_id is required"}, status=400)

        student = Student.objects.filter(id=student_id).select_related('course', 'course__dept').first()
        if not student:
            return Response({"error": "Student not found"}, status=404)

        enrollments = StudentSubjectEnrollment.objects.filter(student_id=student_id).select_related('subject')
        if not enrollments.exists():
            return Response({"message": "No subjects found for this student"}, status=404)

        subjects_data = []
        for enrollment in enrollments:
            subject = enrollment.subject
            teachers = TeacherSubject.objects.filter(subject=subject, course=student.course).select_related('teacher', 'teacher__department')

            teacher_data = None
            if teachers.exists():
                t = teachers.first().teacher
                teacher_data = {
                    "id": t.id,
                    "name": f"{t.first_name} {t.last_name}",
                    "email": t.email,
                    "department": t.department.dept_name if t.department else None
                }

            subjects_data.append({
                "subject_id": subject.id,
                "subject_code": subject.subject_code,
                "subject_name": subject.subject_name,
                "teacher": teacher_data
            })

        response = {
            "student": {
                "id": student.id,
                "roll_number": student.roll_number,
                "name": f"{student.first_name} {student.last_name}"
            },
            "subjects": subjects_data
        }
        return Response(response)

    # -------------------------------------------------------------------------
    # GET /api/students/subjectwise/?subject_id=<id>
    # Purpose: Return all students enrolled in a given subject.
    # How it works: Loads enrollments for subject and returns serialized students.
    # -------------------------------------------------------------------------
    @action(detail=False, methods=['get'])
    def subjectwise(self, request):
        subject_id = request.query_params.get('subject_id')
        if not subject_id:
            return Response({"error": "subject_id is required"}, status=400)

        enrollments = StudentSubjectEnrollment.objects.filter(subject_id=subject_id).select_related('student')
        students = [enrollment.student for enrollment in enrollments]
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)

    # -------------------------------------------------------------------------
    # GET /api/students/contact/?student_id=<id>
    # Purpose: Return a student's full contact profile and academic placement.
    # How it works: fetches student and serializes enriched fields (course/department/semester).
    # -------------------------------------------------------------------------
    @action(detail=False, methods=['get'])
    def contact(self, request):
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({"error": "student_id is required"}, status=400)

        student = Student.objects.select_related('course__dept', 'current_semester').filter(id=student_id).first()
        if not student:
            return Response({"error": "Student not found"}, status=404)

        data = {
            "id": student.id,
            "roll_number": student.roll_number,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "email": student.email,
            "phone_number": student.phone_number,
            "course": student.course.course_name if student.course else None,
            "department": student.course.dept.dept_name if student.course and student.course.dept else None,
            "year_of_study": student.year_of_study,
            "semester": str(student.current_semester) if student.current_semester else None
        }
        return Response(data)


# -----------------------------------------------------------------------------
# Enrollment CRUD (Student ↔ Subject)
# API Base: /api/enrollments/
# Purpose: Manage student enrollments into subjects.
# -----------------------------------------------------------------------------
class StudentSubjectEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = StudentSubjectEnrollment.objects.all()
    serializer_class = StudentSubjectEnrollmentSerializer


"""
================================================================================
2) ATTENDANCE MODULE (CRUD + Custom Reporting)
--------------------------------------------------------------------------------
Includes: bulk mark, subjectwise/studentwise summaries, date-wise listing, and
query-param filtering on list endpoint.
"""

# -----------------------------------------------------------------------------
# Attendance CRUD + custom actions
# API Base: /api/attendance/
# Purpose: Store and report attendance records.
# -----------------------------------------------------------------------------
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    # -------------------------------------------------------------------------
    # POST /api/attendance/mark/
    # Purpose: Bulk mark attendance for a given TeacherSubject (ts_id) and date.
    # Request JSON Example:
    # {
    #   "ts_id": 1,
    #   "attendance_date": "2025-11-09",
    #   "present": [1,2,3],
    #   "absent": [4,5],
    #   "created_by": 1
    # }
    # How it works: Upserts Attendance for each student with Present/Absent.
    # -------------------------------------------------------------------------
    @action(detail=False, methods=['post'])
    def mark(self, request):
        ts_id = request.data.get('ts_id')
        attendance_date = request.data.get('attendance_date')
        present = request.data.get('present', [])
        absent = request.data.get('absent', [])
        created_by = request.data.get('created_by')

        if not ts_id or not attendance_date:
            return Response({"error": "ts_id and attendance_date are required."}, status=status.HTTP_400_BAD_REQUEST)

        teacher_subject = TeacherSubject.objects.filter(id=ts_id).select_related('subject').first()
        if not teacher_subject:
            return Response({"error": "Invalid teacher-subject ID."}, status=status.HTTP_400_BAD_REQUEST)

        teacher = Teacher.objects.filter(id=created_by).first() if created_by else None

        count = 0
        for sid in present:
            Attendance.objects.update_or_create(
                student_id=sid, ts=teacher_subject, attendance_date=attendance_date,
                defaults={'status': 'Present', 'created_by': teacher}
            )
            count += 1
        for sid in absent:
            Attendance.objects.update_or_create(
                student_id=sid, ts=teacher_subject, attendance_date=attendance_date,
                defaults={'status': 'Absent', 'created_by': teacher}
            )
            count += 1

        return Response({
            "message": f"Attendance marked successfully for {count} students.",
            "subject": teacher_subject.subject.subject_name,
            "date": attendance_date
        }, status=status.HTTP_201_CREATED)

    # -------------------------------------------------------------------------
    # LIST with filters
    # GET /api/attendance/?student_id=<id>&ts_id=<id>&date=<YYYY-MM-DD>
    # Purpose: Filter attendance records directly via list endpoint.
    # How it works: Applies optional filters to base queryset.
    # -------------------------------------------------------------------------
    def get_queryset(self):
        queryset = super().get_queryset()
        student_id = self.request.query_params.get('student_id')
        ts_id = self.request.query_params.get('ts_id')
        date = self.request.query_params.get('date')

        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if ts_id:
            queryset = queryset.filter(ts_id=ts_id)
        if date:
            queryset = queryset.filter(attendance_date=date)
        return queryset

    # -------------------------------------------------------------------------
    # GET /api/attendance/subjectwise/?subject_id=<id>
    # Purpose: Summary per student for a subject (total/attended/%).
    # How it works: For each enrolled student, counts total and present records.
    # -------------------------------------------------------------------------
    @action(detail=False, methods=['get'])
    def subjectwise(self, request):
        subject_id = request.query_params.get('subject_id')
        if not subject_id:
            return Response({"error": "subject_id is required."}, status=400)

        enrollments = StudentSubjectEnrollment.objects.filter(subject_id=subject_id).select_related('student')
        if not enrollments.exists():
            return Response({"message": "No students enrolled for this subject."}, status=404)

        data = []
        for enroll in enrollments:
            student = enroll.student
            records = Attendance.objects.filter(student=student, ts__subject_id=subject_id)
            total_classes = records.count()
            attended_classes = records.filter(status='Present').count()
            attendance_percentage = round((attended_classes / total_classes * 100), 2) if total_classes > 0 else 0.0

            data.append({
                "student": {
                    "id": student.id,
                    "roll_number": student.roll_number,
                    "first_name": student.first_name,
                    "last_name": student.last_name
                },
                "total_classes": total_classes,
                "attended_classes": attended_classes,
                "attendance_percentage": attendance_percentage
            })

        return Response(data)

    # -------------------------------------------------------------------------
    # GET /api/attendance/studentwise/?student_id=<id>
    # Purpose: Per-subject summary for one student (total/attended/% per subject).
    # How it works: Iterates over the student's enrollments and aggregates records.
    # -------------------------------------------------------------------------
    @action(detail=False, methods=['get'])
    def studentwise(self, request):
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({"error": "student_id is required."}, status=400)

        enrollments = StudentSubjectEnrollment.objects.filter(student_id=student_id).select_related('subject')
        if not enrollments.exists():
            return Response({"message": "No subjects found for this student."}, status=404)

        data = []
        for enroll in enrollments:
            subject = enroll.subject
            records = Attendance.objects.filter(student_id=student_id, ts__subject=subject)
            total_classes = records.count()
            attended_classes = records.filter(status='Present').count()
            attendance_percentage = round((attended_classes / total_classes * 100), 2) if total_classes > 0 else 0.0

            data.append({
                "subject": {
                    "id": subject.id,
                    "code": subject.subject_code,
                    "name": subject.subject_name
                },
                "total_classes": total_classes,
                "attended_classes": attended_classes,
                "attendance_percentage": attendance_percentage
            })

        return Response(data)

    # -------------------------------------------------------------------------
    # GET /api/attendance/datewise/?subject_id=<id>&date=<YYYY-MM-DD>
    # Purpose: Show attendance list of all students for a given date + subject.
    # How it works: For each enrolled student, fetches the record for the date.
    # -------------------------------------------------------------------------
    @action(detail=False, methods=['get'])
    def datewise(self, request):
        subject_id = request.query_params.get('subject_id')
        attendance_date = request.query_params.get('date')

        if not subject_id or not attendance_date:
            return Response({"error": "Both subject_id and date are required."}, status=400)

        enrollments = StudentSubjectEnrollment.objects.filter(subject_id=subject_id).select_related('student', 'subject')
        if not enrollments.exists():
            return Response({"message": "No students enrolled for this subject."}, status=404)

        records = []
        for enroll in enrollments:
            student = enroll.student
            record = Attendance.objects.filter(
                student=student,
                ts__subject_id=subject_id,
                attendance_date=attendance_date
            ).first()

            status_display = record.status if record else "Not Marked"
            records.append({
                "student_id": student.id,
                "roll_number": student.roll_number,
                "name": f"{student.first_name} {student.last_name}",
                "status": status_display
            })

        subject_name = enrollments.first().subject.subject_name
        return Response({
            "subject": subject_name,
            "date": attendance_date,
            "total_students": len(records),
            "records": records
        })


"""
================================================================================
3) CUSTOM API CLASSES (not ViewSets)
--------------------------------------------------------------------------------
Standalone APIViews that provide custom list endpoints.
"""

# -----------------------------------------------------------------------------
# GET /api/courses/<int:course_id>/subjects/?year=<int>&sem=<int>
# OR  /api/courses/<int:course_id>/subjects/?semester_global=<int>
# Purpose: List subjects for a course filtered by (year, sem) OR by a global
#          semester index where 1→(Y1,S1), 2→(Y1,S2), 3→(Y2,S1), ...
# How it works: Builds a queryset matching nested relations through Semester →
#               AcademicYear → Course and returns serialized Subject list.
# -----------------------------------------------------------------------------
class CourseSubjectsView(APIView):
    def get(self, request, course_id):
        year = request.query_params.get('year')
        sem = request.query_params.get('sem')
        sem_global = request.query_params.get('semester_global')

        qs = Subject.objects.filter(course_subjects__course_id=course_id).distinct()

        if sem_global:
            try:
                sem_global = int(sem_global)
                # Convert global semester index to (year_number, semester_number)
                year_number = ((sem_global - 1) // 2) + 1
                semester_number = ((sem_global - 1) % 2) + 1
                qs = qs.filter(
                    semester__academic_year__course_id=course_id,
                    semester__academic_year__year_number=year_number,
                    semester__semester_number=semester_number
                )
            except ValueError:
                pass
        elif year and sem:
            qs = qs.filter(
                semester__academic_year__course_id=course_id,
                semester__academic_year__year_number=year,
                semester__semester_number=sem
            )

        serializer = SubjectSerializer(qs, many=True)
        return Response(serializer.data)


# -----------------------------------------------------------------------------
# GET /api/teachers/<int:teacher_id>/students/
# Purpose: List distinct students who are enrolled in any subject taught by the
#          specified teacher.
# How it works: Finds TeacherSubject → subject_ids; then unique Students where
#               enrollments.subject_id in that list.
# -----------------------------------------------------------------------------
class TeacherStudentsView(APIView):
    def get(self, request, teacher_id):
        subjects = TeacherSubject.objects.filter(teacher_id=teacher_id).values_list('subject_id', flat=True)
        students = Student.objects.filter(enrollments__subject_id__in=subjects).distinct()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
