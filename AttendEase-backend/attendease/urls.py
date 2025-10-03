# attendease/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "message": "Welcome to AttendEase API",
        "endpoints": {
            "list_create_students": "/api/students/",
            "get_update_student": "/api/students/<id>/"
        }
    })

urlpatterns = [
    path("", home, name="home"),          # Homepage at "/"
    path("admin/", admin.site.urls),
    path("api/", include("students.urls")),
]
