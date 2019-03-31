# chat/consumers.py
from channels.generic.websocket import WebsocketConsumer
import json
from . import models
from . import urls
import socket
from .announcer import messageQ
from .announcer import messageLoop

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        names = message.split( '+')

        group_name = names[0]
        robots_names = names[1:]

        print("Group name: %s" % group_name)
        print("Robots names: %s" % robots_names)

        # Create a group
        group = models.Group.objects.create(name=group_name, rcount=len(robots_names))

        # Get all robots
        '''
        123+Robot-07+Robot-06+Robot-05
        '''
        robots = set()
        for i in robots_names:
            print("Robot name: %s" % i)
            robot = models.Robot.objects.get(name=i)
            print("Robot: %s" % (robot))
            robots.add(robot)
            print(robots)
            # Associate robots and group
            obj = models.RobotGroup.objects.create(group=group, robot=robot)
            print(obj)


        # Routing messages
        # TODO: What's the first message?
        messageQ.put({
            "speaker":robots.pop(),
            "everyone":robots,
            "content":"Hello",
        })
        messageLoop(websocket=self)




        #
        # messages = []
        # for i in range(1,len(names)-1):
        #     messages.append({"robot":robotnames[i],"group":groupname,"content":'Hello'})
        #
        # print(groupname.robots)
        # rsockets = []
        # messagecount = int(0)
        #
        # for i in range(1, groupname.rcount):
        #     rsockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        #     rsockets[i - 1].connect((groupname.robots[i - 1].ip, groupname.robots[i - 1].port))
        #
        # while True:
        #     for i in range(1, groupname.rcount):
        #         sendmsg = messages[i-1]
        #         messagecount = messagecount + 1
        #         if messagecount == 51:
        #             break
        #         sendmsg = sendmsg
        #         for j in range(1, groupname.rcount):
        #             if j != i:
        #                 rsockets[i - 1].send(sendmsg.encode("utf-8"))
        #                 messages[j-1] = rsockets[i - 1].recv(1024)
        #                 print(messages[j-1].decode("utf-8"))
        #         if i == groupname.rcount:
        #             i = 1
        #     if messagecount == 51:
        #         break
        #
        # for i in range(1, groupname.rcount):
        #     rsockets[i - 1].close()




