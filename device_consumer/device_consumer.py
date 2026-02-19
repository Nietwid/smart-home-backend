import logging
from datetime import datetime
from django.db.models import QuerySet
from django.utils import timezone
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from consumers.router_message.builders.basic import get_connected_devices_request
from device.models import Router, Device
from device.serializers.device import DeviceSerializer
from device.serializers.router import RouterSerializer
from consumers.frontend_message.frontend_message_type import FrontendMessageType
from consumers.frontend_message.messenger import FrontendMessenger
from dispatcher.tasks import handle_device_message_task

logger = logging.getLogger(__name__)


class DeviceConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.queue = None
        self.mac = None
        self.router: Router = None
        self.home = None
        self.counter = 0

    async def connect(self):
        self.mac = self.scope["url_route"]["kwargs"]["mac_address"]
        print(f"Router with MAC {self.mac} is trying to connect.")
        self.router: Router = await self.get_router(self.mac)
        if not self.router:
            await self.close(code=4000)
            return

        self.router.last_seen = datetime.now()
        self.router.is_online = True
        await sync_to_async(self.router.save)(update_fields=["last_seen", "is_online"])
        self.queue = {}
        await self.channel_layer.group_add(f"router_{self.mac}", self.channel_name)
        await self.accept()
        await self.set_home()
        await FrontendMessenger().async_update_frontend(
            self.home.id,
            await self.get_router_serialized_data(),
            action=FrontendMessageType.UPDATE_ROUTER,
        )
        connected_message = get_connected_devices_request()
        await self.send(text_data=connected_message.model_dump_json())

    async def disconnect(self, code):
        if not self.router:
            return
        self.router.last_seen = datetime.now()
        self.router.is_online = False
        await sync_to_async(self.router.save)(update_fields=["last_seen", "is_online"])
        await FrontendMessenger().async_update_frontend(
            self.home.id,
            await self.get_router_serialized_data(),
            action=FrontendMessageType.UPDATE_ROUTER,
        )
        router_devices = await self.get_router_devices()
        await self.deactivate_all_device(router_devices)

    async def receive(self, text_data=None, bytes_data=None):
        try:
            handle_device_message_task.delay(text_data, self.home.pk, self.router.mac)
        except Exception as e:
            logger.error(f"Could not push task to RabbitMQ: {e}")

    async def router_send(self, event):
        if not isinstance(event, str):
            event = event["data"]
        await self.send(text_data=event)

    @database_sync_to_async
    def get_router(self, mac: str) -> Router | None:
        """
        Retrieves a Router object by its MAC address.
        Args:
            mac (str): The MAC address of the router.
        Returns:
            Router | None: The Router object if found, otherwise None.
        """
        try:
            return Router.objects.select_related("home").get(mac=mac)
        except Router.DoesNotExist:
            return None

    @database_sync_to_async
    def get_router_devices(self):
        """
        Retrieves all devices associated with the router.
        Returns:
            QuerySet: A queryset of Device objects related to the router.
        """
        return self.router.home.devices.all()

    @database_sync_to_async
    def deactivate_all_device(self, devices: QuerySet[Device, Device]):
        online = devices.filter(is_online=True)
        for device in online:
            device.is_online = False
            device.last_seen = timezone.now()
            device.save(update_fields=["is_online", "last_seen"])
            FrontendMessenger().update_frontend(
                self.home.id, DeviceSerializer(device).data
            )

    ########################### utils ########################################

    @sync_to_async
    def get_router_serialized_data(self):
        return RouterSerializer(self.router).data

    async def send_to_frontend(
        self, status: int, action: FrontendMessageType, data: dict
    ):
        await self.channel_layer.group_send(
            f"home_{self.router.home.id}",
            {
                "type": "send_to_frontend",
                "action": action.value,
                "data": {"status": status, "data": data},
            },
        )

    @database_sync_to_async
    def set_home(self):
        self.home = self.router.home
