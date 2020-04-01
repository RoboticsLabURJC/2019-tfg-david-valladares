#!/bin/sh

# Script provisional de publicación de ejercicios que se alojan en el repositorio de "exercises" y son
# volcados a la aplicación Django de JdeRobot-Kids. A falta de fijar una estructura final.

# Author: Ignacio Arranz Águeda - Abril 2018


# Clon del repositorio de ejercicios
git clone ssh://git@gitlab.jderobot.org:2224/JdeRobot-Kids/exercises.git /tmp/publicar_nuevo_ejercicio

# Clon del repositorio de infraestructura (contiene los mundos)
#git clone ssh://git@gitlab.jderobot.org:2224/JdeRobot-Kids/infraestructura.git /tmp/infraestructura_gazebo_mundos

# Se mueve la carpeta hasta el destino de la aplicación
cp -r /tmp/publicar_nuevo_ejercicio/jupyter/exercises ../jupyter/


# Se elimina de la carpeta 'temp' el contenido descargado.
rm -rf /tmp/publicar_nuevo_ejercicio
#rm -rf /tmp/infraestructura_gazebo_mundos

