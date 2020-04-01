# -*- coding: utf-8 -*-

import os
import shutil
from django.conf import settings
import errno


def mkdir_p(path):
    """mkdir -p
    
    Parameters
    ----------
    path : string
        directories to be created
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def read_file(file):
    """Reads python file and save in string

    Parameters
    ----------
    file : string
        path of file

    Returns
    -------
    string
        file contend or empty string if any error occur
    """

    file_py = ""

    try:  # Building .zip to send to the client.
        file_py = os.popen("cat " + file).read()

    except Exception as e:
        print(e)
        print("Error al leer el fichero" + str(e))

    return file_py


def copy_import(text, text_to_replace, file):
    """Copy in the exercise the contents of the driver to unify 
       everything in a file.

    Parameters
    ----------
    text : string
        text to be copied
    text_to_replace : string
        path to file import - For example: all the pibot driver
        text_to_replace: Contenido del driver del pibot que se 
        sobrescribe en el archivo ejercicio.py
    file : string
        path to file
    """

    os.popen("sed '/^from __future__ import print_function/{s/^/#/}' -i " + file)
    #os.popen("sed -e '\$a\' -i " + text_to_replace)
    os.system("echo '\n\r' >> " + text_to_replace)

    os.popen("sed '/" + text + "/{ \n\t s/" + text +
             "//g \n\t r " + text_to_replace + "\n}' -i " + file)


def prepare_real_execution(user):
    '''Clears the user folder of the previous files.'''

    success = False

    if settings.DEBUG:
        download_path = settings.ARM_DIR
    else:
        download_path = settings.ARM_DIR_PROD

    try:
        print("\nENTRADA DEL IF")
        # Carpeta jderobot_server/static//download/users/username
        mkdir_p(os.path.join(settings.ARM_DIR, "users", user.username))
        # Carpeta kibotics-static/download/users/username
        mkdir_p(os.path.join(download_path, "users", user.username))
        # kibotics-static/download/users/username/PiBot.zip
        if os.path.exists(os.path.join(download_path, "users", user.username, "PiBot.zip")):
            os.remove(os.path.join(download_path, "users", user.username, "PiBot.zip"))
        # jderobot_server/static/download/users/username
        if os.path.exists(os.path.join(settings.ARM_DIR, "users", user.username, "PiBot.zip")):
            os.remove(os.path.join(settings.ARM_DIR, "users", user.username, "PiBot.zip"))
        # jderobot_server/static/download/users/username
        if os.path.exists(os.path.join(settings.ARM_DIR, "users", user.username, "ejercicio.py")):
            os.remove(os.path.join(settings.ARM_DIR, "users", user.username, "ejercicio.py"))
        # jderobot_server/static/download/users/username
        mkdir_p(os.path.join(settings.ARM_DIR, "users", user.username, "pibot_obfuscate"))
        print("\nSALIDA DEL IF")

        success = True
    except Exception as e:
        print("\n------- ERROR en la preparación de la estructura para ejecución real -----\n")
        print(e)
    return success


'''
def building_zip(exercise_id, user, base_dir, local_user_exercise_location, user_exercise_location):
    """Build a zip to send to the pibot with the driver and the necessary files 

    Parameters
    ----------
    exercise_id : string
        id of exercise
    user : object
        object of user
    user_exercise_location : string_to_python
        path to user folder with their code
    local_user_exercise_location : string
        path to folder (named download) to build the zip and send to user.

    notes:
        1 - Se comprueba que la estructura de directorios y ficheros es correcta
        2 - Se ejecuta la ofuscación
        3 - Se preparan los archivos que irán dentro del zip en la carpeta del usuario
        4 - Se realiza la compresión a zip.
        5 - Se construye la ruta al archivo PiBot.zip

    Returns
    -------
    string
        path to zip file to send to user.
    """

    success = False
    debug = True

    if debug:
        info = [" ######################## REAL EXECUTION ##########################",
                "\n\n\nLOCAL USER EXERCISE LOCATION: " + os.path.join(local_user_exercise_location, exercise_id),
                "\t1 ----> Checking that the directory skeleton is correct.",
                "\t2 ----> Files manargement. A function prepares the skeleton for ofuscation.",
                "\t3 ----> Run the obfuscation",
                "\t4 ----> Preparing files to building zip.",
                "\t5 ----> Zip compress",
                "\t6 ----> Move the zip obfuscated to previous folder",
                "\t7 ----> Path to PiBot.zip",
                "###################################################################"
        ]
        print("\n".join(info))

    # 1.-Check if the container is running. If not, it is created.
    docker_client = docker.from_env()
    try:
        print("\nObteniendo información del contenedor . . .\n")
        container = docker_client.containers.get("obfuscator_container")
    except docker.errors.NotFound:
        print("\nArrancando el contenedor . . .\n")
        run_obfuscator_container(docker_client)
    ### 2.- Files manargement. A function prepares the skeleton for ofuscation.
    print("=========== PREPARANDO ENTORNO =========================")
    prepare_real_execution(user)
    shutil.move(os.path.join(local_user_exercise_location, "ejercicio.py"), os.path.join(settings.ARM_DIR, "users", user.username))    
    ### 3.- Run the obfuscation
    os.system('docker exec -i obfuscator_container /bin/bash obfuscator.sh ' + user.username)
    ### 4.- Preparing files to building zip.
    shutil.copy(os.path.join(settings.DRIVERS_DIR, "pibot", "Kibotics.yml"), os.path.join(settings.ARM_DIR, 'users', user.username, "pibot_obfuscate"))
    ### 5.- Zip compress.
    os.system("cd " + settings.ARM_DIR + "/users/" + user.username + "/pibot_obfuscate && zip -r PiBot.zip * ")
    ### 6 and 7.- Move the zip obfuscated to previous folder - Path to PiBot.zip       
    path_to_zip = ""
    if settings.DEBUG:
        shutil.move(os.path.join(settings.ARM_DIR, "users", user.username, "pibot_obfuscate", "PiBot.zip"), os.path.join(settings.ARM_DIR, "users", user.username))
    else:
        shutil.move(os.path.join(settings.ARM_DIR, "users", user.username, "pibot_obfuscate", "PiBot.zip"), os.path.join(settings.ARM_DIR_PROD, "users", user.username))
    path_to_zip = os.path.join(settings.STATIC_URL, "download/users", user.username, "PiBot.zip")

   
    print("\n---------------------------------")
    print(path_to_zip)
    print("---------------------------------\n")
    success = True
    return path_to_zip, success
'''