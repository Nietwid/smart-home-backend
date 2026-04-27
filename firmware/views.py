from django.http import FileResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from firmware.models import FirmwareDevice
from firmware.serializers import FirmwareDeviceSerializer
from redis_cache import redis_cache


class FirmwareDownload(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.GET.get("token")
        if not token:
            return Response({}, status=HTTP_400_BAD_REQUEST)
        firmware_id = redis_cache.get_and_delete_update_firmware(token)
        if not firmware_id:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        firmware = FirmwareDevice.objects.get(id=firmware_id)
        file = firmware.file
        return FileResponse(
            file.open("rb"),
            as_attachment=True,
            filename=file.name,
            content_type="application/octet-stream",
        )


class FirmwareList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FirmwareDeviceSerializer
    queryset = FirmwareDevice.objects.all()
