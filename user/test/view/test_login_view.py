import pytest
from django.urls import reverse
from rest_framework import status
from django.conf import settings


@pytest.mark.django_db
class TestLoginView:

    def test_login_sets_cookie_correctly(self, auth_client, user, home):
        # Given
        url = reverse("login")
        data = {"username": "testuser", "password": "testpass"}

        # When
        response = auth_client.post(url, data, format="json")

        # Then
        assert response.status_code == status.HTTP_200_OK
        assert "refresh" in response.cookies
        cookie = response.cookies["refresh"]

        assert cookie["httponly"] is True
        assert cookie["secure"] is True
        assert cookie["samesite"].lower() == "none"

        assert cookie.value == response.data["refresh"]
        expected_max_age = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()
        assert int(cookie["max-age"]) == int(expected_max_age)

    def test_login_fails_invalid_credentials(self, auth_client, user):
        # Given
        url = reverse("login")
        data = {"username": "testboss", "password": "WrongPassword"}

        # When
        response = auth_client.post(url, data, format="json")

        # Then
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "refresh" not in response.cookies
