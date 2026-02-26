from django.http import FileResponse
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, get_object_or_404

from consumers.device.messages.enum import MessageEvent

# from consumers.device.messages.builders import update_firmware_request
from device.serializers.device import DeviceSerializer
from firmware.models import FirmwareDevice
from firmware.serializers import FirmwareDeviceSerializer
from device.models import Device
from uuid import uuid4
from django.core.cache import cache
from django.conf import settings


class FirmwareView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response("Hello World")


class FirmwareDownload(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.GET.get("token")
        if not token:
            return Response({}, status=HTTP_400_BAD_REQUEST)
        firmware_id = cache.get(f"update_firmware_{token}")
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


class FirmwareUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        pk = request.data.get("id")
        if not pk:
            return Response({}, status=HTTP_400_BAD_REQUEST)
        device = get_object_or_404(Device, pk=pk, home__users=request.user)
        firmware_name = f"{device.fun}_{device.chip_type}"
        firmware = (
            FirmwareDevice.objects.filter(to_device=firmware_name)
            .order_by("-version")
            .first()
        )
        if not firmware:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        token = uuid4().hex
        cache.set(f"update_firmware_{token}", firmware.pk, timeout=60)
        payload = {
            "url": settings.FIRMWARE_DEVICE_ENDPOINT + f"?token={token}",
            "version": firmware.version,
            "to_device": firmware_name,
        }
        # message = update_firmware_request(device.mac, payload)
        # DeviceMessenger().send(device.get_router_mac(), message)
        device.pending.append(MessageEvent.UPDATE_FIRMWARE.value)
        device.save(update_fields=["pending"])
        return Response(DeviceSerializer(device).data, status=200)


class FirmwareList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FirmwareDeviceSerializer
    queryset = FirmwareDevice.objects.all()
