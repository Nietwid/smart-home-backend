from consumers.device.messages.builder.action_event_intent import (
    action_event_intent_builder,
)
from consumers.device.messages.enum import MessageAction
from consumers.device.messages.payload.basic import BasicResponse
from consumers.frontend.messages.message import FrontendMessage
from consumers.frontend.messages.types import FrontendMessageType
from dispatcher.command_message.message import CommandMessage
from dispatcher.dispatch_result import DispatchResult
from dispatcher.handlers.base import ActionEventBaseHandler
from dispatcher.handlers.enums import Scope, MessageType, MessageDirection
from dispatcher.handlers.registry import register_action_event
from notifier.message import RouterNotifierData, FrontendNotifierData
from peripherals.serializers import PeripheralSerializer
from redis_cache import redis_cache


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
        notifications = [
            RouterNotifierData(
                router_mac=message.peripheral.device.get_router_mac(),
                data=device_message,
            )
        ]
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
        notifications = [
            FrontendNotifierData(
                home_id=message.peripheral.device.home.id,
                data=FrontendMessage(
                    action=FrontendMessageType.UPDATE_PERIPHERAL_STATE,
                    data=message.peripheral.state,
                ),
            )
        ]

        return DispatchResult(notifications=notifications)
