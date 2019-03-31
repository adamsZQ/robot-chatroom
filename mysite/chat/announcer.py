
import queue
import socket
from . import models

import json

# class MessageQueue():
#     Q = queue.Queue()
#
#     def put(self, *args, **kwargs):
#         return self.Q.put(*args, **kwargs)
#
#     def get(self):
#         obj = self.Q.get()
#         print("MQ:get:%s" % (obj))
#         # Sync message to front end
#
#         return obj

connection_poll = {}
# messageQ = MessageQueue()
messageQ = queue.Queue()

def messageLoop(websocket, max_message_number=0x10):
    i = 0
    while i < max_message_number:
        item = messageQ.get()
        websocket.send(text_data=json.dumps({
            'message': {
                "speaker": item['speaker'].name,
                "content": item['content'],
            }
        }))

        broadcase(
            item['speaker'],
            item['everyone'],
            item['content'],
        )
        i += 1

def broadcase(speaker, everyone, message):
    print("[MSG] %s: %s" % (speaker, message))
    speakerset = set()
    speakerset.add(speaker)
    receivers = everyone - speakerset
    for receiver in receivers:
        connection_poll[receiver.name].send(message.encode("utf-8"))
        reply = connection_poll[receiver.name].recv(1024).decode("utf-8")
        item = {
            "speaker": receiver,
            "everyone": everyone,
            "content": reply,
        }
        messageQ.put(item)
        print("[MSG] %s: (RE) %s" % (receiver, reply))

def init_connection_poll():
    for robot in models.Robot.objects.all():
        ip = robot.ip
        port = robot.port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, port))
            print("%s (%s:%d) connected" % (robot.name, ip, port))
            connection_poll[robot.name] = s
        except Exception as e:
            print(e)


def clean_up_connection_poll():
    for name, s in connection_poll.items():
        print("Closing %s => %s" % (name, s))
        s.close()