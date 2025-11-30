from django.db import transaction
# REPLACE 'api' WITH YOUR ACTUAL APP NAME
from core.models import Department, Course, Subject, CourseSubject

@transaction.atomic
def populate_data():
    print("--- Starting Syllabus Data Population ---")

    # 1. Create Department
    dept, _ = Department.objects.get_or_create(dept_name="Department of Computer Science")
    print(f"Department: {dept.dept_name}")

    # 2. Create Courses
    # MCA (2 Years = 4 Semesters)
    mca_course, _ = Course.objects.get_or_create(
        course_name="MCA",
        defaults={'dept': dept, 'total_semesters': 4}
    )
    
    # M.Sc. (2 Years = 4 Semesters)
    msc_course, _ = Course.objects.get_or_create(
        course_name="M.Sc. Computer Science",
        defaults={'dept': dept, 'total_semesters': 4}
    )
    print(f"Courses: {mca_course.course_name}, {msc_course.course_name}")

    # ---------------------------------------------------------
    # DATA DEFINITION
    # Format: (Semester, Code, Subject Name, Credits)
    # ---------------------------------------------------------
    
    # MCA Subjects (From your PDF)
    mca_data = [
        # Semester 1
        (1, "DSC101", "Object Oriented Programming", 4),
        (1, "DSC102", "Data Structures", 4),
        (1, "DSC103", "Database Systems", 4),
        (1, "SEC101", "Software Tools and Techniques", 2), # SEC is usually 2 credits
        (1, "DSE101", "Network Science", 4),
        (1, "DSE102", "Graph Theory", 4),
        
        # Semester 2
        (2, "DSC201", "Design and Analysis of Algorithms", 4),
        (2, "DSC202", "Operating Systems", 4),
        (2, "DSC203", "Artificial Intelligence and Machine Learning", 4),
        (2, "SEC201", "Scientific Writing and Computational Analysis Tools", 2),
        (2, "DSE201", "Social Networks Analysis", 4),

        # Semester 3
        (3, "DSC301", "Data Communication and Computer Networks", 4),
        (3, "DSC302", "Information Security", 4),
        
        # Semester 4
        (4, "DSC401", "Software Engineering", 4),
        (4, "DSC402", "Deep Learning", 4),
    ]

    # M.Sc. Subjects (Standard DU Syllabus)
    msc_data = [
        # Semester 1
        (1, "MCSC101", "Design and Analysis of Algorithms", 4),
        (1, "MCSC102", "Artificial Intelligence", 4),
        (1, "MCSC103", "Information Security", 4),
        (1, "MCSC104", "Mathematical Foundations of Computer Science", 4),
        (1, "MCSC105", "Data Mining", 4),

        # Semester 2
        (2, "MCSC201", "Artificial Neural Networks", 4),
        (2, "MCSC202", "Deep Learning", 4),
        (2, "MCSC203", "Internetworking with TCP/IP", 4),
        (2, "MCSC204", "Cloud Computing", 4),
    ]

    # ---------------------------------------------------------
    # POPULATION LOGIC
    # ---------------------------------------------------------

    # Helper function to create subject and link it
    def add_subjects(course_obj, data_list):
        for sem, code, name, credits in data_list:
            # 1. Create or Get Subject
            # We set current_semester on the Subject model as per your schema
            subject, created = Subject.objects.get_or_create(
                subject_code=code,
                defaults={
                    'subject_name': name,
                    'credits': credits,
                    'current_semester': sem
                }
            )
            
            # 2. Link to Course via CourseSubject Junction
            CourseSubject.objects.get_or_create(
                course=course_obj,
                subject=subject
            )
            if created:
                print(f"Created Subject: {code} - {name}")

    # Run for MCA
    print("\nProcessing MCA Subjects...")
    add_subjects(mca_course, mca_data)

    # Run for MSc
    print("\nProcessing M.Sc. Subjects...")
    add_subjects(msc_course, msc_data)

    print("\n--- Success! Data populated for Department, Courses, and Subjects. ---")

# Run the function
populate_data()