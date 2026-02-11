from hardware.base import RequestResponseInterface


class TurnOn(RequestResponseInterface):

    @classmethod
    def request(cls) -> None: ...

    @classmethod
    def response(cls) -> None: ...
