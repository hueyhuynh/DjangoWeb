from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


# Create your models here.
class Timesheet(models.Model):
    total_hours_worked = models.IntegerField()
    total_hours_break = models.IntegerField()
    submission_date = models.DateField("Date")
    approval_date = models.DateField("Date")
    employee = models.ForeignKey(
        User,
        null=True,
        related_name='employee_that_submitted_timesheet',
        on_delete=models.CASCADE
        )
    approving_manager = models.ForeignKey(
        User,
        null=True,
        related_name='manager_that_approved_timesheet',
        on_delete=models.CASCADE)

class PasswordReset(models.Model):
    date_time = models.DateTimeField(default=datetime.now(), blank=True)
    user = models.OneToOneField(User)
