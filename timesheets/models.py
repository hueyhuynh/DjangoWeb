from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from django.urls import reverse

# Create timesheet object
#class TimesheetManager(models.Manager):
    #def create_timesheet(self, total_hours_worked, total_hours_break, submission_date, approval_date, employee, approving_manager):
        #timesheet = self.create(total_hours_worked=total_hours_worked, total_hours_break=total_hours_break,
                                #submission_date=submission_date, approval_date=approval_date,
                                #employee=employee, approving_manager=approving_manager)
        #return timesheet

# Create your models here.
class Timesheet(models.Model):
    total_hours_worked = models.IntegerField()
    total_hours_break = models.IntegerField()
    submission_date = models.DateTimeField('Date the timesheet was submitted by the employee')
    approval_date = models.DateTimeField(null=True)
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

    def __unicode__(self):
        return self.employee

    def __str__(self):
        return format(self.employee)

    def get_absolute_url(self):
        return reverse('detail', kwargs={"id": self.id})
    #objects = TimesheetManager()

class PasswordReset(models.Model):
    date_time = models.DateTimeField(default=datetime.now(), blank=True)
    user = models.OneToOneField(User)
    on_delete=models.CASCADE

