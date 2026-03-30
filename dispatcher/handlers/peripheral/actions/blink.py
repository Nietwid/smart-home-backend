from dispatcher.device.messages.builder.action_event_intent import (
    action_event_intent_builder,
)
from dispatcher.device.messages.enum import MessageCommand
from dispatcher.device.messages.payload.basic import BasicResult
from dispatcher.command_message.message import CommandMessage
from dispatcher.dispatch_result import DispatchResult
from dispatcher.handlers.base import ActionEventBaseHandler
from dispatcher.device.messages.enum import (
    Scope,
    MessageType,
    MessageDirection,
    ActionResult,
)
from dispatcher.handlers.registry import register_action_event
from notifier.router_notifier_factory import router_notifier_factory
from redis_cache import redis_cache
from dispatcher.tasks import check_command_timeout


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.ACTION,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.BLINK,
)
class BlinkActionIntent(ActionEventBaseHandler):

    def __call__(self, message: CommandMessage) -> DispatchResult:
        device_message = action_event_intent_builder.build_intent(message)
        redis_cache.add_device_message(device_message)
        notifications = [
            router_notifier_factory.device_message(
                router_mac=message.peripheral.device.get_router_mac(),
                message=device_message,
            ),
        ]
        check_command_timeout.apply_async(
            args=(device_message.message_id,), countdown=30, queue="default"
        )
        return DispatchResult(
            notifications=notifications,
        )


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.ACTION,
    direction=MessageDirection.RESULT,
    handler_name=MessageCommand.BLINK,
)
class BlinkActionResult(ActionEventBaseHandler):

    def __call__(self, message: CommandMessage) -> DispatchResult:
        payload: BasicResult = message.payload
        if payload.status == ActionResult.REJECTED:
            return DispatchResult()

        device_message = redis_cache.get_and_delete_device_message(message.message_id)
        if not device_message:
            return DispatchResult()
        return DispatchResult()
