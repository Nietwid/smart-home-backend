from dispatcher.device.messages.builder.rtc import rtc_message_builder
from dispatcher.device.messages.enum import MessageCommand
from dispatcher.command_message.message import CommandMessage
from dispatcher.handlers.base import EventIntentBaseHandler
from dispatcher.device.messages.enum import Scope, MessageType, MessageDirection
from dispatcher.handlers.registry import register_action_event
from notifier.message import NotifierMessage
from notifier.factory.router_notifier_factory import router_notifier_factory


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.EVENT,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.ON_SYNC_TIME,
)
class OnSyncTimeEvent(EventIntentBaseHandler):

    def get_extra_notification(self, message: CommandMessage) -> list[NotifierMessage]:
        return [
            router_notifier_factory.device_message(
                router_mac=message.device.get_router_mac(),
                message=rtc_message_builder.on_sync_time_result(message),
            ),
        ]
