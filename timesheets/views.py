from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, PasswordResetForm, TimesheetForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.mail import send_mail
from models import *
from datetime import datetime
from django.utils import timezone

import uuid

from sep.settings import EMAIL_HOST_USER


def index(request):
    #   template = loader.get_template('timesheets/index.html')
    form = UserForm()
    errors = False
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            errors = True
            return render(request, 'timesheets/index.html', {'form': form, "errors": errors})
    else:
        return render(request, 'timesheets/index.html', {'form': form, "errors": errors})


# return HttpResponse(template.render('', request))

def userLogout(request):
    logout(request)
    return redirect('index')


def dashboard(request):
    if request.user.is_active:
        return render(request, 'timesheets/dashboard.html', '')
    else:
        return redirect('registration_form')


# This function-based view handles the requests to the root URL /. See
# urls.py for the mapping.
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
                message = str("Your username is: %s\n" % form.cleaned_data['username'])
                message += str("Your password is: %s" % password)
                send_mail("User registration completed", message, EMAIL_HOST_USER, [form.cleaned_data['email']])
                return render(request, 'timesheets/messagebox.html',
                              {'message': 'An autogenerated password has been sent to your email address.'})
            except Exception as e:
                return render(request, 'timesheets/messagebox.html',
                              {'message': 'Error: Unable to send mail. Please cross check your email.'})
    else:
        form = RegistrationForm()

    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response('timesheets/registration_form.html', variables, )

def new_timesheets(request):
    if request.method == 'POST':
        form = TimesheetForm(request.POST)


    else:
        return render(request, 'timesheets/messagebox.html',
                              {'message': 'Fail.'})

def success(request):
    return render(request, 'timesheets/success.html', '')


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
                if (t - pr.date_time).days > 5:
                    return render(request, 'timesheets/messagebox.html', {'message': 'Sorry! cannot reset password more than once in a day'})
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