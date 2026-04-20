from consumers.events.base_event import BaseEventRequest
from consumers.microservice.on_measurement import on_measurement
from consumers.rabbitmq_publisher import QueueNames, get_publisher
from dispatcher.device.messages.builders import (
    measurements_sleeping_time_response,
)
from consumers.router_message.device_message import DeviceMessage
from consumers.router_message.message_event import MessageEvent
from utils.waiting_time import waiting_time
from temperature.models import TempHum


class OnMeasureTempHum(BaseEventRequest):
    from consumers.router.messenger import DeviceMessenger

    device_messanger = DeviceMessenger()

    def handle_request(self, consumer, message: DeviceMessage):
        try:
            sensor = TempHum.objects.get(mac=message.device_id)
        except TempHum.DoesNotExist:
            return
        sensor.timestamp = message.payload.timestamp
        sensor.temperature = message.payload.temperature
        sensor.humidity = message.payload.humidity
        sensor.save(update_fields=["timestamp", "temperature", "humidity"])
        self.device_messanger.send(
            consumer.mac, measurements_sleeping_time_response(message, waiting_time())
        )
        publisher = get_publisher()
        sensor_id = sensor.pk
        home_id = sensor.home.pk
        temperature_message = on_measurement(
            MessageEvent.ON_MEASURE_TEMPERATURE,
            sensor_id,
            home_id,
            message.payload.temperature,
        )
        humidity_message = on_measurement(
            MessageEvent.ON_MEASURE_HUMIDITY,
            sensor_id,
            home_id,
            message.payload.humidity,
        )
        publisher.send_message(QueueNames.SENSORS, temperature_message)
        publisher.send_message(QueueNames.SENSORS, humidity_message)
