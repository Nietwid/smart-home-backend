import pytest
from django.contrib.auth.models import User

from light.models import Light
from temperature.models import TempHum
from user.models import Home, Favourite
from room.models import Room
from aquarium.models import Aquarium
from device.models import Device
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from button.models import Button
from lamp.models import Lamp
from rfid.models import Rfid


@pytest.fixture
def user(db):
    user = User.objects.create_user(username="testuser", password="testpass")
    Favourite.objects.create(user=user)
    return user


@pytest.fixture
def auth_client(user) -> APIClient:
    client = APIClient()
    access_token = RefreshToken.for_user(user).access_token
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return client


@pytest.fixture
def home(db, user) -> Home:
    home = Home.objects.create()
    home.users.add(user)
    return home


@pytest.fixture
def room(db, home, user):
    return Room.objects.create(name="Test", user=user, home=home)


@pytest.fixture
def aquarium(room, home):
    return Aquarium.objects.create(
        name="Test Aquarium",
        room=room,
        home=home,
        fun="aquarium",
        mac="00:11:22:33:44:55",
        wifi_strength=-50,
    )


@pytest.fixture
def button(room, home):
    return Button.objects.create(
        name="TestButton", mac="00:11:22:33:44:55", fun="button", room=room, home=home
    )


@pytest.fixture
def device(room, home):
    return Device.objects.create(
        name="Test Device",
        room=room,
        home=home,
        fun="aquarium",
        mac="00:11:22:33:45:55",
        wifi_strength=-50,
    )


@pytest.fixture
def lamp(room, home):
    return Lamp.objects.create(
        room=room,
        home=home,
        name="Test",
        fun="lamp",
        mac="00:11:22:33:25:55",
    )


@pytest.fixture
def rfid(room, home):
    return Rfid.objects.create(
        name="Test RFID",
        fun="rfid",
        room=room,
        home=home,
        mac="00:31:22:33:25:55",
    )


@pytest.fixture
def temp_hum(room, home):
    return TempHum.objects.create(
        room=room,
        home=home,
        mac="00:31:22:33:25:55",
        fun="temp_hum",
        name="Test Temp Hum",
    )


@pytest.fixture
def light(room, home):
    return Light.objects.create(
        room=room,
        home=home,
        mac="00:31:22:33:25:55",
        fun="light",
        name="Test Light",
    )


@pytest.fixture
def mock_device_registry(monkeypatch):
    """Mock DeviceRegistry to control which 'fun' values are valid."""

    class MockDeviceRegistry:
        devices = {"aquarium": {}, "lamp": {}}

    monkeypatch.setattr("device_registry.DeviceRegistry", MockDeviceRegistry)
    return MockDeviceRegistry
