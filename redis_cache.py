import logging

from consumers.device.messages.device_message import DeviceMessage
from django.core.cache import cache
from cache_key import CacheKey
from consumers.device.messages.enum import MessageCommand

logger = logging.getLogger(__name__)


class RedisCache:

    def save_device_message(self, message: DeviceMessage) -> None:
        cache.set(
            CacheKey.device_message(message.message_id),
            message.model_dump(),
            timeout=30,
        )

    def get_device_message_and_delete(self, message_id: str) -> DeviceMessage | None:
        raw = cache.get(CacheKey.device_message(message_id))
        if not raw:
            return None
        cache.delete(CacheKey.device_message(message_id))
        try:
            if isinstance(raw, str):
                return DeviceMessage.model_validate_json(raw)
            elif isinstance(raw, dict):
                return DeviceMessage.model_validate(raw)
            else:
                logger.warning(f"Unsupported cache type for {message_id}: {type(raw)}")
                return None

        except Exception as exc:
            logger.exception(f"Failed to reconstruct DeviceMessage {message_id}")
            return None

    def get_peripherals_pending(self, pk: int) -> list[str]:
        return cache.get(CacheKey.peripheral_pending(pk))

    def get_device_pending(self, pk: int) -> list[str]:
        return cache.get(CacheKey.device_pending(pk))

    def add_peripheral_pending(self, pk: int, command: MessageCommand) -> list[str]:
        pending = self.get_peripherals_pending(pk)
        if not pending:
            pending = []
        if not command in pending:
            pending.append(command)
        cache.set(CacheKey.peripheral_pending(pk), pending, timeout=60)
        return pending

    def delete_peripheral_pending(self, pk: int, command: MessageCommand) -> list[str]:
        pending = self.get_peripherals_pending(pk)
        if not pending:
            return []
        if command in pending:
            pending.remove(command)
        cache.set(CacheKey.peripheral_pending(pk), pending, timeout=60)
        return pending

    def delete_device_pending(self, pk: int, command: MessageCommand):
        pending = self.get_device_pending(pk)
        if not pending:
            return []
        if command in pending:
            pending.remove(command)
        cache.set(CacheKey.device_pending(pk), pending, timeout=60)
        return pending


redis_cache = RedisCache()
