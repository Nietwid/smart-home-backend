from threading import Lock
from django.db.models import QuerySet

from ai_assistance.device_model import DeviceModel
from ai_assistance.intent_model import IntentModel
from consumers.frontend.messages.message import FrontendMessage
from consumers.frontend.messages.types import (
    FrontendMessageType,
)
from consumers.frontend.messages.messenger import FrontendMessenger
from device_registry import DeviceRegistry
from utils.get_available_for_user_device import get_all_available_for_user_device
from utils.get_available_intents import get_available_intent
from device.models import Device


class AiAssistance:
    _instance = None
    _lock = Lock()
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, intent_model: IntentModel, device_model: DeviceModel):
        print("Initializing AiAssistance...")
        with self.__class__._lock:
            if self.__class__._initialized:
                print("Already initialized, returning")
                return
            self.__class__._initialized = True
        self.__class__._initialized = True
        self.intent_model = intent_model
        self.device_model = device_model
        self.messanger = FrontendMessenger()

        print("Initializing AiAssistance... COMPLETE")

    def run(self, user_id: int, prompt: str, replay_channel: str):

        if not self._initialized:
            raise RuntimeError(
                "AiAssistance not initialized. Call initialize() during app startup."
            )
        all_devices = get_all_available_for_user_device(user_id).prefetch_related(
            "room"
        )
        available_intent = get_available_intent(user_id, all_devices)
        intents = self.intent_model.run(available_intent, prompt)
        self.messanger.send_to_channel(
            replay_channel,
            FrontendMessage(
                action=FrontendMessageType.AI_RESPONSE,
                data={"message": "1 etap " + str(intents)},
                status=200,
            ),
        )
        for intent in intents:
            rooms, devices = self.get_room_and_device(intent, all_devices)
            response = self.device_model.run(rooms, devices, intent["prompt"])
            response.update(intent)
            self.messanger.send_to_channel(
                replay_channel,
                FrontendMessage(
                    action=FrontendMessageType.AI_RESPONSE,
                    data={"message": "2 etap " + str(response)},
                    status=200,
                ),
            )
            device_to_make_action = all_devices.all()
            if not self.is_none_value(response.get("room", None)):
                device_to_make_action = device_to_make_action.filter(
                    room__name__in=response["room"]
                )
            if not self.is_none_value(response.get("device_type", None)):
                device_to_make_action = device_to_make_action.filter(
                    fun=response["device_type"]
                )
            if not self.is_none_value(response.get("device_name", None)):
                device_to_make_action = device_to_make_action.filter(
                    name=response["device_name"]
                )
            self.messanger.send_to_channel(
                replay_channel,
                FrontendMessage(
                    action=FrontendMessageType.AI_RESPONSE,
                    data={
                        "message": "3 etap "
                        + ",".join(
                            f"{device.name} {device.room.name}"
                            for device in device_to_make_action
                        )
                    },
                    status=200,
                ),
            )
            device_registry = DeviceRegistry()
            for device in device_to_make_action:
                device = device_registry.get_model(device.fun).objects.get(pk=device.pk)
                device.make_intent(response)
        return ""

    def get_room_and_device(
        self, intent: dict, available_devices: QuerySet[Device]
    ) -> tuple[list[str], list[str]]:
        intent = intent["intent"]
        device_registry = DeviceRegistry()
        rooms = []
        devices = []
        for device in available_devices:
            if intent in device_registry.get_available_intents(device.fun):
                rooms.append(device.room.name)
                devices.append(f"{device.fun} {device.name}")
        return rooms, devices

    def is_none_value(self, value):
        if value is None:
            return True
        if isinstance(value, str) and value.strip().lower() in ("none", ""):
            return True
        return False

    @classmethod
    def initialize(cls, intent_model: IntentModel, device_model: DeviceModel):
        """Initialize singleton during app startup"""
        instance = cls(intent_model=intent_model, device_model=device_model)
        print(f"AiAssistance singleton initialized: {instance._initialized}")
        return instance

    @classmethod
    def get_instance(cls):
        """Get singleton instance"""

        if cls._instance is None or not cls._instance._initialized:
            raise RuntimeError("AiAssistance not initialized yet")
        return cls._instance
