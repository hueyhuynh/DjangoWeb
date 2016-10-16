from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from django.urls import reverse


# Create your models here.
class Timesheet(models.Model):
    #integer fields for the total hours worked and hours on break
    total_hours_worked = models.IntegerField()
    total_hours_break = models.IntegerField()
    #this field will be used for tracking the submission of the timesheet, this is automatic
    submission_date = models.DateTimeField('Date the timesheet was submitted by the employee')
    #this field will be used for tracking the approval of the timesheet, this is automatic
    approval_date = models.DateTimeField(null=True)
    #Used to get the employee's ID (Unique) this is the same for the approving manager
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


    def __str__(self):
        return format(self.employee)

    def get_absolute_url(self):
        return reverse('detail', kwargs={"id": self.id})

    class Meta:
        ordering = ["-submission_date"]

class PasswordReset(models.Model):
    date_time = models.DateTimeField(default=datetime.now(), blank=True)
    user = models.OneToOneField(User)
    on_delete=models.CASCADE

