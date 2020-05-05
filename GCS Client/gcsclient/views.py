from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import Settings
from .utils import train_OneClassSVM, train_LocalOutlierFactor, train_Autoencoder
from .mav_util import *
from background_task import background

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')
    return render(request, 'login.html')

@login_required()
def dashboard(request):
    listen_link(repeat=1, repeat_until=None)

    return render(request, 'gcsclient/dashboard.html')

@login_required()
def settings(request):
    setting = Settings.objects.first()
    context = {
        'setting': setting
    }

    if request.method == 'POST':
        if request.POST.get('check_dos') == 'on':
            setting.dos_enabled = True
        else:
            setting.dos_enabled = False
        if request.POST.get('check_gps') == 'on':
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
    output = ''
    if request.method == 'POST':
        if request.POST.get('ocsvm') == 'on':
            output += "\n=======One-Class SVM=======\n"
            output += train_OneClassSVM()
        if request.POST.get('autoencoder') == 'on':
            output += "\n========Autoencoder========\n"
            output += train_Autoencoder()
        if request.POST.get('lof') == 'on':
            output += "\n=======Local Outlier Factor=======\n"
            output += train_LocalOutlierFactor()

    context = {
        'output': output
    }
    return render(request, 'gcsclient/training.html', context)

@login_required()
def reports(request):
    return render(request, 'gcsclient/reports.html')
