# matcher/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ajax/process/', views.ajax_process, name='ajax_process'),
]
