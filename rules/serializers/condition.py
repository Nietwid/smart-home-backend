from rest_framework import serializers
from rules.models import RuleCondition


class RuleConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuleCondition
        fields = "__all__"
