from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.response import Response

from consumers.frontend.messages.messenger import FrontendMessenger

# from consumers.device.messages.builders import get_event_request
from consumers.router.messenger import DeviceMessenger
from device.models import Device, Event
from device.serializers.device import DeviceSerializer
from device_registry import DeviceRegistry
from event.serializer import EventSerializer
from utils.get_models_with_supported_actions import get_models_with_supported_actions


class CreateDeleteEvent(APIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        return Device.objects.filter(room__user=self.request.user)

    def post(self, request, *args, **kwargs):
        device = get_object_or_404(Device, pk=request.data["device"])
        target_device = get_object_or_404(Device, pk=request.data["target_device"])
        extra_settings = request.data["extra_settings"]
        model = DeviceRegistry().get_model(target_device.fun)
        available_extra_settings = model.objects.get(
            pk=target_device.id
        ).extra_settings()
        for k, v in extra_settings.items():
            if k not in available_extra_settings:
                return Response(
                    {"extra_settings": "Invalid extra_settings"},
                    status=HTTP_400_BAD_REQUEST,
                )
        event = Event.objects.create(
            device=device,
            target_device=target_device,
            action=request.data["action"],
            event=request.data["event"],
            extra_settings=extra_settings,
        )
        FrontendMessenger().update_frontend(
            device.home.id, DeviceSerializer(device).data, 200
        )
        return Response(EventSerializer(event).data, 201)

    def delete(self, request, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs["pk"])
        device_id = event.device.id
        event.delete()
        device = get_object_or_404(Device, pk=device_id)
        FrontendMessenger().update_frontend(
            device.home.id, DeviceSerializer(device).data, 200
        )
        return Response({}, 200)


class GetActionsAndEvents(APIView):

    def get(self, request):
        id = request.query_params.get("id")
        fun = request.query_params.get("fun")
        models = get_models_with_supported_actions(request.user)
        register = DeviceRegistry()
        model = register.get_model(fun)
        device = get_object_or_404(model, home__users=request.user, pk=id)
        return Response(
            {
                "models": models,
                "available_events": device.available_events(),
            },
            200,
        )


class GetAvailableActionAndExtraSettings(APIView):

    def get(self, request):
        fun = request.query_params.get("function")
        register = DeviceRegistry()
        model = register.get_model(fun.lower())
        if not model:
            return Response([], 404)
        instance = model.objects.filter(home__users=request.user).first()
        return Response(
            {
                "actions": instance.available_actions(),
                "settings": instance.extra_settings(),
            },
            200,
        )


class TriggerEvent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        device_id = request.data.get("id", None)
        event_type = request.data.get("type", None)
        if not device_id or not event_type:
            return Response({}, HTTP_400_BAD_REQUEST)
        device = get_object_or_404(Device, pk=device_id)
        events = device.events.filter(event=event_type)
        if not events:
            return Response({}, HTTP_200_OK)
        dm = DeviceMessenger()
        # for event in events:
        #     dm.send(device.get_router_mac(), get_event_request(event))
        return Response({}, HTTP_200_OK)
