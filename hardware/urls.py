from django.urls import path
from django.urls.resolvers import URLPattern
from hardware.views import HardwareList

urlpatterns: list[URLPattern] = [
    path("schemas/", HardwareList.as_view()),
]
