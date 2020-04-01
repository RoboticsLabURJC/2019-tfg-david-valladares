#!/us/bin/env python

###############################################################################
# This script gets information from the running containers. 
# It obtains the date of creation of each of them and deletes it 
# if it has been active for more than one hour.
################### Author: Ignacio Arranz - n.arranz.agueda@gmail.com ########

import os, commands, sys, time, datetime
import dateutil
from dateutil import tz
from dateutil.parser import parse
from datetime import datetime
import datetime
from datetime import timedelta
import pytz
from pytz import UTC, timezone


utc=pytz.UTC
spain_zone = tz.gettz('Europe/Madrid')


# Get the info of all the running containers.
containers_running = commands.getoutput("docker ps --format '{{.ID}}-{{.Names}}' -f name='kibotics_simulation'")

if containers_running != "":

	containers_running = containers_running.split("\n")

	# Get the ID of all the containers.
	containers_id = []
	for container in containers_running:
		containers_id.append(container.split("-")[0])
	print(containers_id)

	# Get the creation date of all the containers on the list.
	dict_of_containers_and_dates = {}
	for container in containers_id:
		containerStartedAt = commands.getoutput("docker inspect -f '{{ .Created }}' " + container)
		# Python returns an error because docker timestamp are too long. 
		# The value is set to the maximum permissible value per Python (-4).
		containerStartedAt = containerStartedAt[:-4]
		print(containerStartedAt)
		dict_of_containers_and_dates[container] = containerStartedAt
	print(dict_of_containers_and_dates)

	# Get current time.
	current_time = datetime.datetime.now(tz=spain_zone)

	for key, value in dict_of_containers_and_dates.iteritems():
		#print(dateutil.parser.parse(value))
		#if current_time < (dateutil.parser.parse(value) + datetime.timedelta(hours=1)):
		limite_time = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f") + datetime.timedelta(hours=1)
		current_time_UTC = current_time.astimezone(utc).replace(tzinfo=spain_zone)
		limite_time_UTC = limite_time.replace(tzinfo=spain_zone)
		print "CURRENT_TIME: " + str(current_time_UTC)
		print "LIMIT TIME: " + str(limite_time_UTC)
		if current_time_UTC > limite_time_UTC:
			os.system('docker stop ' + key)
			print("Stopping container " + key)
		else:
			print("It hasn't been long enough")

else:
	print("No containers running")

