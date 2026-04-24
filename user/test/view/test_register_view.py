import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from user.models import Home, Favourite


@pytest.mark.django_db
class TestRegisterView:

    def test_register_success_creates_full_stack(self, auth_client):
        # Given
        url = reverse("register")
        data = {
            "username": "new_boss",
            "password": "SecurePassword123!",
            "password2": "SecurePassword123!",
        }

        # When
        response = auth_client.post(url, data, format="json")

        # Then
        assert response.status_code == 201
        assert response.data["message"] == "User created successfully"
        user = User.objects.get(username="new_boss")
        assert user.check_password("SecurePassword123!")
        home = Home.objects.filter(users=user).first()
        assert home is not None
        assert home.add_uid is not None
        assert Favourite.objects.filter(user=user).exists()

    def test_register_fails_invalid_data(self, auth_client):
        # Given
        url = reverse("register")
        data = {
            "username": "fail_user",
            "password": "Password1",
            "password2": "DifferentPassword2",
        }

        # When
        response = auth_client.post(url, data, format="json")

        # Then
        assert response.status_code == 400
        assert "password2" in response.data
        assert not User.objects.filter(username="fail_user").exists()
        assert Home.objects.count() == 0

    def test_register_duplicate_username(self, auth_client):
        # Given
        User.objects.create_user(username="busy_boss", password="password123")
        initial_home_count = Home.objects.count()

        url = reverse("register")
        data = {
            "username": "busy_boss",
            "password": "NewPassword123!",
            "password2": "NewPassword123!",
        }

        # When
        response = auth_client.post(url, data, format="json")

        # Then
        assert response.status_code == 400
        assert "username" in response.data
        assert Home.objects.count() == initial_home_count
