# chat/urls.py
# from django.conf.urls import url
from django.urls import path

from chatx import views

app_name = 'chatx'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
]