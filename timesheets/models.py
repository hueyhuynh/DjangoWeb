from django.db import models

class Timesheet(models.Model):
    date = models.DateField('date of timesheet')
    time_hour = models.IntegerField()
    comment = models.CharField(max_length=1000)
    submission = models.DateTimeField('date of submission')
