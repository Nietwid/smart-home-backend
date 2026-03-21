from django.urls import path
from django.urls.resolvers import URLPattern
from hardware.views import HardwareList, ActionExtraSettings

urlpatterns: list[URLPattern] = [
    path("schemas/", HardwareList.as_view()),
    path("action/settings", ActionExtraSettings.as_view()),
]
