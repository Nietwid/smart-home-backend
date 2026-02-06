from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from camera.serializer import CameraReadSerializer, CameraWriteSerializer
from .models import Camera


class ListCreateCameraView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CameraWriteSerializer
        return CameraReadSerializer

    def get_queryset(self):
        return Camera.objects.filter(home__users=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data["home"] = request.user.home.first().id
        return super().create(request, *args, **kwargs)


class RetrieveUpdateDestroyCameraView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CameraReadSerializer

    def get_queryset(self):
        return Camera.objects.filter(home__users=self.request.user)
