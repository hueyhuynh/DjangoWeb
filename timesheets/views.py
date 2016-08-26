from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import UserForm
from django.contrib.auth import authenticate, login

def index(request):
#   template = loader.get_template('timesheets/index.html')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = UserForm()
        return render(request, 'timesheets/index.html', {'form' : form})
#    return HttpResponse(template.render('', request))

def logout(request):
    logout(request)
    return redirect('index')