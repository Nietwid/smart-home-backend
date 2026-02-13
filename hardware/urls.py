from django.urls import path
from hardware.views import Schema
urlpatterns = [
    path('schemas', Schema.as_view(), name='hardware-schema'),
]