from django.urls import path
from .consumers import Chatconsumer
websocket_urlpatterns= [
    path('room/<str:pk>/',Chatconsumer.as_asgi()),
]