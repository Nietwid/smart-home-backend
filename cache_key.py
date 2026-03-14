class CacheKey:
    @staticmethod
    def peripheral_pending(pk: int) -> str:
        return f"peripheral-pending:{pk}"

    @staticmethod
    def device_pending(pk: str) -> str:
        return f"device-pending:{pk}"

    @staticmethod
    def device_message(message_id: str) -> str:
        return f"device-message:{message_id}"

    @staticmethod
    def update_peripheral(device_mac: str) -> str:
        return f"device:update-peripheral:{device_mac}"

    @staticmethod
    def sync_rule(device_mac: str) -> str:
        return f"device:sync-rule:{device_mac}"
