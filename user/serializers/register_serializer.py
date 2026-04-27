from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import django.contrib.auth.password_validation as validators


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("User with this username already exists.")
        return value

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password2": "Passwords do not match."})
        try:
            validators.validate_password(password=data["password"])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return data
