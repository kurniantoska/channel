# chatx/routing.py
from django.urls import path
from django.conf.urls import url

from chatx import consumers

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
]