from django.db import models
from django.utils.translation import gettext_lazy as _

from uuid import uuid4


class ConverterString(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid4)
    raw_string = models.CharField(_('raw_string'), max_length=128, db_index=True)
    convert_string = models.CharField(_('convert_string'), max_length=128, db_index=True)

    class Meta:
        ordering = '-raw_string',
        verbose_name = 'строка'
        verbose_name_plural = 'строки'

    def __str__(self):
        return f'{self.raw_string} {self.convert_string}'
