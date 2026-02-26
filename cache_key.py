class CacheKey:
    @staticmethod
    def peripheral_pending(pk: int) -> str:
        return f"peripheral-pending:{pk}"

    @staticmethod
    def device_pending(pk: int) -> str:
        return f"device-pending:{pk}"

    @staticmethod
    def device_message(message_id: str) -> str:
        return f"device-message:{message_id}"
