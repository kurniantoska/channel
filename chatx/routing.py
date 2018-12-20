# chatx/routing.py
from django.urls import path
from django.conf.urls import url

from chatx.consumers import ChatConsumer

websocket_urlpatterns = [
    # url(r'^ws/chat/(?P<room_name>[^/]+)/$', ChatConsumer),
    path('ws/chat/<str:room_name>/', ChatConsumer),
]