import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from user.serializers.change_password_serializer import ChangePasswordSerializer


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="OldPassword123!")


@pytest.fixture
def rf():
    return APIRequestFactory()


@pytest.mark.django_db
class TestChangePasswordSerializer:

    def test_change_password_success(self, user, rf):
        request = rf.post("/")
        request.user = user

        data = {
            "current_password": "OldPassword123!",
            "new_password": "NewSecurePassword88!",
            "new_password2": "NewSecurePassword88!",
        }

        serializer = ChangePasswordSerializer(data=data, context={"request": request})

        assert serializer.is_valid() is True
        assert serializer.validated_data["new_password"] == "NewSecurePassword88!"

    def test_fails_on_incorrect_current_password(self, user, rf):
        request = rf.post("/")
        request.user = user

        data = {
            "current_password": "WrongPassword",
            "new_password": "NewSecurePassword88!",
            "new_password2": "NewSecurePassword88!",
        }

        serializer = ChangePasswordSerializer(data=data, context={"request": request})

        assert serializer.is_valid() is False
        assert "current_password" in serializer.errors
        assert (
            serializer.errors["current_password"][0] == "Current password is incorrect."
        )

    def test_fails_when_new_passwords_do_not_match(self, user, rf):
        request = rf.post("/")
        request.user = user

        data = {
            "current_password": "OldPassword123!",
            "new_password": "NewPassword1!",
            "new_password2": "DifferentPassword2!",
        }

        serializer = ChangePasswordSerializer(data=data, context={"request": request})

        assert serializer.is_valid() is False
        assert "new_password2" in serializer.errors
        assert serializer.errors["new_password2"][0] == "New passwords do not match."

    def test_fails_when_new_password_is_same_as_old(self, user, rf):
        request = rf.post("/")
        request.user = user

        data = {
            "current_password": "OldPassword123!",
            "new_password": "OldPassword123!",
            "new_password2": "OldPassword123!",
        }

        serializer = ChangePasswordSerializer(data=data, context={"request": request})

        assert serializer.is_valid() is False
        assert "new_password" in serializer.errors
        assert (
            serializer.errors["new_password"][0]
            == "New password must be different from current password."
        )
