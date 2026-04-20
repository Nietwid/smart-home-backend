import logging
from datetime import datetime
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from consumers.tasks import deactivate_all_device
from device.models import Router
from device.serializers.router import RouterSerializer
from dispatcher.command_message.message import CommandMessage
from dispatcher.device.messages.builder.action_event_intent import (
    action_event_intent_builder,
)
from dispatcher.device.messages.device_message import DeviceMessage
from dispatcher.device.messages.enum import (
    MessageDirection,
    MessageCommand,
    MessageType,
    Scope,
)
from dispatcher.tasks import handle_device_message_task
from fixtures import command_message
from notifier.frontend_notifier_factory import frontend_notifier_factory
from notifier.notifier import notifier
from notifier.router_notifier_factory import router_notifier_factory

logger = logging.getLogger("base")


class RouterConsumer(AsyncWebsocketConsumer):
    router: Router

    async def connect(self):
        mac = self.scope["url_route"]["kwargs"]["mac_address"]
        print(f"Router with MAC {mac} is trying to connect.")
        self.router = await Router.objects.select_related("home").aget(mac=mac)
        if not self.router:
            await self.close(code=4000)
            return

        self.router.last_seen = datetime.now()
        self.router.is_online = True
        await self.router.asave(update_fields=["last_seen", "is_online"])
        await self.channel_layer.group_add(
            f"router_{self.router.mac}", self.channel_name
        )
        await self.accept()
        await self.notify_frontend()
        await self.send_get_connected_message()

    async def disconnect(self, code):
        if not self.router:
            return
        self.router.last_seen = datetime.now()
        self.router.is_online = False
        await self.router.asave(update_fields=["last_seen", "is_online"])
        deactivate_all_device.delay(self.router.pk)

    async def receive(self, text_data=None, bytes_data=None):
        try:
            logger.debug(f"Received message: {text_data}")
            handle_device_message_task.delay(
                text_data, self.router.home.pk, self.router.mac
            )
        except Exception as e:
            logger.error(f"Could not push task to RabbitMQ: {e}")

    async def router_send(self, event):
        if not isinstance(event, str):
            event = event["data"]
        await self.send(text_data=event)

    @database_sync_to_async
    def notify_frontend(self):
        data = RouterSerializer(self.router).data
        notifier.notify(
            [
                frontend_notifier_factory.update_router(
                    home_id=self.router.home.pk, data=data
                )
            ]
        )

    @database_sync_to_async
    def send_get_connected_message(self):
        device_message = DeviceMessage(
            direction=MessageDirection.INTENT,
            command=MessageCommand.GET_CONNECTED_DEVICES,
            type=MessageType.ACTION,
            scope=Scope.CPU,
            device_id="00:00:00:00:00:00",
            peripheral_id=0,
            payload={},
        )
        notifications = [
            router_notifier_factory.device_message(
                router_mac=self.router.mac,
                message=device_message,
            ),
        ]
        notifier.notify(notifications)
