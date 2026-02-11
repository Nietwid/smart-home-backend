from hardware.base import RequestResponseInterface


class SetColor(RequestResponseInterface):

    @classmethod
    def request(cls) -> None: ...

    @classmethod
    def response(cls) -> None: ...
