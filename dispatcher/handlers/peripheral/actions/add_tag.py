from peripherals.models import RfidCard
from dispatcher.command_message.message import CommandMessage
from dispatcher.device.messages.builder.action_event_intent import (
    action_event_intent_builder,
)
from dispatcher.device.messages.enum import (
    Scope,
    MessageType,
    MessageDirection,
    MessageCommand,
)
from dispatcher.dispatch_result import DispatchResult
from dispatcher.handlers.base import ActionEventBaseHandler
from dispatcher.handlers.registry import register_action_event
from dispatcher.tasks import check_command_timeout
from notifier.frontend_notifier_factory import frontend_notifier_factory
from notifier.frontend_notifier_payload import AddTagResultPayload
from notifier.router_notifier_factory import router_notifier_factory
from redis_cache import redis_cache
from dispatcher.device.messages.payload.rfid import AddTagResult, AddTagIntent


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.ACTION,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.ADD_TAG,
)
class AddTagActionIntent(ActionEventBaseHandler):
    def __call__(self, message: CommandMessage) -> DispatchResult:
        device_message = action_event_intent_builder.build_intent(message)
        print(f"{device_message=}")
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
            args=(device_message.message_id,), countdown=50, queue="default"
        )
        return DispatchResult(
            notifications=notifications,
        )


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.ACTION,
    direction=MessageDirection.RESULT,
    handler_name=MessageCommand.ADD_TAG,
)
class AddTagActionResult(ActionEventBaseHandler):
    def __call__(self, message: CommandMessage) -> DispatchResult:
        payload: AddTagResult = message.payload
        uid = payload.uid
        home_id = message.device.home.id
        old_message = redis_cache.get_and_delete_device_message(message.message_id)
        if not old_message:
            return DispatchResult()

        peripheral = message.peripheral
        device = peripheral.device
        pending = redis_cache.delete_peripheral_pending(peripheral.pk, message.command)
        notifications = [
            frontend_notifier_factory.update_peripheral_pending(
                home_id=home_id,
                device_id=device.pk,
                pending=pending,
                peripheral_id=peripheral.pk,
            )
        ]
        old_payload: AddTagIntent = old_message.payload
        if not uid:
            notifications.append(
                frontend_notifier_factory.add_tag_result(
                    home_id=home_id,
                    context=AddTagResultPayload(
                        status=400,
                        intent_id=old_payload.intent_id,
                        card_name=old_payload.name,
                        peripheral_id=peripheral.pk,
                    ),
                )
            )
        elif RfidCard.objects.filter(uid=uid).exists():
            notifications.append(
                frontend_notifier_factory.add_tag_result(
                    home_id=home_id,
                    context=AddTagResultPayload(
                        status=409,
                        intent_id=old_payload.intent_id,
                        card_name=old_payload.name,
                        peripheral_id=peripheral.pk,
                    ),
                )
            )
        else:
            card = RfidCard.objects.create(
                uid=uid,
                name=old_payload.name,
            )
            card.allowed_peripherals.add(peripheral)
            notifications.append(
                frontend_notifier_factory.add_tag_result(
                    home_id=home_id,
                    context=AddTagResultPayload(
                        status=201,
                        intent_id=old_payload.intent_id,
                        card_name=old_payload.name,
                        peripheral_id=peripheral.pk,
                    ),
                )
            )
        return DispatchResult(notifications=notifications)
