from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'academic-years', AcademicYearViewSet)
router.register(r'semesters', SemesterViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'course-subjects', CourseSubjectViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'teacher-subjects', TeacherSubjectViewSet)
router.register(r'students', StudentViewSet)
router.register(r'enrollments', StudentSubjectEnrollmentViewSet)
# router.register(r'attendance', AttendanceViewSet)
router.register(r'attendance', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path('', include(router.urls)),
    path('courses/<int:course_id>/subjects/', CourseSubjectsView.as_view()),
    path('teachers/<int:teacher_id>/students/', TeacherStudentsView.as_view()),
    # path('attendance/mark/', AttendanceViewSet.as_view()),
    # path('api/', include(router.urls)),
]
