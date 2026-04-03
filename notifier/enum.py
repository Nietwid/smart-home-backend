from enum import Enum


class Destinations(Enum):
    ROUTER = 0
    FRONTEND = 1
    MICROSERVICE = 2

class MicroserviceQueueName(Enum):
    NOTIFICATION = "notification_queue"
    EVENTS = "events"
    METRICS = "metrics"
