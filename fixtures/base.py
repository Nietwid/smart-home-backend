import pytest
from django.contrib.auth.models import User

from device.models import Device, Router
from user.models import Home, Favourite
from room.models import Room
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


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
def routr(home) -> Router:
    return Router.objects.create(
        ip="192.168.1.1", mac="1234", home=home, wifi_strength=-10, is_online=True
    )


@pytest.fixture
def room(db, home, user):
    return Room.objects.create(name="Test", user=user, home=home)


@pytest.fixture
def device(home, room):
    return Device.objects.create(mac="AA:BB:CC:DD:EE:FF", home=home, room=room)
