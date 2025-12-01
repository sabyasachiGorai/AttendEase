import random
from datetime import date, timedelta
from django.db import transaction, IntegrityError
from django.contrib.auth import get_user_model

from core.models import (
    Department, Course, Subject, CourseSubject,
    Teacher, TeacherSubject, Student, StudentSubjectEnrollment,
    Attendance
)

User = get_user_model()

# Seed for reproducibility
RNG_SEED = 12345
random.seed(RNG_SEED)


# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------

def create_or_get(model, defaults=None, **kwargs):
    if defaults is None:
        defaults = {}
    obj, created = model.objects.get_or_create(defaults=defaults, **kwargs)
    return obj, created


def make_email(name, domain="cs.du.ac.in"):
    name_part = name.lower().replace(" ", ".")
    return f"{name_part}@{domain}"


def weekday_dates_last_n_weeks(n_weeks=8):
    end = date.today()
    start = end - timedelta(days=n_weeks * 7)
    dates = []
    d = start
    while d <= end:
        if d.weekday() < 5:  # Mon-Fri
            dates.append(d)
        d += timedelta(days=1)
    return dates


# ------------------------------------------------------------
# Core Data Creation Logic
# ------------------------------------------------------------

@transaction.atomic
def create_department_and_courses():
    dept, _ = create_or_get(Department, dept_name="Department of Computer Science")

    course_mca, _ = create_or_get(
        Course, course_name="MCA", dept=dept,
        defaults={"total_semesters": 4}
    )

    course_msc, _ = create_or_get(
        Course, course_name="M.Sc Computer Science", dept=dept,
        defaults={"total_semesters": 4}
    )

    return dept, {"MCA": course_mca, "M.Sc Computer Science": course_msc}


@transaction.atomic
def create_all_subjects(course_objs):
    subjects_by_course = {"MCA": [], "M.Sc Computer Science": []}

    def add_sub(course_key, code, name, sem, credits=4):
        subj_code = code if course_key == "M.Sc Computer Science" else f"MCA-{code}"
        subj, created = Subject.objects.get_or_create(
            subject_code=subj_code,
            defaults={"subject_name": name, "credits": credits, "current_semester": sem}
        )
        if subj.current_semester != sem:
            subj.current_semester = sem
            subj.save()

        CourseSubject.objects.get_or_create(
            course=course_objs[course_key],
            subject=subj
        )
        subjects_by_course[course_key].append(subj)
        return subj

    # ------------------ M.Sc CS ------------------
    # Sem 1
    add_sub("M.Sc Computer Science", "DSC101", "Advanced Algorithms", 1)
    add_sub("M.Sc Computer Science", "DSC102", "Machine Learning", 1)
    add_sub("M.Sc Computer Science", "DSC103", "Mathematical Foundations of Computer Science", 1)
    add_sub("M.Sc Computer Science", "SBC101", "Scientific Writing & Computational Tools", 1)
    add_sub("M.Sc Computer Science", "LAB101", "Programming Lab", 1)

    # Sem 2
    add_sub("M.Sc Computer Science", "DSC201", "Database Systems & Big Data", 2)
    add_sub("M.Sc Computer Science", "DSC202", "Theory of Computation", 2)
    add_sub("M.Sc Computer Science", "DSC203", "Statistical Methods", 2)
    add_sub("M.Sc Computer Science", "SBC201", "Research Methodology", 2)
    add_sub("M.Sc Computer Science", "LAB201", "DB & Analytics Lab", 2)

    # Sem 3
    add_sub("M.Sc Computer Science", "DSC301", "Natural Language Processing", 3)
    add_sub("M.Sc Computer Science", "DSC302", "Optimization Methods", 3)
    add_sub("M.Sc Computer Science", "DSC303", "Computer Vision", 3)
    add_sub("M.Sc Computer Science", "SBC301", "Seminar & Project I", 3)
    add_sub("M.Sc Computer Science", "LAB301", "AI/ML Lab", 3)

    # Sem 4
    add_sub("M.Sc Computer Science", "DSC401", "Distributed Systems", 4)
    add_sub("M.Sc Computer Science", "DSC402", "Advanced ML (Elective)", 4)
    add_sub("M.Sc Computer Science", "SBC401", "Project II", 4)
    add_sub("M.Sc Computer Science", "ELECTIV401", "Blockchain/IoT/Quantum", 4)
    add_sub("M.Sc Computer Science", "LAB401", "Project Lab", 4)

    # ------------------ MCA ------------------
    # Sem 1
    add_sub("MCA", "DSC101", "Object Oriented Programming", 1)
    add_sub("MCA", "DSC102", "Data Structures", 1)
    add_sub("MCA", "DSC103", "Database Systems", 1)
    add_sub("MCA", "SEC101", "Software Tools Lab", 1)
    add_sub("MCA", "AEC101", "Communication Skills", 1)

    # Sem 2
    add_sub("MCA", "DSC201", "Operating Systems", 2)
    add_sub("MCA", "DSC202", "Computer Networks", 2)
    add_sub("MCA", "DSC203", "Software Engineering", 2)
    add_sub("MCA", "LAB201", "OS & Networking Lab", 2)
    add_sub("MCA", "GE201", "Generic Elective", 2)

    # Sem 3
    add_sub("MCA", "DSC301", "DCN", 3)
    add_sub("MCA", "DSC302", "Information Security", 3)
    add_sub("MCA", "DSC303", "Web Technologies", 3)
    add_sub("MCA", "SBC301", "Mini Project", 3)
    add_sub("MCA", "LAB301", "Web/Security Lab", 3)

    # Sem 4
    add_sub("MCA", "DSC401", "Distributed Systems", 4)
    add_sub("MCA", "DSC402", "Machine Learning", 4)
    add_sub("MCA", "SBC401", "Major Project", 4)
    add_sub("MCA", "ELECTIV401", "Elective", 4)
    add_sub("MCA", "LAB401", "Project Lab", 4)

    return subjects_by_course


@transaction.atomic
def create_teachers():
    teacher_names = [
        "Dr Amit Singh", "Dr Pooja Sharma", "Dr Rajiv Kumar",
        "Ms Neha Verma", "Mr Sandeep Roy", "Dr Kavita Jain",
        "Ms Anjali Mehta", "Mr Rohit Kapoor"
    ]

    teachers = []
    dept = Department.objects.get(dept_name="Department of Computer Science")

    for i, tn in enumerate(teacher_names, start=1):
        email = make_email(tn)
        user, created = User.objects.get_or_create(
            email=email,
            defaults={"name": tn, "gender": "other", "role": "teacher"}
        )

        if created:
            user.set_password("password123")
            user.save()

        teacher_obj, _ = Teacher.objects.get_or_create(
            user=user,
            defaults={
                "employee_code": f"TCHR{i:03d}",
                "phone_number": f"98765{random.randint(10000,99999)}",
                "department": dept,
                "designation": "Assistant Professor"
            }
        )
        teachers.append(teacher_obj)

    return teachers


@transaction.atomic
def create_students(course_objs):
    student_groups = {}

    for course_key, sem_list in [("MCA", [1, 3]), ("M.Sc Computer Science", [1, 3])]:
        for sem in sem_list:
            key = f"{course_key}_sem{sem}"
            student_groups[key] = []

            for i in range(1, 11):
                name = f"{course_key.split()[0][:3].upper()}_S{sem}_{i:02d}"
                roll = f"{course_key.split()[0][:3].upper()}{sem:02d}{i:03d}"
                email = make_email(name)

                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={
                        "name": name,
                        "gender": random.choice(["male", "female", "other"]),
                        "role": "student",
                    }
                )
                if created:
                    user.set_password("studentpass")
                    user.save()

                student_obj, _ = Student.objects.get_or_create(
                    user=user,
                    defaults={
                        "roll_number": roll,
                        "phone_number": f"9{random.randint(700000000,999999999)}",
                        "course": course_objs[course_key],
                        "current_semester": sem,
                        "year_of_study": 1 if sem == 1 else 2
                    }
                )
                student_groups[key].append(student_obj)

    return student_groups


@transaction.atomic
def link_teachers_and_assign_subjects(teachers, course_objs, subjects_by_course):
    tcount = len(teachers)
    t_idx = 0

    # round-robin assignment
    for course_key, subj_list in subjects_by_course.items():
        for subj in subj_list:
            teacher = teachers[t_idx % tcount]
            TeacherSubject.objects.get_or_create(
                teacher=teacher, subject=subj, course=course_objs[course_key]
            )
            t_idx += 1

    # ensure first 3 teachers teach both sem1 and sem3
    sem1 = []
    sem3 = []

    for course_key, sl in subjects_by_course.items():
        for s in sl:
            if s.current_semester == 1:
                sem1.append((course_objs[course_key], s))
            if s.current_semester == 3:
                sem3.append((course_objs[course_key], s))

    for i in range(3):
        if sem1:
            c1, s1 = sem1[i % len(sem1)]
            TeacherSubject.objects.get_or_create(
                teacher=teachers[i], subject=s1, course=c1
            )
        if sem3:
            c3, s3 = sem3[i % len(sem3)]
            TeacherSubject.objects.get_or_create(
                teacher=teachers[i], subject=s3, course=c3
            )


@transaction.atomic
def enroll_students(student_groups, subjects_by_course, course_objs):
    enrollments = []

    for course_key, course_obj in course_objs.items():
        for sem in [1, 2, 3, 4]:
            key = f"{course_key}_sem{sem}"
            if key not in student_groups:
                continue

            students = student_groups[key]
            subj_list = [
                s for s in subjects_by_course[course_key]
                if s.current_semester == sem
            ]

            for st in students:
                for subj in subj_list:
                    StudentSubjectEnrollment.objects.get_or_create(
                        student=st, subject=subj, current_semester=sem
                    )
                    enrollments.append((st, subj, course_obj))

    return enrollments


@transaction.atomic
def generate_attendance(enrollments, n_weeks=8):
    dates = weekday_dates_last_n_weeks(n_weeks)

    grouped = {}
    for st, subj, course in enrollments:
        key = (course.id, subj.id)
        grouped.setdefault(key, {"students": [], "subject": subj, "course": course})
        grouped[key]["students"].append(st)

    for key, info in grouped.items():
        subj = info["subject"]
        students = info["students"]
        course = info["course"]

        ts = TeacherSubject.objects.filter(subject=subj, course=course).first()

        low_count = min(4, max(1, len(students)//3))
        low_students = random.sample(students, low_count)

        for st in students:
            prob = 0.62 if st in low_students else 0.92

            for d in dates:
                status = "Present" if random.random() < prob else "Absent"

                try:
                    Attendance.objects.create(
                        student=st,
                        ts=ts,
                        attendance_date=d,
                        status=status,
                        created_by=ts.teacher if ts else None
                    )
                except IntegrityError:
                    continue


# ------------------------------------------------------------
# RUN() — the function you call from Django shell
# ------------------------------------------------------------

def run():
    print("Starting data population...")

    dept, course_objs = create_department_and_courses()
    subjects_by_course = create_all_subjects(course_objs)
    teachers = create_teachers()
    student_groups = create_students(course_objs)
    link_teachers_and_assign_subjects(teachers, course_objs, subjects_by_course)
    enrollments = enroll_students(student_groups, subjects_by_course, course_objs)
    generate_attendance(enrollments)

    print("POPULATION COMPLETE ✔")
    print(f"Teachers: {Teacher.objects.count()}")
    print(f"Students: {Student.objects.count()}")
    print(f"Subjects: {Subject.objects.count()}")
    print(f"Attendance Records: {Attendance.objects.count()}")
    print("Emails use @cs.du.ac.in")
    print("Low attendance (<75%) students generated.")
