from enum import Enum


class Scope(Enum):
    CPU = 1
    PERIPHERAL = 2


class MessageType(Enum):
    ACTION = 1
    EVENT = 2


class MessageDirection(Enum):
    INTENT = 1
    RESULT = 2
