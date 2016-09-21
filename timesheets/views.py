from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext


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
            # creating user object
            user = User.objects.create_user(
                first_name=form.cleaned_data['name'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('success')
    else:
        form = RegistrationForm()

    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response('timesheets/registration_form.html', variables, )


def success(request):
    return render(request, 'timesheets/success.html', '')