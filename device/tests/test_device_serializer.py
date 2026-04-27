import pytest


@pytest.fixture
def mock_redis(mocker):
    return mocker.patch("device.serializers.device.redis_cache.get_device_pending")


import pytest
from device.serializers.device import DeviceSerializer
from model_bakery import baker


@pytest.mark.django_db
class TestDeviceSerializer:

    def test_serialize_model_with_pending_data(self, mock_redis):
        # # Given
        device = baker.make("device.Device", name="Test 1")
        pending_mock_data = ["update_firmware", "change_color"]
        mock_redis.return_value = pending_mock_data

        # # When
        serializer = DeviceSerializer(instance=device)
        data = serializer.data

        # # Then
        assert data["name"] == "Test 1"
        assert data["pending"] == pending_mock_data
        mock_redis.assert_called_once_with(device.pk)

    def test_serialize_model_with_empty_pending(self, mock_redis):
        # # Given
        device = baker.make("device.Device")
        mock_redis.return_value = None

        # # When
        serializer = DeviceSerializer(instance=device)

        # # Then
        assert serializer.data["pending"] == []

    def test_read_only_fields(self):
        # # Given
        device = baker.make("device.Device", mac="AA:BB:CC")
        update_data = {
            "name": "New Name",
            "mac": "FF:FF:FF",
        }

        # # When
        serializer = DeviceSerializer(instance=device, data=update_data, partial=True)
        assert serializer.is_valid()
        serializer.save()

        # # Then
        device.refresh_from_db()
        assert device.name == "New Name"
        assert device.mac == "AA:BB:CC"
