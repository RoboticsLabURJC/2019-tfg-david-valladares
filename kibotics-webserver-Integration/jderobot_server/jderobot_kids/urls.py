# -*- coding: utf-8 -*-

from django.conf.urls import *
from jderobot_kids import views

from django.contrib import admin
from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = [
    ### PORTADA DE LA APLICACIÓN Y PÁGINA PRINCIPAL ###
    url(r'^$', views.index),  # Página Principal de la Aplicación
    url(r'^main_page', views.main_page, name='main'),  # Main page. List of practices

    ### PÁGINAS DE LOS CURSOS ###
    url(r'^courses', views.courses_page),  # Main Courses Page. List of Courses.
    url(r'^course/(?P<course_id>[\w\-]+)/', views.course_description),  # Simulation

    ### LOGIN, LOGOUT Y REGISTRO EN LA APP ###
    url(r'^login', views.login),  # Login en la Aplicación
    url(r'^logout/?(?P<inactivity>\w+|)', views.logout),  # Logout de la Aplicación
    url(r'^registration', views.registration),  # Logout de la Aplicación
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate,
        name="activate"),

    # APP ADMINISTRATION #
    url(r'^apache_log', views.apache_log),  # Apache log
    url(r'^visits/(?P<from_date>[0-9]+)/(?P<to_date>[0-9]+)', views.visits_analytics), #Visor de estadísticas de Visitantes
    # url(r'^users', views.users), # Vista con el listado de todos los usuarios de la App
    url(r'^update_exercises', views.update_exercises),  # Actualiza la lista de ejercicios
    url(r'^reboot_app', views.reboot_app),  # Recarga la lista de simulaciones
    url(r'^kill_simulation/(?P<container_id>[0-9A-Za-z_\-]+)', views.stop_simulation),
    url(r'^kill_user_simulations', views.kill_user_simulations),
    url(r'^terms', views.terms),

    ### SIMULACIÓN EJERCICIO ###
    url(r'^simutest/(?P<exercise_id>[\w\-]+)$', views.simutest),  # Simulation
    url(r'^montaje_pibot/(?P<exercise_id>[\w\-]+)', views.montaje_pibot),  # Devuelve la guía de montaje del pibot.
    url(r'^websim/js/(?P<exercise_id>[\w\-]+)', views.websim_js),
    # Vista para que usuarios sin registrase puedan probar la Aplicación
    url(r'^websim-scratch/(?P<simulation_type>[\w\-]+)/(?P<exercise_id>[\w\-]+)', views.websim_blockly),
    # Vista para que usuarios sin registrase puedan probar la Aplicación
    url(r'^websim-ace/(?P<simulation_type>[\w\-]+)/(?P<exercise_id>[\w\-]+)', views.websim_python),
    url(r'^exit_simulation', views.exit_simulation),  # Vista de transición al salir de una simulación
    url(r'^save_user_code', views.save_user_code),  # Método para guardar el código de un ejercicio en GitHub
    url(r'^get_python_to_arduino_code', views.get_python_to_arduino_code),
    url(r'^get_python_to_javascript_code', views.get_python_to_javascript_code),
    url(r'^get_robot_code', views.get_robot_code),

    ### PÁGINAS DE DOCENCIAS ###
    # url(r'^students', views.students), # Web con información para el profesor

    ### RECUPERACIÓN CONTRASEÑA ###
    url(r'^password_reset/$', auth_views.password_reset, {'template_name': 'reset_password/password_reset_form.html'},
        name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done,
        {'template_name': 'reset_password/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {'template_name': 'reset_password/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        {'template_name': 'reset_password/password_reset_complete.html'}, name='password_reset_complete'),

    ### TESTING ###
    url(r'^testing', views.testing),  # Actualiza la lista de ejercicios

    url(r'^PRUEBAS', views.pruebas),  # Vista para pruebas

 
]
