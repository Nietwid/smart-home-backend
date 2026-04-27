from pydantic import BaseModel

from consumers.microservice.message import MicroserviceMessage
from dispatcher.device.messages.enum import MessageCommand
from notifier.enum import MicroserviceQueueName, RabbitRoutingKey, RabbitExchange
from notifier.message import MicroserviceNotifierData
from peripherals.models import Peripherals


class MicroserviceNotifierFactory:

    def log_event(
            self,
            peripheral:Peripherals,
            event_type:MessageCommand,
            payload:dict | BaseModel,
            exchange:RabbitExchange,
            routing_key:RabbitRoutingKey,
    ) -> MicroserviceNotifierData:
        payload = payload.model_dump() if isinstance(payload, BaseModel) else payload
        return MicroserviceNotifierData(
            exchange=exchange,
            routing_key=routing_key,
            data = MicroserviceMessage(
                message_event=event_type,
                device_id=peripheral.device.mac,
                peripheral_id=peripheral.pk,
                home_id=peripheral.device.home.pk,
                payload=payload,
            )
        )


microservice_message_factory = MicroserviceNotifierFactory()
