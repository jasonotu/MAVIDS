from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from .models import Settings

def login(request):
    msg = []
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')
            else:
                msg.append('You account has been deactivated!')
    else:
        msg.append('Invalid Login credentials, try again!')
    return render(request, 'login.html', {'errors': msg})

@login_required()
def dashboard(request):
    return render(request, 'gcsclient/dashboard.html')

@login_required()
def settings(request):
    return render(request, 'gcsclient/settings.html')

@login_required()
def training(request):
    return render(request, 'gcsclient/training.html')

@login_required()
def reports(request):
    return render(request, 'gcsclient/reports.html')
