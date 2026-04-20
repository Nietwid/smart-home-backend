from dispatcher.device.messages.enum import MessageCommand
from dispatcher.handlers.base import EventIntentBaseHandler
from dispatcher.device.messages.enum import Scope, MessageType, MessageDirection
from dispatcher.handlers.registry import register_action_event
from notifier.enum import MicroserviceQueueName
from peripherals.models import Peripherals
from peripherals.serializers.peripheral import PeripheralSerializer


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.EVENT,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.ON_UPDATE_STATE,
)
class OnUpdateStateHandler(EventIntentBaseHandler):
    send_command = False
    update_frontend_peripheral_state = True
    history_queue = MicroserviceQueueName.EVENTS

    def update_peripheral_state(self, peripheral: Peripherals, state: dict) -> None:
        serializer = PeripheralSerializer(
            data={
                "name": peripheral.name,
                "state": state,
                "device": peripheral.device.pk,
            },
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        clean_state = serializer.validated_data.get("state", {})
        if clean_state:
            peripheral.state.update(clean_state)
            peripheral.save(update_fields=["state"])
