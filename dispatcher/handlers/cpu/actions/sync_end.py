import logging

from device.models import Device
from dispatcher.command_message.factory import command_message_factory
from dispatcher.device.messages.builder.action_event_intent import (
    action_event_intent_builder,
)
from dispatcher.device.messages.payload.basic import BasicResult
from dispatcher.device.messages.payload.cpu import StartSyncPayload
from dispatcher.device.messages.payload.enum import StartSyncType
from dispatcher.dispatch_result import DispatchResult
from dispatcher.device.messages.enum import MessageCommand, ActionResult
from dispatcher.command_message.message import CommandMessage
from dispatcher.handlers.base import ActionEventBaseHandler
from dispatcher.device.messages.enum import Scope, MessageType, MessageDirection
from dispatcher.handlers.registry import register_action_event
from notifier.frontend_notifier_factory import frontend_notifier_factory
from notifier.router_notifier_factory import router_notifier_factory
from redis_cache import redis_cache

logger = logging.getLogger("base")


@register_action_event(
    scope=Scope.CPU,
    message_type=MessageType.ACTION,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.SYNC_END,
)
class SyncEndActionIntent(ActionEventBaseHandler):
    def __call__(self, message: CommandMessage) -> DispatchResult:
        device_message = action_event_intent_builder.build_intent(message)
        redis_cache.add_device_message(device_message)
        notifications = [
            router_notifier_factory.device_message(
                router_mac=message.device.get_router_mac(),
                message=device_message,
            ),
        ]
        return DispatchResult(notifications=notifications)


@register_action_event(
    scope=Scope.CPU,
    message_type=MessageType.ACTION,
    direction=MessageDirection.RESULT,
    handler_name=MessageCommand.SYNC_END,
)
class SyncEndActionResult(ActionEventBaseHandler):
    def __call__(self, message: CommandMessage) -> DispatchResult:
        payload: BasicResult = message.payload
        old_message = redis_cache.get_and_delete_device_message(message.message_id)
        device: Device = message.device
        home_id = device.home.id
        if payload.status == ActionResult.REJECTED:
            return DispatchResult(
                notifications=frontend_notifier_factory.display_toaster(
                    home_id=home_id,
                    message="Error syncing device. Please try again.",
                )
            )
        pending = redis_cache.delete_device_pending(
            device.pk, MessageCommand.SYNC_START
        )
        notifications = [
            frontend_notifier_factory.update_device_pending(
                home_id=home_id,
                pending=pending,
                device_id=device.pk,
            )
        ]
        old_payload: StartSyncPayload = old_message.payload
        if old_payload.sync_type == StartSyncType.PERIPHERAL:
            if MessageCommand.UPDATE_PERIPHERAL in device.required_action:
                device.required_action.remove(MessageCommand.UPDATE_PERIPHERAL)
                device.save(update_fields=["required_action"])
                notifications.append(
                    frontend_notifier_factory.update_device_required_action(
                        home_id=home_id,
                        actions=device.required_action,
                        device_id=device.pk,
                    )
                )
        next_step_message = command_message_factory.restart(device)
        return DispatchResult(notifications=notifications, commands=[next_step_message])
