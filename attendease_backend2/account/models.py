from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, name, gender,role, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not role:
            raise ValueError("Role is required")
        
        # Allow role='admin' ONLY for superuser creation
        if role == "admin" and not extra_fields.get("is_superuser"):
            raise ValueError("Only superusers can have role='admin'.")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, gender=gender, role=role, **extra_fields)
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(
        email=email,
        name=name,
        gender = 'other',
        role="admin",   # superuser role fixed
        password=password,
        **extra_fields
        )

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)   # used by Django admin

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    def __str__(self):
        return self.email