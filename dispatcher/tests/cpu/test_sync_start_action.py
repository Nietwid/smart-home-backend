import pytest
from django.core.cache import cache

from cache_key import CacheKey
from dispatcher.command_message.message import CommandMessage
from dispatcher.device.messages.enum import (
    Scope,
    MessageType,
    MessageDirection,
    MessageCommand,
)
from dispatcher.handlers.cpu.actions.sync_start import SyncStartActionIntent


@pytest.fixture
def message(device):
    return CommandMessage(
        scope=Scope.CPU,
        type=MessageType.ACTION,
        direction=MessageDirection.INTENT,
        command=MessageCommand.SYNC_START,
        home_id=1,
        router_mac="AA:BB:CC:DD:EE:FF",
        payload={},
        device=device,
    )


def test_sync_start_action(message):
    # Given
    handler = SyncStartActionIntent()

    # When
    result = handler(message)
    message_id = result.notifications[0].data.payload.message_id

    # Then
    assert len(result.notifications) == 2
    assert cache.get(CacheKey.device_message(message_id)) is not None
    assert MessageCommand.SYNC_START in cache.get(
        CacheKey.device_pending(message.device.pk)
    )
