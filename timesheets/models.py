from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Timesheet(models.Model):
    total_hours_worked = models.IntegerField()
    total_hours_break = models.IntegerField()
    submission_date = models.DateTimeField('Date the timesheet was submitted by the employee')
    approval_date = models.DateTimeField('Date the timesheet was approved by the Approving Manager')
    employee = models.ForeignKey(
        User,
        null=True,
        limit_choices_to={'groups__name': "employees"},
        related_name='employee_that_submitted_timesheet',
        on_delete=models.CASCADE
        )
    approving_manager = models.ForeignKey(
        User,
        null=True,
        limit_choices_to={'groups__name': "managers"},
        related_name='manager_that_approved_timesheet',
        on_delete=models.CASCADE
        )
