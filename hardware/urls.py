from django.urls import path
from hardware.views import Schema
urlpatterns = [
    path('schema', Schema.as_view(), name='hardware-schema'),
]