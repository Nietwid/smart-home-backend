from enum import Enum, StrEnum


class Destinations(Enum):
    ROUTER = 0
    FRONTEND = 1
    MICROSERVICE = 2

class MicroserviceQueueName(Enum):
    NOTIFICATION = "notification_queue"
    EVENTS = "events"
    METRICS = "metrics"

class RabbitExchange(StrEnum):
    SENSOR_SERVICE = "sensor_service_exchange"

class RabbitRoutingKey(StrEnum):
    NOTIFICATION = "sensor_service.notification"
    EVENTS = "sensor_service.events"
    METRICS = "sensor_service.metrics"