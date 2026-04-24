import pytest
from rest_framework.exceptions import ValidationError
from device.serializers.router import RouterSerializer
from model_bakery import baker


@pytest.mark.django_db
class TestRouterSerializer:

    def test_get_device_counts(self, home, router):
        # Given
        room = baker.make("room.Room", home=home)
        baker.make("device.Device", room=room, is_online=True, _quantity=2)
        baker.make("device.Device", room=room, is_online=False)

        other_home_room = baker.make("room.Room")
        baker.make("device.Device", room=other_home_room, is_online=True)

        # When
        serializer = RouterSerializer(instance=router)
        data = serializer.data

        # Then
        assert data["connected_devices"] == 3
        assert data["online_device"] == 2

    def test_validate_mac_already_exists(self):
        # Given
        existing_mac = "AA:BB:CC:DD:EE:FF"
        baker.make("device.Router", mac=existing_mac)

        data = {"mac": existing_mac, "name": "New Router"}
        serializer = RouterSerializer(data=data)

        # When / Then
        with pytest.raises(ValidationError) as excinfo:
            serializer.is_valid(raise_exception=True)

        assert "Router already exists" in str(excinfo.value)

    def test_validate_mac_empty(self):
        # Given
        data = {"mac": "", "name": "Empty MAC Router"}
        serializer = RouterSerializer(data=data)

        # When
        is_valid = serializer.is_valid()

        # Then
        assert is_valid is False
        assert "mac" in serializer.errors
        assert serializer.errors["mac"][0].code == "blank"

    def test_validate_mac_success(self):
        # Given
        data = {
            "mac": "00:11:22:33:44:55",
            "name": "Valid Router",
            "home": baker.make("user.Home").pk,
        }
        serializer = RouterSerializer(data=data)

        # When
        is_valid = serializer.is_valid()

        # Then
        assert is_valid is True
        assert serializer.validated_data["mac"] == "00:11:22:33:44:55"
