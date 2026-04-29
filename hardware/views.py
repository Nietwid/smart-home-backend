from rest_framework.views import APIView
from rest_framework.response import Response

from hardware.registry import HARDWARE_REGISTRY


class HardwareList(APIView):

    def get(self, request):
        schemas = {
            key: value.config_model.model_json_schema()
            for key, value in HARDWARE_REGISTRY.items()
        }
        return Response(schemas, status=200)


class ActionExtraSettings(APIView):

    def get(self, request):
        name = request.query_params.get("name")
        action = request.query_params.get("action")
        cls = HARDWARE_REGISTRY.get(name)
        if not cls:
            return Response({}, status=404)
        cls_action = cls.actions.get(action)
        if not cls_action:
            return Response(None, status=200)
        extra_settings = cls_action.model_json_schema()
        return Response(extra_settings, status=200)


class EventCondition(APIView):
    def get(self, request):
        name = request.query_params.get("name")
        event = request.query_params.get("event")
        cls = HARDWARE_REGISTRY.get(name)
        if not cls:
            return Response({}, status=404)
        try:
            cls_event_conditions = cls.events.get(event)
            if not cls_event_conditions:
                return Response(None, status=200)
        except Exception as e:
            print(e)
            return Response(None, status=200)
        event_conditions = cls_event_conditions.model_json_schema()
        return Response(event_conditions, status=200)
