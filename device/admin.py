from django.contrib import admin

from .models import Device, Event, Router

# Register your models here.

admin.site.register(Device)
admin.site.register(Router)
admin.site.register(Event)
