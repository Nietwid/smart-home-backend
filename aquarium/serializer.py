from rest_framework import serializers

from utils.check_hour_in_range import check_hour_in_range
from .models import Aquarium


class AquariumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Aquarium
        exclude = ["fun", "mac"]

    def validate(self, attrs):
        self.validate_led_time(attrs)
        self.validate_fluo_lamp_time(attrs)
        return attrs

    def validate_led_time(self, data):
        if not any([data.get("led_start"), data.get("led_stop")]):
            return data
        led_start = data.get("led_start", self.instance.led_start)
        led_stop = data.get("led_stop", self.instance.led_stop)
        led_mode = check_hour_in_range(led_start, led_stop)
        self.instance.led_mode = led_mode
        return data

    def validate_fluo_lamp_time(self, data):
        if not any([data.get("fluo_start"), data.get("fluo_stop")]):
            return data
        fluo_start = data.get("fluo_start", self.instance.fluo_start)
        fluo_stop = data.get("fluo_stop", self.instance.fluo_stop)
        fluo_mode = check_hour_in_range(fluo_start, fluo_stop)
        self.instance.fluo_mode = fluo_mode
        return data

    def validate_mode(self, data):
        fluo_mode = check_hour_in_range(
            self.instance.fluo_start, self.instance.fluo_stop
        )
        self.instance.fluo_mode = fluo_mode
        led_mode = check_hour_in_range(self.instance.led_start, self.instance.led_stop)
        self.instance.led_mode = led_mode
        return data

    # def update(self, instance, validated_data):
    #     super().update(instance, validated_data)
    #     send_set_settings_request(instance)
    #     return instance


class AquariumSerializerDevice(serializers.ModelSerializer):
    led_mode = serializers.SerializerMethodField()
    fluo_mode = serializers.SerializerMethodField()

    class Meta:
        model = Aquarium
        fields = [
            "color_r",
            "color_g",
            "color_b",
            "led_mode",
            "fluo_mode",
        ]

    def get_led_mode(self, obj: Aquarium):
        if obj.mode:
            return check_hour_in_range(obj.led_start, obj.led_stop)
        return obj.led_mode

    def get_fluo_mode(self, obj: Aquarium):
        if obj.mode:
            return check_hour_in_range(obj.fluo_start, obj.fluo_stop)
        return obj.fluo_mode
