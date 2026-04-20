import logging

from dispatcher.command_message.message import CommandMessage
from dispatcher.device.messages.device_message import DeviceMessage
from django.core.cache import cache
from cache_key import CacheKey
from dispatcher.device.messages.enum import MessageCommand

logger = logging.getLogger("base")


class RedisCache:
    DEFAULT_TIMEOUT = 60

    def add_device_message(self, message: DeviceMessage) -> None:
        cache.set(
            CacheKey.device_message(message.message_id),
            message.model_dump(),
            timeout=self.DEFAULT_TIMEOUT,
        )

    def add_device_pending(self, mac: str, command: MessageCommand) -> list[str]:
        pending = self.get_device_pending(mac)
        cache_key = CacheKey.device_pending(mac)
        return self._add_pending(pending, cache_key, command)

    def add_update_firmware(self, token: str, firmware_id: int):
        cache.set(CacheKey.firmware_update(token), firmware_id, timeout=60)

    def add_peripheral_pending(
        self, pk: int, command: MessageCommand, timeout=DEFAULT_TIMEOUT
    ) -> list[str]:
        pending = self.get_peripherals_pending(pk)
        cache_key = CacheKey.peripheral_pending(pk)
        return self._add_pending(pending, cache_key, command, timeout)

    def add_device_update_peripherals_ids(self, ids: list[int], device_mac: str):
        cache.set(
            CacheKey.update_peripheral(device_mac), ids, timeout=self.DEFAULT_TIMEOUT
        )

    def get_and_delete_update_firmware(self, token: str) -> int | None:
        firmware_id = cache.get(CacheKey.firmware_update(token))
        if firmware_id:
            cache.delete(CacheKey.firmware_update(token))
        return firmware_id

    def get_device_update_peripheral_id(self, device_mac: str) -> int | None:
        ids = cache.get(CacheKey.update_peripheral(device_mac))
        if not ids:
            return None
        next_id = ids.pop(0)
        self.add_device_update_peripherals_ids(ids, device_mac)
        return next_id

    def add_sync_rule_ids(self, ids: list[int], device_mac: str):
        cache.set(CacheKey.sync_rule(device_mac), ids, timeout=self.DEFAULT_TIMEOUT)

    def get_sync_rule_id(self, device_mac: str) -> int | None:
        ids = cache.get(CacheKey.sync_rule(device_mac))
        if not ids:
            return None
        next_id = ids.pop(0)
        self.add_sync_rule_ids(ids, device_mac)
        logger.debug(cache.get(CacheKey.sync_rule(device_mac)))
        return next_id

    def get_peripherals_pending(self, pk: int) -> list[str]:
        return cache.get(CacheKey.peripheral_pending(pk))

    def get_device_pending(self, mac: str) -> list[str]:
        return cache.get(CacheKey.device_pending(mac))

    def get_and_delete_device_message(self, message_id: str) -> DeviceMessage | None:
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

    def delete_device_pending(self, mac: str, command: MessageCommand) -> list[str]:
        pending = self.get_device_pending(mac)
        cache_key = CacheKey.device_pending(mac)
        return self._delete_pending(pending, cache_key, command)

    def delete_peripheral_pending(self, pk: int, command: MessageCommand) -> list[str]:
        pending = self.get_peripherals_pending(pk)
        cache_key = CacheKey.peripheral_pending(pk)
        return self._delete_pending(pending, cache_key, command)

    def _add_pending(
        self,
        pending: list[str] | None,
        cache_key: str,
        command: MessageCommand,
        timeout=DEFAULT_TIMEOUT,
    ) -> list[str]:
        if not pending:
            pending = []
        if not command in pending:
            pending.append(command)
        cache.set(cache_key, pending, timeout=timeout)
        return pending

    def _delete_pending(
        self, pending: list[str], cache_key: str, command: MessageCommand
    ):
        if not pending:
            return []
        if command in pending:
            pending.remove(command)
        cache.set(cache_key, pending, timeout=self.DEFAULT_TIMEOUT)
        return pending


redis_cache = RedisCache()
