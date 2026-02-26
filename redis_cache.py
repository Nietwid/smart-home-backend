from consumers.device.messages.device_message import DeviceMessage
from django.core.cache import cache

from cache_key import CacheKey


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


redis_cache = RedisCache()
