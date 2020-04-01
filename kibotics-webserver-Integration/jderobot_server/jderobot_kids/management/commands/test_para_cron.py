#!/usr/bin/env python
#-*- coding: utf-8 -*-
  
import os
from django.core.management.base import BaseCommand, CommandError
from jderobot_kids.models import *



class Command(BaseCommand):
    help = 'Runs through email queue and sends emails'

    def add_arguments(self, parser):
        parser.add_argument('--id')

    def handle(self, *args, **options):
        print("------------------------------------")
        print("ESTO ES UNA PRUEBA")
        print("------------------------------------")

        os.system("touch /home/nachoaz/test_$(date +%Y_%m_%d_%H_%M).txt") 
