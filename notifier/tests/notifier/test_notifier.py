import pytest
from unittest.mock import MagicMock
from notifier.enum import Destinations
from consumers.router.message.enum import RouterMessageType
from notifier.message import RouterNotifierData
from notifier.message import FrontendNotifierData
from notifier.notifier import notifier


@pytest.fixture
def mock_messengers(mocker):
    return {
        "router": mocker.patch("notifier.notifier.router_messenger.send"),
        "frontend": mocker.patch("notifier.notifier.frontend_messenger.send"),
        "router_outbox": mocker.patch("notifier.notifier.handle_router_outbox"),
        "micro_outbox": mocker.patch("notifier.notifier.handle_microservice_outbox"),
    }


def test_notify_router_device_goes_to_outbox(mock_messengers):
    # Given
    msg = MagicMock(spec=RouterNotifierData)
    msg.destination = Destinations.ROUTER
    msg.data = MagicMock()
    msg.data.target = RouterMessageType.DEVICE

    # When
    notifier.notify([msg])

    # Then
    mock_messengers["router_outbox"].assert_called_once_with(msg)
    mock_messengers["router"].assert_not_called()


def test_notify_router_non_device_goes_to_messenger(mock_messengers):
    # Given
    msg = MagicMock(spec=RouterNotifierData)
    msg.destination = Destinations.ROUTER
    msg.data = MagicMock()
    msg.data.target = "SYSTEM"
    msg.router_mac = "AA:BB:CC"

    # When
    notifier.notify([msg])

    # Then
    mock_messengers["router"].assert_called_once_with("AA:BB:CC", msg.data)
    mock_messengers["router_outbox"].assert_not_called()


def test_notify_frontend_routing(mock_messengers):
    # Given
    msg = MagicMock(spec=FrontendNotifierData)
    msg.destination = Destinations.FRONTEND
    msg.home_id = 10

    # When
    notifier.notify([msg])

    # Then
    mock_messengers["frontend"].assert_called_once_with(10, msg)
