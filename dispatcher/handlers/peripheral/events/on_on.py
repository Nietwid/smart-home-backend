from dispatcher.device.messages.enum import MessageCommand
from dispatcher.handlers.base import EventIntentBaseHandler
from dispatcher.device.messages.enum import Scope, MessageType, MessageDirection
from dispatcher.handlers.registry import register_action_event
from notifier.enum import MicroserviceQueueName
from peripherals.models import Peripherals


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.EVENT,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.ON_ON,
)
class OnOnEventHandler(EventIntentBaseHandler):
    update_frontend_peripheral_state = True
    history_queue = MicroserviceQueueName.EVENTS

    def update_peripheral_state(self, peripheral: Peripherals, state: dict) -> None:
        peripheral.state.update({"is_on": True})
        peripheral.save(update_fields=["state"])
