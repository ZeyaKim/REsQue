from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection

from REsQue.settings import USER_APPS


class Command(BaseCommand):
    help = "Resets migrations, creates new ones, and applies them"

    def handle(self, *args, **options):
        self.stdout.write("Resetting migrations...")
        for app in USER_APPS:
            call_command("migrate", app, "zero")

        self.stdout.write("Dropping all tables...")
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
            )
            tables = cursor.fetchall()
            for table in tables:
                cursor.execute(f'DROP TABLE IF EXISTS "{table[0]}" CASCADE')

        self.stdout.write("Creating new migrations...")
        call_command("makemigrations")

        self.stdout.write("Applying new migrations...")
        call_command("migrate")

        self.stdout.write(self.style.SUCCESS("Re-migration completed successfully!"))
