import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestChangePasswordView:
    url = "change-password"

    def test_change_password_view_success(self, auth_client, user):
        # Given
        url = reverse(self.url)
        data = {
            "current_password": "testpass",
            "new_password": "NewSecurePass88!",
            "new_password2": "NewSecurePass88!",
        }

        # When
        response = auth_client.post(url, data, format="json")

        # Then
        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Password updated successfully."
        user.refresh_from_db()
        assert user.check_password("NewSecurePass88!") is True
        assert user.check_password("testpass") is False

    def test_change_password_view_validation_error(self, auth_client, user):
        # Given
        url = reverse(self.url)
        auth_client.force_authenticate(user=user)

        data = {
            "current_password": "WrongCurrentPassword",
            "new_password": "NewSecurePass88!",
            "new_password2": "NewSecurePass88!",
        }

        # When
        response = auth_client.post(url, data, format="json")

        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "current_password" in response.data
        user.refresh_from_db()
        assert user.check_password("testpass") is True

    def test_change_password_requires_authentication(self, auth_client):
        # Given
        url = reverse(self.url)
        data = {
            "current_password": "any",
            "new_password": "any",
            "new_password2": "any",
        }

        # When
        response = auth_client.post(url, data, format="json")

        # Then
        assert response.status_code == status.HTTP_400_BAD_REQUEST
