import pytest
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch


@pytest.mark.django_db
class TestFavouriteView:
    url = reverse("favourite")

    @patch("user.service.favourite_service.FavouriteService.get_user_favourites")
    def test_get_favourites_success(self, mock_get_favs, auth_client, user):
        # Given
        mock_data = {"rooms": [1, 2], "devices": [5], "cameras": []}
        mock_get_favs.return_value = mock_data
        auth_client.force_authenticate(user=user)

        # When
        response = auth_client.get(self.url)

        # Then
        assert response.status_code == status.HTTP_200_OK
        assert response.data == mock_data
        mock_get_favs.assert_called_once_with(user)

    @patch("user.service.favourite_service.FavouriteService.toggle_favourite")
    def test_put_favourite_success(self, mock_toggle, auth_client, user):
        # Given
        payload = {"type": "room", "id": 10, "is_favourite": False}
        auth_client.force_authenticate(user=user)

        # When
        response = auth_client.put(self.url, payload, format="json")

        # Then
        assert response.status_code == status.HTTP_200_OK
        mock_toggle.assert_called_once_with(
            user=user, obj_type="room", obj_id=10, is_already_favourite=False
        )

    @patch("user.service.favourite_service.FavouriteService.toggle_favourite")
    def test_put_favourite_invalid_type_returns_400(
        self, mock_toggle, auth_client, user
    ):
        # Given
        mock_toggle.side_effect = ValueError("Invalid object type.")
        auth_client.force_authenticate(user=user)
        payload = {"type": "wrong_type", "id": 1}

        # When
        response = auth_client.put(self.url, payload, format="json")

        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid object type."
