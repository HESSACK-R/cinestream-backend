# cinestream\backend\homepage\consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class HomepageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("homepage_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("homepage_updates", self.channel_name)

    async def homepage_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))
