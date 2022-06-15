from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from uuid import uuid4


class Notes(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='notes')
    title = models.CharField(_('Заголовок'), max_length=128)
    body = models.TextField(_('Заметка'))
    created_at = models.DateTimeField(_('Создан'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Обновлен'), auto_now=True)
    is_active = models.BooleanField(_('Активна'), default=True)

    class Meta:
        ordering = ('-user',)
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'

    def __str__(self):
        return f'{self.user} {self.title}'

    def delete(self, using=None, keep_parents=False):
        if self.is_active:
            self.is_active = False
            self.save()
