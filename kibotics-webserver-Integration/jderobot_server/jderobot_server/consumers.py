# -*- coding: utf-8 -*-

import simplejson as json
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from jderobot_kids.models import Simulation, User, Host, Exercise
import jderobot_kids.file_utils as fu
from jderobot_kids.utils import ColorPrint
from datetime import datetime, date
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch

from channels import Group
from online_users.models import OnlineUserActivity

from channels.generic.websockets import WebsocketConsumer

userGroups = {}
onlineUsers = {}


class SimConsumer(WebsocketConsumer):
    groups = ["running_simulations"]

    def connect(self, message, **kwargs):
        simulation = {}

        split_message = message.content["query_string"].decode().split("&")
        for split in split_message:
            simulation[split.split("=")[0]] = split.split("=")[1]

        try:
            simulation = Simulation.objects.get(id=simulation["simulation_id"])
            simulation.ws_channel = message.content["reply_channel"]
            self.ws_channel = message.content["reply_channel"]
            simulation.active = True
            simulation.save()

            message.reply_channel.send({"accept": True})
            message.reply_channel.send({
                "text": json.dumps(
                    "Simulation Registered !"
                )
            })

            onlineUsers[simulation.user] = self.message.reply_channel

            print(ColorPrint.BLUE + "Conexion WebSocket Establecida=> Simulacion en proceso: User: " + simulation.user + " Tipo de Simulacion: " + simulation.simulation_type + " Ejercicio: " + simulation.exercise + ColorPrint.END)

        except Exception as e:
            print(e)

    def keepalive(self, message):
        pass

    def receive(self, text=None, bytes=None, **kwargs):
        simulation = Simulation.objects.get(ws_channel=self.message.reply_channel)
        user = User.objects.get(username=simulation.user)
        exercise = Exercise.objects.get(exercise_id=simulation.exercise)
        str_msg = ""

        msg = json.loads(text)

        str_msg = "Message:\n  type: '" + str(msg['type']) + "'\n  Data:"
        if msg["type"] == "save_scratch":
            try:
                assets = json.loads(exercise.assets)
                user.gh_push_file(msg["content"], exercise, assets["notebook"])
            except Exception as e:
                print(e)

        elif msg["type"] == "searchOpponent":
            opponent = msg["user"]
            userList = []
            founded = False;

            for user_activity in OnlineUserActivity.get_user_activities():
                if opponent == str(user_activity.user) and opponent != str(user):
                    token = str(user) + "-" + opponent
                    userList.append(self.message.reply_channel)
                    userGroups[token] = userList
                    Group(token).add(self.message.reply_channel)

                    onlineUsers[opponent].send({
                        "text": json.dumps({
                            "type": "requestOpponent",
                            "user": str(user),
                            "token": token
                        })
                    })
                    founded = True
                    break
                elif opponent == str(user):
                    self.message.reply_channel.send({
                        'text': json.dumps({
                            "type": "requestOpponent",
                            "user": "",
                            "token": ""
                        })
                    })
                    founded = True
                    break

            if not founded:
                self.message.reply_channel.send({
                    'text': json.dumps({
                        "type": "requestOpponent",
                        "user": "",
                        "token": ""
                    })
                })
            str_msg += "\n    Opponent: " + str(opponent)

        elif msg["type"] == "joinRoom":
            remoteUser = msg["user"]
            userList = []
            token = remoteUser + "-" + str(user)

            print(userGroups[token])
            userList.append(userGroups[token][0])
            userList.append(self.message.reply_channel)

            userGroups[token] = userList
            Group(token).add(self.message.reply_channel)

            for channel in userGroups[token]:
                if str(channel) != str(self.message.reply_channel):
                    channel.send({
                        "text": json.dumps({
                        "type": "joinRoom",
                            "user": "server",
                            "message": str(user) + " se ha unido.",
                            "token": token
                        })
                    })

            str_msg += "\n    Join: " + str(user)

        elif msg["type"] == "chat":
            token = msg["token"]
            str_userList = [str(i) for i in userGroups[token]]

            if str(self.message.reply_channel) in str_userList:
                str_msg += "\n    User: " + str(user) + "\n    Text: " + msg['text']
                answer = json.dumps({
                    "type": msg['type'],
                    "user": str(user),
                    "message": msg['text']
                })
                for channel in userGroups[token]:
                    if str(channel) != str(self.message.reply_channel):
                        channel.send({'text': answer})
            else:
                str_msg += "\n    Error: User not in chat group."

        elif msg["type"] == "leaveChat":
            token = msg["token"]

            for channel in userGroups[token]:
                if str(self.message.reply_channel) == str(channel):
                    userGroups[token].remove(channel)
                    Group(token).discard(self.message.reply_channel)

                    for ch in userGroups[token]:
                        ch.send({
                            'text': json.dumps({
                                "type": "leaveChat",
                                "user": "server",
                                "message": str(user) + " has leaved the chat."
                            })
                        })

            str_msg += "\n    User" + str(user) + " has leaved the chat."
        if msg["type"] == "candidate":
            token = msg["token"]

            for channel in userGroups[token]:
                if str(channel) != str(self.message.reply_channel):
                    channel.send({
                        "text": json.dumps({
                            "type": msg["type"],
                            "candidate": msg["candidate"]
                        })
                    });
            str_msg += "\n    Candidate: " + str(msg["candidate"])
        elif msg["type"] == "RTC-Offer":
            token = msg["token"]

            for channel in userGroups[token]:
                if str(channel) != str(self.message.reply_channel):
                    channel.send({
                        "text": json.dumps({
                            "type": msg["type"],
                            "offer": msg["offer"],
                            "user": "server",
                            "message": str(user) + " has started the stream"
                        })
                    });
            str_msg += "\n    Offer: " + str(msg["offer"])

        elif msg["type"] == "RTC-Answer":
            token = msg["token"]

            for channel in userGroups[token]:
                if str(channel) != str(self.message.reply_channel):
                    channel.send({
                        "text": json.dumps({
                            "type": msg["type"],
                            "answer": msg["answer"]
                        })
                    });

            str_msg += "\n    Answer: " + str(msg["answer"])

        elif msg["type"] == "stopStream":
            token = msg["token"]

            for channel in userGroups[token]:
                if str(channel) != str(self.message.reply_channel):
                    channel.send({
                        "text": json.dumps({
                            "type": msg["type"],
                            "user": "server",
                            "message": str(user) + " has stopped the stream"
                        })
                    });

            str_msg += "\n    Close: The RTCPeerConnection has been closed."

        elif msg["type"] == "simulate":
            token = msg["token"]

            for channel in userGroups[token]:
                if str(channel) != str(self.message.reply_channel):
                    channel.send({
                        "text": json.dumps({
                            "type": msg["type"]
                        })
                    });

            str_msg += "\n    Action: Change to simulate"

        elif msg["type"] == "loadCode":
            token = msg["token"]
            assets = json.loads(exercise.assets)
            user_code = user.gh_pull_file(exercise, assets['notebook'])

            for channel in userGroups[token]:
                if str(channel) != str(self.message.reply_channel):
                    channel.send({
                        "text": json.dumps({
                            "type": msg["type"],
                            "code": user_code
                        })
                    });

            str_msg += "\n    Code: " + str(user_code)

        elif msg["type"] == "unloadCode":
            token = msg["token"]

            for channel in userGroups[token]:
                if str(channel) != str(self.message.reply_channel):
                    channel.send({
                        "text": json.dumps({
                            "type": msg["type"],
                        })
                    });

            str_msg += "\n    Code: Coded unloaded"

        elif msg["type"] == "startGame" or msg["type"] == "stopGame":
            token = msg["token"]

            for channel in userGroups[token]:
                if str(channel) != str(self.message.reply_channel):
                    channel.send({
                        "text": json.dumps({
                            "type": msg["type"],
                        })
                    });

            str_msg += "\n    Play/Stop from remote"            

        print(str_msg)

    def disconnect(self, message, **kwargs):
        try:
            simulation = Simulation.objects.get(ws_channel=self.message.reply_channel)

            print(ColorPrint.BLUE + "Conexion WebSocket Finalizada => Finalizando simulacion: User: " + simulation.user + " Tipo de Simulacion: " + simulation.simulation_type + " Ejercicio: " + simulation.exercise + ColorPrint.END)
            if simulation.simulation_type in ["simulator"]:
                kill_simulation(simulation, None)
            elif simulation.simulation_type in ["websim", "real"]:
                simulation.delete()
                if not settings.DEBUG:
                    # Search the latest open simulation for a  specific user and exercise id
                    latest_simulation = Search(index="kibotics_simulation_log*") \
                        .query("match", username=simulation.user) \
                        .query("match", exercise_id=simulation.exercise) \
                        .query('match', duration=0) \
                        .sort({"start_date": {'order': 'desc'}})[0]

                    # Update previous query with exit date and simulation duration
                    for hit in latest_simulation:
                        duration = datetime.now() - datetime.strptime(hit.start_date, "%Y-%m-%dT%H:%M:%S.%f")
                        Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts']).update(index='kibotics_simulation_log', id=hit.meta.id,
                                               body={"doc":
                                                         {'end_date': datetime.now(),
                                                          'duration': duration.total_seconds()
                                                          }
                                                     })

        except ObjectDoesNotExist as e:
            print(e)
            print('\033[91m Error: No se ha podido localizar la simulación a terminar en la base de datos. ¿La simulación ya había finalizado? \033[0m')
