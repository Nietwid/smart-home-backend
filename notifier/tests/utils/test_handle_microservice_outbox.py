from uuid import uuid4
import pytest
from unittest.mock import MagicMock
from consumers.models import RabbitOutbox
from notifier.utils.handle_microservice_outbox import handle_microservice_outbox


@pytest.fixture
def mock_send(mocker):
    return mocker.patch(
        "notifier.utils.handle_microservice_outbox.send_microservice_notification.delay"
    )


@pytest.mark.django_db
def test_handle_microservice_outbox_success(mock_send):
    # Given
    uuid = uuid4()
    msg_data = MagicMock()
    msg_data.data.message_id = uuid
    msg_data.exchange = "commands"
    msg_data.routing_key = "device.restart"
    msg_data.data.model_dump_json.return_value = '{"action": "restart"}'

    # When
    handle_microservice_outbox(msg_data)

    # Then
    outbox = RabbitOutbox.objects.get(external_id=uuid)
    assert outbox.exchange == "commands"
    assert outbox.routing_key == "device.restart"
    assert outbox.payload == '{"action": "restart"}'
    mock_send.assert_called_once()


@pytest.mark.django_db
def test_handle_microservice_outbox_duplicate_ignored(mock_send):
    # Given
    uuid = uuid4()
    msg_data = MagicMock()
    msg_data.data.message_id = uuid
    msg_data.exchange = "commands"
    msg_data.routing_key = "device.restart"
    msg_data.data.model_dump_json.return_value = '{"action": "restart"}'

    # When
    handle_microservice_outbox(msg_data)
    handle_microservice_outbox(msg_data)

    # Then
    assert RabbitOutbox.objects.filter(external_id=uuid).count() == 1
    assert mock_send.call_count == 1
