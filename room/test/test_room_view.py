import pytest
from django.urls import reverse
from rest_framework import status
from model_bakery import baker
from room.models import Room


@pytest.fixture
def mock_home_repository(mocker):
    return mocker.patch("user.repository.home_repository.HomeRepository")


@pytest.mark.django_db
class TestListCreateRoomView:
    url = "room-list-create"

    def test_list_rooms_returns_only_accessible(self, auth_client, user):
        # Given
        home = baker.make("user.Home")
        home.users.add(user)

        baker.make(Room, name="My Private", user=user, home=home, visibility="PR")
        baker.make(Room, name="Public Room", home=home, visibility="PU")
        baker.make(Room, name="Other Private", home=home, visibility="PR")

        url = reverse(self.url)

        # When
        response = auth_client.get(url)

        # Then
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        names = [r["name"] for r in response.data]
        assert "My Private" in names
        assert "Public Room" in names
        assert "Other Private" not in names

    def test_create_room_assigns_home_and_user(
        self, auth_client, user, mock_home_repository
    ):
        # Given
        home = baker.make("user.Home")
        home.users.add(user)
        mock_home_repository.get_home_by_user.return_value = home

        url = reverse(self.url)
        payload = {"name": "New", "visibility": "PU"}

        # When
        response = auth_client.post(url, payload)

        # Then
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "New"

        room = Room.objects.get(id=response.data["id"])
        assert room.user == user
        assert room.home == home


@pytest.mark.django_db
class TestRetrieveUpdateDestroyRoomView:
    url = "room-retrieve-update-destroy"

    def test_retrieve_room_success(self, auth_client, user):
        # Given
        home = baker.make("user.Home")
        home.users.add(user)
        room = baker.make(Room, home=home, user=user)

        url = reverse(self.url, kwargs={"pk": room.pk})

        # When
        response = auth_client.get(url)

        # Then
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == room.pk

    def test_retrieve_room_forbidden_if_not_in_home(self, auth_client, user):
        # Given
        other_home = baker.make("user.Home")
        room = baker.make(Room, home=other_home)

        url = reverse(self.url, kwargs={"pk": room.pk})

        # When
        response = auth_client.get(url)

        # Then
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_room_name(self, auth_client, user):
        # Given
        home = baker.make("user.Home")
        home.users.add(user)
        room = baker.make(Room, home=home, user=user, name="Old Name")

        url = reverse(self.url, kwargs={"pk": room.pk})
        payload = {"name": "New Awesome Name"}

        # When
        response = auth_client.patch(url, payload)

        # Then
        assert response.status_code == status.HTTP_200_OK
        room.refresh_from_db()
        assert room.name == "New Awesome Name"
