from consumers.router_message.device_message import DeviceMessage
from hardware.base import ActionHandler


class TurnOn(ActionHandler):

    @classmethod
    def handle_action(cls) -> None: ...

    @classmethod
    def handle_response(cls, message: DeviceMessage) -> None: ...
