from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response

from dispatcher.device.messages.enum import MessageCommand
from notifier.factory.frontend_notifier_factory import frontend_notifier_factory
from rules.models import Rule
from rules.serializers.rule import RuleSerializer
from notifier.notifier import notifier


class CreateRule(CreateAPIView):
    model = Rule
    serializer_class = RuleSerializer


class RetrieveUpdateDestroyRule(RetrieveUpdateDestroyAPIView):
    model = Rule
    serializer_class = RuleSerializer
    queryset = Rule.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_local:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        enabled = request.data.get("enabled", None)
        if enabled is None:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        instance.enabled = enabled
        instance.save(update_fields=["enabled"])
        return Response({}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        rule = self.get_object()
        is_local = rule.is_local
        device = rule.device
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204 and is_local:
            if not MessageCommand.UPDATE_RULE in device.required_action:
                device.required_action.append(MessageCommand.UPDATE_RULE)
                device.save(update_fields=["required_action"])
                message = frontend_notifier_factory.update_device_required_action(
                    device.home.pk, device.required_action, device.pk
                )
                notifier.notify([message])

        return response
