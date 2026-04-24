import pytest
from unittest.mock import MagicMock
from django.utils import timezone
from datetime import timedelta
from consumers.models import RouterInbox, MessageStatus
from model_bakery import baker

from dispatcher.tasks import process_device_message_task


@pytest.fixture
def mock_command_message_factory(mocker):
    return mocker.patch("dispatcher.tasks.command_message_factory")


@pytest.fixture
def action_event_command_processor(mocker):
    return mocker.patch("dispatcher.tasks.action_event_command_processor")


@pytest.mark.django_db(transaction=True)
def test_process_device_message_task_success(
    mocker, mock_command_message_factory, action_event_command_processor
):
    # Given
    home = baker.make("user.Home")
    payload = '{"direction":1, "peripheral_id":0, "device_id": "AA:BB:CC:DD:EE:FF", "scope": 1, "type": 1, "command": "device_connect", "payload": {"chip_type": "ESP32","wifi_strength":-20,"firmware_version":1.0}}'
    task = baker.make(
        RouterInbox,
        payload=payload,
        status=MessageStatus.PENDING,
        home_id=home.id,
        router_mac="ROUTER_MAC",
        expired_at=timezone.now() + timedelta(minutes=10),
    )
    mock_factory = mock_command_message_factory.return_value = MagicMock()

    # When
    process_device_message_task.run()

    # Then
    task.refresh_from_db()
    assert task.status == MessageStatus.PROCESSED
    assert action_event_command_processor.called
