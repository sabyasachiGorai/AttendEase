from django.core.management.base import BaseCommand
from core.scripts.populate import run

class Command(BaseCommand):
    help = "Populate database with demo data (courses, teachers, students, attendance)"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting data population...")
        run()
        self.stdout.write(self.style.SUCCESS("Data population complete ✔"))
