import pytest
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch, MagicMock


@pytest.mark.django_db
class TestLogoutView:
    url = reverse("logout")

    @patch("user.service.auth_service.AuthService.logout")
    def test_logout_web_clears_cookie(self, mock_logout, auth_client):
        # Given
        auth_client.cookies["refresh"] = "some_token"

        # When
        response = auth_client.delete(self.url)

        # Then
        assert response.status_code == status.HTTP_204_NO_CONTENT
        mock_logout.assert_called_once()
        cookie = response.cookies.get("refresh")
        assert cookie is not None
        assert (
            cookie["expires"] == "Thu, 01 Jan 1970 00:00:00 GMT"
            or cookie["max-age"] == 0
        )

    @patch("user.service.auth_service.AuthService.logout")
    def test_logout_mobile_does_not_clear_cookie(self, mock_logout, auth_client):
        # When
        response = auth_client.delete(self.url, HTTP_X_CLIENT_TYPE="mobile")

        # Then
        assert response.status_code == status.HTTP_204_NO_CONTENT
        mock_logout.assert_called_once()

        assert "refresh" not in response.cookies

    @patch("user.views.logger")
    @patch("user.service.auth_service.AuthService.logout")
    def test_logout_exception_returns_400(self, mock_logout, mock_logger, auth_client):
        # Given
        mock_logout.side_effect = Exception("Blacklist error")

        # When
        response = auth_client.delete(self.url)

        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        mock_logger.error.assert_called_once()
