from unittest.mock import Mock, patch, MagicMock
import pytest

from consumers.events.state_change import StateChange, light_state_change
from consumers.router_message.device_message import DeviceMessage
from consumers.device.messages.device_state import DeviceState
from consumers.router_message.message_event import MessageEvent
from consumers.router_message.message_type import MessageType
from consumers.rabbitmq_publisher import QueueNames


@patch("consumers.events.state_change.get_publisher")
@patch("consumers.events.state_change.FrontendMessenger")
def test_light_state_change_on(frontend_mock, publisher_mock, light):
    """Test turning device state to ON"""
    mock_publisher = MagicMock()
    publisher_mock.return_value = mock_publisher

    message = DeviceMessage(
        message_type=MessageType.REQUEST,
        message_event=MessageEvent.STATE_CHANGE,
        device_id=light.mac,
        message_id="1",
        payload={"state": DeviceState.ON},
    )

    light_state_change(light.pk, message)

    # Assert device state was updated to ON
    light.refresh_from_db()
    assert light.on is True

    # Assert frontend messenger was called once with correct home_id
    frontend_mock.return_value.update_frontend.assert_called_once()
    call_args = frontend_mock.return_value.update_frontend.call_args
    assert call_args[0][0] == light.home.pk

    # Assert message was sent to microservice queue
    mock_publisher.send_message.assert_called_once()
    call_args = mock_publisher.send_message.call_args
    assert call_args[0][0] == QueueNames.SENSORS


@patch("consumers.events.state_change.get_publisher")
@patch("consumers.events.state_change.FrontendMessenger")
def test_light_state_change_off(frontend_mock, publisher_mock, light):
    """Test turning device state to OFF"""
    # Setup: device is initially ON
    light.on = True
    light.save()

    mock_publisher = MagicMock()
    publisher_mock.return_value = mock_publisher

    message = DeviceMessage(
        message_type=MessageType.REQUEST,
        message_event=MessageEvent.STATE_CHANGE,
        device_id=light.mac,
        message_id="2",
        payload={"state": DeviceState.OFF},
    )

    light_state_change(light.pk, message)

    # Assert device state was updated to OFF
    light.refresh_from_db()
    assert light.on is False

    # Assert frontend received the update
    frontend_mock.return_value.update_frontend.assert_called_once()

    # Assert message was published to RabbitMQ
    mock_publisher.send_message.assert_called_once()


@patch("consumers.events.state_change.get_publisher")
@patch("consumers.events.state_change.FrontendMessenger")
def test_light_state_change_sends_correct_data_to_frontend(
    frontend_mock, publisher_mock, light
):
    """Test that frontend receives correct serialized device data"""
    mock_publisher = MagicMock()
    publisher_mock.return_value = mock_publisher

    message = DeviceMessage(
        message_type=MessageType.REQUEST,
        message_event=MessageEvent.STATE_CHANGE,
        device_id=light.mac,
        message_id="3",
        payload={"state": DeviceState.ON},
    )

    light_state_change(light.pk, message)

    # Assert frontend received the serialized device data
    frontend_mock.return_value.update_frontend.assert_called_once()
    call_args = frontend_mock.return_value.update_frontend.call_args

    home_id = call_args[0][0]
    device_data = call_args[0][1]

    assert home_id == light.home.pk
    assert device_data["id"] == light.pk
    assert device_data["on"] is True


@patch("consumers.events.state_change.get_publisher")
@patch("consumers.events.state_change.FrontendMessenger")
def test_state_change_handle_request_light(frontend_mock, publisher_mock, light):
    """Test StateChange.handle_request processes light device correctly"""
    mock_publisher = MagicMock()
    publisher_mock.return_value = mock_publisher
    mock_consumer = Mock()

    instance = StateChange()
    message = DeviceMessage(
        message_type=MessageType.REQUEST,
        message_event=MessageEvent.STATE_CHANGE,
        device_id=light.mac,
        message_id="1",
        payload={"state": DeviceState.ON},
    )

    instance.handle_request(mock_consumer, message)

    # Assert light_state_change was executed and device was updated
    light.refresh_from_db()
    assert light.on is True
    frontend_mock.return_value.update_frontend.assert_called_once()
    mock_publisher.send_message.assert_called_once()


@pytest.mark.django_db
@patch("consumers.events.state_change.get_publisher")
@patch("consumers.events.state_change.FrontendMessenger")
def test_state_change_handle_request_device_not_found(frontend_mock, publisher_mock):
    """Test StateChange gracefully handles non-existent device"""
    mock_consumer = Mock()
    instance = StateChange()

    message = DeviceMessage(
        message_type=MessageType.REQUEST,
        message_event=MessageEvent.STATE_CHANGE,
        device_id="FF:FF:FF:FF:FF:FF",  # Non-existent MAC address
        message_id="1",
        payload={"state": DeviceState.ON},
    )

    # Should return None without raising exception
    result = instance.handle_request(mock_consumer, message)
    assert result is None

    # Assert downstream handlers were not called
    frontend_mock.return_value.update_frontend.assert_not_called()
    publisher_mock.return_value.send_message.assert_not_called()


@patch("consumers.events.state_change.get_publisher")
@patch("consumers.events.state_change.FrontendMessenger")
def test_state_change_handle_request_unmapped_device_type(
    frontend_mock, publisher_mock, device
):
    """Test StateChange raises exception for device type without registered mapper"""
    mock_consumer = Mock()
    instance = StateChange()

    # device.fun is 'aquarium', which has no mapper in state_mapper
    message = DeviceMessage(
        message_type=MessageType.REQUEST,
        message_event=MessageEvent.STATE_CHANGE,
        device_id=device.mac,
        message_id="1",
        payload={"state": DeviceState.ON},
    )

    # Assert exception is raised with descriptive message
    with pytest.raises(Exception):
        instance.handle_request(mock_consumer, message)
