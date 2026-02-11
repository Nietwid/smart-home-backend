from abc import ABC, abstractmethod


class RequestResponseInterface(ABC):

    @classmethod
    @abstractmethod
    def request(cls) -> None: ...

    @classmethod
    @abstractmethod
    def response(cls) -> None: ...
