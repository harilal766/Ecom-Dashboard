import json
from channels.generic.websocket import AsyncWebsocketConsumer
from helpers.messages import color_text

class WebsocketBase(AsyncWebsocketConsumer):
    async def connect(self):
        color_text("Websocket connected...")
        await self.accept()
        await self.send(text_data=json.dumps({"message":"Websocket connected"}))

    async def disconnect(self, code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data.get("message",None)

        await self.send(text_data=json.dumps({"message" : message}))
