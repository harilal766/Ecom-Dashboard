import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from helpers.messages import color_text

from datetime import datetime
class WebsocketBase(AsyncWebsocketConsumer):
    async def connect(self):
        color_text("Websocket connected...")
        await self.accept()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await self.send_time()


        while True:
            await asyncio.sleep(1)  # Wait for 1 second
            await self.send_time()

    async def send_time(self):
        # Get the current time and send it as a string
        now = str(datetime.now())
        await self.send(json.dumps({"time": now}))
        
    async def receive(self, text_data):
        pass  # Handle any incomin

