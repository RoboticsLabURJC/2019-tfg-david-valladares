#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import requests
import time
import smtplib
from email.mime.text import MIMEText

"""
Script to send an email to several people to inform them of the 
operation of JdeRobot services.

For the WebSocket request it is necessary to install a client
of WebSocket. One of the most popular is: websocket-client,
can be installed via pip.
"""

__author__ = "Ignacio Arranz Águeda"
__license__ = "GPL"
__version__ = "0.01"
__email__ = "n.arranz.agueda@gmail.com"
__status__ = "Production"


services = [
        "https://kids.jderobot.org",
        "https://makers.jderobot.org",
        "https://academy.jderobot.org",
        "https://developers.jderobot.org",
        "https://gitlab.jderobot.org",
        "https://jderobot.org/Main_Page"
    ]


def send_email(sites):

    # Building message and users.
    addressees = [
                'xarlye13@gmail.com',
                'n.arranz.agueda@gmail.com',
                'aitor.martinez.fernandez@gmail.com',
                'f.perez475@gmail.com',
                'josemaria.plaza@gmail.com'
            ]

    for addr in addressees:
        message = "Correo de alerta:\n Fallo en el servicio: " + str(sites)
        msg = MIMEText(message)
        msg['Subject'] = "Servicio Caído"
        msg['From']    = 'JdeRobot-Admin <jderobot@gmail.com>'
        msg['To']      = addr

        # Sending email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("jderobot", "gsoc2015")
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print("\nMain sent to " + str(addr))


if __name__ == "__main__":
    # List of services than are down.
    downed_services = []

    for site in services:
        try:
            code = requests.get(site)
            if code.status_code != 200:
                downed_services.append(site)
                print(site, " DOWN")
        except:
            print("Error en la solicitud: " + site + "\n")
            downed_services.append(site)
            print("\n=== DOWNED SERVICES =====================================")
            #print(str(downed_services))
            print(*downed_services, sep = "\n") 
            print("=========================================================\n")
     
    #print(downed_services)
    if len(downed_services) != 0: send_email(downed_services)
