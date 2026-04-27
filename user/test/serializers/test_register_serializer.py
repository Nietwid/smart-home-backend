import pytest
from django.contrib.auth.models import User
from user.serializers.register_serializer import RegisterSerializer


@pytest.mark.django_db
class TestRegisterSerializer:

    def test_registration_success(self):
        data = {
            "username": "new_user",
            "password": "SecurePassword123!",
            "password2": "SecurePassword123!",
        }
        serializer = RegisterSerializer(data=data)

        assert serializer.is_valid() is True
        assert serializer.validated_data["username"] == "new_user"

    def test_fails_when_username_already_exists(self):
        # Given
        User.objects.create_user(username="existing_user", password="somepassword")

        data = {
            "username": "existing_user",
            "password": "SecurePassword123!",
            "password2": "SecurePassword123!",
        }
        serializer = RegisterSerializer(data=data)

        # When & Then
        assert serializer.is_valid() is False
        assert "username" in serializer.errors
        assert (
            serializer.errors["username"][0]
            == "User with this username already exists."
        )

    def test_fails_when_passwords_do_not_match(self):
        data = {
            "username": "new_user",
            "password": "Password123!",
            "password2": "DifferentPassword123!",
        }
        serializer = RegisterSerializer(data=data)

        assert serializer.is_valid() is False
        assert "password2" in serializer.errors
        assert serializer.errors["password2"][0] == "Passwords do not match."

    def test_fails_on_too_common_password(self):
        data = {
            "username": "new_user",
            "password": "password123",
            "password2": "password123",
        }
        serializer = RegisterSerializer(data=data)

        assert serializer.is_valid() is False
        assert "password" in serializer.errors
        assert any(
            "common" in msg.lower() or "too simple" in msg.lower()
            for msg in serializer.errors["password"]
        )

    def test_fails_on_short_password(self):
        data = {"username": "new_user", "password": "123", "password2": "123"}
        serializer = RegisterSerializer(data=data)

        assert serializer.is_valid() is False
        assert "password" in serializer.errors
        assert any("short" in msg.lower() for msg in serializer.errors["password"])
