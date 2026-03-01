from consumers.device.messages.builder.action_event_intent import (
    action_event_intent_builder,
)
from consumers.device.messages.payload.basic import BasicResponse
from dispatcher.dispatch_result import DispatchResult
from consumers.device.messages.enum import MessageCommand
from dispatcher.command_message.message import CommandMessage
from dispatcher.handlers.base import ActionEventBaseHandler
from dispatcher.handlers.enums import Scope, MessageType, MessageDirection
from dispatcher.handlers.registry import register_action_event
from dispatcher.tasks import check_command_timeout
from notifier.frontend_notifier_factory import frontend_notifier_factory
from notifier.router_notifier_factory import router_notifier_factory
from redis_cache import redis_cache


@register_action_event(
    scope=Scope.CPU,
    message_type=MessageType.ACTION,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.UPDATE_PERIPHERAL,
)
class UpdatePeripheralActionIntent(ActionEventBaseHandler):
    def __call__(self, message: CommandMessage) -> DispatchResult:
        device_message = action_event_intent_builder.build_intent(message)
        redis_cache.save_device_message(device_message)
        pending = redis_cache.add_device_pending(message.device.pk, message.command)
        notifications = [
            router_notifier_factory.device_message(
                router_mac=message.device.get_router_mac(),
                message=device_message,
            ),
            frontend_notifier_factory.update_device_pending(
                home_id=message.device.home.id,
                pending=pending,
                device_id=message.device.pk,
            ),
        ]
        check_command_timeout.apply_async(
            args=(device_message.message_id,), countdown=30, queue="default"
        )
        return DispatchResult(notifications=notifications)


@register_action_event(
    scope=Scope.CPU,
    message_type=MessageType.ACTION,
    direction=MessageDirection.RESULT,
    handler_name=MessageCommand.UPDATE_PERIPHERAL,
)
class UpdatePeripheralActionResult(ActionEventBaseHandler):
    def __call__(self, message: CommandMessage) -> DispatchResult:
        payload: BasicResponse = message.payload
        if payload.status != "success":
            return DispatchResult()

        device_message = redis_cache.get_device_message_and_delete(message.message_id)
        if not device_message:
            return DispatchResult()

        pending = redis_cache.delete_device_pending(message.device.pk, message.command)
        home_id = message.device.home.id
        notifications = [
            frontend_notifier_factory.update_device_pending(
                home_id=home_id,
                pending=pending,
                device_id=message.device.pk,
            ),
        ]

        return DispatchResult(notifications=notifications)
