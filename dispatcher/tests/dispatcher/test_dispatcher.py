import pytest
from unittest.mock import MagicMock
from dispatcher.device.messages.enum import (
    Scope,
    MessageType,
    MessageDirection,
    MessageCommand,
)
from dispatcher.dispatcher import ActionEventDispatcher
from notifier.message import NotifierMessage


@pytest.fixture
def mock_handler():
    handler = MagicMock()
    handler.return_value = MagicMock(notifications=[], commands=[])
    return handler


def test_dispatch_calls_correct_handler(mock_handler):
    # Given
    key = (
        Scope.CPU,
        MessageType.ACTION,
        MessageDirection.INTENT,
        MessageCommand.RESTART,
    )
    registry = {key: mock_handler}
    dispatcher = ActionEventDispatcher(registry)

    message = MagicMock()
    message.scope, message.type, message.direction, message.command = key

    # When
    dispatcher.dispatch(message)

    # Then
    mock_handler.assert_called_once_with(message)


def test_dispatch_returns_empty_on_missing_handler(caplog):
    # Given
    dispatcher = ActionEventDispatcher({})
    message = MagicMock(
        scope=Scope.CPU,
        type=MessageType.ACTION,
        direction=MessageDirection.INTENT,
        command=MessageCommand.RESTART,
    )

    # When
    result = dispatcher.dispatch(message)

    # Then
    assert result == []
    assert "No handler registered" in caplog.text


def test_recursive_dispatch(mocker):
    # Given

    msg_1 = MagicMock(
        scope=Scope.CPU,
        type=MessageType.ACTION,
        direction=MessageDirection.INTENT,
        command=MessageCommand.SYNC_START,
    )
    msg_2 = MagicMock(
        scope=Scope.CPU,
        type=MessageType.ACTION,
        direction=MessageDirection.INTENT,
        command=MessageCommand.SYNC_END,
    )

    n1 = MagicMock(spec=NotifierMessage)
    n2 = MagicMock(spec=NotifierMessage)

    handler_1 = MagicMock(return_value=MagicMock(notifications=[n1], commands=[msg_2]))
    handler_2 = MagicMock(return_value=MagicMock(notifications=[n2], commands=[]))

    registry = {
        (
            Scope.CPU,
            MessageType.ACTION,
            MessageDirection.INTENT,
            MessageCommand.SYNC_START,
        ): handler_1,
        (
            Scope.CPU,
            MessageType.ACTION,
            MessageDirection.INTENT,
            MessageCommand.SYNC_END,
        ): handler_2,
    }

    dispatcher = ActionEventDispatcher(registry)

    # When
    all_notifications = dispatcher.dispatch(msg_1)

    # Then
    assert len(all_notifications) == 2
    assert n1 in all_notifications
    assert n2 in all_notifications
    handler_2.assert_called_once_with(msg_2)
