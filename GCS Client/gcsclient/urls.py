from django.urls import path, include
from . import views
import subprocess

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='gcsclient-dashboard'),
    path('settings/', views.settings, name='gcsclient-settings'),
    path('training/', views.training, name='gcsclient-training'),
    path('reports/', views.reports, name='gcsclient-reports'),
    path('heartbeat/', views.heartbeat, name='gcsclient-heartbeat'),
    path('state', views.state, name='gcsclient-state')
]

subprocess.Popen(['python','gcsclient/subscript.py'])