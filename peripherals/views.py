from pydantic import ValidationError
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from dispatcher.command_message.factory import command_message_factory
from dispatcher.processor.action_event_command import action_event_command_processor
from peripherals.action_event_frontend_message import ActionEventFrontendMessage
from peripherals.serializers.peripheral import PeripheralSerializer
from peripherals.serializers.rfid_card import RfidCardSerializer
from peripherals.models import RfidCard


class CreatePeripheral(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PeripheralSerializer


class HandleEventAction(APIView):

    def put(self, request, *args, **kwargs):
        try:
            frontend_message = ActionEventFrontendMessage(**request.data)
            print(frontend_message)
        except ValidationError as e:
            errors = {}
            for err in e.errors():
                path = ".".join(str(x) for x in err["loc"])
                errors[path] = err["msg"]
            return Response(errors, status=400)
        except Exception as e:
            print(f"{e=}")
            return Response({}, status=400)
        command_message = command_message_factory.from_frontend_message(
            frontend_message
        )
        action_event_command_processor(command_message)
        return Response({}, status=200)


class GetAllPeripheralRfidCards(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RfidCardSerializer

    def get_queryset(self):
        peripheral_id = self.kwargs.get("pk")
        if peripheral_id is None:
            return []
        return RfidCard.objects.filter(allowed_peripherals__id=peripheral_id)


class CardDestroyAPIView(DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = RfidCard.objects.all()

    def perform_destroy(self, instance: RfidCard):
        peripheral_id = self.kwargs.get("peripheral_id")

        if peripheral_id:
            instance.allowed_peripherals.remove(peripheral_id)
            if not instance.allowed_peripherals.exists():
                instance.delete()
        else:
            instance.delete()
