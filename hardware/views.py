from rest_framework.views import APIView
from rest_framework.response import Response

from hardware.registry import HARDWARE_REGISTRY


class HardwareList(APIView):

    def get(self, request):
        schemas = {
            key: value.config_model.model_json_schema()
            for key, value in HARDWARE_REGISTRY.items()
        }
        return Response(schemas, status=200)
