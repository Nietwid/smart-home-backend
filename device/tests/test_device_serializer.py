import pytest
from unittest.mock import MagicMock, patch
from device.serializers.device import DeviceSerializer
from device.models import Device, Event


@pytest.mark.django_db
@patch("device.serializers.device.EventSerializer")
@patch("device.serializers.device.DeviceRegistry")
def test_to_representation_calls_nested_serializers(
    mock_registry, mock_event_serializer, room, device, user
):
    """
    Should call device-specific serializer and EventSerializer
    and include 'events' in the representation
    """
    mock_model = device.__class__
    mock_device_serializer = MagicMock()
    mock_device_serializer.data = {"name": device.name}
    mock_registry.return_value.get_model.return_value = mock_model
    mock_registry.return_value.get_serializer.return_value = (
        lambda *args, **kwargs: mock_device_serializer
    )

    event = Event.objects.create(device=device)
    mock_event_serializer.return_value.data = [{"device": device.id}]

    serializer = DeviceSerializer(device)
    data = serializer.data

    assert "events" in data
    assert data["events"] == [{"device": device.id}]


@pytest.mark.django_db
@patch("device.serializers.device.DeviceRegistry")
@patch("device.serializers.device.FrontendMessenger")
def test_update_calls_frontend_messenger(mock_messenger, mock_registry, device, mocker):
    """
    update() should call device-specific serializer.save() and FrontendMessenger.update_frontend
    """
    mock_model = device.__class__
    mock_device_serializer = MagicMock()
    mock_device_serializer.is_valid.return_value = True
    mock_device_serializer.save.return_value = device

    mock_registry.return_value.get_model.return_value = mock_model
    mock_registry.return_value.get_serializer.return_value = (
        lambda *args, **kwargs: mock_device_serializer
    )

    serializer = DeviceSerializer(
        instance=device, data={"name": "Updated"}, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    mock_device_serializer.save.assert_called()
    mock_messenger.return_value.update_frontend.assert_called()
