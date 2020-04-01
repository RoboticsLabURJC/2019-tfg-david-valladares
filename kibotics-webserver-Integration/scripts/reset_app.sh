#!/bin/bash
# Script que reinicia el servicio de JderobotKids-App

# Para especificar la fila del proceso incluir NR=='nºfila': NR==2{print $3}
PID="$(ps aux | grep runserver | grep -v grep | awk '{print $2}')"

echo $PID

if [ "$PID" != "" ]; then # -z => if string is null
	printf "\nReiniciando el servicio ...\n\n"
	#kill -9 $PID # Se elimina el servicio

        printf "Remove corrupt containers ..."
        docker rm $(docker ps -a -q -f 'status=exited' -f 'ancestor=academy-simulation')

	printf "Iniciando el servidor de X"
        Xvfb :1 -screen 0 1600x1200x16  &
        export DISPLAY=:1.0

	printf "Iniciando el servidor"
	cd ../jderobot_server
	python manage.py runserver 0.0.0.0:8000
	cd ..
else
	printf "\nEl servicio no estaba activo: Iniciando ...\n"
	cd ../jderobot_server
	python manage.py runserver 0.0.0.0:8000
	cd ..
	printf "\nServicio Iniciado!!\n\n"
fi
