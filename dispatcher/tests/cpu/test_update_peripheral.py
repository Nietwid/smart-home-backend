import pytest

from dispatcher.command_message.message import CommandMessage
from dispatcher.device.messages.enum import (
    Scope,
    MessageType,
    MessageDirection,
    MessageCommand,
)
from dispatcher.handlers.cpu.actions.update_peripheral import (
    UpdatePeripheralActionIntent,
)
from redis_cache import redis_cache


@pytest.fixture
def message(device_with_peripherals):
    return CommandMessage(
        scope=Scope.CPU,
        type=MessageType.ACTION,
        direction=MessageDirection.INTENT,
        command=MessageCommand.UPDATE_PERIPHERAL,
        home_id=1,
        router_mac="1234",
        payload={},
        device=device_with_peripherals,
    )


def test_update_peripheral(message):
    # Given
    handler = UpdatePeripheralActionIntent()

    # When
    result = handler(message)

    # Then
    assert len(result.notifications) == message.device.peripherals.count()
