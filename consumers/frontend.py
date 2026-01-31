import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from uuid import uuid4
from ai_assistance.tasks import ai_test
from consumers.router_message.device_message import DeviceMessage
from consumers.router_message.message_event import MessageEvent
from consumers.router_message.message_type import MessageType
from consumers.router_message.messenger import DeviceMessenger
from consumers.utils import validate_user


class UserConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user_instance = None

    async def connect(self):
        token = self.scope["url_route"]["kwargs"]["token"]
        user = await validate_user(token)
        if not user:
            await self.close()
            return
        home_id = await self.get_home_id(user)
        self.user_instance = user
        await self.channel_layer.group_add(f"home_{home_id}", self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        command_type = data.get("type", None)
        match command_type:
            case "aiCommand":
                message = data.get("message", None)
                ai_test.delay(self.user_instance.pk, message, self.channel_name)
            case "camera_open":
                camera_id = data.get("id", None)
                if not camera_id:
                    return
                message = await self.get_camera_start_message(camera_id)
                if not message:
                    return
                await DeviceMessenger().send_async(await self.get_router_mac(), message)
            case "camera_close":
                camera_id = data.get("id", None)
                if not camera_id:
                    return
                message = await self.get_camera_stop_message(camera_id)
                if not message:
                    return
                await DeviceMessenger().send_async(await self.get_router_mac(), message)

    async def send_to_frontend(self, event):
        await self.send(text_data=event["data"])

    async def disconnect(self, code):
        print("disconnect", code)

    @sync_to_async
    def get_home_id(self, user):
        return user.home.first().id

    @database_sync_to_async
    def get_router_mac(self):
        return self.user_instance.home.first().router.mac

    @database_sync_to_async
    def get_camera_start_message(self, pk: int) -> DeviceMessage | None:
        camera = self.user_instance.home.first().cameras.filter(pk=pk)
        if not camera.exists():
            return None
        return DeviceMessage(
            message_type=MessageType.REQUEST,
            message_event=MessageEvent.CAMERA_START,
            device_id="camera",
            payload={
                "id": pk,
                "rtsp": camera.first().rtsp,
            },
            message_id=uuid4().hex,
        )

    @database_sync_to_async
    def get_camera_stop_message(self, pk: int) -> DeviceMessage | None:
        camera = self.user_instance.home.first().cameras.filter(pk=pk)
        if not camera.exists():
            return None
        return DeviceMessage(
            message_type=MessageType.REQUEST,
            message_event=MessageEvent.CAMERA_STOP,
            device_id="camera",
            payload={
                "id": pk,
            },
            message_id=uuid4().hex,
        )
