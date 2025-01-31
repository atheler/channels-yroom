from typing import Optional

from django.db import models


class YDocUpdateManager(models.Manager):
    def get_snapshot(self, name) -> Optional[bytes]:
        try:
            result = self.get(name=name).data
            if not isinstance(result, bytes):
                # Postgres returns memoryview
                return bytes(result)
            return result
        except YDocUpdate.DoesNotExist:
            return None

    def save_snapshot(self, name, data):
        return self.update_or_create(name=name, defaults={"data": data})


class YDocUpdate(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    timestamp = models.DateTimeField(auto_now=True)
    data = models.BinaryField()

    objects = YDocUpdateManager()

    def __str__(self):
        return self.name
