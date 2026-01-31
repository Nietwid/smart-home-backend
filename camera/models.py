from django.db import models
from user.models import Home


class Camera(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name="cameras")
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    port = models.PositiveIntegerField(default=554)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    path = models.CharField(max_length=100, null=True, blank=True)

    @property
    def rtsp(self):
        if self.username and self.password:
            return f"rtsp://{self.username}:{self.password}@{self.ip_address}:{self.port}{self.path}"
        return f"rtsp://{self.ip_address}:{self.port}{self.path}"

    def __str__(self):
        return self.name
