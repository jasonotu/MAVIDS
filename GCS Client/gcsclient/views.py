from django.shortcuts import render

def login(request):
    return render(request, 'gcsclient/login.html')

def dashboard(request):
    return render(request, 'gcsclient/dashboard.html')

def settings(request):
    return render(request, 'gcsclient/settings.html')

def training(request):
    return render(request, 'gcsclient/training.html')

def reports(request):
    return render(request, 'gcsclient/reports.html')
