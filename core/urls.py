from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

# CRUD with queryset (no basename needed)
router.register(r'departments', DepartmentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'course-subjects', CourseSubjectViewSet)
router.register(r'teacher-subjects', TeacherSubjectViewSet)
router.register(r'enrollments', StudentSubjectEnrollmentViewSet)

# ViewSets without queryset → need basename
router.register(r'teachers', TeacherViewSet, basename='teachers')
router.register(r'students', StudentViewSet, basename='students')
router.register(r'attendance', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path('', include(router.urls)),
    path('courses/<int:course_id>/subjects/', CourseSubjectsView.as_view()),
    path('teachers/<int:teacher_id>/students/', TeacherStudentsView.as_view()),
]
