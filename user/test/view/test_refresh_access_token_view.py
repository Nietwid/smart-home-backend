import pytest
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch


@pytest.mark.django_db
class TestRefreshAccessTokenView:
    url = reverse("token-refresh")

    @patch("user.service.auth_service.AuthService.refresh_access_token")
    def test_refresh_access_token_success(self, mock_refresh, auth_client):
        # Given
        mock_refresh.return_value = "fake_new_access_token"

        # When
        response = auth_client.get(self.url)

        # Then
        assert response.status_code == status.HTTP_200_OK
        assert response.data["access"] == "fake_new_access_token"
        mock_refresh.assert_called_once()

    @patch("user.service.auth_service.AuthService.refresh_access_token")
    def test_refresh_access_token_invalid_raises_403(self, mock_refresh, auth_client):
        # Given
        mock_refresh.side_effect = Exception("Token expired")

        # When
        response = auth_client.get(self.url)

        # Then
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == "Invalid or expired refresh token."

    @patch("user.views.logger")
    @patch("user.service.auth_service.AuthService.refresh_access_token")
    def test_refresh_access_token_logs_error(
        self, mock_refresh, mock_logger, auth_client
    ):
        # Given
        error_msg = "Critical token failure"
        mock_refresh.side_effect = Exception(error_msg)

        # When
        auth_client.get(self.url)

        # Then
        mock_logger.error.assert_called_once()
        args, _ = mock_logger.error.call_args
        assert error_msg in args[0]
