from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from hardware.repository import HardwareSchemaRepository


class Schema(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        name = request.GET.get("name")
        if name:
            schema = HardwareSchemaRepository.get_config_by_name(name)
            return Response({"schema": schema}, status=status.HTTP_200_OK)

        schema = HardwareSchemaRepository.get_configs()
        return Response(schema, status=200)
