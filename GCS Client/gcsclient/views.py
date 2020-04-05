from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import Settings

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')
    return render(request, 'login.html')

@login_required()
def dashboard(request):
    return render(request, 'gcsclient/dashboard.html')

@login_required()
def settings(request):
    setting = Settings.objects.first()
    context = {
        'setting': setting
    }

    if request.method == 'POST':
        if request.POST.get('check_dos', '') == 'on':
            setting.dos_enabled = True
        else:
            setting.dos_enabled = False
        if request.POST.get('check_gps', '') == 'on':
            setting.gps_enabled = True
        else:
            setting.gps_enabled = False

        setting.default_action = request.POST.get('default_action')
        setting.default_initiate_time = request.POST.get('default_initiate_time')
        setting.default_return_time = request.POST.get('default_return_time')
        setting.connection_method = request.POST.get('connection_method')
        setting.save()

    return render(request, 'gcsclient/settings.html', context)

@login_required()
def training(request):
    return render(request, 'gcsclient/training.html')

@login_required()
def reports(request):
    return render(request, 'gcsclient/reports.html')
