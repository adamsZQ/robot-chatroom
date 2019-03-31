from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from .models import *

def index(request):
    return render(request, 'chat/index.html', {})

def debug(request):
    for i in range(0x10):
        name = "Robot-%02d" % (i)
        ip = "127.0.0.1"
        port = 9999
        Robot.objects.create(name=name, ip=ip, port=port)
    return "Hello world"

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })