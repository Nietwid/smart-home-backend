from django.db import models


class MessageStatus(models.TextChoices):
    PENDING = "PENDING", "pending"
    SENDING = "SENDING", "sending"
    DELIVERED = "DELIVERED", "delivered"
    FAILED = "FAILED", "failed"
    TIMEOUT = "TIMEOUT", "timeout"
    PROCESSED = "PROCESSED", "processed"
    EXPIRED = "EXPIRED", "expired"


class BaseMessage(models.Model):
    payload = models.JSONField()
    status = models.CharField(
        max_length=20, choices=MessageStatus.choices, default=MessageStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    external_id = models.UUIDField(unique=True)

    class Meta:
        abstract = True


class RabbitOutbox(BaseMessage):
    exchange = models.CharField(max_length=100)
    routing_key = models.CharField(max_length=100)


class RouterOutbox(BaseMessage):
    router_mac = models.CharField(max_length=17)
    expired_at = models.DateTimeField()


class RouterInbox(BaseMessage):
    router_mac = models.CharField(max_length=17)
    home_id = models.IntegerField()
    expired_at = models.DateTimeField()

    class Meta:
        unique_together = ("router_mac", "external_id")
