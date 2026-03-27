from rest_framework import serializers

from device.models import Device
from dispatcher.device.messages.enum import MessageCommand
from notifier.frontend_notifier_factory import frontend_notifier_factory
from rules.models import Rule, RuleAction, RuleCondition, RuleTrigger
from rules.serializers.action import RuleActionSerializer
from rules.serializers.condition import RuleConditionSerializer
from rules.serializers.trigger import RuleTriggerSerializer
from notifier.notifier import notifier


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
        conditions_data = validated_data.pop("conditions", [])

        rule = Rule.objects.create(**validated_data)

        for trigger in triggers_data:
            RuleTrigger.objects.create(rule=rule, **trigger)

        for action in actions_data:
            RuleAction.objects.create(rule=rule, **action)

        for condition in conditions_data:
            RuleCondition.objects.create(rule=rule, **condition)

        rule.save()

        if rule.is_local:
            device: Device = rule.device
            if MessageCommand.UPDATE_RULE in device.required_action:
                return rule

            device.required_action.append(MessageCommand.UPDATE_RULE)
            device.save(update_fields=["required_action"])
            message = frontend_notifier_factory.update_device_required_action(
                device.home.pk, device.required_action, device.pk
            )
            notifier.notify([message])

        return rule
