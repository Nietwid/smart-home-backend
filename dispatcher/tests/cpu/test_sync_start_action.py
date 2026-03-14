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
from dispatcher.device.messages.payload.basic import BasicResult
from dispatcher.device.messages.payload.enum import StartSyncType
from dispatcher.handlers.cpu.actions.sync_start import (
    SyncStartActionIntent,
    SyncStartActionResult,
)
from dispatcher.device.messages.payload.cpu import StartSyncPayload
from dispatcher.device.messages.enum import ActionResult
from rules.models import Rule


@pytest.fixture
def message_intent(device):
    return CommandMessage(
        scope=Scope.CPU,
        type=MessageType.ACTION,
        direction=MessageDirection.INTENT,
        command=MessageCommand.SYNC_START,
        home_id=1,
        router_mac="AA:BB:CC:DD:EE:FF",
        payload=StartSyncPayload(sync_type=StartSyncType.RULE),
        device=device,
        message_id="1234",
    )


@pytest.fixture
def message_result(device):
    return CommandMessage(
        scope=Scope.CPU,
        type=MessageType.ACTION,
        direction=MessageDirection.RESULT,
        command=MessageCommand.SYNC_START,
        home_id=1,
        router_mac="AA:BB:CC:DD:EE:FF",
        payload=BasicResult(status=ActionResult.ACCEPTED),
        device=device,
        message_id="1234",
    )


def test_sync_start_action(message_intent):
    # Given
    handler = SyncStartActionIntent()

    # When
    result = handler(message_intent)
    message_id = result.notifications[0].data.payload.message_id

    # Then
    assert len(result.notifications) == 2
    assert cache.get(CacheKey.device_message(message_id)) is not None
    assert MessageCommand.SYNC_START in cache.get(
        CacheKey.device_pending(message_intent.device.mac)
    )


def test_sync_start_action_result(message_intent, message_result, device):
    # Given
    Rule.objects.create(device=device, is_local=True)

    handler_intent = SyncStartActionIntent()
    handler_intent(message_intent)
    handler = SyncStartActionResult()

    # When
    result = handler(message_result)
