from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response

from rules.models import Rule
from rules.serializers.rule import RuleSerializer


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
