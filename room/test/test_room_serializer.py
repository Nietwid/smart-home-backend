from unittest.mock import MagicMock
import pytest
from django.utils import timezone
from datetime import timedelta
from model_bakery import baker
from room.models import Room
from room.serializer import RoomSerializer


@pytest.mark.django_db
class TestRoomSerializer:

    def test_serialization_fields(self):
        # Given
        room = baker.make(Room, name="Salon", visibility=Room.Visibility.PUBLIC)
        baker.make("device.Device", room=room, _quantity=3, last_seen=timezone.now())

        # When
        serializer = RoomSerializer(instance=room)
        data = serializer.data

        # Then
        assert data["name"] == "Salon"
        assert data["visibility"] == "public"
        assert data["device_count"] == 3
        assert len(data["device"]) == 3

    def test_active_device_count_logic(self):
        # Given
        now = timezone.now()
        room = baker.make(Room)

        baker.make("device.Device", room=room, last_seen=now)
        baker.make("device.Device", room=room, last_seen=now - timedelta(minutes=9))
        baker.make("device.Device", room=room, last_seen=now - timedelta(minutes=11))

        # When
        serializer = RoomSerializer(instance=room)
        active_count = serializer.data["active_device_count"]

        # Then
        assert active_count == 2

    def test_visibility_internal_value_mapping(self):
        # Given
        data = {"name": "Kitchen", "visibility": "PU"}

        # When
        serializer = RoomSerializer(data=data)

        # Then
        assert serializer.is_valid()
        assert serializer.validated_data["visibility"] == Room.Visibility.PUBLIC

    def test_validate_name_length(self):
        # Given
        data = {"name": "S", "visibility": "public"}
        serializer = RoomSerializer(data=data)

        # When
        is_valid = serializer.is_valid()

        # Then
        assert is_valid is False
        assert "Name must be at least 3 characters long" in str(
            serializer.errors["name"]
        )
