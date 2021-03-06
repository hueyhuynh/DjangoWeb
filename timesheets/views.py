from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, PasswordResetForm, PasswordChangeForm, CreateTimesheetForm
from django.contrib.auth.models import User, Group
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.mail import send_mail
from models import *
from datetime import datetime
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect

import uuid

from sep.settings import EMAIL_HOST_USER

def index(request):
    #   template = loader.get_template('timesheets/index.html')
    form = UserForm()
    errors = False
    if request.method == 'POST':
        #Request signin form - Gets username and password
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            #if user is returned through the authenticate method - login through the dashboard
            if user.is_authenticated:

                login(request, user)
                return redirect('dashboard')

        else:
            errors = True
            return render(request, 'timesheets/index.html', {'form': form, "errors": errors})
    else:
        return render(request, 'timesheets/index.html',{'form': form})

def userLogout(request):
    logout(request)
    return redirect('index')

def registration_form(request):
    # If the request method is POST, it means that the form has been submitted
    # and we need to validate it.
    if request.method == 'POST':
        # Create a RegistrationForm instance with the submitted data
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                password = str(uuid.uuid4().get_hex().upper()[0:6])
                # creating user object
                user = User.objects.create_user(
                    first_name=form.cleaned_data['name'],
                    username=form.cleaned_data['username'],
                    password=password,
                    email=form.cleaned_data['email']
                )
                # Add user to the employees group
                #user.groups.add(Group.objects.get(name='employees'))
                g = Group.objects.get(name='employees')
                g.user_set.add(user)

                message = str("Your username is: %s\n" % form.cleaned_data['username'])
                message += str("Your password is: %s" % password)
                send_mail("User registration completed", message, EMAIL_HOST_USER, [form.cleaned_data['email']])
                return render(request, 'timesheets/messagebox2.html',

                                  {'message': 'An autogenerated password has been sent to your email address.'})

                              #{'message': 'An autogenerated password (' + password + ') has been sent to your email address.'})

            except Exception as e:
                return render(request, 'timesheets/messagebox2.html',
                              {'message': 'Error: Unable to send mail. Please cross check your email.'})
    else:
        form = RegistrationForm()

    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response('timesheets/registration_form.html', variables, )

def password_change(request):

    if request.method == 'POST':

        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            errors = False
            try:
                u = User.objects.get(username__exact=form.cleaned_data['username'])
                pr = PasswordReset.objects.get_or_create(user=u)[0]
                t = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
                if (t - pr.date_time).days > 5:
                    return render(request, 'timesheets/messagebox2.html', {'message': 'Sorry! cannot reset password more than once in a day'})
                pr.date_time = t
                pr.save()
                passwrd = form.cleaned_data["password"]
                u.set_password(passwrd)
                u.save()
                message = str("Your new password is: %s" % passwrd)
                send_mail("Password changed", message, EMAIL_HOST_USER, [u.email])
            except Exception as e:
                errors = True
            return render_to_response('timesheets/success_password_sent.html', {'errors': errors},)
    else:
        form = PasswordChangeForm()

    variables = RequestContext(request, {
    'form': form
    })
    return render_to_response('timesheets/password_change.html', variables,)

def password_reset(request):
    # If the request method is POST, it means that the form has been submitted
    # and we need to validate it.
    if request.method == 'POST':
        # Create a PasswordResetForm instance with the submitted data
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            errors = False
            try:
                u = User.objects.get(email__exact=form.cleaned_data['email'])
                pr = PasswordReset.objects.get_or_create(user=u)[0]
                t = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
                if (t - pr.date_time).days < 1:
                    return render(request, 'timesheets/messagebox2.html', {'message': 'Sorry! cannot reset password more than once in a day'})
                pr.date_time = t
                pr.save()
                passwrd = str(uuid.uuid4().get_hex().upper()[0:6])
                u.set_password(passwrd)
                u.save()
                message = str("Your new password is: %s" % passwrd)
                send_mail("Password changed", message, EMAIL_HOST_USER, [u.email])
            except Exception as e:
                errors = True
            return render_to_response('timesheets/success_password_sent.html', {'errors': errors},)
    else:
        form = PasswordResetForm()

    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response('timesheets/password_reset.html', variables,)

def dashboard(request):
    user_in_group = Group.objects.get(name='employees').user_set.all()
    if request.user not in user_in_group:
        timesheet_list = Timesheet.objects.all().filter(approving_manager=request.user)
        paginator = Paginator(timesheet_list, 5)  # Show 5 objects per page
        page = request.GET.get('page')
        try:
            timesheets = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page
            timesheets = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999) deliver last page of results.
            timesheets = paginator.page(paginator.num_pages)
        return render(request, 'timesheets/dashboard.html',
                      {'timesheets': timesheets})
        #return render(request, 'timesheets/dashboard.html', '')
    else:
        #views existing timesheets of that employee
        queryset_list = Timesheet.objects.all().filter(employee=request.user)
        paginator = Paginator(queryset_list, 5) #Show 5 objects per page
        page_request_var = "page"
        page = request.GET.get(page_request_var)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            #If page is not an integer, deliver first page
            queryset = paginator.page(1)
        except EmptyPage:
            #If page is out of range (e.g. 9999) deliver last page of results.
            queryset =paginator.page(paginator.num_pages)
        context = {
            "object_list": queryset,
            "employee": "List",
            "page_request_var": page_request_var
        }
        return render(request, 'timesheets/dashboard.html', context)

def create_timesheet(request):
    # post method through the form
    if request.method == 'POST':
        form = CreateTimesheetForm(request.POST)
        if form.is_valid():
            try:
                timesheet = form.save(commit=False)
                #takes the user that is currently logged in
                timesheet.employee = request.user
                #takes the current time for the submission date
                timesheet.submission_date = timezone.now()
                timesheet.save()
                #inform user of the timesheet update
                return render(request, 'timesheets/messagebox.html',
                              {'message': 'Timesheet Created.'})
            except Exception as e:
                print(e) # print the error to Django console
                return render(request, 'timesheets/messagebox.html',
                              {'message': 'Error: Unable to create timesheet.'})
    else:
        form = CreateTimesheetForm()

    return render(request, 'timesheets/create_timesheet.html', {'form': form})

def timesheet_detail(request, id=None):

    instance = get_object_or_404(Timesheet, id=id)
    context = {
        "employee": "Detail",
        "instance": instance,
    }
    return render(request,"timesheets/timesheet_detail.html", context)

def timesheet_edit(request, id=None):
    instance = get_object_or_404(Timesheet, id=id)
    form = CreateTimesheetForm(request.POST, instance=instance)
    if form.is_valid():
        try:
            timesheet = form.save(commit=False)
            timesheet.employee = request.user
            timesheet.submission_date = timezone.now()
            timesheet.save()
            return render(request, 'timesheets/messagebox.html',
                          {'message': ' Timesheet Edited.'})
        except Exception as e:
            print(e)  # print the error to Django console
            return render(request, 'timesheets/messagebox.html',
                          {'message': 'Error: Unable to edit timesheet.'})
    context = {
        "employee": instance.employee,
        "instance": instance,
        "form": form,
    }
    return render(request,"timesheets/update_timesheet.html", context)

def timesheet_delete(request, id=None):
    instance = get_object_or_404(Timesheet, id=id)
    try:
        instance.delete()
        return render(request, 'timesheets/messagebox.html',
                          {'message': ' Timesheet Deleted.'})
    except Exception as e:
        return render(request, 'timesheets/messagebox.html',
                          {'message': ' Unable to delete timesheet.'})

def approve_timesheet(request):
    if request.method == 'POST':
        results = request.POST.dict()
        try:
            approved_timesheet_id = int(results.keys()[results.values().index(u'Approve')])
            manager = request.user
            timesheet = Timesheet.objects.get(pk=approved_timesheet_id)
            if manager.groups.filter(name="managers").exists():
                timesheet.approving_manager = manager
                timesheet.approval_date = timezone.now()
                timesheet.save()
        except Exception as e:
            print(e)  # Print the error to Django console
            return render(request, 'timesheets/messagebox.html',
                          {'message': 'Error: Unable to approve timesheet.'})

    return render(request, 'timesheets/approve_timesheet.html',
                  {'timesheets': Timesheet.objects.filter(approving_manager__isnull=True)})






