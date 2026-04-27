import logging
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from consumers.router.message.message import (
    RouterMessagePacket,
    AckRouterMessage,
    DeviceRouterMessage,
)
from consumers.router.service import RouterService
from device.models import Router

logger = logging.getLogger("base")


class RouterConsumer(AsyncWebsocketConsumer):
    router: Router
    service: RouterService

    async def connect(self):
        mac = self.scope["url_route"]["kwargs"]["mac_address"]
        print(f"Router with MAC {mac} is trying to connect.")
        router = await database_sync_to_async(RouterService.handle_connect)(mac)
        if router is None:
            await self.close(code=4000)
            return
        self.router = router
        self.service = RouterService(self.router)

        await self.channel_layer.group_add(
            f"router_{self.router.mac}", self.channel_name
        )
        await self.accept()
        await database_sync_to_async(self.service.notify_frontend)()
        await database_sync_to_async(self.service.send_get_connected_message)()

    async def disconnect(self, code):
        if not self.router:
            return
        await database_sync_to_async(self.service.handle_disconnect)()

    async def router_send(self, event):
        if not isinstance(event, str):
            event = event["data"]
        await self.send(text_data=event)

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return
        logger.debug(f"Received message: {text_data}")
        packet = RouterMessagePacket.model_validate_json(text_data).root
        if isinstance(packet, AckRouterMessage):
            await database_sync_to_async(self.service.handle_ack_received)(packet)
        elif isinstance(packet, DeviceRouterMessage):
            await database_sync_to_async(self.service.handle_device_message)(packet)
