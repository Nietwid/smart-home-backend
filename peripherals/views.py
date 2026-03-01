from pydantic import ValidationError
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from dispatcher.command_message.factory import command_message_factory
from dispatcher.processor.action_event_command import action_event_command_processor
from peripherals.action_event_frontend_message import ActionEventFrontendMessage
from peripherals.serializers import PeripheralSerializer


class CreatePeripheral(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PeripheralSerializer


class HandleEventAction(APIView):

    def put(self, request, *args, **kwargs):
        try:
            frontend_message = ActionEventFrontendMessage(**request.data)
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
