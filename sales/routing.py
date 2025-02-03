from django.urls import re_path
from sales.consumers import WebsocketBase

websocket_urlpatterns =[
    re_path("ws/websocket/",WebsocketBase.as_asgi()),
]

