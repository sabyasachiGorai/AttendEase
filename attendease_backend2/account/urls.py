
from django.urls import path
from .views import (userRegistrationView, userLoginView, UserProfileView, changeUserPasswordView,
                    userPasswordResetEmailView, userPasswordResetView, StudentRegistrationView,
                    teacherRegistrationView)

urlpatterns = [
    path('register/', userRegistrationView.as_view(), name='user-registration'),
    path('login/', userLoginView.as_view(), name='user-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('changeUserPassword/', changeUserPasswordView.as_view(), name='changeUser-Password'),
    path('send-password-reset-email/', userPasswordResetEmailView.as_view(), name='send-password-reset-email'),
    path('reset/<uid>/<token>/', userPasswordResetView.as_view(), name='password-reset'),

    path('studentRegistration/', StudentRegistrationView.as_view(), name='student-registration'),
    path('teacherRegistration/', teacherRegistrationView.as_view(), name='teacher-registration'),
    
]