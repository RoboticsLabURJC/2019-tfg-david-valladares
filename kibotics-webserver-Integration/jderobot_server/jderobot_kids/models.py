# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from time import strftime, localtime
import os
import base64
import json
import shutil
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from github import GithubException
from os.path import isfile, join
from taggit_autosuggest.managers import TaggableManager
from taggit.models import Tag


class Exercise(models.Model):
    exercise_id = models.CharField(max_length=40, blank=False, unique=True)
    name = models.CharField(max_length=40, blank=False, unique=True)

    STATE = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('testing', 'Testing')
    )
    state = models.CharField(max_length=40, blank=False, choices=STATE)

    PLATFORM = (
        ('websim', 'WebSim'),
        ('pyonbrowser-theory', 'PyOnBrowser Theory'),
        ('real', 'Real')
    )
    platform = models.CharField(max_length=40, blank=True, choices=PLATFORM)

    EXERCISE_TYPES = (
        ('challenge', 'Challenge'),
        ('shared_game', 'Shared game'),
        ('webIDE', 'WebIDE')
    )
    type = models.CharField(max_length=40, blank=True, choices=EXERCISE_TYPES)

    LANGUAGE = {
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('scratch', 'Scratch')
    }
    language = models.CharField(max_length=40, choices=LANGUAGE)
    description = models.CharField(max_length=400, blank=False)
    tags = TaggableManager(blank=True)
    video = models.CharField(max_length=100, blank=True)
    topic = models.CharField(max_length=100, blank=True)
    thumbnail = models.CharField(max_length=100, blank=True)
    assets = models.CharField(max_length=2000, default=json.dumps({"notebook": ""}))  # JSON Object.
    gui = models.CharField(max_length=2000, blank=True) # Estructura {"client":"", "server":""}
    evaluator = models.CharField(max_length=2000, blank=True) # Estructura {"client":"", "server":""}
    compute_load = models.IntegerField(blank=False, default=100) # Unidades: Unidad de Computo (UC)
    observations = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    def exercise_location(self):
        """ Ruta a la carpeta que contiene los archivos propios de cada ejercicio """
        return settings.EXERCISES_DIR + '/' + self.language + "/" + self.exercise_id + '/'

    def exercise_file_location(self):
        """ Ruta al archivo con el código base (cuadernillo por defecto) del ejercicio """
        assets = json.loads(self.assets)
        return settings.BASE_DIR + "/exercises/" + self.language + "/" + self.exercise_id + "/" + assets["notebook"]

    def get_random_pack(self):
        return Exercise.tags.all().order_by("?").first()

class Permissions(models.Model):
    class Meta:
        permissions = (
            ("is_admin", "admin"),
            ("is_profesor", "profesor"),
            ("is_alumno", "alumno"),
        )


class Host(models.Model):
    host = models.CharField(max_length=200)
    ip = models.CharField(max_length=200)
    main_server = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.host

    @property
    def get_name(self):
        """ Nombre de la máquina sin el dominio """
        return self.host.split(".")[0]


class Simulation(models.Model):
    user = models.CharField(max_length=200)
    init_simulation = models.CharField(max_length=200)
    simulation_type = models.CharField(max_length=200)
    exercise = models.CharField(max_length=200)
    client_ip = models.CharField(max_length=200)
    host_ip = models.CharField(max_length=200)
    ws_channel = models.CharField(max_length=200)
    active = models.BooleanField(default=False)

    @property
    def getHostName(self):
        """ Retorna el nombre de la máquina donde se está ejecutando esta simulación"""
        return Host.objects.get(ip=self.host_ip).host

    def up_time(self):
        """ Calcula el tiempo que lleva iniciada la simulación en minutos """
        now = datetime.now()
        delta = now - datetime.strptime(self.init_simulation, "%d/%m/%Y %H:%M:%S")
        return delta.seconds//60

class Code(models.Model):
    code = models.CharField(max_length=32)
    group = models.CharField(max_length=200, help_text="Si no existe, se creará uno nuevo.",  blank=True) # get group of user -> user_group = user.code.all()[0].group
                                             # get all users from group -> users_in_group = User.objects.filter(code__group='BETATESTER')
    packs = models.ManyToManyField(Tag, blank=True)
    exercises = models.ManyToManyField(Exercise, blank=True)
    observations = models.TextField(max_length=500, blank=True)
    promotional = models.BooleanField(default=False)
    expires = models.DateField(null=True)

    def __str__(self):
        return self.code

def upload_to(instance, filename):
    return '{username}/{filename}'.format(
        username=instance.username, filename=filename)

class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('Betatester', 'Betatester'),
        ('profesor', 'Profesor'),
        ('alumno', 'Alumno')
    )

    role = models.CharField(max_length=40, choices=ROLES, blank=True)
    code = models.ManyToManyField(Code, blank=True)
    observations = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(blank=True, upload_to=upload_to, default = 'anonymous_avatar.png')
    subscription_expiration = models.DateTimeField(blank=False, default=datetime.now()) # date evaluated now resulting in datetime from the past
                                                                                        # suscriptions with no datetime specified will be considered as expired
    group = TaggableManager(blank=True, verbose_name="Grupos", help_text="Etiquetas de Grupo Separadas por coma (i.e: grupo1, grupo2, ...)")

    # ======================================= RUTAS A ARCHIVOS ===========================================

    def __str__(self):
        return self.username

    def local_user_location(self):
        """ Obtiene el path de la carpeta del usuario en el servidor principal. En ella se almacenan de forma temporal los ejercicios de dicho usuario

        Returns:
            str: Path al directorio del usuario
        """
        return settings.USERS_LOCAL_DIR + '/' + self.username + '/'

    def local_user_exercise_location(self, exercise):
        """ Obtiene el path de la carpeta del ejercicio deñ usuario en el servidor principal.

        Returns:
            str: Path al directorio del ejercicio del usuario
        """
        return str(self.local_user_location() + exercise.exercise_id + '/')

    def repo_user_exercise_location(self, exercise):
        """ Path de la carpeta del ejercicio del usuario en el repositorio de GitHub

        Args:
            exercise (Exercise Object): Ejercicio del que obtener la ruta

        Returns:
            str: Path del ejercicio del usuario en Github
        """
        return settings.GITHUB_USERS_DIR + self.username + '/' + exercise.exercise_id

    def exercises_files(self, exercise):
        """ Listado de los archivos de la carpeta self.local_user_exercise_location(exercise)"

        Args:
            exercise (Exercise Object):  Ejercicio del que obtener los archivos

        Returns:
            array : Array con los archivos de la carpeta user.local_user_exercise_location
        """

        local_user_exercise_location = self.local_user_exercise_location(exercise)
        exercises_files = [f for f in os.listdir(local_user_exercise_location) if isfile(join(local_user_exercise_location, f))]

        return exercises_files

    def prepare_directory(self, exercise):
        """ Prepara los directorios del usuario en el servidor principal. Si no existe, los crea y si existe elimina los existente para
            prepararlos para nuevos archivos.

        Args:
             exercise (Exercise Object):  Ejercicio del que preparar los directorios
        """
        if not os.path.isdir(self.local_user_location()):
            os.mkdir(self.local_user_location())
        if os.path.isdir(self.local_user_exercise_location(exercise)):
            shutil.rmtree(self.local_user_exercise_location(exercise))
        os.mkdir(self.local_user_exercise_location(exercise))


    def gh_push_file(self, content, exercise, file_name):
        """ Sube a GitHub el contenido de un archivo

        Args:
            content (): Contenido del archivo a subir
            exercise (Exercises Object): Ejercicio al que pertenece el archivo
            file_name (str): Nombre del archivo a subir a GitHub
        """

        repo_file_path = self.repo_user_exercise_location(exercise) + "/" + file_name
        try:
            file_repo = settings.REPOSITORY.get_file_contents(repo_file_path)
            commit = strftime("%d/%m/%Y %H:%M:%S ", localtime()) + "User: " + self.username + " File: " + repo_file_path
            update_message = settings.REPOSITORY.update_file(repo_file_path, commit, content, file_repo.sha)
            print(update_message)
            print("\033[94m Archivo " + repo_file_path + " actualizado en GitHub" + "\033[0m")

        except GithubException as e:
            print(e)
            if e.status == 404:
                print("\033[93m No existen archivos de la practica " + exercise.exercise_id + " del usuario " + self.username + " en el directorio " + self.repo_user_exercise_location(exercise) + ". Copiando archivos por defecto." + "\033[0m")
                commit = strftime("%d/%m/%Y %H:%M:%S ", localtime()) + "User: " + self.username + " File: " + repo_file_path
                update_message = settings.REPOSITORY.create_file(repo_file_path, commit, content)
                print(update_message)
                print("\033[94m Archivo " + repo_file_path + " subido a GitHub" + "\033[0m")


    def gh_pull_file(self, exercise, file_name):
        """ Obtiene el contenido del archivo con el nombre "file_name" perteneciente al ejercicio correspondiente. Tipicamente utilizado para descargar desde GitHub
        el código del usuario al iniciar una simulación. Puesto que unicamente necesitamos el contenido no lo guardamos en ningún archivo del servidor principal.

        Args:
            exercise (Exercises Object): Ejercicio al que pertenece el archivo
            file_name (str): Nombre del archivo

        Returns:
            []: Contenido del archivo
        """
        file_contents = settings.REPOSITORY.get_contents(self.repo_user_exercise_location(exercise) + '/' + file_name)
        file_data = base64.b64decode(file_contents.content)

        return file_data

    def gh_pull_exercise(self, exercise):
        """ Descarga desde GitHub todos los archivos del ejercicio correspodiente.Estos son almacenados en la carpeta self.local_user_exercise_location(exercise)
        del servidor principal

        Args:
            exercise (Exercises object): Ejercicio de los archvios a descargar desde GitHub
        """
        try:
            repository_directory_content = settings.REPOSITORY.get_contents(self.repo_user_exercise_location(exercise))
            for file in repository_directory_content:
                if file.type == "file" and "Untitled" not in file.name:
                    file_data = base64.b64decode(file.content)
                    file_out = open(
                        str(self.local_user_exercise_location(exercise) + file.name), "w")
                    os.chmod(self.local_user_exercise_location(exercise) + file.name, 0o664)
                    file_out.write(file_data)
                    file_out.close()

        except GithubException as e:
            print(e)
            if e.status == 404:
                print("\033[93m No existen archivos de la practica " + exercise.exercise_id + " del usuario " + self.username + " en el repositorio. Copiando archivos por defecto." + "\033[0m")
                assets = json.loads(exercise.assets)
                shutil.copyfile(exercise.exercise_file_location(), self.local_user_exercise_location(exercise) + assets["notebook"])

class CodePermissions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    # | --------------------------------------------------------------|
    # |                     Permission Options:                       |
    # |  p = presentation  |  r = read  |  w = write  |  x = execute  |
    # | --------------------------------------------------------------|
    p = models.BooleanField(default=True)
    r = models.BooleanField(default=True)
    w = models.BooleanField(default=True)
    x = models.BooleanField(default=True)

    def __str__(self):
        permissions = ''
        if self.p:
            permissions += 'p'
        if self.r:
            permissions += 'r'
        if self.w:
            permissions += 'w'
        if self.x:
            permissions += 'x'
        return self.user.username+'-'+self.exercise.exercise_id+'-'+permissions
