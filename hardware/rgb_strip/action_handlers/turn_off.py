from hardware.base import RequestResponseInterface


class TurnOff(RequestResponseInterface):

    @classmethod
    def request(cls) -> None: ...

    @classmethod
    def response(cls) -> None: ...
