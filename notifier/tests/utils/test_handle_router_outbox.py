import pytest
from unittest.mock import MagicMock
from consumers.models import RouterOutbox
from notifier.utils.handle_router_outbox import handle_router_outbox
from uuid import uuid4


@pytest.fixture
def mock_task(mocker):
    return mocker.patch(
        "notifier.utils.handle_router_outbox.process_router_outbox_task.delay"
    )


@pytest.mark.django_db
def test_handle_router_outbox_creates_record_and_calls_task(mock_task):
    # Given
    uuid = uuid4()
    message_data = MagicMock()
    message_data.router_mac = "AA:BB:CC:DD:EE:FF"
    message_data.data.message_id = uuid
    message_data.data.payload.model_dump_json.return_value = '{"test": "data"}'

    # When
    handle_router_outbox(message_data)

    # Then
    outbox_item = RouterOutbox.objects.get(external_id=uuid)
    assert outbox_item.router_mac == "AA:BB:CC:DD:EE:FF"
    assert outbox_item.payload == '{"test": "data"}'
    mock_task.assert_called_once()


@pytest.mark.django_db
def test_handle_router_outbox_is_idempotent(mock_task):
    # Given
    uuid = uuid4()
    message_data = MagicMock()
    message_data.router_mac = "AA:BB:CC:DD:EE:FF"
    message_data.data.message_id = uuid
    message_data.data.payload.model_dump_json.return_value = "{}"

    # When
    handle_router_outbox(message_data)
    assert RouterOutbox.objects.count() == 1
    assert mock_task.call_count == 1

    handle_router_outbox(message_data)

    # Then
    assert RouterOutbox.objects.count() == 1
    assert mock_task.call_count == 1
