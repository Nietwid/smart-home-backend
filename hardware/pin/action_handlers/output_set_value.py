from hardware.base import RequestResponseInterface


class OutputSetValue(RequestResponseInterface):

    @classmethod
    def request(cls): ...

    @classmethod
    def response(cls): ...
