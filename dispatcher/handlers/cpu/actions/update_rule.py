import logging

from dispatcher.command_message.factory import command_message_factory
from dispatcher.device.messages.builder.cpu import cpu_message_builder
from dispatcher.device.messages.payload.basic import BasicResult
from dispatcher.device.messages.payload.cpu import (
    UpdatePeripheralIntentPayload,
    UpdateRuleIntentPayload,
)
from dispatcher.device.messages.payload.enum import StartSyncType
from dispatcher.dispatch_result import DispatchResult
from dispatcher.device.messages.enum import MessageCommand, ActionResult
from dispatcher.command_message.message import CommandMessage
from dispatcher.handlers.base import ActionEventBaseHandler
from dispatcher.device.messages.enum import Scope, MessageType, MessageDirection
from dispatcher.handlers.registry import register_action_event
from dispatcher.tasks import check_command_timeout
from notifier.frontend_notifier_factory import frontend_notifier_factory
from notifier.router_notifier_factory import router_notifier_factory
from peripherals.serializers import PeripheralSerializerDevice
from redis_cache import redis_cache
from rules.repository import RuleRepository
from rules.serializers.rule import RuleSerializerDevice

logger = logging.getLogger("base")


@register_action_event(
    scope=Scope.CPU,
    message_type=MessageType.ACTION,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.UPDATE_RULE,
)
class UpdateRuleActionIntent(ActionEventBaseHandler):
    def __call__(self, message: CommandMessage) -> DispatchResult:
        payload: UpdateRuleIntentPayload = message.payload
        rule_id = payload.rule_id

        # Get rule data
        data = RuleSerializerDevice(RuleRepository.get_rule(rule_id)).data

        # Prepare device messages
        device_message = cpu_message_builder.update_rule_intent(message, data)
        redis_cache.add_device_message(device_message)
        redis_cache.add_device_pending(message.device.mac, message.command)

        check_command_timeout.apply_async(
            args=(device_message.message_id,), countdown=30, queue="default"
        )
        router_mac = message.device.get_router_mac()

        # Prepare notifications to send
        notifications = [
            router_notifier_factory.device_message(
                router_mac=router_mac,
                message=device_message,
            )
        ]
        return DispatchResult(notifications=notifications)


@register_action_event(
    scope=Scope.CPU,
    message_type=MessageType.ACTION,
    direction=MessageDirection.RESULT,
    handler_name=MessageCommand.UPDATE_RULE,
)
class UpdateRuleActionResult(ActionEventBaseHandler):
    def __call__(self, message: CommandMessage) -> DispatchResult:
        payload: BasicResult = message.payload
        if payload.status == ActionResult.REJECTED:
            home_id = message.device.home.id
            return DispatchResult(
                notifications=frontend_notifier_factory.display_toaster(
                    home_id=home_id,
                    message="Error syncing device. Please try again.",
                )
            )
        device_mac = message.device.mac
        redis_cache.get_and_delete_device_message(message.message_id)
        redis_cache.delete_device_pending(device_mac, message.command)
        next_id = redis_cache.get_sync_rule_id(device_mac)

        logger.debug(f"next_id: {next_id}")

        if next_id:
            next_step_message = command_message_factory.update_rule(
                message.device, next_id
            )
        else:
            next_step_message = command_message_factory.sync_end(message.device)

        return DispatchResult(commands=[next_step_message])
