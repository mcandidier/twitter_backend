import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token

from notification.models import Notification

from channels.auth import login


class NotificationConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = f'user_{self.user.id}'
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()


    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        notification_id = data.get('notification_id')
        await self.channel_layer.group_send(
            self.room_name,
            {"type": "send_nofication", "data": notification_id}
        )

    async def send_notification(self, event):
        data = event["message"]
        await self.send(text_data=json.dumps(data))