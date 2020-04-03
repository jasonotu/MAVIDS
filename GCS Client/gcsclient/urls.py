from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='gcsclient-dashboard'),
    path('settings/', views.settings, name='gcsclient-settings'),
    path('training/', views.training, name='gcsclient-training'),
    path('reports/', views.reports, name='gcsclient-reports'),
]