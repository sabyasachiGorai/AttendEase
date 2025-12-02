"""
===========================================================
 File Name: models.py
 Author: Aman Ansari
 Description:
     This file contains the Custom User Model and 
     UserManager for handling authentication, 
     registration, and role-based access in the system.

     It replaces Django's default User model by using:
         - AbstractBaseUser (for authentication)
         - PermissionsMixin (for groups & permissions)
         - BaseUserManager (for user creation methods)

     Features:
     - Email-based login
     - Role-based access: student, teacher, admin
     - Prevents "admin" role from being assigned to normal users
===========================================================
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, name, gender,role, password=None, **extra_fields):
        """
        Creates and returns a normal user.

        Args:
            email (str): User's email address (required).
            name (str): Full name of the user.
            gender (str): Gender value from allowed choices.
            role (str): User role -> student | teacher | admin
            password (str): Password for the user.
            extra_fields: Additional optional fields.

        Raises:
            ValueError: If email or role is missing.
            ValueError: If someone tries to assign role='admin'
                        without being a superuser.

        Returns:
            User: Newly created User instance.
        """
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
        """
        Creates and returns a superuser (admin).

        Automatically sets:
            - is_staff = True
            - is_superuser = True
            - role = "admin"

        Args:
            email (str): Superuser email.
            name (str): Superuser name.
            password (str): Password.

        Returns:
            User: Newly created superuser instance.
        """
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
    """
    Custom User Model that replaces Django's default User.
    
    Features:
        - Uses email instead of username for login
        - Includes different user roles:
            student | teacher | admin
        - Supports gender options
        - Timestamps for created and updated records
    """
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