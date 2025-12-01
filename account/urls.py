
from django.urls import path
from .views import (userRegistrationView, userLoginView, UserProfileView, changeUserPasswordView,
                    userPasswordResetEmailView, userPasswordResetView, StudentRegistrationView,
                    teacherRegistrationView, TeacherProfileView, StudentProfileView, userLogoutView,
                    send_attendance_warningView, send_bulk_attendance_warningView)

urlpatterns = [
    path('register/', userRegistrationView.as_view(), name='user-registration'),
    path('login/', userLoginView.as_view(), name='user-login'),
    path('logout/', userLogoutView.as_view(), name='user-logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('changeUserPassword/', changeUserPasswordView.as_view(), name='changeUser-Password'),
    path('send-password-reset-email/', userPasswordResetEmailView.as_view(), name='send-password-reset-email'),
    path('reset/<uid>/<token>/', userPasswordResetView.as_view(), name='password-reset'),

    path('studentRegistration/', StudentRegistrationView.as_view(), name='student-registration'),
    path('teacherRegistration/', teacherRegistrationView.as_view(), name='teacher-registration'),
    path('teacherProfile/', TeacherProfileView.as_view(), name='teacher-profile'),
    path('studentProfile/', StudentProfileView.as_view(), name='student-profile'),
    
    # New URL pattern for sending attendance email
    path('send-attendance-warning/', send_attendance_warningView.as_view(), name='send-attendance-warning'),
    path('send-bulk-attendance-warning/', send_bulk_attendance_warningView.as_view(), name='send-bulk-attendance-warning'),
]