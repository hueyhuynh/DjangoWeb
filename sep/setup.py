# Class for setting up the default database, if it doesn't exist upon running the server
import os.path
# import django
# django.setup()
from django.db import models

from django.contrib.auth.models import User

class DatabaseSetup:
    def __init__(self):
        if self.database_exists():
            print("Database exists, nothing to do.")
        else:
            print("Populating database with initial data")
            self.setup_database()

    def database_exists(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(BASE_DIR, 'db.sqlite3')
        db_exists = os.path.isfile(db_path)
        return db_exists

    def setup_database(self):
        # Create staff/admin superuser
        email = 'admin@staff.com'
        super_user = User.objects.create(username='admin', email=email, is_staff=True)
        super_user.set_password(qweqweqwe)
        super_user.save()

        # Create employees
        employee1 = User.objects.create_user(
            username='employee',
            password='qweqweqwe'
            )
        employee2 = User.objects.create_user(
            username='employee2',
            password='qweqweqwe'
            )

