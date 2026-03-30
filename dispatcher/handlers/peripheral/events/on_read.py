from dispatcher.command_message.message import CommandMessage
from dispatcher.device.messages.enum import (
    Scope,
    MessageType,
    MessageDirection,
    MessageCommand,
)
from dispatcher.device.messages.payload.rfid import OnReadIntent
from dispatcher.dispatch_result import DispatchResult
from dispatcher.handlers.base import ActionEventBaseHandler
from dispatcher.handlers.registry import register_action_event


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.EVENT,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.ON_READ,
)
class UpdateStateActionIntent(ActionEventBaseHandler):

    def __call__(self, message: CommandMessage) -> DispatchResult:
        payload: OnReadIntent = message.payload
        uid = payload.uid
        print(uid)
        # device = self._get_device(message.device_id)
        # result = Card.objects.filter(rfid=device, uid=uid).exists()
        # event = MessageEvent.ON_READ_SUCCESS if result else MessageEvent.ON_READ_FAILURE
        return DispatchResult()
