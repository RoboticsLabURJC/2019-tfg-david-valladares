#!/bin/bash
# Jderobot-Academy-Web reset script

# To specify the row, add: NR=='nºfila': NR==2{print $3}
PID="$(ps aux | grep runserver | grep -v grep | awk '{print $2}')"

echo $PID

if [ "$PID" != "" ]; then # -z => if string is null
    printf "\nReiniciando el servicio ...\n\n"
    #kill -9 $PID

    printf "Remove corrupt containers ..."
    docker rm $(docker ps -a -q -f 'status=exited' -f 'ancestor=academy-simulation')

    printf "Iniciando el servidor de X"
    Xvfb :1 -screen 0 1600x1200x16  &
    export DISPLAY=:1.0

    cd ../jderobot_server
    nohup python manage.py runserver 0.0.0.0:8000 &
    cd ..
    printf "\nRestarted process!\n"
else
    printf "\nThe service was not active: Initiating...\n"
    cd ../jderobot_server
    nohup python manage.py runserver 0.0.0.0:8000 &
    cd ..
    printf "\nProcess initiated!!\n\n"
fi

