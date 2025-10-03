# students/models.py
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    roll_number = models.CharField(max_length=50, unique=True)
    # percentage up to 100.00 (use decimal for precision)
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"
