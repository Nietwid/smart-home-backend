from hardware.base import ActionHandler
from consumers.router_message.device_message import DeviceMessage


class SetValue(ActionHandler):

    @classmethod
    def handle_action(cls) -> None: ...

    @classmethod
    def handle_response(cls, message: DeviceMessage) -> None: ...
