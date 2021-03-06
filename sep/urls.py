"""sep URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include

from timesheets import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'userLogout', views.userLogout, name='userLogout'),
    url(r'dashboard', views.dashboard, name='dashboard'),
    url(r'registration_form', views.registration_form, name='registration_form'),
    url(r'password_reset', views.password_reset, name='password_reset'),
    url(r'password_change', views.password_change, name='password_change'),
    url(r'create_timesheet', views.create_timesheet, name='create_timesheet'),
    url(r'^(?P<id>\d+)/$', views.timesheet_detail, name='detail'),
    url(r'^(?P<id>\d+)/edit/$', views.timesheet_edit, name='edit'),
    url(r'^(?P<id>\d+)/delete/$', views.timesheet_delete, name='delete'),
    url(r'approve_timesheet', views.approve_timesheet, name='approve_timesheet')

]
