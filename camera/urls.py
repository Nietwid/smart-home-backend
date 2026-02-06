from django.urls import path

from camera.views import ListCreateCameraView, RetrieveUpdateDestroyCameraView

urlpatterns = [
    path("", ListCreateCameraView.as_view(), name="camera-list-create"),
    path(
        "<pk>",
        RetrieveUpdateDestroyCameraView.as_view(),
        name="retrieve-update-destroy-camera",
    ),
]
