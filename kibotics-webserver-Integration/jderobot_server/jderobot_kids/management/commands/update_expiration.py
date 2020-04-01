#!/usr/bin/env python
#-*- coding: utf-8 -*-
  
import os
from django.core.management.base import BaseCommand, CommandError
from jderobot_kids.models import *
from datetime import date
from dateutil.relativedelta import relativedelta


class Command(BaseCommand):
    help = 'Update Expiration Date of Users who last logged in recently'

    def add_arguments(self, parser):
        parser.add_argument('month', nargs='+', type=int)

    def handle(self, *args, **options):
	      if options['month']:
	          x_month_ago = date.today() + relativedelta(months=-options['month'][0])
	      else:
	          x_month_ago = date.today() + relativedelta(months=-4)
              print("------------------------------------")
              print("EXTENDING subscription_expiration DATE FOR USERS WHOSE LAST LOG IN WAS IN:")
	      print(x_month_ago)
              print("------------------------------------")
	      
	      new_expiration = datetime.now() + relativedelta(months=+10)
	      ordered_users = User.objects.order_by('-last_login')
	      recently_logged_users = []
	      for user in ordered_users:
	          if (user.last_login and user.last_login.date() >= x_month_ago):
		      recently_logged_users.append(user)
		      user.subscription_expiration = new_expiration 
		      user.save()

	      print(recently_logged_users)
