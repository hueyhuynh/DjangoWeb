from __future__ import unicode_literals

from django.apps import AppConfig
# from .setup import DatabaseSetup


class TimesheetsConfig(AppConfig):
    name = 'timesheets'
    # def ready(self):
    #     print('Running setup.DatabaseSetup()')
    #     dbs = DatabaseSetup()