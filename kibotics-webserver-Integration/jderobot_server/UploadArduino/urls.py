# -*- coding: utf-8 -*-

from django.conf.urls import *
from jderobot_kids import views
from UploadArduino import views as views_upArduino

from django.contrib import admin
from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = [
    ### Pagina Carga de Arduino ###
    url(r'', views_upArduino.upApp),

 
]
