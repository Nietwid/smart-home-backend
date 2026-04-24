from rest_framework import serializers


class HomeCodeSerializer(serializers.Serializer):
    code = serializers.UUIDField(
        required=True,
        error_messages={
            "invalid": "Invalid home code format.",
            "required": "Code is required.",
        },
    )
