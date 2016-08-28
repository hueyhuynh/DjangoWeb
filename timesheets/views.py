from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout

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