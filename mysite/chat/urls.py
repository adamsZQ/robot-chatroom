# chat/urls.py
from django.conf.urls import url

from . import views
from .announcer import init_connection_poll

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^debug$', views.debug, name='debug'),

    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
]


init_connection_poll()