# -*- coding: utf-8 -*-

import os
import shutil
import threading
from datetime import datetime
import json
from django.conf import settings
from jderobot_kids.utils import ColorPrint
from jderobot_kids.models import Simulation, Exercise, User
from datetime import date

LOCK_REPOSITORY = threading.Lock()

def get_client_ip(request):
    ''' Function for get IP client from HTTP request '''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def update_file(user, exercise, file_name):

    local_file_path = user.local_user_exercise_location(exercise) + file_name
    os.system("jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace " + local_file_path)

    file = open(local_file_path, "r")
    file_content = file.read()
    file.close()

    LOCK_REPOSITORY.acquire()
    user.gh_push_file(file_content, exercise, file_name)
    LOCK_REPOSITORY.release()

def save_simulation_code(simulation):
    """ Procedimiento para obtener el código del usuario y subirlo a GitHub durante una simulación de cualquier tipo """

    user = User.objects.get(username=simulation.user)
    exercise = Exercise.objects.get(exercise_id=simulation.exercise)

    try:
        exercises_files = user.exercises_files(exercise)
    except OSError as e:
        print(e)
        print(ColorPrint.ORANGE + " No se ha encontrado la carpeta " + user.local_user_exercise_location(exercise) + ColorPrint.END)
        exercises_files = []

    for file_name in exercises_files:
        if file_name == json.loads(exercise.assets)["notebook"]:
            # XML Scratch Code, Python ACE editor
            local_file_path = user.local_user_exercise_location(exercise) + file_name
            file = open(local_file_path, "r")
            file_content = file.read()
            file.close()
            user.gh_push_file(file_content, exercise, file_name)


def kill_simulation(simulation, request):
    """ Standard end simulation procedure. Uploads the notebook to GitHub. """

    user = User.objects.get(username=simulation.user)
    exercise = Exercise.objects.get(exercise_id=simulation.exercise)

    if not settings.DEBUG:
        try:
            exercises_files = user.exercises_files(exercise)
        except OSError as e:
            print(e)
            print(ColorPrint.ORANGE + " No se ha encontrado la carpeta " + user.local_user_exercise_location(exercise) + ColorPrint.END)
            exercises_files = []
        threads = []
        for file_name in exercises_files:
            try:
                if file_name == json.loads(exercise.assets)["notebook"]:
                    thread = threading.Thread(target=update_file, args=(user, exercise, file_name,))

                    thread.daemon = True
                    thread.start()
                    threads.append(thread)
            except Exception as e:
                print(e)
                print('\033[91m' + " Error al subir el archivo " + file_name + " a Github " + '\033[0m')

        for hilo in threads:
            # El programa esperará a que este hilo finalice:
            hilo.join()
        try:
            shutil.rmtree(user.local_user_exercise_location(exercise))
        except OSError as e:
            print(e)
            print(ColorPrint.ORANGE + " No se ha encontrado la carpeta " + user.local_user_exercise_location(exercise) + ColorPrint.END)

    simulation.delete()

    log = open(settings.BASE_DIR + "/logs/" + str(date.today()) + "-log.txt", "a")
    if request is not None:
        user_agent = request.META['HTTP_USER_AGENT']
    else:
        user_agent = ''
    traze = "4 | " + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + " | " + simulation.user + \
            " | " + simulation.client_ip + " | " + simulation.simulation_type + " | " + \
            simulation.exercise + " | " + user_agent + "\n"
    log.write(traze)
    log.close()

