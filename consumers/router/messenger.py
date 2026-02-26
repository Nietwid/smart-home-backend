from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from consumers.router.message.message import RouterMessage


class RouterMessenger:
    def __init__(self):
        """Initialize the Channels layer."""
        self.channel_layer = get_channel_layer()
        self._initialized = True

    async def send_async(self, router_mac: str, message: RouterMessage) -> None:
        """Asynchronously send data to a device.

        Args:
            router_mac: The MAC address of the router (e.g., 'AA:BB:CC:DD:EE:FF').
            message: The data to send.
        """
        await self.channel_layer.group_send(
            f"router_{router_mac}",
            {"type": "router_send", "data": message.model_dump_json()},
        )

    def send(self, router_mac: str, message: RouterMessage) -> None:
        """Synchronously send data to a device.

        Args:
            router_mac: The MAC address of the router (e.g., 'AA:BB:CC:DD:EE:FF').
            message: The data to send.
        """
        async_to_sync(self.send_async)(router_mac, message)


router_messenger = RouterMessenger()
