from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm

def index(request):
#   template = loader.get_template('timesheets/index.html')
    if request.method == 'POST':
        form = UserForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'timesheets/dashboard.html', {'form': form})
        else:
            return redirect('index')
    else:
        form = UserForm()
        return render(request, 'timesheets/index.html', {'form' : form})
#    return HttpResponse(template.render('', request))

def userLogout(request):
    logout(request)
    return redirect('index')

def dashboard(request):
    return render(request, 'timesheets/dashboard.html', '')


# This function-based view handles the requests to the root URL /. See
# urls.py for the mapping.
def registration_form(request):
    # If the request method is POST, it means that the form has been submitted
    # and we need to validate it.
    if request.method == 'POST':
        # Create a RegistrationForm instance with the submitted data
        form = RegistrationForm(request.POST)
        # Returns True if it is valid and
        # False if it is invalid.
        if form.is_valid():
            # If form is valid
            # rendering a success template page.
            return render(request, "timesheets/success.html", '')

            # This means that the request is a GET request. So we need to
            # create an instance of the RegistrationForm class and render it in
            # the template
    else:
        form = RegistrationForm()

        # Render the registration form template with a RegistrationForm instance. If the
        # form was submitted and the data found to be invalid, the template will
        # be rendered with the entered data and error messages. Otherwise an empty
        # form will be rendered. Check the comments in the registration_form.html template
        # to understand how this is done.
    return render(request, "timesheets/registration_form.html", {'form': form})