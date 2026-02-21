from threading import Lock
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from consumers.device.messages import DeviceMessage


class DeviceMessenger:
    """Singleton class for sending data to routers via Django Channels."""

    _instance = None
    _lock = Lock()
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the Channels layer."""
        if self._initialized:
            return
        self.channel_layer = get_channel_layer()
        self._initialized = True

    async def send_async(self, router_mac: str, message: DeviceMessage) -> None:
        """Asynchronously send data to a device.

        Args:
            router_mac: The MAC address of the router (e.g., 'AA:BB:CC:DD:EE:FF').
            message: The data to send.
        """
        await self.channel_layer.group_send(
            f"router_{router_mac}",
            {"type": "router_send", "data": message.model_dump_json()},
        )

    def send(self, router_mac: str, message: DeviceMessage) -> None:
        """Synchronously send data to a device.

        Args:
            router_mac: The MAC address of the router (e.g., 'AA:BB:CC:DD:EE:FF').
            message: The data to send.
        """
        async_to_sync(self.send_async)(router_mac, message)
