from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from .models import Settings, Connection
from .utils import *
from .mav_util import *
from background_task import background
import json

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
    print("hello")

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
        returned_df = read_file()
        # if request.POST.get('ocsvm') == 'on':
        #     output += "\n=======One-Class SVM=======\n"
        #     output += train_OneClassSVM()
        # if request.POST.get('autoencoder') == 'on':
        #     output += "\n========Autoencoder========\n"
        #     output += train_Autoencoder()
        # if request.POST.get('lof') == 'on':
        #     output += "\n=======Local Outlier Factor=======\n"
        #     output += train_LocalOutlierFactor()

    context = {
        'output': 'hello'
    }
    return render(request, 'gcsclient/training.html', context)

@login_required()
def reports(request):
    return render(request, 'gcsclient/reports.html')

def heartbeat(request):
    setting = Settings.objects.first()
    connection = Connection.objects.first()
    
    if not connection:
        connection = Connection()
        connection.save()

    json_req = json.loads(request.body)

    if json_req['established'] != connection.established:
        connection.established = json_req['established']
        connection.save()

    modules = ""
    modules += str(int(setting.dos_enabled))
    modules += str(int(setting.gps_enabled))
    modules += "000000"
    data = {'timestamp': time.time(), 'default_action': setting.default_action, 'default_initiate_time':setting.default_initiate_time, 'default_return_time':setting.default_return_time, 'modules_enabled':modules}
    return HttpResponse(json.dumps(data), content_type='application/json')

def state(request):
    connection = Connection.objects.first()
    print(connection.established)
    data = {'established': connection.established}

    return HttpResponse(json.dumps(data), content_type='application/json')