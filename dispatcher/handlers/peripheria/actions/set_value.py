from consumers.device.messages.builder.action_event_intent import (
    action_event_intent_builder,
)
from consumers.device.messages.enum import MessageAction
from consumers.device.messages.payload.basic import BasicResponse
from dispatcher.command_message.message import CommandMessage
from dispatcher.dispatch_result import DispatchResult
from dispatcher.handlers.base import ActionEventBaseHandler
from dispatcher.handlers.enums import Scope, MessageType, MessageDirection
from dispatcher.handlers.registry import register_action_event
from notifier.frontend_notifier_factory import frontend_notifier_factory
from notifier.router_notifier_factory import router_notifier_factory
from peripherals.serializers import PeripheralSerializer
from redis_cache import redis_cache
from dispatcher.tasks import check_command_timeout
from django.core.cache import cache


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.ACTION,
    direction=MessageDirection.INTENT,
    handler_name=MessageAction.SET_VALUE,
)
class SetValueActionIntent(ActionEventBaseHandler):

    def __call__(self, message: CommandMessage) -> DispatchResult:
        serializer = PeripheralSerializer(
            data={
                "name": message.peripheral.name,
                "state": message.payload,
                "device": message.peripheral.device.pk,
            },
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        device_message = action_event_intent_builder.build_intent(message)

        redis_cache.save_device_message(device_message)
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
            args=(device_message.message_id,), queue="default"
        )
        print(f"{cache.keys("*")=}")
        return DispatchResult(
            notifications=notifications,
        )


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.ACTION,
    direction=MessageDirection.RESULT,
    handler_name=MessageAction.SET_VALUE,
)
class SetValueActionResult(ActionEventBaseHandler):

    def __call__(self, message: CommandMessage) -> DispatchResult:
        payload: BasicResponse = message.payload
        if payload.status != "success":
            return DispatchResult()

        device_message = redis_cache.get_device_message_and_delete(message.message_id)
        if not device_message:
            return DispatchResult()

        message.peripheral.state.update(device_message.payload)
        message.peripheral.state.save(update_fields=["state"])
        pending = redis_cache.delete_peripheral_pending(message.peripheral.pk)
        home_id = message.peripheral.device.home.id
        notifications = [
            frontend_notifier_factory.update_peripheral_state(
                home_id=home_id, state=message.peripheral.state
            ),
            frontend_notifier_factory.update_peripheral_pending(
                home_id=message.peripheral.device.home.id,
                pending=pending,
                device_id=message.peripheral.device.pk,
                peripheral_id=message.peripheral.pk,
            ),
        ]

        return DispatchResult(notifications=notifications)
