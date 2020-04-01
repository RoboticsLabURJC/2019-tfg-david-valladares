#!/usr/bin/python
# -*- coding: utf-8 -*-


import os, sys
import commands



if __name__ == "__main__":


	command = "ps aux | grep /usr/local/bin/daphne | grep -v grep | awk 'NR==1{print $12}'"
	daphne = commands.getoutput(command).split("/")[-1]


	if daphne:
		print("Daphne UP")
		os.system("echo 'LANZADO DESDE APACHE!!!!! --> EL SERVICIO ESTÁ LEVANTADO!!!' >> /tmp/CGI_APACHE_TEST.txt")
	else:
		print("Daphne Down")
		os.system("echo 'LANZADO DESDE APACHE!!!!! --> EL SERVICIO ESTÁ CAÍDO!!!' >> /tmp/CGI_APACHE_TEST.txt")
	

