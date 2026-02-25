from consumers.router_message.message_event import MessageEvent
from device.models import Device
from dispatcher.base import ActionEventBaseHandler
from dispatcher.command_message import CommandMessage
from dispatcher.dispatch_result import DispatchResult
from notifier.message import NotifierMessage


class OnClickEvent(ActionEventBaseHandler):

    def __call__(self, message: CommandMessage) -> DispatchResult:
        """
        Handle the incoming request for a click event.
        """
        device: Device = message.device
        return DispatchResult(commands=device.get_event_request(MessageEvent.ON_CLICK))


class OnClickEventResponseHandler(ActionEventBaseHandler):

    def __call__(self, message: CommandMessage) -> DispatchResult:
        """
        Handle the response from the device for a click event.
        """
        # Process the response as needed
        return DispatchResult()
