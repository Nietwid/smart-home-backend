import pytest
from model_bakery import baker

from device.models import Device
from dispatcher.command_message.message import CommandMessage
from dispatcher.handlers.base import EventIntentBaseHandler
from notifier.message import FrontendNotifierData, MicroserviceNotifierData


@pytest.fixture
def mock_rule_engine(mocker):
    return mocker.patch(
        "dispatcher.handlers.base.RuleEngineService.get_event_request", return_value=[]
    )


@pytest.fixture
def mock_service_factory(mocker):
    return mocker.patch(
        "dispatcher.handlers.base.microservice_message_factory.log_event"
    )


@pytest.fixture
def mock_frontend_factory(mocker):
    return mocker.patch(
        "dispatcher.handlers.base.frontend_notifier_factory.update_peripheral_state"
    )


@pytest.fixture
def handler():
    class TestHandler(EventIntentBaseHandler):
        def update_peripheral_state(self, peripheral, state):
            peripheral.last_state = state

    return TestHandler()


@pytest.fixture
def message(device_with_peripherals: Device):
    peripheral = device_with_peripherals.peripherals.first()
    return CommandMessage.model_construct(
        peripheral=peripheral, command="on_measure", payload={"value": 25.5}
    )


@pytest.mark.django_db
def test_handler_basic_flow(handler, message, mock_rule_engine, mock_service_factory):
    # Given
    handler.exchange: str = "test"
    handler.routing_key: str = "test"
    mock_service_factory.return_value = MicroserviceNotifierData.model_construct()
    mock_rule_engine.return_value = [
        CommandMessage.model_construct(command="rule_command")
    ]

    # When
    result = handler(message)

    # Then
    assert isinstance(result.notifications[0], MicroserviceNotifierData)
    assert isinstance(result.commands[0], CommandMessage)


@pytest.mark.django_db
def test_handler_frontend_update_enabled(handler, message, mock_frontend_factory):
    # Given
    handler.update_frontend_peripheral_state = True
    mock_frontend_factory.return_value = FrontendNotifierData.model_construct()

    # When
    result = handler(message)

    # Then
    assert isinstance(result.notifications[0], FrontendNotifierData)


@pytest.mark.django_db
def test_edge_case_no_exchange_no_notification(handler, message, mock_service_factory):
    # Given
    handler.exchange = None
    handler.routing_key = "some_key"

    # When
    result = handler(message)

    # Then
    assert mock_service_factory.call_count == 0
    assert len(result.notifications) == 0


@pytest.mark.django_db
def test_edge_case_send_command_false(handler, message, mock_rule_engine):
    # Given
    handler.send_command = False

    # When
    result = handler(message)

    # Then
    assert mock_rule_engine.call_count == 0
    assert len(result.commands) == 0


@pytest.mark.django_db
def test_extra_commands_and_notifications_merging(handler, message, mocker):
    # Given
    mocker.patch.object(
        handler,
        "get_extra_notification",
        return_value=[FrontendNotifierData.model_construct()],
    )
    mocker.patch.object(
        handler, "get_extra_commands", return_value=[CommandMessage.model_construct()]
    )

    # When
    result = handler(message)

    # Then
    assert isinstance(result.notifications[0], FrontendNotifierData)
    assert isinstance(result.commands[0], CommandMessage)


@pytest.mark.django_db
def test_empty_payload_behavior(handler, mock_rule_engine):
    # Given
    peripheral = baker.prepare("peripherals.Peripherals")
    msg_empty = CommandMessage.model_construct(
        peripheral=peripheral, command="ping", payload={}
    )

    # When
    result = handler(msg_empty)

    # Then
    assert result.notifications is not None
    assert msg_empty.peripheral.state == {}


@pytest.mark.django_db
def test_rule_engine_returns_multiple_commands(handler, message, mock_rule_engine):
    # Given
    mock_rule_engine.return_value = [
        CommandMessage.model_construct(command="on_time"),
        CommandMessage.model_construct(command="device_disconnect"),
        CommandMessage.model_construct(command="get_connected_devices"),
    ]

    # When
    result = handler(message)

    # Then
    assert len(result.commands) == 3


@pytest.mark.django_db
def test_dispatch_result_immutability_logic(handler, message):
    # When
    result = handler(message)

    # Then
    assert isinstance(result.notifications, list)
    assert isinstance(result.commands, list)


@pytest.mark.django_db
def test_handler_without_routing_key_skips_service_log(
    handler, message, mock_service_factory
):
    # Given
    handler.exchange = "exists"
    handler.routing_key = None

    # When
    result = handler(message)

    # Then
    mock_service_factory.assert_not_called()
