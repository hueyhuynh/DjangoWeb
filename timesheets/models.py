from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Timesheet(models.Model):
    total_hours_worked = models.IntegerField()
    total_hours_break = models.IntegerField()
    submission_date = models.DateTimeField('Date the timesheet was submitted by the employee')
    approval_date = models.DateTimeField('Date the timesheet was approved by the Approving Manager')
