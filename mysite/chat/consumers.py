from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.auth import get_user

GROUP_NAME = "FOO_GROUP"

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            GROUP_NAME,
            self.channel_name
        )

    async def receive_json(self, content):
        user = await get_user(self.scope)
        await self.channel_layer.group_add(
            GROUP_NAME,
            self.channel_name
        )

    async def broadcast_message(self, event):
        await self.send_json({"broadcast": "important update"})

