import pytest
from uuid import uuid4
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch, MagicMock


@pytest.mark.django_db
class TestHomeView:
    url = reverse("home")

    @patch("user.service.home_service.HomeService.get_user_home")
    def test_get_home_code_success(self, mock_get_home, auth_client, user):
        # Given
        fake_uuid = uuid4()
        mock_home = MagicMock(add_uid=fake_uuid)
        mock_get_home.return_value = mock_home

        # When
        response = auth_client.get(self.url)

        # Then
        assert response.status_code == status.HTTP_200_OK
        assert response.data["code"] == fake_uuid
        mock_get_home.assert_called_once_with(user)

    @patch("user.service.home_service.HomeService.join_home")
    def test_put_join_home_success(self, mock_join, auth_client, user):
        # Given
        new_uuid = str(uuid4())
        payload = {"code": new_uuid}

        # When
        response = auth_client.put(self.url, payload, format="json")

        # Then
        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Successfully joined new home."
        mock_join.assert_called_once()
        args, kwargs = mock_join.call_args
        assert str(kwargs["new_home_uuid"]) == new_uuid

    def test_put_join_home_invalid_uuid(self, auth_client, user):
        # Given
        payload = {"code": "not-a-uuid"}

        # When
        response = auth_client.put(self.url, payload, format="json")

        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "code" in response.data

    @patch("user.service.home_service.HomeService.leave_and_create_new")
    def test_delete_leave_home_success(self, mock_leave, auth_client, user):
        # When
        response = auth_client.delete(self.url)

        # Then
        assert response.status_code == status.HTTP_204_NO_CONTENT
        mock_leave.assert_called_once_with(user)
