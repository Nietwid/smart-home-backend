import pytest
from unittest.mock import MagicMock, patch
from user.service.auth_service import AuthService


class TestAuthService:

    def test_get_token_from_header_for_mobile(self):
        request = MagicMock()
        request.headers = {"X-Client-Type": "mobile", "Token": "mobile_token_123"}

        token = AuthService.get_refresh_token_string(request)

        assert token == "mobile_token_123"

    def test_get_token_from_cookies_for_web(self):
        request = MagicMock()
        request.headers = {"X-Client-Type": "web"}
        request.COOKIES = {"refresh": "cookie_token_456"}

        token = AuthService.get_refresh_token_string(request)

        assert token == "cookie_token_456"

    @patch("user.service.auth_service.RefreshToken")
    def test_refresh_access_token_success(self, mock_refresh_token):
        # Given
        request = MagicMock()
        request.headers = {"X-Client-Type": "mobile", "Token": "valid_token"}

        mock_token_instance = MagicMock()
        mock_token_instance.access_token = "new_access_token_abc"
        mock_refresh_token.return_value = mock_token_instance

        # Action
        result = AuthService.refresh_access_token(request)

        # Assert
        assert result == "new_access_token_abc"
        mock_refresh_token.assert_called_once_with("valid_token")

    def test_refresh_access_token_missing_token_raises_error(self):
        request = MagicMock()
        request.headers = {}
        request.COOKIES = {}

        with pytest.raises(ValueError, match="Refresh token missing"):
            AuthService.refresh_access_token(request)

    @patch("user.service.auth_service.RefreshToken")
    def test_logout_blacklists_token(self, mock_refresh_token):
        request = MagicMock()
        request.headers = {"X-Client-Type": "mobile", "Token": "token_to_kill"}

        mock_token_instance = MagicMock()
        mock_refresh_token.return_value = mock_token_instance

        AuthService.logout(request)

        mock_token_instance.blacklist.assert_called_once()
        mock_refresh_token.assert_called_once_with("token_to_kill")

    @patch("user.service.auth_service.RefreshToken")
    def test_logout_does_nothing_if_no_token(self, mock_refresh_token):
        request = MagicMock()
        request.headers = {}
        request.COOKIES = {}

        AuthService.logout(request)

        mock_refresh_token.assert_not_called()
