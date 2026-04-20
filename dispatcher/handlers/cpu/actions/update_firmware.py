import logging
from uuid import uuid4
from device.models import Device
from dispatcher.command_message.factory import command_message_factory
from dispatcher.device.messages.builder.action_event_intent import (
    action_event_intent_builder,
)
from dispatcher.device.messages.builder.cpu import cpu_message_builder
from dispatcher.device.messages.payload.basic import BasicResult
from dispatcher.dispatch_result import DispatchResult
from dispatcher.device.messages.enum import MessageCommand, ActionResult
from dispatcher.command_message.message import CommandMessage
from dispatcher.handlers.base import ActionEventBaseHandler
from dispatcher.device.messages.enum import Scope, MessageType, MessageDirection
from dispatcher.handlers.registry import register_action_event
from firmware.models import FirmwareDevice
from notifier.frontend_notifier_factory import frontend_notifier_factory
from notifier.router_notifier_factory import router_notifier_factory
from redis_cache import redis_cache

logger = logging.getLogger("base")


@register_action_event(
    scope=Scope.CPU,
    message_type=MessageType.ACTION,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.UPDATE_FIRMWARE,
)
class SyncEndActionIntent(ActionEventBaseHandler):
    def __call__(self, message: CommandMessage) -> DispatchResult:
        firmware_name = message.device.chip_type
        firmware = (
            FirmwareDevice.objects.filter(to_device=firmware_name)
            .order_by("-version")
            .first()
        )
        if not firmware:
            return DispatchResult()
        token = uuid4().hex
        device_message = cpu_message_builder.update_firmware_intent(
            message, token, firmware_name, firmware.version
        )
        redis_cache.add_device_message(device_message)
        redis_cache.add_update_firmware(token, firmware.pk)
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
    handler_name=MessageCommand.UPDATE_FIRMWARE,
)
class SyncEndActionResult(ActionEventBaseHandler):
    def __call__(self, message: CommandMessage) -> DispatchResult:
        payload: BasicResult = message.payload
        old_message = redis_cache.get_and_delete_device_message(message.message_id)
        if not old_message:
            return DispatchResult()

        device: Device = message.device
        home_id = device.home.id

        if payload.status == ActionResult.REJECTED:
            return DispatchResult(
                notifications=frontend_notifier_factory.display_toaster(
                    home_id=home_id,
                    message="Error updating device. Please try again.",
                )
            )
        # TODO - update required action
        # device.required_action.append(MessageCommand.UPDATE_FIRMWARE)
        # device.save(update_fields=["required_action"])
        # notifications = [
        #     frontend_notifier_factory.update_device_required_action(
        #         device.home.pk, device.required_action, device.pk
        #     )
        # ]
        # return DispatchResult(notifications=notifications)
        return DispatchResult()
