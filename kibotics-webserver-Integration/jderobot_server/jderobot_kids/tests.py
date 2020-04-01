# -*- coding: utf-8 -*-

from django.test import TestCase

from django.test import RequestFactory, TestCase
from .views import index

from django.conf import settings

from .models import Exercise, User, Host, Simulation

import json

from channels.test import ChannelTestCase, WSClient, apply_routes
from jderobot_server.consumers import SimConsumer


def setup_BBDD_simulation():
    userdata = {
        'username': 'testuser',
        'password': 'secret'}


    User.objects.create_user(**userdata)
    with open(settings.BASE_DIR + '/test_data/exercises.json') as json_file: #actualizar JSON, probablemente no funcione 
        data = json.load(json_file)
        n_exercises = len(data)

        for i in data:
            Exercise.objects.create(**i)

        all_elements = Exercise.objects.all()
        user = User.objects.get(username=userdata["username"])

        for el in all_elements:
            permission = CodePermissions.objects.create(
                user = user,
                exercise = el,
                p = True,
                r = True,
                w = True,
                x = True
            )
        #user.exercises.set(all_elements)

    Host.objects.create(**{"host": "localhost", "ip": "localhost", "main_server": True, "active": True, "max_simulations": 1, "running_simulations": 0, "priority": 0, "cpu_limit": 5.0, "compute_load": 0, "compute_capacity":100, "memory_limit": "1g", "uc_equivalence": 3.5})

    return (userdata,  n_exercises)

    

class TestPortada(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('')

        # Test my_view() as if it were deployed at /customer/details
        response = index(request)
        self.assertEqual(response.status_code, 200)


class LogInTest(TestCase):
    def setUp(self):

        ## saving data in BBDD
        self.userdata = {
            'username': 'testuser',
            'password': 'secret'}

        User.objects.create_user(**self.userdata)


        self.credentials_error_user = {
            'username': 'notuser',
            'password': 'secret'}

        self.credentials_error_pass = {
            'username': 'testuser',
            'password': 'wrong'}
        


    def test_login(self):
        # send login data
        response = self.client.post('/login/', self.userdata, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)


    def test_login_error(self):
        # send login data for error user
        response = self.client.post('/login/', self.credentials_error_user, follow=True)

        self.assertFalse(response.context['user'].is_active)

        # send login data for error password
        response = self.client.post('/login/', self.credentials_error_pass, follow=True)

        self.assertFalse(response.context['user'].is_active)


class SimTest(TestCase):

    @classmethod
    def setUp(self):
        #settings.DEBUG = True

        self.userdata, self.n_exercises= setup_BBDD_simulation()
        
        #self.docker_client = docker.from_env()
            
            

    def test_load_from_file(self):
        user = User.objects.get(username=self.userdata["username"])
        self.assertTrue(self.n_exercises == len(user.exercises.all()))


    def test_main_page(self):
        self.assertTrue(self.client.login(username=self.userdata["username"], password=self.userdata["password"]))
        response = self.client.get('/main_page', follow=True)
        self.assertFalse("<!-- LOGIN SITE -->" in response.content)

    '''
    def test_simulation(self):
        self.assertTrue(self.client.login(username=self.userdata["username"], password=self.userdata["password"]))
        response = self.client.get('/simulation/simulator/sigue_linea_ir', follow=True)

        sim_id = response.content.split("?simulation_id=")[1].split('"')[0]

        sim = Simulation.objects.get(id=sim_id)
        self.assertFalse(sim.active)
        ex = Exercise.objects.get(exercise_id=sim.exercise)

        host = Host.objects.get(ip = sim.host_ip)

        self.assertTrue(ex.compute_load == host.compute_load)

       

        container = self.docker_client.containers.get(sim.docker_id)
        self.assertTrue(container.status == "running")

        container.stop()
    '''


class WSTests(ChannelTestCase):
    """
    def setUp(self):

        self.userdata, self.n_exercises = setup_BBDD_simulation()

        self.sim_data = {
            "user": self.userdata["username"],
            "docker_id": "docker_id",
            "exercise":"sigue_linea_ir",
            "client_ip": "127.0.0.1",
            "simulation_type": "simulator",
            "host_ip": "localhost",
            "active": False
        }

        host = Host.objects.get(ip = self.sim_data["host_ip"])
        ex = Exercise.objects.get(exercise_id=self.sim_data["exercise"])

        host.compute_load += ex.compute_load
        host.save()

        Simulation.objects.create(**self.sim_data)
    """

    def test_ws(self):
        
        client = WSClient()
        with apply_routes([SimConsumer.as_route(path='/new')]):

            sim = Simulation.objects.get(user=self.sim_data["user"])


            client.login(username=self.userdata["username"], password=self.userdata["password"])
            client.send_and_consume(u'websocket.connect', path='/new?simulation_id=' + str(sim.id))
            
            sim = Simulation.objects.get(user=self.sim_data["user"])

            self.assertTrue(sim.active)


            client.send_and_consume(u'websocket.disconnect', path='/new?simulation_id=' + str(sim.id))

            self.assertTrue(len(Simulation.objects.all()) == 0)
            host = Host.objects.get(ip = self.sim_data["host_ip"])
            print(host.compute_load)
            self.assertTrue(host.compute_load == 0)


