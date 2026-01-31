import pytest
from django.utils import timezone
from room.serializer import RoomSerializer
from room.models import Room
from device.models import Device


@pytest.mark.django_db
def test_device_counts(room, device):
    serializer = RoomSerializer(room)
    data = serializer.data
    assert data["device_count"] == room.devices.count()
    device.last_seen = timezone.now()
    device.save()
    serializer = RoomSerializer(room)
    data = serializer.data
    assert data["active_device_count"] == 1


@pytest.mark.django_db
def test_to_representation_visibility(room):
    room.visibility = Room.Visibility.PUBLIC
    serializer = RoomSerializer(room)
    data = serializer.data
    assert data["visibility"] == room.get_visibility_display()


@pytest.mark.django_db
def test_validate_name_min_length(room):
    serializer = RoomSerializer(
        context={"view": type("view", (), {"get_queryset": lambda self: [room]})()}
    )
    with pytest.raises(Exception) as e:
        serializer.validate_name("ab")
    assert "at least 3 characters" in str(e.value)


@pytest.mark.django_db
def test_validate_name_unique(room):
    serializer = RoomSerializer(
        context={"view": type("view", (), {"get_queryset": lambda self: [room]})()}
    )
    with pytest.raises(Exception) as e:
        serializer.validate_name(room.name)
    assert "already exists" in str(e.value)
