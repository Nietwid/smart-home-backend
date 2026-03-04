import logging

from dispatcher.device.messages.builder.action_event_intent import (
    action_event_intent_builder,
)
from dispatcher.device.messages.payload.basic import BasicResult
from dispatcher.dispatch_result import DispatchResult
from dispatcher.device.messages.enum import MessageCommand, ActionResult
from dispatcher.command_message.message import CommandMessage
from dispatcher.handlers.base import ActionEventBaseHandler
from dispatcher.device.messages.enum import Scope, MessageType, MessageDirection
from dispatcher.handlers.registry import register_action_event
from dispatcher.tasks import check_command_timeout
from notifier.frontend_notifier_factory import frontend_notifier_factory
from notifier.router_notifier_factory import router_notifier_factory
from redis_cache import redis_cache

logger = logging.getLogger("base")


@register_action_event(
    scope=Scope.CPU,
    message_type=MessageType.ACTION,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.RESTART,
)
class RestartActionIntent(ActionEventBaseHandler):
    def __call__(self, message: CommandMessage) -> DispatchResult:
        logger.debug(f"{message}")
        device_message = action_event_intent_builder.build_intent(message)
        redis_cache.add_device_message(device_message)
        pending = redis_cache.add_device_pending(message.device.mac, message.command)
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
    handler_name=MessageCommand.RESTART,
)
class RestartActionResult(ActionEventBaseHandler):
    def __call__(self, message: CommandMessage) -> DispatchResult:
        logger.debug(f"{message}")
        payload: BasicResult = message.payload
        if payload.status != ActionResult.ACCEPTED:
            redis_cache.get_and_delete_device_message(message.message_id)
            return DispatchResult()
        pending = redis_cache.delete_device_pending(message.device.pk, message.command)
        home_id = message.device.home.id
        logger.debug(f"{pending}")
        return DispatchResult(
            notifications=[
                frontend_notifier_factory.update_device_pending(
                    home_id=home_id,
                    pending=pending,
                    device_id=message.device.pk,
                ),
                frontend_notifier_factory.display_toaster(
                    home_id=home_id,
                    message="Peripheral has beed updated. Device will restart in 10s",
                ),
            ]
        )
