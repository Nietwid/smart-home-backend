import pytest

from dispatcher.command_message.message import CommandMessage
from dispatcher.device.messages.enum import (
    Scope,
    MessageType,
    MessageDirection,
    MessageCommand,
)
from dispatcher.device.messages.payload.cpu import UpdateRuleIntentPayload
from dispatcher.handlers.cpu.actions.update_rule import UpdateRuleActionIntent
from rules.models import Rule


@pytest.fixture
def rule(device):
    return Rule.objects.create(device=device, is_local=True)


@pytest.fixture
def message_intent(device, rule):
    return CommandMessage(
        scope=Scope.CPU,
        type=MessageType.ACTION,
        direction=MessageDirection.RESULT,
        command=MessageCommand.UPDATE_RULE,
        home_id=1,
        router_mac="AA:BB:CC:DD:EE:FF",
        payload=UpdateRuleIntentPayload(rule_id=rule.pk),
        device=device,
        message_id="1234",
    )


def test_update_rule_action(message_intent):
    # Given
    handler = UpdateRuleActionIntent()

    # When
    result = handler(message_intent)
    print(result)
    # Then
