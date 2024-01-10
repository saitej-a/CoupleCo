from django.urls import path
from .consumers import Chatconsumer,videoConsumer,getresults,selected
websocket_urlpatterns= [
    path('room/<str:pk>/',Chatconsumer.as_asgi()),
    path('room/<str:pk>/video',videoConsumer.as_asgi()),
    path('room/<str:pk>/getresults',getresults.as_asgi()),
    path("room/<str:pk>/selected",selected.as_asgi()),
]