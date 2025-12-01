import random
from django.db import transaction
from django.contrib.auth import get_user_model

from core.models import (
    Course, CourseSubject, Student,
    StudentSubjectEnrollment, Teacher, TeacherSubject
)

User = get_user_model()


def get_phone():
    return f"98765{random.randint(10000, 99999)}"


@transaction.atomic
def populate_sem3_students_and_assign_teachers():

    print("\n=== ADDING SEM-3 STUDENTS (YEAR 2) + ASSIGNING SEM-3 TEACHERS ===")

    # ------------------------------------------------------------
    # 1. Fetch Courses
    # ------------------------------------------------------------
    mca = Course.objects.filter(course_name="MCA").first()
    msc = Course.objects.filter(course_name="M.Sc. Computer Science").first()

    if not mca:
        print("ERROR: MCA course missing.")
        return

    # ------------------------------------------------------------
    # 2. Fetch Semester-3 Subjects (MCA + MSc)
    # ------------------------------------------------------------
    mca_sem3 = list(CourseSubject.objects.filter(
        course=mca,
        subject__current_semester=3
    ))

    msc_sem3 = []
    if msc:
        msc_sem3 = list(CourseSubject.objects.filter(
            course=msc,
            subject__current_semester=3
        ))

    print(f"MCA Sem-3 subjects found: {len(mca_sem3)}")
    print(f"MSc Sem-3 subjects found: {len(msc_sem3)}")

    if not mca_sem3:
        print("❌ MCA does NOT have Sem-3 subjects. Cannot continue.")
        return

    # ============================================================
    # A) CREATE SEM-3 STUDENTS SAFELY
    # ============================================================

    def create_sem3_students(course_obj, prefix, sem3_subjects):
        existing = Student.objects.filter(
            course=course_obj,
            current_semester=3
        ).count()

        print(f"\nCreating 10 NEW {prefix.upper()} Semester-3 (Year 2) Students...")

        for i in range(1, 11):

            idx = existing + i
            roll_no = f"{prefix.upper()}2024{idx:03d}"
            email = f"{prefix.lower()}_sem3_{idx}@du.ac.in"

            if User.objects.filter(email=email).exists():
                continue

            # Create user
            user = User.objects.create_user(
                email=email,
                name=f"{prefix.upper()} Sem3 Student {idx}",
                gender=random.choice(["male", "female", "other"]),
                role="student",
                password="pass1234"
            )

            # Create student profile
            student = Student.objects.create(
                user=user,
                roll_number=roll_no,
                course=course_obj,
                current_semester=3,
                year_of_study=2,
                phone_number=get_phone()
            )

            # Enroll in SEM-3 subjects
            StudentSubjectEnrollment.objects.bulk_create([
                StudentSubjectEnrollment(
                    student=student,
                    subject=cs.subject,
                    current_semester=3
                ) for cs in sem3_subjects
            ])

            print(f"✓ Created Sem-3 Student: {roll_no}")

    # -------------------------------
    # Create MCA Sem-3 Students
    # -------------------------------
    create_sem3_students(mca, "mca", mca_sem3)

    # -------------------------------
    # Create MSc Sem-3 Students ONLY IF SUBJECTS EXIST
    # -------------------------------
    if msc and len(msc_sem3) > 0:
        create_sem3_students(msc, "msc", msc_sem3)
    else:
        print("\n⚠ Skipping MSc Semester-3 Students — No Sem-3 subjects available.")

    # ============================================================
    # B) ASSIGN TEACHERS TO SEM-3 SUBJECTS
    # ============================================================

    print("\nAssigning Sem-3 subjects to teachers...")

    teachers = list(Teacher.objects.all())

    if len(teachers) < 2:
        print("ERROR: Need at least 2 teachers.")
        return

    # Pick 3 teachers if possible else pick all
    k = min(3, len(teachers))
    selected_teachers = random.sample(teachers, k=k)

    # Combine MCA + MSc sem-3 subjects
    all_sem3 = mca_sem3 + msc_sem3
    random.shuffle(all_sem3)

    assigned = 0

    for teacher, cs in zip(selected_teachers, all_sem3):

        if TeacherSubject.objects.filter(teacher=teacher, subject=cs.subject).exists():
            continue

        TeacherSubject.objects.create(
            teacher=teacher,
            subject=cs.subject,
            course=cs.course
        )

        print(f"✓ Teacher {teacher.user.email} now teaches Sem-3 subject: {cs.subject.subject_name}")
        assigned += 1

    print(f"\n--- DONE: Assigned Sem-3 subjects to {assigned} teachers ---\n")
