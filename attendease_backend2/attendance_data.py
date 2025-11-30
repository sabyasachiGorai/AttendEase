import random
import datetime
from django.db import transaction
from django.utils import timezone
# REPLACE 'api' WITH YOUR ACTUAL APP NAME
from core.models import (
    StudentSubjectEnrollment, 
    TeacherSubject, 
    Attendance
)

@transaction.atomic
def populate_attendance_3months():
    print("--- Starting Attendance Generation (Last 3 Months) ---")

    # 1. Setup Date Range (90 Days)
    end_date = timezone.now().date()
    start_date = end_date - datetime.timedelta(days=90)
    
    # 2. Fetch all enrollments (Student + Subject)
    # We filter for semester 1 enrollments as per previous steps
    enrollments = StudentSubjectEnrollment.objects.filter(current_semester=1).select_related('student', 'subject')
    
    if not enrollments.exists():
        print("No enrollments found. Please run populate_users.py first.")
        return

    # Cache TeacherSubjects to avoid repeated DB hits
    # Map: subject_id -> TeacherSubject Object
    ts_map = {}
    teacher_subjects = TeacherSubject.objects.all()
    for ts in teacher_subjects:
        ts_map[ts.subject.id] = ts

    total_records = 0
    current_date = start_date

    # 3. Iterate through every day in the range
    while current_date <= end_date:
        # Skip Weekends (Saturday=5, Sunday=6)
        if current_date.weekday() >= 5:
            current_date += datetime.timedelta(days=1)
            continue
            
        # Optional: Skip random days (e.g., holidays) - 5% chance the whole class was off
        if random.random() < 0.05:
            print(f"Skipping {current_date} (Simulated Holiday)")
            current_date += datetime.timedelta(days=1)
            continue

        print(f"Processing Date: {current_date}...")
        
        daily_records = []
        
        for enroll in enrollments:
            student = enroll.student
            subject = enroll.subject
            
            # Find the TeacherSubject for this subject
            ts_obj = ts_map.get(subject.id)
            
            if not ts_obj:
                continue

            # Random Status (85% Present, 15% Absent)
            status = 'Present' if random.random() > 0.15 else 'Absent'
            
            # Check if record already exists to avoid duplicates if you run script twice
            if not Attendance.objects.filter(student=student, ts=ts_obj, attendance_date=current_date).exists():
                record = Attendance(
                    student=student,
                    ts=ts_obj,
                    attendance_date=current_date,
                    status=status,
                    created_by=ts_obj.teacher
                )
                daily_records.append(record)

        # Bulk Create for performance
        if daily_records:
            Attendance.objects.bulk_create(daily_records)
            total_records += len(daily_records)
        
        current_date += datetime.timedelta(days=1)

    print(f"\n--- Success! Generated {total_records} attendance records for the last 3 months. ---")

# Execute
populate_attendance_3months()