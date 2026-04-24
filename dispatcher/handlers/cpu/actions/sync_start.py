import logging

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
from dispatcher.tasks import check_command_timeout
from notifier.factory.frontend_notifier_factory import frontend_notifier_factory
from notifier.factory.router_notifier_factory import router_notifier_factory
from redis_cache import redis_cache
from rules.repository import RuleRepository

logger = logging.getLogger("base")


@register_action_event(
    scope=Scope.CPU,
    message_type=MessageType.ACTION,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.SYNC_START,
)
class SyncStartActionIntent(ActionEventBaseHandler):
    def __call__(self, message: CommandMessage) -> DispatchResult:
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
    handler_name=MessageCommand.SYNC_START,
)
class SyncStartActionResult(ActionEventBaseHandler):
    def __call__(self, message: CommandMessage) -> DispatchResult:
        payload: BasicResult = message.payload
        home_id = message.device.home.id
        intent_message = redis_cache.get_and_delete_device_message(message.message_id)
        if not intent_message:
            return DispatchResult()
        intent_payload: StartSyncPayload = intent_message.payload
        if payload.status == ActionResult.REJECTED:
            return DispatchResult(
                notifications=frontend_notifier_factory.display_toaster(
                    home_id=home_id,
                    message="Error syncing device. Please try again.",
                )
            )

        if intent_payload.sync_type == StartSyncType.PERIPHERAL:
            peripheral_ids = [p.id for p in message.device.peripherals.all()]
            redis_cache.add_device_update_peripherals_ids(
                peripheral_ids, message.device.mac
            )
            first_id = redis_cache.get_device_update_peripheral_id(message.device.mac)
            next_step_message = command_message_factory.update_peripheral(
                message.device, first_id
            )
            return DispatchResult(commands=[next_step_message])

        elif intent_payload.sync_type == StartSyncType.RULE:
            rule_ids = RuleRepository.get_local_ids(message.device.mac)
            redis_cache.add_sync_rule_ids(rule_ids, message.device.mac)
            first_id = redis_cache.get_sync_rule_id(message.device.mac)
            next_step_message = command_message_factory.update_rule(
                message.device, first_id
            )
            return DispatchResult(commands=[next_step_message])

        return DispatchResult(
            notifications=frontend_notifier_factory.display_toaster(
                home_id=home_id,
                message="Error syncing device. Please try again.",
            )
        )
