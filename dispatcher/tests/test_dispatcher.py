from consumers.device.messages.enum import MessageEvent
from dispatcher.dispatcher import ActionEventDispatcher
from unittest.mock import Mock

from dispatcher.enums import Scope, MessageType, MessageDirection


class FakeResult:
    def __init__(self, notifications=None, commands=None):
        self.notifications = notifications or []
        self.commands = commands or []


def test_dispatch_calls_handler():
    # given
    message = Mock()
    message.scope = Scope.CPU
    message.type = MessageType.EVENT
    message.direction = MessageDirection.INTENT
    message.command = MessageEvent.DEVICE_CONNECT

    handler = Mock(return_value=FakeResult(notifications=["n1"]))

    registry = {
        (
            Scope.CPU,
            MessageType.EVENT,
            MessageDirection.INTENT,
            MessageEvent.DEVICE_CONNECT,
        ): handler
    }

    dispatcher = ActionEventDispatcher(registry)

    # when
    result = dispatcher.dispatch(message)

    # then
    handler.assert_called_once_with(message)
    assert result == ["n1"]


def test_dispatch_recursively_dispatches_nested_commands():
    # given
    root_message = Mock()
    root_message.scope = Scope.CPU
    root_message.type = MessageType.EVENT
    root_message.direction = MessageDirection.INTENT
    root_message.command = MessageEvent.DEVICE_CONNECT

    nested_message = Mock()
    nested_message.scope = Scope.CPU
    nested_message.type = MessageType.EVENT
    nested_message.direction = MessageDirection.INTENT
    nested_message.command = MessageEvent.DEVICE_DISCONNECT

    root_handler = Mock(
        return_value=FakeResult(
            notifications=["root_notification"], commands=[nested_message]
        )
    )

    nested_handler = Mock(
        return_value=FakeResult(notifications=["nested_notification"], commands=[])
    )

    registry = {
        (
            Scope.CPU,
            MessageType.EVENT,
            MessageDirection.INTENT,
            MessageEvent.DEVICE_CONNECT,
        ): root_handler,
        (
            Scope.CPU,
            MessageType.EVENT,
            MessageDirection.INTENT,
            MessageEvent.DEVICE_DISCONNECT,
        ): nested_handler,
    }

    dispatcher = ActionEventDispatcher(registry)

    # when
    result = dispatcher.dispatch(root_message)

    # then
    assert result == ["root_notification", "nested_notification"]
