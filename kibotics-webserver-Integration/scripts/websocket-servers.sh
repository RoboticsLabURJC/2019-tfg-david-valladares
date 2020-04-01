#!/bin/bash

#-----------------------------------------------------------#
# Starts the two servers needed for management of WebSockets
# for Django in production behind the Apache servers.
#----------------------------- Ignacio Arranz --------------#

cd /var/www/academy-web/jderobot_server/
daphne jderobot_server.asgi:channel_layer --port 8000
python manage.py runworker

