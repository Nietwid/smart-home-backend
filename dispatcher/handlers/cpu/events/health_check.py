from dispatcher.device.messages.builder.cpu import cpu_message_builder
from dispatcher.device.messages.enum import MessageCommand
from dispatcher.command_message.message import CommandMessage
from dispatcher.handlers.base import ActionEventBaseHandler
from dispatcher.dispatch_result import DispatchResult
from dispatcher.device.messages.enum import Scope, MessageType, MessageDirection
from dispatcher.handlers.registry import register_action_event
from notifier.router_notifier_factory import router_notifier_factory


@register_action_event(
    scope=Scope.CPU,
    message_type=MessageType.EVENT,
    direction=MessageDirection.INTENT,
    handler_name=MessageCommand.HEALTH_CHECK,
)
class HealthCheckEvent(ActionEventBaseHandler):
    def __call__(self, message: CommandMessage) -> DispatchResult:
        device = message.device
        return DispatchResult(
            notifications=[
                router_notifier_factory.device_message(
                    router_mac=device.get_router_mac(),
                    message=cpu_message_builder.health_check_response(message),
                ),
            ]
        )
