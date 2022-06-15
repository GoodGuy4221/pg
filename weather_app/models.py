from django.db import models

from uuid import uuid4


class City(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
