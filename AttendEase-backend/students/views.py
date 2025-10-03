# students/views.py
from rest_framework import generics
from .models import Student
from .serializers import StudentSerializer

class StudentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Student.objects.all().order_by("id")
    serializer_class = StudentSerializer

class StudentRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
