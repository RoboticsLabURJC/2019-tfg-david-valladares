#!/bin/bash


USER=$1

OUTPUT_DIR=/home/jderobot/users/$USER


cd /home/jderobot/users/$USER
pyarmor obfuscate -O /home/jderobot/users/$USER/pibot_obfuscate ejercicio.py
