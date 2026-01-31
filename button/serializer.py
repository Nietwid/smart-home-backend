from rest_framework import serializers

from utils.button_type_change import (
    button_type_change,
)
from utils.send_set_settings_request import send_set_settings_request
from .models import Button, ButtonType


class ButtonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Button
        read_only_fields = ["fun"]
        exclude = ["mac"]

    def update(self, instance: Button, validated_data: dict):
        if "button_type" in validated_data:
            button_type_change(validated_data["button_type"], instance)

        response = super().update(instance, validated_data)

        if "button_type" in validated_data:
            send_set_settings_request(instance)
        return response


class ButtonSerializerDevice(serializers.ModelSerializer):

    class Meta:
        model = Button
        fields = ["button_type"]
