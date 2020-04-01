 #-*- coding: utf-8 -*-

from django.test import TestCase, Client
from jderobot_kids.models import Exercise, User

class UserTestCase(TestCase):

    def setUp(self):
        '''
        Save in database a user with many properties.
        '''

        User.objects.create(
            username   = "testing_user",
            first_name = "First_test",
            last_name  = "Last_test",
            email      = "test@test.com",
            password   = "testpassword",

            role       = "testing",
        )


    def test_user_create(self):
        '''
        Create an user and check their username.
        '''

        # Get from database
        user = User.objects.get(username="testing_user")

        # Checking
        self.assertEqual(user.username, 'testing_user')
       
