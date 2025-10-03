# students/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("students/", views.StudentListCreateAPIView.as_view(), name="student-list-create"),
    path("students/<int:pk>/", views.StudentRetrieveUpdateAPIView.as_view(), name="student-detail-update"),
]
