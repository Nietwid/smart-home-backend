from dispatcher.device.messages.builder.action_event_intent import (
    action_event_intent_builder,
)
from dispatcher.device.messages.enum import MessageCommand
from dispatcher.device.messages.payload.button import ToggleResult
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
from notifier.frontend_notifier_factory import frontend_notifier_factory
from notifier.router_notifier_factory import router_notifier_factory
from redis_cache import redis_cache
from dispatcher.tasks import check_command_timeout
import logging

logger = logging.getLogger(__name__)


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.ACTION,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.TOGGLE,
)
class ToggleActionIntent(ActionEventBaseHandler):

    def __call__(self, message: CommandMessage) -> DispatchResult:
        device_message = action_event_intent_builder.build_intent(message)
        logger.info(f"device_message: {device_message}")
        redis_cache.add_device_message(device_message)
        pending = redis_cache.add_peripheral_pending(
            message.peripheral.pk, message.command
        )

        notifications = [
            router_notifier_factory.device_message(
                router_mac=message.peripheral.device.get_router_mac(),
                message=device_message,
            ),
            frontend_notifier_factory.update_peripheral_pending(
                home_id=message.peripheral.device.home.id,
                pending=pending,
                device_id=message.peripheral.device.pk,
                peripheral_id=message.peripheral.pk,
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
    handler_name=MessageCommand.TOGGLE,
)
class ToggleActionResult(ActionEventBaseHandler):

    def __call__(self, message: CommandMessage) -> DispatchResult:
        payload: ToggleResult = message.payload
        device_message = redis_cache.get_and_delete_device_message(message.message_id)
        logger.info(f"device_message: {device_message}")

        if not device_message:
            return DispatchResult()
        message.peripheral.state["is_on"] = payload.is_on
        message.peripheral.save(update_fields=["state"])

        pending = redis_cache.delete_peripheral_pending(
            message.peripheral.pk, message.command
        )
        home_id = message.peripheral.device.home.id
        notifications = [
            frontend_notifier_factory.update_peripheral_state(
                home_id=home_id, state=message.peripheral.state
            ),
            frontend_notifier_factory.update_peripheral_pending(
                home_id=home_id,
                pending=pending,
                device_id=message.peripheral.device.pk,
                peripheral_id=message.peripheral.pk,
            ),
        ]

        if payload.status == ActionResult.REJECTED:
            notifications.append(
                frontend_notifier_factory.display_toaster(
                    home_id=home_id,
                    message=f"Unable to toggle peripheral on {message.peripheral.device.name}",
                )
            )
        return DispatchResult(notifications=notifications)
