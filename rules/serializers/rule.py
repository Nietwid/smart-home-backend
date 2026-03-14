from rest_framework import serializers

from dispatcher.command_message.factory import command_message_factory
from dispatcher.device.messages.payload.enum import StartSyncType
from dispatcher.processor.action_event_command import action_event_command_processor
from rules.models import Rule, RuleAction, RuleCondition, RuleTrigger
from rules.serializers.action import RuleActionSerializer
from rules.serializers.condition import RuleConditionSerializer
from rules.serializers.trigger import RuleTriggerSerializer


class RuleSerializerDevice(serializers.ModelSerializer):
    triggers = RuleTriggerSerializer(many=True)
    conditions = RuleConditionSerializer(many=True, required=False)
    actions = RuleActionSerializer(many=True)

    class Meta:
        model = Rule
        fields = (
            "id",
            "triggers",
            "conditions",
            "actions",
        )


class RuleSerializer(serializers.ModelSerializer):
    triggers = RuleTriggerSerializer(many=True)
    conditions = RuleConditionSerializer(many=True, required=False)
    actions = RuleActionSerializer(many=True)

    class Meta:
        model = Rule
        fields = (
            "id",
            "device",
            "name",
            "enabled",
            "is_local",
            "created_at",
            "triggers",
            "conditions",
            "actions",
        )

    def validate(self, data):
        device = data["device"]

        trigger = data["triggers"][0]
        action = data["actions"][0]

        trigger_peripheral = trigger["peripheral"]
        action_peripheral = action["peripheral"]

        trigger_device = trigger_peripheral.device
        action_device = action_peripheral.device

        if trigger_device != device:
            raise serializers.ValidationError(
                "Trigger peripheral must belong to rule device"
            )

        data["is_local"] = trigger_device == action_device

        return data

    def create(self, validated_data):

        triggers_data = validated_data.pop("triggers")
        actions_data = validated_data.pop("actions")

        rule = Rule.objects.create(**validated_data)

        for trigger in triggers_data:
            RuleTrigger.objects.create(rule=rule, **trigger)

        for action in actions_data:
            RuleAction.objects.create(rule=rule, **action)
        rule.save()

        if rule.is_local:
            command_message = command_message_factory.sync_start(
                rule.device, StartSyncType.RULE
            )
            action_event_command_processor(command_message)
        return rule
