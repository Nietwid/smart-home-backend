import pytest
from dispatcher.device.messages.enum import Scope
from unittest.mock import MagicMock
from model_bakery import baker
from dispatcher.tasks import check_command_timeout


@pytest.fixture
def mock_redis(mocker):
    return mocker.patch("dispatcher.tasks.redis_cache")


@pytest.fixture
def mock_peripheral_repository(mocker):
    return mocker.patch("dispatcher.tasks.peripheral_repository")


@pytest.fixture
def mock_notify(mocker):
    return mocker.patch("dispatcher.tasks.notifier.notify")


@pytest.mark.django_db
def test_check_command_timeout_peripheral(
    mocker, mock_redis, mock_peripheral_repository, mock_notify, device_with_peripherals
):
    # Given
    msg_id = "test-msg-id"
    mock_msg = MagicMock()
    mock_msg.scope = Scope.PERIPHERAL
    mock_msg.peripheral_id = 1
    mock_msg.command = "TURN_ON"

    mock_redis.get_and_delete_device_message.return_value = mock_msg
    mock_redis.delete_peripheral_pending.return_value = []
    mock_peripheral_repository.get_by_id_with_device.return_value = (
        device_with_peripherals.peripherals.first()
    )

    # When

    check_command_timeout.run(msg_id)

    # Then
    notifications = mock_notify.call_args[0][0]
    assert any("unreachable" in str(n) for n in notifications)
