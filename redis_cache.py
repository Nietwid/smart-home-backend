from consumers.device.messages.device_message import DeviceMessage
from django.core.cache import cache
from cache_key import CacheKey
from consumers.device.messages.enum import MessageCommand


class RedisCache:

    def save_device_message(self, message: DeviceMessage) -> None:
        cache.set(
            CacheKey.device_message(message.message_id),
            message.model_dump(),
            timeout=30,
        )

    def get_device_message_and_delete(self, message_id: str) -> DeviceMessage | None:
        message = cache.get(CacheKey.device_message(message_id))
        if message:
            cache.delete(CacheKey.device_message(message_id))
        return message

    def get_peripherals_pending(self, pk: int) -> list[str]:
        return cache.get(CacheKey.peripheral_pending(pk))

    def add_peripheral_pending(self, pk: int, command: MessageCommand) -> list[str]:
        pending = self.get_peripherals_pending(pk)
        if not pending:
            pending = []
        if not command in pending:
            pending.append(command)
        cache.set(CacheKey.peripheral_pending(pk), pending, timeout=30)
        return pending

    def delete_peripheral_pending(self, pk: int, command: MessageCommand) -> list[str]:
        pending = self.get_peripherals_pending(pk)
        if not pending:
            return []
        if command in pending:
            pending.remove(command)
        return pending


redis_cache = RedisCache()
