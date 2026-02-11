from hardware.base import RequestResponseInterface


class SetValue(RequestResponseInterface):

    @classmethod
    def request(cls) -> None: ...

    @classmethod
    def response(cls) -> None: ...
