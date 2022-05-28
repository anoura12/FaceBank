from unicodedata import name
from django.urls import include, re_path, path
from pip import main

from . import views

app_name = 'main'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    path('face_capture/', views.face_capture, name='face_capture'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('money_transfer/', views.money_transfer, name='money_transfer'),
    path('face_verify/', views.face_verify, name='face_verify'),
    
]
 