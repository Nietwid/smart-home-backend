from dispatcher.device.messages.enum import MessageCommand
from dispatcher.command_message.message import CommandMessage
from dispatcher.device.messages.payload.lamp import OnBlinkPayload, OnBlinkStatus
from dispatcher.dispatch_result import DispatchResult
from dispatcher.handlers.base import ActionEventBaseHandler
from dispatcher.device.messages.enum import (
    Scope,
    MessageType,
    MessageDirection,
)
from dispatcher.handlers.registry import register_action_event
from notifier.frontend_notifier_factory import frontend_notifier_factory
from redis_cache import redis_cache
from dispatcher.tasks import check_peripheral_pending


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.EVENT,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.ON_BLINK,
)
class UpdateStateActionIntent(ActionEventBaseHandler):

    def __call__(self, message: CommandMessage) -> DispatchResult:
        payload: OnBlinkPayload = message.payload
        if payload.status == OnBlinkStatus.START:
            pending = redis_cache.add_peripheral_pending(
                message.peripheral.pk, message.command, timeout=90
            )
            check_peripheral_pending.apply_async(
                args=(
                    message.peripheral.pk,
                    message.command,
                ),
                countdown=60,
                queue="default",
            )
        elif payload.status == OnBlinkStatus.STOP:
            pending = redis_cache.delete_peripheral_pending(
                message.peripheral.pk, message.command
            )
        else:
            raise ValueError(f"Invalid status: {payload.status}")

        notifications = [
            frontend_notifier_factory.update_peripheral_pending(
                home_id=message.peripheral.device.home.id,
                pending=pending,
                device_id=message.peripheral.device.pk,
                peripheral_id=message.peripheral.pk,
            ),
        ]
        return DispatchResult(
            notifications=notifications,
        )
