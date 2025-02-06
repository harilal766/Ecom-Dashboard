from django.urls import re_path
from dashboard.consumers import WebsocketBase

websocket_urlpatterns =[
    re_path("ws/websocket/",WebsocketBase.as_asgi()),
]

