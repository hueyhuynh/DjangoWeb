# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-17 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Timesheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name=b'date of timesheet')),
                ('time_hour', models.IntegerField(max_length=2)),
                ('comment', models.CharField(max_length=1000)),
                ('submission', models.DateTimeField(verbose_name=b'date of submission')),
            ],
        ),
    ]
