import random
from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils import timezone
# REPLACE 'api' WITH YOUR ACTUAL APP NAME
from core.models import (
    Department, Course, Subject, CourseSubject, 
    Teacher, TeacherSubject, Student, StudentSubjectEnrollment
)

# 1. Get your Custom User Model
User = get_user_model()

# Helper for fake phone numbers
def get_phone():
    return f"98765{random.randint(10000, 99999)}"

@transaction.atomic
def populate_users():
    print("--- Starting User Population (Custom User Model) ---")

    # Fetch Prerequisites (Created in previous syllabus script)
    try:
        dept = Department.objects.get(dept_name="Department of Computer Science")
        mca_course = Course.objects.get(course_name="MCA")
        msc_course = Course.objects.get(course_name="M.Sc. Computer Science")
    except Department.DoesNotExist:
        print("Error: Departments or Courses missing. Run populate_syllabus.py first.")
        return

    # =============================================
    # PART A: TEACHERS
    # Requirement: "in each semester he can teach one subject"
    # Strategy: For Sem 1, we create a UNIQUE teacher for every subject.
    # =============================================
    print("\n--- Creating Teachers (Custom User + Teacher Profile) ---")
    
    # Get all subjects for Semester 1
    mca_subjects = CourseSubject.objects.filter(course=mca_course, subject__current_semester=1)
    msc_subjects = CourseSubject.objects.filter(course=msc_course, subject__current_semester=1)
    
    all_sem1_mappings = list(mca_subjects) + list(msc_subjects)
    
    teacher_counter = 1

    for mapping in all_sem1_mappings:
        subject = mapping.subject
        course = mapping.course
        
        # Generates unique email based on subject code (e.g., prof.dsc101@du.ac.in)
        email = f"prof.{subject.subject_code.lower()}@du.ac.in"
        name = f"Prof. {subject.subject_name.split(' ')[0]}" # First word of subject as name
        
        # 1. Create Custom User (Using your UserManager)
        if not User.objects.filter(email=email).exists():
            user = User.objects.create_user(
                email=email,          # Username Field
                name=name,            # Required Field
                gender='male',        # Custom Field
                role='teacher',       # Custom Field (Critical for your logic)
                password='pass1234'
            )
            
            # 2. Create Teacher Profile (OneToOne Link)
            teacher = Teacher.objects.create(
                user=user,
                employee_code=f"TCH{teacher_counter:03d}",
                department=dept,
                designation="Assistant Professor",
                phone_number=get_phone(),
                joining_date=timezone.now().date()
            )
            
            # 3. Assign Subject
            TeacherSubject.objects.create(
                teacher=teacher,
                subject=subject,
                course=course
            )
            print(f"Created Teacher: {email} -> {subject.subject_name}")
            teacher_counter += 1

    # =============================================
    # PART B: STUDENTS
    # Requirement: 10 MCA Students, 10 MSc Students (Sem 1)
    # =============================================
    
    def create_batch(course_obj, prefix, count, subjects_query):
        print(f"\n--- Creating {count} {prefix} Students ---")
        
        # List of subjects to enroll in
        subjects_list = [cs.subject for cs in subjects_query]
        
        for i in range(1, count + 1):
            roll_no = f"{prefix}2025{i:03d}"  # e.g., MCA2025001
            email = f"{prefix.lower()}{i}@du.ac.in"
            name = f"{prefix} Student {i}"
            gender = random.choice(['male', 'female'])
            
            # 1. Create Custom User
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(
                    email=email,
                    name=name,
                    gender=gender,
                    role='student',    # Custom Field
                    password='pass1234'
                )
                
                # 2. Create Student Profile (OneToOne Link)
                student = Student.objects.create(
                    user=user,
                    roll_number=roll_no,
                    course=course_obj,
                    current_semester=1,
                    year_of_study=1,
                    phone_number=get_phone()
                )
                
                # 3. Enroll in ALL Sem 1 Subjects
                enrollments = []
                for sub in subjects_list:
                    enrollments.append(StudentSubjectEnrollment(
                        student=student,
                        subject=sub,
                        current_semester=1
                    ))
                StudentSubjectEnrollment.objects.bulk_create(enrollments)
                
                print(f"Created Student: {roll_no} ({name})")

    # Generate 10 MCA Students
    create_batch(mca_course, "MCA", 10, mca_subjects)

    # Generate 10 MSc Students
    create_batch(msc_course, "MSC", 10, msc_subjects)

    print("\n--- User Population Complete ---")

# Run the function
populate_users()