from dispatcher.device.messages.builder.action_event_intent import (
    action_event_intent_builder,
)
from dispatcher.device.messages.enum import MessageCommand
from dispatcher.device.messages.payload.basic import BasicResult
from dispatcher.command_message.message import CommandMessage
from dispatcher.dispatch_result import DispatchResult
from dispatcher.handlers.base import (
    ActionEventBaseHandler,
    ActionIntentBaseHandler,
    ActionResultBaseHandler,
)
from dispatcher.device.messages.enum import (
    Scope,
    MessageType,
    MessageDirection,
    ActionResult,
)
from dispatcher.handlers.registry import register_action_event
from notifier.frontend_notifier_factory import frontend_notifier_factory
from notifier.router_notifier_factory import router_notifier_factory
from peripherals.serializers.peripheral import PeripheralSerializer
from redis_cache import redis_cache
from dispatcher.tasks import check_command_timeout


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.ACTION,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.UPDATE_STATE,
)
class UpdateStateActionIntent(ActionIntentBaseHandler):
    def validate_payload(self, message: CommandMessage) -> None:
        serializer = PeripheralSerializer(
            data={
                "name": message.peripheral.name,
                "state": message.payload,
                "device": message.peripheral.device.pk,
            },
            partial=True,
        )
        serializer.is_valid(raise_exception=True)


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.ACTION,
    direction=MessageDirection.RESULT,
    handler_name=MessageCommand.UPDATE_STATE,
)
class UpdateStateActionResult(ActionResultBaseHandler): ...
