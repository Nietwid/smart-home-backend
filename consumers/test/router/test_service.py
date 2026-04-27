from django.utils import timezone
import pytest
from uuid import uuid4
from consumers.router.service import RouterService
from consumers.router.message.message import AckRouterMessage, DeviceRouterMessage
from consumers.models import RouterOutbox, MessageStatus, RouterInbox


@pytest.fixture
def mock_notifier(mocker):
    return mocker.patch("consumers.router.service.notifier.notify")


@pytest.fixture
def mock_tasks(mocker):
    return {
        "deactivate": mocker.patch(
            "consumers.router.service.deactivate_all_device.delay"
        ),
        "process_msg": mocker.patch(
            "consumers.router.service.process_device_message_task.delay"
        ),
    }


def test_handle_connect_success(db, router):
    # Given
    result = RouterService.handle_connect(router.mac)

    # Then
    assert result is not None
    assert result.is_online is True
    assert result.last_seen is not None


def test_handle_disconnect(db, router, mock_tasks):
    # Given
    service = RouterService(router)

    # When
    service.handle_disconnect()

    # Then
    router.refresh_from_db()
    assert router.is_online is False
    mock_tasks["deactivate"].assert_called_once_with(router.pk)


def test_handle_device_message_new_packet(
    db, router, mock_notifier, mock_tasks, mocker
):
    # Given
    uuid = uuid4()
    service = RouterService(router)
    payload = mocker.Mock()
    payload.model_dump_json.return_value = '{"temp": 22}'
    packet = DeviceRouterMessage.model_construct(message_id=uuid, payload=payload)

    # When
    service.handle_device_message(packet)

    # Then
    assert RouterInbox.objects.filter(external_id=uuid).exists()
    assert mock_notifier.called
    mock_tasks["process_msg"].assert_called_once()


def test_handle_device_message_duplicate_packet(
    db, router, mock_notifier, mock_tasks, mocker
):
    # Given
    uuid = uuid4()
    RouterInbox.objects.create(
        router_mac=router.mac,
        external_id=uuid,
        home_id=router.home.pk,
        payload="{}",
        expired_at=timezone.now(),
    )

    service = RouterService(router)
    payload = mocker.Mock()
    payload.model_dump_json.return_value = "{}"
    packet = DeviceRouterMessage.model_construct(message_id=uuid, payload=payload)

    # When
    service.handle_device_message(packet)

    # Then
    mock_tasks["process_msg"].assert_not_called()


def test_handle_ack_received_updates_status(db, router, mocker):
    # Given
    uuid = uuid4()
    outbox = RouterOutbox.objects.create(
        external_id=uuid, router_mac=router.mac, payload={}, expired_at=timezone.now()
    )
    packet = AckRouterMessage(message_id=uuid)
    service = RouterService(router)

    # When
    service.handle_ack_received(packet)

    # Then
    outbox.refresh_from_db()
    assert outbox.status == MessageStatus.DELIVERED


def test_handle_ack_received_ignores_missing_message(db, router, mocker):
    # Given
    packet = AckRouterMessage(message_id=uuid4())
    service = RouterService(router)

    # When
    service.handle_ack_received(packet)

    # Then
    pass
