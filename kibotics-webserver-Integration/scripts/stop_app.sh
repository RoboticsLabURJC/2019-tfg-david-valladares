#!/bin/bash
# Detiene todos los servicios de la aplicación

PID="$(ps aux | grep runserver | grep -v grep | awk '{print $2}')"
echo $PID


if [ "$PID" != "" ]; then # -z => if string is null
    kill -9 $PID # Se elimina el servicio
    printf "\nServicio eliminado\n\n"

    printf "Remove corrupt containers ..."
    docker rm $(docker ps -a -q -f 'status=exited' -f 'ancestor=academy-simulation')
else
    printf "\nERROR: El servicio no está activo!\n\n"
fi
