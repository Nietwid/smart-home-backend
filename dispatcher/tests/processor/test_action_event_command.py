import pytest
from unittest.mock import MagicMock
from dispatcher.command_message.message import CommandMessage
from dispatcher.device.messages.enum import Scope, MessageType
from dispatcher.processor.action_event_command import (
    action_event_validator,
    action_event_command_processor,
)


@pytest.fixture
def mock_dispatcher(mocker):
    return mocker.patch(
        "dispatcher.processor.action_event_command.action_event_dispatcher.dispatch"
    )


@pytest.fixture
def mock_notifier(mocker):
    return mocker.patch("dispatcher.processor.action_event_command.notifier.notify")


@pytest.fixture
def mock_registry(mocker):
    return mocker.patch(
        "dispatcher.processor.action_event_command.HARDWARE_REGISTRY", {}
    )


@pytest.fixture
def mock_cpu_hardware(mocker):
    return mocker.patch("dispatcher.processor.action_event_command.CpuHardware")


@pytest.fixture
def mock_action_event_validator(mocker):
    return mocker.patch(
        "dispatcher.processor.action_event_command.action_event_validator"
    )


def test_validator_raises_error_on_missing_peripheral():
    # Given
    msg = MagicMock(spec=CommandMessage)
    msg.scope = Scope.PERIPHERAL
    msg.peripheral = None

    # When / Then
    with pytest.raises(ValueError, match="Peripheral is required"):
        action_event_validator(msg)


def test_validator_allows_valid_cpu_command(mocker, mock_cpu_hardware):
    msg = MagicMock(spec=CommandMessage)
    msg.scope = Scope.CPU
    msg.type = MessageType.ACTION
    msg.command = "RESTART"

    mock_cpu_hardware.get_available_actions.return_value = ["RESTART"]

    # When / Then
    action_event_validator(msg)


def test_validator_raises_error_on_invalid_command(mocker, mock_registry):
    # Given
    msg = MagicMock(spec=CommandMessage)
    msg.scope = Scope.PERIPHERAL
    msg.type = MessageType.ACTION
    msg.command = "EXPLODE"
    msg.peripheral = MagicMock()
    msg.peripheral.name = "LED_STRIP"

    mock_hw = MagicMock()
    mock_hw.get_available_actions.return_value = ["TURN_ON", "TURN_OFF"]
    mock_registry["LED_STRIP"] = mock_hw

    # When / Then
    with pytest.raises(ValueError, match="Invalid action: EXPLODE"):
        action_event_validator(msg)


def test_processor_executes_full_flow(
    mocker, mock_dispatcher, mock_notifier, mock_action_event_validator
):
    # Given
    msg = MagicMock(spec=CommandMessage)

    mock_dispatcher.return_value = ["success_msg"]

    # When
    action_event_command_processor(msg)

    # Then
    mock_dispatcher.assert_called_once_with(msg)
    mock_notifier.assert_called_once_with(["success_msg"])


def test_processor_stops_on_validation_error(
    mocker, mock_dispatcher, mock_action_event_validator
):
    # Given

    msg = MagicMock(spec=CommandMessage)

    mock_action_event_validator.side_effect = ValueError("Validation Failed")

    # When
    with pytest.raises(ValueError):
        action_event_command_processor(msg)

    # Then
    mock_dispatcher.assert_not_called()
