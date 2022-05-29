from unicodedata import name
from django.urls import include, re_path, path
from pip import main

from . import views
from django.contrib.auth import views as Views



app_name = 'main'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    path('face_capture/', views.face_capture, name='face_capture'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('money_transfer/', views.money_transfer, name='money_transfer'),
    path('face_verify/', views.face_verify, name='face_verify'),
    path('create_bank_account/', views.create_bank_account, name='create_bank_account'),
    path('bank_account_details/', views.bank_account_details, name='bank_account_details'),
]
 