# -*- coding: utf-8 -*-

import sys
sys.path.append('/home/.local/lib/python3.6/site-packages')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .decorators import user_have_exercise
from django.conf import settings
from .models import Host, Simulation
from .documents import SessionDocument, SimulationDocument, ErrorDocument, VisitDocument
import os
import time
import subprocess
import shutil
import json
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse, HttpResponseForbidden, FileResponse, JsonResponse
from django.utils.encoding import force_bytes, force_text
from .simulations import get_client_ip, kill_simulation, save_simulation_code
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime  # , timezone #uncomment for python3.x
import re
from django.db.models import F, Q
import jderobot_kids.file_utils as fu
from .forms import *
from .utils import ColorPrint, UTC
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from django.views.decorators.cache import never_cache
from user_agents import parse
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
from io import BytesIO
import base64
from mpl_toolkits.basemap import Basemap
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch
from geoip import geolite2



# mBot PyOnArduino real
from sys import path
import ast
from subprocess import call
import zipfile
from mimetypes import guess_type

# PyGithub for Github Repositories
from github import GithubException

# PyGithub for Discourse (Forum) REST API
from pydiscourse import client
from pydiscourse.exceptions import DiscourseError

# Cargamos el modelo extendido de Usuarios en lugar del modelo por defecto de Django
User = get_user_model()

# Cada vez que lanzamos de nuevo el servidor limpiamos la base de datos de simulaciones y
Simulation.objects.all().delete()


# ==============================================================================
# ================================== INDEX =====================================
# ==============================================================================

def index(request):
    """ Página comercial de la Aplicación """
    if not settings.DEBUG:
        user_agent = parse(request.META['HTTP_USER_AGENT'])
        VisitDocument(
            date=datetime.now(),
            client_ip=get_client_ip(request),
            browser = user_agent.browser.family + " " + user_agent.browser.version_string,
            os = user_agent.os.family + " " + user_agent.os.version_string,
            device = user_agent.device.family
        ).save()

    context = {
        "authenticate": False
    }
    return render(request, 'jderobot_kids/index.html', context)


# ==============================================================================
# ============================== MAIN PAGE =====================================
# ==============================================================================

@login_required()
@never_cache
def main_page(request, extendedContext={}):
    """ Página principal de la Aplicación """

    # random_pack = Exercise.objects.get(pk=1).get_random_pack() # to get random courses or packs

    if request.user.is_authenticated():
        user = User.objects.get(username=request.user.username)
        # Get User's Permissions over Exercises
        user_exercises_permissions = CodePermissions.objects.filter(user=user)
        user_exercises_permissions_dict = {}  # User's Permissions over Exercises, Sorted by Tag
        user_presentation_permissions = []  # User's Only Presentation Permissions
        user_unlabeled_exercises = []  # User's Permissions over Exercises with no Tag
        user_exercises_type = {}

        for ex in user_exercises_permissions:
            if ex.p:
                if ex.r or ex.w or ex.x:
                    if ex.exercise.type == 'challenge':
                        exercise_type = 'Reto'
                    elif ex.exercise.type == 'shared_game':
                        exercise_type = 'Juego compartido'
                    elif ex.exercise.type == 'webIDE':
                        exercise_type = 'Web IDE'
                    else:
                        exercise_type = 'Otros'

                    if exercise_type not in user_exercises_type:
                        user_exercises_type[exercise_type] = []

                    user_exercises_type[exercise_type].append(ex)

        for p in user_exercises_permissions:
            if p.p:
                if p.r or p.w or p.x:
                    # sort exercises with access permission
                    if p.exercise.tags.all():
                        # sort exercises with their tag as category
                        for tag in p.exercise.tags.all():
                            if not tag.name in user_exercises_permissions_dict:
                                user_exercises_permissions_dict[tag.name] = []
                            user_exercises_permissions_dict[tag.name].append(p)
                    else:
                        # group untagged exercises within the category "Tus Ejercicios"
                        user_unlabeled_exercises.append(p)
                else:
                    # grouping only-presentation permissions
                    user_presentation_permissions.append(p)

        # Sort Modules (Packs) and Individual Exercises
        user_exercises_permissions_set = []
        for k, v in user_exercises_permissions_dict.items():
            user_exercises_permissions_set.append((k, v))  # Copy items into List to make thme sortable

        if (user_unlabeled_exercises):
            user_exercises_permissions_set.append(
                ("Tus Ejercicios", user_unlabeled_exercises))  # At the end of the List
        context = {
            "authenticate": True,
            "user": user,
            "user_exercises_permissions": user_exercises_permissions_set,
            "user_presentation_permissions": user_presentation_permissions,
            "user_exercises_type": user_exercises_type,
            "latest_release_version": settings.WEBSERVER_REPOSITORY.get_latest_release().tag_name
        }
        context.update(extendedContext)
        if (user.subscription_expiration <= datetime.now(UTC())):  # datetime.now(timezone.utc) -> python 3.x
            context["message"] = "Tu subscripción ha caducado [" + str(
                datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + "]. "
            context["expired"] = True
        return render(request, 'jderobot_kids/main_page.html', context)
    else:
        context = {
            "authenticate": False
        }
        return render(request, 'jderobot_kids/login.html', context)


# ==============================================================================
# ============================ COURSES PAGES ===================================
# ==============================================================================

@never_cache
def courses_page(request):
    """ Página Principal de Cursos de la Aplicación """
    context = {}
    return render(request, 'jderobot_kids/courses_page.html', context)


def course_description(request, course_id):
    """ Vista Individual de Descripción de un Curso """
    context = {}
    return render(request, 'jderobot_kids/course.html', context)


# ==============================================================================
# ============================= USERS LOGIN ====================================
# ==============================================================================

def login(request):
    """ Página de Inicio de sesión """
    if not request.user.is_authenticated():
        if request.POST:
            form = request.POST
            username = form.get("username")
            password = form.get("password")
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    if not settings.DEBUG:
                        user_agent = parse(request.META['HTTP_USER_AGENT'])
                        SessionDocument(
                            username = username,
                            start_date = datetime.now(),
                            end_date = datetime.now(),
                            duration = 0,
                            client_ip = get_client_ip(request),
                            browser = user_agent.browser.family + " " + user_agent.browser.version_string,
                            os = user_agent.os.family + " " + user_agent.os.version_string,
                            device = user_agent.device.family
                        ).save()
                    return redirect('/main_page')
                else:
                    context = {
                        "error": True,
                        "message": "La cuenta está desactivada",
                        "authenticate": False,
                    }
                    return render(request, 'jderobot_kids/main_page.html', context)
            else:
                context = {
                    "error": True,
                    "message": "Nombre de Usuario o Contraseña incorrectos",
                    "authenticate": False,
                }
                return render(request, 'jderobot_kids/main_page.html', context)

        elif request.GET:
            context = {
                "authenticate": False,
            }
            return render(request, 'jderobot_kids/main_page.html', context)
        else:
            context = {
                "authenticate": False,
            }
            return render(request, 'jderobot_kids/main_page.html', context)
    else:
        return redirect('/main_page')


# ==============================================================================
# ============================ LOGOUT USUARIOS =================================
# ==============================================================================

def logout(request, inactivity):
    """ Pagina de Logout de la aplicación para que los usuarios puedan cerar sesión """

    if request.user.is_authenticated():
        username = request.user.username
        auth.logout(request)
        if not settings.DEBUG:
            # Busqueda de la ultima sesion abierta para cierto usuario
            latestSession = Search(index="kibotics_session_log*") \
                        .query("match", username=username) \
                        .query('match', duration=0) \
                        .sort({"start_date": {'order':'desc'}})[0]

            # Update de la query anterior con la fecha de salida y la duracion de la sesion
            for hit in latestSession:
                duration = datetime.now() - datetime.strptime(hit.start_date, "%Y-%m-%dT%H:%M:%S.%f")
                Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts']).update(index='kibotics_session_log', id=hit.meta.id, \
                        body={"doc":
                                {'end_date':datetime.now(),
                                'duration':duration.total_seconds()
                                }
                             })

        if inactivity == 'inactivity':
            msg = "¡Sesión cerrada por inactividad!"
            idle = True
            success = False
        else:
            msg = "¡Sesión cerrada correctamente!"
            success = True
            idle = False
        context = {
            "success": success,
            "inactivity": idle,
            "message": msg,
            "authenticate": False,
        }
    else:
        context = {
            "authenticate": False,
        }
    return render(request, 'jderobot_kids/main_page.html', context)


# ==============================================================================
# ========================== REGISTRO DE USUARIOS ==============================
# ==============================================================================


def registration(request):
    """ Permite a los usuarios registrarse en la aplicación """

    if request.method == "GET":
        form = UserForm()
        return render(request, 'jderobot_kids/registration.html', {'form': form})
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            user.is_active = False

            code = form.cleaned_data['code']
            if code:
                user.code.add(Code.objects.get(code=code))
                if not Code.objects.get(code=code).promotional:
                    expiration_datetime = datetime.combine(Code.objects.get(code=code).expires, datetime.now().time())
                else:
                    expiration_datetime = datetime.now() + relativedelta(months=+2) # two month from now
                user.subscription_expiration = expiration_datetime
            user.save()

            current_site = get_current_site(request)
            site_name = request.get_host()
            mail_subject = 'Activa tu cuenta de %(site)s!' % {'site': site_name},

            message = render_to_string('confirmation_email/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            # Registro en Foro de Kibotics
            uname = user.username
            c = client.DiscourseClient(
                'https://foro.kibotics.org',
                api_username='cawadall',
                api_key='5729edade80cc5531e65ceec69fa9841d2b2844b029d7ff00ba166c9c6146d7a')
            try:
                user = c.create_user(user.get_full_name(), uname.encode("ascii", "ignore"), user.email,
                                     request.POST['password1'])
            except DiscourseError as e:
                try:
                    print(
                        "[FORO] Fallo al registrar al usuario {} en https://foro.kibotics.org . Motivo: {}".format(
                            uname, e))
                except Exception as e:
                    print(
                        "[FORO] Fallo al registrar al usuario {} en https://foro.kibotics.org . Es posible que el usuario ya esté registrado o pendiente de activación.".format(
                            uname))
                    print(e)
                user = {}
                user['success'] = False
                # return redirect('/main_page')

            success = user['success']
            if success:
                print("[FORO] Usuario {} registrado con éxito en https://foro.kibotics.org".format(uname))
                msg = "Debes recibir un correo electrónico de verificación de Kibotics y otro de verificación para el acceso al foro. Por favor, confirma ambas cuentas de correo electrónico antes de completar el registro. Si no ves alguno de los correos de confirmación, recuerda buscar en tu bandeja de 'Correo no deseado'."
            else:
                msg = "Debes recibir un correo electrónico de verificación de Kibotics. Por favor, confirma tu cuenta de correo electrónico antes de completar el registro. Recuerda registrate también en el foro foro.kibotics.org."

            context = {
                "success": True,
                "message": msg,
                "authenticate": False,
            }

            return render(request, 'jderobot_kids/main_page.html', context)

        else:
            context = {
                "error": True,
                "message": "Error en el formulario: " + str(form.errors) + "Por favor, intentelo de nuevo.",
                "form_errors": json.loads(form.errors.as_json()),
                "authenticate": False
            }
            return render(request, 'jderobot_kids/registration.html', context)


# ==============================================================================
# ========================== ACTIVACIÓN DE CUENTA ==============================
# ==============================================================================

def activate(request, uidb64, token):
    """ Vista que permite la activación de la cuenta de usuario """

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        group = None
        if user.code.exists():
            packs = user.code.all()[0].packs.all()
            group = user.code.all()[0].group

        else:
            packs = Code.objects.get(code="__null__").packs.all()

        if group:
            user.group.add(group)  # Assigns User to Group (tag).

        # Create CodePermissions Entries for both Exercises and Packs of the User
        assigned_exercises = user.code.all()[0].exercises.all()
        for t in user.code.all()[0].packs.all():
            assigned_exercises = assigned_exercises | Exercise.objects.filter(tags=t)

        user.save()
        for ex in assigned_exercises:
            if CodePermissions.objects.filter(user=user, exercise=ex).exists():
                duplicated = CodePermissions.objects.filter(user=user, exercise=ex)[0]
                duplicated.delete()
            permission = CodePermissions.objects.create(
                user=user,
                exercise=ex,
                p=True,
                r=True,
                w=True,
                x=True
            )

        os.makedirs("users/" + user.username)
        try:
            user_directory_path = "/users/" + user.username + "/" + ".gitignore"
            settings.REPOSITORY.create_file(user_directory_path, "(New User): " + user.username, "")
        except Exception as e:
            print(e)
            print(
                "El archivo que se ha intentado crear en github ya existe. Para crear un nuevo archivo con ese nombre, por favor, borre primero ese archivo o actualicelo")
        context = {
            "success": True,
            "message": "Gracias por la confirmación de tu cuenta de correo electrónico, ¡Ahora ya puedes iniciar sesión!",
            "authenticate": False,
        }

        return render(request, 'jderobot_kids/main_page.html', context)
    else:

        context = {
            "success": False,
            "message": "¡El link de activación no es válido!",
            "authenticate": False,
        }
        return render(request, 'jderobot_kids/main_page.html', context)


@staff_member_required
def apache_log(request):
    log_file_path = "/var/log/apache2/error.log"

    try:
        with open(log_file_path, 'r') as file:
            ap_log_exists = True
            apache_logs = file.readlines()
            file.close()
        # Shows the last 200 lines from error.log file.
        apache_logs = apache_logs[:200]
    except:
        ap_log_exists = False
        apache_logs = "No such Apache log file"

    context = {
        "authenticate": True,
        "ap_log_exists": ap_log_exists,
        "apache_logs": apache_logs,
        "latest_release_version": settings.WEBSERVER_REPOSITORY.get_latest_release().tag_name
    }

    return render(request, 'jderobot_kids/apache_log.html', context)


@staff_member_required
def update_exercises(request):
    ''' Publica un nuevo ejercicio que proviene del repositorio "exercises" '''

    subprocess.call("scripts/publicacion_nuevo_ejercicio.sh", shell=True)

    context = {
        "authenticate": True,
    }
    return render(request, 'jderobot_kids/index.html', context)


@never_cache
def websim_blockly(request, simulation_type, exercise_id):
    ''' Main site of simulation with Websim and Scratch '''
    exercise = get_object_or_404(Exercise, exercise_id=exercise_id)
    assets = json.loads(exercise.assets)
    client_ip = get_client_ip(request)
    main_server = Host.objects.get(main_server=True)

    if request.user.is_authenticated():
        user = User.objects.get(username=request.user.username)
        exercise_permissions = CodePermissions.objects.get(user=user, exercise=exercise)
        username = user.username
        try:
            user_code = user.gh_pull_file(exercise, assets['notebook'])
        except GithubException as e:
            print(e)
            if e.status == 404:
                print(
                    "\033[93m No existen archivos de la practica " + exercise_id + " del usuario " + user.username + " en el repositorio. Copiando archivos por defecto." + "\033[0m")
                file = open(exercise.exercise_file_location(), "r")
                user_code = file.read()
                file.close()
    else:
        print(
            "\033[93m Simulacion en Websim con usuario no registrado. Cargando plantilla de codigo por defecto " + exercise.exercise_file_location() + "\033[0m")
        user = None
        username = 'AnonymusUser'
        exercise_permissions = CodePermissions(User.objects.none(), exercise, p=True, r=True, w=True, x=True)
        file = open(exercise.exercise_file_location(), "r")
        user_code = file.read()
        file.close()

    # Crear entrada de simulación en la BBDD
    simulation = Simulation.objects.create(
        user=username,
        init_simulation=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        simulation_type=simulation_type,
        exercise=exercise.exercise_id,
        client_ip=client_ip,
    )

    # WebSockets Simulation connection (Keep Alive)
    if settings.DEBUG:
        ws_url = 'ws://' + '127.0.0.1' + ':8000'
    else:
        ws_url = 'wss://' + main_server.host + "/_ws_/"

    context = {
        "username": username,
        "simulation_site": True,
        "simulation_type": simulation_type,
        "authenticate": True,
        "exercise": exercise,
        "exercise_permissions": exercise_permissions,
        "simulation": simulation,
        "client_ip": client_ip,
        "ws_url": ws_url
    }

    if simulation_type == "websim":

        # Simulación en WebSim con Scratch
        context["world"] = "assets/websim-config/" + assets["world"]
        # Código del evaluador del ejercicio

        if exercise.evaluator:
            exercise.evaluator = json.loads(exercise.evaluator)
            context["evaluator"] = exercise.evaluator["code"]
            if "icon" in exercise.evaluator:
                if len(exercise.evaluator["icon"]) > 1:
                    context["evaluator_icon2"] = exercise.evaluator["icon"][1]
                context["evaluator_icon1"] = exercise.evaluator["icon"][0]

        if exercise.observations and "Synchronous" in json.loads(exercise.observations):
            context["synchronous"] = True
        else:
            context["synchronous"] = False

        # Configuración para ejercicios competitivos en WebSim con Scratch
        if exercise.observations and json.loads(exercise.observations)["Competitive"] and not context["synchronous"]:
            context["competitive"] = True
            context["userCode1"] = user_code
            # Código de DonPerfecto
            dnprfct = User.objects.get(username="donperfecto")
            try:
                challenger_code = dnprfct.gh_pull_file(exercise, assets['notebook'])
            except GithubException as e:
                print(e)
                if e.status == 404:
                    print(
                        "\033[93m No existen archivos de la practica " + exercise_id + " del usuario " + dnprfct.username + " en el repositorio. Copiando archivos por defecto." + "\033[0m")
                    file = open(exercise.exercise_file_location(), "r")
                    challenger_code = file.read()
                    file.close()
            context["userCode2"] = challenger_code
        elif exercise.observations and json.loads(exercise.observations)["Competitive"] and context["synchronous"]:
            context["competitive"] = True
            context["userCode1"] = user_code
        else:
            context["user_code"] = user_code

    elif simulation_type == "real":
        if "guide" in assets:
            context["guide"] = assets["guide"]
        # Real robots in Scratch
        context["user_code"] = user_code
        user.prepare_directory(exercise)
    else:
        return render(request, 'jderobot_kids/error_page/404_error.html', {}, status=404)

    if not settings.DEBUG:

        user_agent = parse(request.META['HTTP_USER_AGENT'])
        SimulationDocument(
            username = username,
            start_date = datetime.now(),
            end_date = datetime.now(),
            duration = 0,
            client_ip = get_client_ip(request),
            simulation_type = simulation_type,
            exercise_id = exercise_id,
            browser = user_agent.browser.family + " " + user_agent.browser.version_string,
            os = user_agent.os.family + " " + user_agent.os.version_string,
            device = user_agent.device.family
        ).save()

    context["latest_release_version"] = settings.WEBSERVER_REPOSITORY.get_latest_release().tag_name
    return render(request, 'jderobot_kids/websim_scratch.html', context)


def websim_python(request, simulation_type, exercise_id):
    ''' Main site of simulation with WebSim and Python '''
    exercise = get_object_or_404(Exercise, exercise_id=exercise_id)
    assets = json.loads(exercise.assets)
    client_ip = get_client_ip(request)
    main_server = Host.objects.get(main_server=True)

    if request.user.is_authenticated():
        user = User.objects.get(username=request.user.username)
        exercise_permissions = CodePermissions.objects.get(user=user, exercise=exercise)
        username = user.username
        assets = json.loads(exercise.assets)
        try:
            user_code = user.gh_pull_file(exercise, assets['notebook'])
        except GithubException as e:
            print(e)
            if e.status == 404:
                print(
                    "\033[93m No existen archivos de la practica " + exercise_id + " del usuario " + user.username + " en el repositorio. Copiando archivos por defecto." + "\033[0m")
                file = open(exercise.exercise_file_location(), "r")
                user_code = file.read()
                file.close()
    else:
        print(
            "\033[93m Simulacion en Websim con usuario no registrado. Cargando plantilla de codigo por defecto " + exercise.exercise_file_location() + "\033[0m")
        user = None
        username = 'AnonymusUser'
        exercise_permissions = CodePermissions(User.objects.none(), exercise, p=True, r=True, w=True, x=True)
        file = open(exercise.exercise_file_location(), "r")
        user_code = file.read()
        file.close()

    simulation = Simulation.objects.create(
        user=username,
        init_simulation=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        simulation_type=simulation_type,
        exercise=exercise.exercise_id,
        client_ip=client_ip,
    )

    if settings.DEBUG:
        ws_url = 'ws://' + '127.0.0.1' + ':8000'
    else:
        ws_url = 'wss://' + main_server.host + "/_ws_/"

    context = {
        "simulation_site": True,
        "simulation_type": simulation_type,
        "authenticate": True,
        "exercise": exercise,
        "exercise_permissions": exercise_permissions,
        "simulation": simulation,
        "client_ip": client_ip,
        "user_code": user_code,
        "ws_url": ws_url,
        "exercise_id": exercise.exercise_id,
        "latest_release_version": settings.WEBSERVER_REPOSITORY.get_latest_release().tag_name
    }

    if user:
        user.prepare_directory(exercise)
    if simulation_type == "websim":
        # Simulación en WebSim con Python
        context["world"] = "assets/websim-config/" + assets["world"]
        # context[world"] = exercise.language.lower() + "/" + exercise.exercise_id + "/" + assets["world"]

        if exercise.evaluator:
            exercise.evaluator = json.loads(exercise.evaluator)
            context["evaluator"] = exercise.evaluator["code"]
            if "icon" in exercise.evaluator:
                if len(exercise.evaluator["icon"]) > 1:
                    context["evaluator_icon2"] = exercise.evaluator["icon"][1]
                context["evaluator_icon1"] = exercise.evaluator["icon"][0]

        if exercise.observations and "Synchronous" in json.loads(exercise.observations):
            context["synchronous"] = True
        else:
            context["synchronous"] = False

        # Configuración para ejercicios competitivos en WebSim con Scratch
        if exercise.observations and json.loads(exercise.observations)["Competitive"] and not context["synchronous"]:
            context["competitive"] = True
            context["userCode1"] = user_code
            # Código de DonPerfecto
            dnprfct = User.objects.get(username="donperfecto")
            try:
                challenger_code = dnprfct.gh_pull_file(exercise, assets['notebook'])
            except GithubException as e:
                print(e)
                if e.status == 404:
                    print(
                        "\033[93m No existen archivos de la practica " + exercise_id + " del usuario " + dnprfct.username + " en el repositorio. Copiando archivos por defecto." + "\033[0m")
                    file = open(exercise.exercise_file_location(), "r")
                    challenger_code = file.read()
                    file.close()
            context["userCode2"] = challenger_code
        elif exercise.observations and json.loads(exercise.observations)["Competitive"] and context["synchronous"]:
            context["competitive"] = True
            context["userCode1"] = user_code
        else:
            context["user_code"] = user_code
    elif simulation_type == "real":
        print(assets)
        if "guide" in assets:
            context["guide"] = assets["guide"]
        # Robots Reales en Python (ACE)
    else:
        return render(request, 'jderobot_kids/error_page/404_error.html', {}, status=404)

    if not settings.DEBUG:
        user_agent = parse(request.META['HTTP_USER_AGENT'])
        SimulationDocument(
            username = username,
            start_date = datetime.now(),
            end_date = datetime.now(),
            duration = 0,
            client_ip = get_client_ip(request),
            simulation_type = simulation_type,
            exercise_id = exercise_id,
            browser = user_agent.browser.family + " " + user_agent.browser.version_string,
            os = user_agent.os.family + " " + user_agent.os.version_string,
            device = user_agent.device.family
        ).save()

    return render(request, 'jderobot_kids/websim_ace.html', context)


def websim_js(request, exercise_id):
    context = {

        "exercise": exercise_id

    }
    return render(request, 'jderobot_kids/websim_js.html', context)


# ==============================================================================
# ============================ SIMULATION UTILS ================================
# ==============================================================================

@login_required()
def save_user_code(request):
    """ Manager de peticiones de guardado de código de cualquier tipo """
    if request.method == "POST":
        success = False
        json_data = json.loads(request.body)
        if 'simulation_code' in json_data:
            code = json_data['simulation_code']
            running_simulation = Simulation.objects.filter(user=request.user.username)
            if len(running_simulation) > 1:
                pass
            else:
                simulation = running_simulation[0]
                simulation_type = running_simulation[0].simulation_type
                user = User.objects.get(username=request.user.username)
                exercise = Exercise.objects.get(exercise_id=simulation.exercise)
                if simulation_type != "simulator":
                    # Create XML or PY files
                    exercise_dir = user.local_user_exercise_location(exercise)
                    with open(exercise_dir + json.loads(exercise.assets)["notebook"], "w") as code_file:
                        code_file.write(code)
                try:
                    # Upload the code file to GitHub
                    save_simulation_code(running_simulation[0])
                    print("Simulation code uploaded to GitHub")
                    success = True
                except Exception as e:
                    print("[ERROR] Couldn't save simulation code. Exception: [{}]".format(e))

        data = {
            'success': success,
        }
        return JsonResponse(data)
    else:
        return render(request, 'jderobot_kids/error_page/404_error.html', {}, status=404)


@login_required()
def kill_user_simulations(request):
    """ Vista para que el usuario pueda eliminar todas las simulaciones asociados a él """

    running_simulations = Simulation.objects.filter(user=request.user.username)

    for simulation in running_simulations:
        kill_simulation(simulation, request)

    context = {
        "success": True,
        "message": "Todas las simulaciones fueron finalizadas con éxito.",
    }
    return main_page(request, context)


@staff_member_required()
def stop_simulation(request, container_id):
    return redirect("/config")


@login_required()
def exit_simulation(request):
    tic = time.time()
    user = User.objects.get(username=request.user.username)

    if not settings.DEBUG:
        while True:
            user_simulations = Simulation.objects.filter(~Q(simulation_type='websim'), user=user.username)
            n_user_simulations = len(user_simulations)
            if n_user_simulations == 0 or (time.time() - tic) > 15.0:
                break
            time.sleep(1)
    else:
        running_simulations = Simulation.objects.filter(user=request.user.username)
        for simulation in running_simulations:
            simulation.delete()

    return redirect("/main_page")


# ==============================================================================
# ============================= MONTAJE PIBOT ==================================
# ==============================================================================

@login_required()
def montaje_pibot(request, exercise_id):
    exercises_location = settings.EXERCISES_DIR + "/" + "pibot/" + exercise_id + "/templates/"

    context = {
        "authenticate": True,
        "tutorial": True,
    }
    return render(request, exercises_location + exercise_id + '.html', context)


# ==============================================================================
# =============================== STUDENTS =====================================
# ==============================================================================
'''
@staff_member_required()
def students(request):
    # Devuelve una lista de los alumnos con prácticas.

    students = User.objects.all()

    context = {
        "authenticate": True,
        "user": user,
        "students": students,
    }
    return render(request, 'jderobot_kids/students.html', context)
'''

# ==============================================================================
# =============================== REBOOT APP ===================================
# ==============================================================================
@staff_member_required
def reboot_app(request):
    Simulation.objects.all().delete()

    context = {
        "authenticate": True,
        "success": True,
        "message": "Reboot App Success!",
        "user": request.user,
    }

    return main_page(request, context)


# ==============================================================================
# ============================ ERROR HANDLERS ==================================
# ==============================================================================

@staff_member_required()
def users(request):
    users = User.objects.all()

    context = {
        "users": users
    }

    return render(request, 'jderobot_kids/users.html', context)


def error_handler404(request):
    return render(request, 'jderobot_kids/error_page/404_error.html', {}, status=404)


def error_handler500(request):
    if not settings.DEBUG:
        user_agent = parse(request.META['HTTP_USER_AGENT'])

        ErrorDocument(
            type=500,
            date=datetime.now(),
            username=request.user.username,
            client_ip=get_client_ip(request),
            browser = user_agent.browser.family + " " + user_agent.browser.version_string,
            os = user_agent.os.family + " " + user_agent.os.version_string,
            device = user_agent.device.family
        ).save()
    return render(request, 'jderobot_kids/error_page/500_error.html', status=500)


# ==============================================================================
# ================================ TESTING =====================================
# ==============================================================================

@login_required()
def testing(request):
    return redirect('/main_page')


@login_required()
def simutest(request, exercise_id):
    user = User.objects.get(username=request.user.username)
    exercise = Exercise.objects.get(exercise_id=exercise_id)

    context = {
        "authenticate": True,
        "simulation_type": "simulator",
        "simulation_site": True,
        "user": user,
        "exercise": exercise,
        "simulation_type": "test",
        "visor": True
    }

    return render(request, 'jderobot_kids/simutest.html', context)


@login_required()
def pruebas(request):
    user = User.objects.get(username=request.user.username)
    context = {
        "authenticate": True,
        "success": True,
        "user": user
    }

    return render(request, 'jderobot_kids/testing_main_page.html', context)


def terms(request):
    return render(request, 'jderobot_kids/terms.html', {})

# ==============================================================================
# ============================== REAL ROBOTS ===================================
# ==============================================================================
@csrf_exempt
def evaluate_py_style(request):
	try:
		from pylint import epylint as lint
		import io
		import tempfile
		python_code = request.GET.get('python_code', None)
		if not python_code:
			body_unicode = request.body.decode('utf-8')
			body_unicode = body_unicode[0:18] + body_unicode[18: len(body_unicode) - 2].replace('"',"'") + body_unicode[-2:]
			body = json.loads(body_unicode, strict=False)
			python_code = body['python_code']
		python_code = python_code.lstrip('\\').lstrip('"')
		python_code = python_code.replace('\\n','\n')
		python_code = python_code.replace('\\"', '"').replace("\\'", "'")
		code_file = tempfile.NamedTemporaryFile()
		code_file.write(python_code.encode())
		code_file.seek(0)
		options = code_file.name + ' --enable=similarities'
		(stdout, stderr) = lint.py_run(options, return_std=True)
		code_file.seek(0)
		code_file.close()
		print(stdout.getvalue())
		print(stderr.getvalue())
		return HttpResponse(stdout.getvalue(), content_type="text/plain")
	except Exception as e: print(e)

def get_python_to_arduino_code(request):
    simulation = Simulation.objects.get(user=request.user.username)
    exercise = Exercise.objects.get(exercise_id=simulation.exercise)
    py_on_arduino_path = 'kibotics-pyonarduino/'
    os.chdir(settings.BASE_DIR)
    path.append(py_on_arduino_path + 'translator')
    import Translator as translator
    python_code = json.loads(request.GET.get('python_code', None))
    if exercise.language == "scratch":
        lines = python_code.split('\n')
        for idx in range(len(lines)):
            lines[idx] = "  " + lines[idx]
        python_code = '\n'.join(lines)
        python_code = python_code.replace('  myRobot = None', "import HALduino.halduino as halduino\ndef loop():\n")
        python_code = python_code.replace('myRobot', "halduino")
        lines = python_code.split('\n')
        for idx in range(len(lines)):
            if "if" in lines[idx]:
                if ":" not in lines[idx]:
                    lines[idx] = lines[idx] + lines[idx + 1]
                    lines[idx + 1] = ''
        python_code = '\n'.join(lines)

    parsed_file = ast.parse(python_code)
    translator.robot = 'MBot'
    translator.robot_architecture = ''
    translator.vars.Variables()
    translator.vars.halduino_directory = py_on_arduino_path + 'HALduino/halduino'
    translator.TranslatorVisitor().visit(parsed_file)
    translator.create_setup()
    translator.variables_manager = translator.create_variables_manager(
        file=py_on_arduino_path + 'HALduino/variablesManager.ino')
    translator.create_output('output-front.ino')
    translator.create_makefile('MBot', py_on_arduino_path + 'makefiles/')
    shutil.copyfile(os.path.join(settings.BASE_DIR, 'kibotics-drivers/mbot/avrdude'), './avrdude')
    shutil.copyfile(os.path.join(settings.BASE_DIR, 'kibotics-drivers/mbot/libftdi1.so'), './libftdi.so')
    shutil.copyfile(os.path.join(settings.BASE_DIR, 'kibotics-drivers/mbot/libreadline.so'), './libreadline.so.6')
    shutil.copyfile(os.path.join(settings.BASE_DIR, 'kibotics-drivers/mbot/avrdude.conf'), './avrdude.conf')
    shutil.copytree(os.path.join(settings.BASE_DIR, 'kibotics-drivers/mbot/arduino-1.8.10/'), 'arduino/')
    call(['make'])
    exercise_dir = './'
    pyinstaller_cmd = "pyinstaller -F --distpath " + exercise_dir + "dist --workpath " + exercise_dir + "build --specpath " + exercise_dir + " --clean " + os.path.join(
        settings.BASE_DIR, 'kibotics-drivers/mbot/proxy/mBot_upload.py')
    os.system(pyinstaller_cmd)
    py_installer_file = open(exercise_dir + 'mBot_upload.spec', 'r')
    file_content = py_installer_file.readlines()

    file_content = "".join(file_content)
    py_installer_file.close()
    file_content = file_content.replace(')', ")\n\
a.datas += Tree('build-uno/', prefix='build-uno/')\n\
a.datas += Tree('arduino/', excludes=['libraries'], prefix='arduino/')\n\
a.datas += [ ('avrdude.conf', 'avrdude.conf', \"DATA\" ) ]\n\
a.binaries += [ ( 'avrdude', 'avrdude', \"BINARY\" ) ]\n\
a.binaries += [ ( 'libftdi.so', 'libftdi.so', \"BINARY\" ) ]\n\
a.binaries += [ ( 'libreadline.so.6', 'libreadline.so.6', \"BINARY\" ) ]\n\
a.binaries += [ ( 'libusb-1.0.so.0', '/lib/x86_64-linux-gnu/libusb-1.0.so.0', \"BINARY\" ) ]\n\
a.binaries += [ ( 'libusb-0.1.so.4', '/lib/x86_64-linux-gnu/libusb-0.1.so.4', \"BINARY\" ) ]", 1)

    py_installer_file = open(exercise_dir + 'mBot_upload.spec', 'w')
    py_installer_file.write(file_content)
    py_installer_file.close()
    call(['pyinstaller', exercise_dir + 'mBot_upload.spec'])

    print('Python code: ' + python_code)

    os.chdir('dist')
    zipf = zipfile.ZipFile('../../output.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk('./'):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()
    os.chdir('../../')

    with open('output.zip', 'rb') as f:
        response = HttpResponse(f, content_type=guess_type('output.zip')[0])
        response['Content-Length'] = len(response.content)
        shutil.rmtree("output/")
        os.remove('output.zip')
        return response


@csrf_exempt
def get_python_to_javascript_code(request):
    print(evaluate_py_style(request))
    py_on_browser_path = os.path.join(settings.BASE_DIR, 'kibotics-websim/kibotics-pyonbrowser/')
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode, strict=False)
    python_code = body['python_code']

    # Create file from python code so it can be sent to PyOnBrowser
    current_path = os.getcwd()
    os.chdir(py_on_browser_path)
    file = open('python_to_javascript_code.py', 'w+')
    file.write(python_code)
    file.close()

    # Send code to PyOnBrowser to translate
    os.system('python3 main.py python_to_javascript_code.py --outfile=python_websim.js')

    # Get Javascript code and send back to web
    javascript_code = open('python_websim.js', 'r')
    os.chdir(current_path)
    response = HttpResponse(javascript_code)
    response["Access-Control-Allow-Origin"] = "*"

    return response


# Para Tello Real
@login_required
def get_robot_code(request):
    """
    Vista que permite extraer el código destinado a ejecutarse en el robot real
    del cuadernillo del estudiante y generar un "Ejecutable Congelado" de Python.
    """
    # Procesando Petición POST
    body = json.loads(request.body)
    exercise_id = body["exercise_id"]
    exercise = Exercise.objects.get(exercise_id=exercise_id)
    user = User.objects.get(username=request.user.username)
    if exercise.language == "python":
        code = json.loads(body["notebook"].encode('ascii', 'ignore'))
        exercise_dir = user.local_user_exercise_location(exercise)
        with open(exercise_dir + "tello_code.py", "w") as text_file:
            text_file.write(code)
        tic = time.time()

        # generar bundle con pyinstaller (WIP)
        # --------------------------------------------------------------------------
        subprocess.call(". kibotics-drivers/tello/tello_env/bin/activate; pyinstaller -F --distpath " +
                        exercise_dir + "dist --workpath " + exercise_dir + "build --specpath " + exercise_dir + " --clean " + exercise_dir +
                        "tello_code.py", shell=True)
        time_elapsed = time.time() - tic
        print("Tiempo empleando en generar el Bundle de Python: {} segundos.".format(time_elapsed))

        total_size = 0
        for subdir, dirs, files in os.walk(exercise_dir + 'dist/'):
            for f in files:
                filepath = subdir + os.sep + f
                fsz = os.path.getsize(filepath)
                total_size += fsz
        print("Tamaño total de archivos generados en el Bundle: {} bytes.".format(total_size))
        # --------------------------------------------------------------------------

        response = FileResponse(open(exercise_dir + "dist/tello_code", 'rb'), content_type='application/octet-stream')
        shutil.rmtree(exercise_dir + "dist/")
        shutil.rmtree(exercise_dir + "build/")
        os.remove(exercise_dir + "tello_code.spec")
    else:
        code = body["code"]
        # For Tello
        code = code.replace('myRobot = None',
                            "from tello.tello_wrapper import Drone\nimport time\nmyRobot = Drone('', 9005)")
        exercise_dir = user.local_user_exercise_location(exercise)
        with open(exercise_dir + "tello_code.py", "w") as text_file:
            text_file.write(code)

        tic = time.time()
        # generar bundle con pyinstaller (WIP)
        # --------------------------------------------------------------------------
        subprocess.call(". kibotics-drivers/tello/tello_env/bin/activate; pyinstaller -F --distpath " + exercise_dir
                        + "dist --workpath " + exercise_dir + "build --specpath " + exercise_dir + " --clean " + exercise_dir
                        + "tello_code.py", shell=True)

        time_elapsed = time.time() - tic
        print("Tiempo empleando en generar el Bundle de Python: {} segundos.".format(time_elapsed))

        total_size = 0
        for subdir, dirs, files in os.walk(exercise_dir + 'dist/'):
            for f in files:
                filepath = subdir + os.sep + f
                # print(filepath)
                fsz = os.path.getsize(filepath)
                total_size += fsz
        print("Tamaño total de archivos generados en el Bundle: {} bytes.".format(total_size))
        # --------------------------------------------------------------------------

        response = FileResponse(open(exercise_dir + "dist/tello_code", 'rb'), content_type='application/octet-stream')
        shutil.rmtree(exercise_dir + "dist/")
        shutil.rmtree(exercise_dir + "build/")
        os.remove(exercise_dir + "tello_code.spec")

    return response


def hour_graph_visit(data):
    usage = []
    hours = []
    for i in range(0, 24):
        aux = str(i)
        if int(aux)<10:
            aux = '0'+aux
        hours += [aux+':00']
        count = 0
        for d in data:
            if d.split("T")[1].split(":")[0] == aux:
                count += 1
        usage += [count]

    x_pos = [i for i, _ in enumerate(hours)]
    fig, ax = plt.subplots(facecolor='#f6f6f6', figsize=(17, 3))

    plt.bar(x_pos, usage)
    plt.ylabel("Accesos")
    fig.tight_layout()
    ax.set_frame_on(False)
    ax.grid(color='#b9b9b9', linestyle='solid', linewidth=1, axis="y")

    plt.xticks(x_pos, hours)

    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300, facecolor=fig.get_facecolor())
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    return image_base64


def weekly_usage_visit(data):
    days = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    usage = [0, 0, 0, 0, 0, 0, 0]  # Dias de la semana

    for d in data:
        try:
            usage[datetime.strptime(d, "%Y-%m-%dT%H:%M:%S.%f").weekday()] += 1
        except Exception as e:
            print(e)
            usage[datetime.strptime(d, "%Y-%m-%dT%H:%M:%S").weekday()] += 1

    fig, ax = plt.subplots(facecolor='#f6f6f6', figsize=(17, 3))
    ax.plot(days, usage, marker='o', linestyle='solid', linewidth=1, markersize=5, markerfacecolor='#3F7FBF',
            markeredgewidth=1.5, markeredgecolor='#13487d'),

    ax.set(ylabel='Accesos')
    ax.grid(color='#b9b9b9', linestyle='solid', linewidth=1, axis="y")
    ax.set_ylim([0, np.ceil(float(np.amax(usage))*1.1)])

    ax.set_frame_on(False)

    for i, j in zip(days, usage):
        ax.annotate(str(j), xy=(i, j), ha='center', textcoords="offset points", xytext=(0, 10))

    fig.tight_layout()
    if usage == [0, 0, 0, 0, 0, 0, 0]:
        ax.set_ybound(lower=10*-0.02, upper=10*1.1)
    else:
        ax.set_ybound(lower=np.amax(usage)*-0.02, upper=np.amax(usage)*1.1)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300, facecolor=fig.get_facecolor())
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    return image_base64


def pie_chart(data, title):

    fig, axs = plt.subplots(facecolor='#f6f6f6')

    axs.pie(list(data.values()), labels=list(data.keys()), autopct='%1.1f%%', startangle=90)

    plt.title(title)
    plt.tight_layout()
    axs.axis('equal')
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300, facecolor=fig.get_facecolor())
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    return image_base64


def IP_map(IPs):
    fig, ax = plt.subplots(facecolor='#f6f6f6', figsize=(20, 10))

    map = Basemap(lat_0=0, lon_0=0)
    map.drawcoastlines()
    map.fillcontinents()

    for ip in IPs:
        try:
            map.plot(geolite2.lookup(ip).location[1], geolite2.lookup(ip).location[0], markersize=15, marker='o',
                     color='#3F7FBF', alpha=0.5)
        except Exception as e:
            print(e)

    buf = BytesIO()
    plt.tight_layout()
    ax.axis('off')

    plt.savefig(buf, format='png', dpi=300, facecolor=fig.get_facecolor())
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    return image_base64


@login_required()
def visits_analytics(request, from_date, to_date):
    default_range = 30
    try:
        from_date = datetime.strptime(from_date, '%Y%m%d')
    except ValueError:
        from_date = datetime.today() - timedelta(days=default_range-1)

    try:
        to_date = datetime.strptime(to_date, '%Y%m%d')
    except ValueError:
        to_date = datetime.today()

    if from_date > to_date:
        aux_date = from_date
        from_date = to_date
        to_date = aux_date

    from_date = from_date.replace(hour=00, minute=00, second=00)
    to_date = to_date.replace(hour=23, minute=59, second=59)

    used_range = (to_date - from_date).days + 1
    if used_range > 365:
        from_date = to_date - timedelta(days=365-1)
        used_range = (to_date - from_date).days + 1

    print(from_date)
    print(to_date)

    data = Search(index="kibotics_visit_log").filter('range', **{'date': {'gte': from_date, 'lte': to_date}})

    print(data.count())
    dates = []
    IPs = []
    os = {}
    device = {}
    browser = {}
    for hit in data.scan():
        dates += [hit.date]

        try:
            if hit.client_ip not in IPs:
                IPs += [hit.client_ip]
        except Exception as e:
            print(e)

        try:
            if hit.os in os:
                os[hit.os] += 1
            else:
                os[hit.os] = 1
        except Exception as e:
            print(e)

        try:
            if hit.device in device:
                device[hit.device] += 1
            else:
                device[hit.device] = 1
        except Exception as e:
            print(e)

        try:
            if hit.browser in browser:
                browser[hit.browser] += 1
            else:
                browser[hit.browser] = 1
        except Exception as e:
            print(e)

    image_visit_hour = hour_graph_visit(dates)
    image_visit_week = weekly_usage_visit(dates)
    image_os = pie_chart(os, 'SISTEMA OPERATIVO')
    image_device = pie_chart(device, 'DISPOSITIVO')
    image_browser = pie_chart(browser, 'NAVEGADOR')
    image_data_IP_map = IP_map(IPs)
    image_IP_map = image_data_IP_map

    context = {'image_IP_map': image_IP_map,
                'image_visit_hour': image_visit_hour,
                'image_visit_week': image_visit_week,
                'image_os': image_os,
                'image_device': image_device,
                'image_browser': image_browser,
                'used_range': used_range}
    return render(request, 'jderobot_kids/visits_analytics.html', context)
