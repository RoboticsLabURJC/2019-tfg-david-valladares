 #-*- coding: utf-8 -*-

from django.test import TestCase, Client
from jderobot_kids.models import Exercise

class ExerciseTestCase(TestCase):
    
    def test_exercises_exist(self):

       Exercise.objects.create(
               name = "ejercicio_test",
            )
       exercise = Exercise.objects.all()
       print(exercise[0].name)
       print("--------------- PRUEBA DE TEST -----------")
       print(exercise.values())
       print("------------------------------------------")


if __name__ == '__main__':
    unittest.main()
