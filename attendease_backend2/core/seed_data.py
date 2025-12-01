import random
import datetime
from django.db import transaction
from django.utils import timezone
from core.models import (
    StudentSubjectEnrollment,
    TeacherSubject,
    Attendance
)


@transaction.atomic
def populate_attendance_3months():
    print("\n--- Starting Attendance Generation (Last 3 Months) ---")

    # 1. Date range (90 days)
    end_date = timezone.now().date()
    start_date = end_date - datetime.timedelta(days=90)

    # 2. Get enrollments (Semester 1 students)
    enrollments = StudentSubjectEnrollment.objects.filter(
        current_semester=1
    ).select_related("student", "subject")

    if not enrollments.exists():
        print("No enrollments found. Run populate_users.py first.")
        return

    # 3. TeacherSubject map (subject_id → ts object)
    ts_map = {ts.subject.id: ts for ts in TeacherSubject.objects.all()}

    # 4. Pick 3–4 students who will have <75% attendance
    all_students = list({e.student for e in enrollments})
    low_attendance_students = random.sample(all_students, k=min(4, len(all_students)))

    print(f"Low Attendance Students (Forced <75%): {[s.id for s in low_attendance_students]}")
    print("--- Generating daily attendance ---")

    total_created = 0
    total_updated = 0

    current_date = start_date

    while current_date <= end_date:

        # Skip weekends
        if current_date.weekday() >= 5:
            current_date += datetime.timedelta(days=1)
            continue

        # 5% chance of holiday
        if random.random() < 0.05:
            print(f"Skipping {current_date} → Simulated Holiday")
            current_date += datetime.timedelta(days=1)
            continue

        print(f"Processing date: {current_date}...")

        # Process attendance for every student in enrollments
        for enroll in enrollments:
            student = enroll.student
            subject = enroll.subject

            ts_obj = ts_map.get(subject.id)
            if not ts_obj:
                continue

            # Attendance probability
            if student in low_attendance_students:
                # Low attendance students (Only ~40% present)
                status = "Present" if random.random() < 0.40 else "Absent"
            else:
                # Normal students (85% present)
                status = "Present" if random.random() > 0.15 else "Absent"

            # Update existing record OR create new one
            obj, created = Attendance.objects.update_or_create(
                student=student,
                ts=ts_obj,
                attendance_date=current_date,
                defaults={
                    "status": status,
                    "created_by": ts_obj.teacher
                }
            )

            if created:
                total_created += 1
            else:
                total_updated += 1

        # Move to next day
        current_date += datetime.timedelta(days=1)

    print("\n--- Attendance Generation Complete ---")
    print(f"Created records: {total_created}")
    print(f"Updated records: {total_updated}")
    print("---------------------------------------\n")


# Execute
populate_attendance_3months()
