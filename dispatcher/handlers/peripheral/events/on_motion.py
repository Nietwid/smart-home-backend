from dispatcher.device.messages.enum import MessageCommand
from dispatcher.device.messages.payload.sensor import OnMotionIntent
from dispatcher.handlers.base import EventIntentBaseHandler
from dispatcher.device.messages.enum import Scope, MessageType, MessageDirection
from dispatcher.handlers.registry import register_action_event
from notifier.enum import RabbitExchange, RabbitRoutingKey
from peripherals.models import Peripherals


@register_action_event(
    scope=Scope.PERIPHERAL,
    message_type=MessageType.EVENT,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.ON_MOTION,
)
class OnClickEventIntentHandler(EventIntentBaseHandler):
    exchange = RabbitExchange.SENSOR_SERVICE
    routing_key = RabbitRoutingKey.EVENTS
    update_frontend_peripheral_state = True

    def update_peripheral_state(self, peripheral: Peripherals, state: OnMotionIntent):
        peripheral.state.update({"is_on": state.is_on})
        peripheral.save(update_fields=["state"])
