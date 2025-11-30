from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

# Core CRUD routes
router.register(r'departments', DepartmentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'course-subjects', CourseSubjectViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'teacher-subjects', TeacherSubjectViewSet)
router.register(r'students', StudentViewSet)
router.register(r'enrollments', StudentSubjectEnrollmentViewSet)
router.register(r'attendance', AttendanceViewSet, basename='attendance')


urlpatterns = [
    path('', include(router.urls)),

    # Custom endpoints
    path('courses/<int:course_id>/subjects/', CourseSubjectsView.as_view()),
    path('teachers/<int:teacher_id>/students/', TeacherStudentsView.as_view()),
    
    # Secure Student APIs (no ID in URL)
    path('students/me/subjects-attendance/', StudentSubjectsAttendance.as_view()),
    path('students/me/attendance/', StudentSubjectWiseAttendance.as_view()),
    path('teachers/me/teacher-subject-ids/', TeacherSubjectIDs.as_view()),

]
