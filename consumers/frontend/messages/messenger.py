from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from consumers.frontend.messages.message import FrontendMessage
from consumers.frontend.messages.types import (
    FrontendMessageType,
)


class FrontendMessenger:
    """Singleton class for sending command to the frontend via Django Channels."""

    def __init__(self):
        """Initialize the Channels layer."""
        self.channel_layer = get_channel_layer()

    def update_frontend(
        self,
        home_id: int,
        data: dict,
        status=200,
        action=FrontendMessageType.UPDATE_DEVICE,
    ) -> None:

        message = FrontendMessage(
            action=action,
            status=status,
            data=data,
        )
        self.send(home_id, message)

    async def async_update_frontend(
        self,
        home_id: int,
        data: dict,
        status=200,
        action=FrontendMessageType.UPDATE_DEVICE,
    ) -> None:
        """Asynchronously update the frontend with the given data."""

        message = FrontendMessage(
            action=action,
            status=status,
            data=data,
        )
        await self.send_async(home_id, message)

    async def send_async(self, home_id: int, message: FrontendMessage) -> None:
        """Asynchronously send a message to the frontend.

        Args:
            home_id: The ID of the home for the Channels group (e.g., forms 'home_123').
            message: The FrontendMessage object to send.
        """
        await self.channel_layer.group_send(
            f"home_{home_id}",
            {
                "type": "send_to_frontend",
                "data": message.model_dump_json(),
            },
        )

    def send(self, home_id: int, message: FrontendMessage) -> None:
        """Synchronously send a message to the frontend.

        Args:
            home_id: The ID of the home for the Channels group (e.g., forms 'home_123').
            message: The FrontendMessage object to send.
        """
        async_to_sync(self.send_async)(home_id, message)

    def send_to_channel(self, channel_name: str, message: FrontendMessage):
        async_to_sync(self.send_to_channel_async)(channel_name, message)

    async def send_to_channel_async(self, channel_name: str, message: FrontendMessage):
        await self.channel_layer.send(
            channel_name,
            {"type": "send_to_frontend", "data": message.model_dump_json()},
        )


frontend_messenger = FrontendMessenger()