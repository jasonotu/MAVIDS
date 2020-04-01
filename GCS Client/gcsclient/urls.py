from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='gcsclient-login'),
    path('dashboard/', views.dashboard, name='gcsclient-dashboard'),
    path('settings/', views.settings, name='gcsclient-settings'),
    path('training/', views.training, name='gcsclient-training'),
    path('reports/', views.reports, name='gcsclient-reports'),
]