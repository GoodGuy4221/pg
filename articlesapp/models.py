from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.utils import article_image_directory_path
from utils.mixins import IsActiveFalseMixin


class Topic(IsActiveFalseMixin, models.Model):
    name = models.CharField(_('название'), unique=True, db_index=True, max_length=64)
    desc = models.TextField(_('описание'), blank=True)
    is_active = models.BooleanField(_('активна'), default=True)

    class Meta:
        ordering = '-name',
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return f'{_(self.Meta.verbose_name)} {self.name}'


class Articles(IsActiveFalseMixin, models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name='articles')
    title = models.CharField(_('заголовок'), max_length=64, db_index=True)
    image = models.ImageField(_('изображение'), upload_to=article_image_directory_path, blank=True)
    body = models.TextField(_('текст'))
    is_active = models.BooleanField(_('активна'), default=True)
    created_at = models.DateTimeField(_('создана'), auto_now_add=True)
    updated_at = models.DateTimeField(_('отредактирована'), auto_now=True)

    class Meta:
        ordering = '-topic',
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'

    def __str__(self):
        return f'{_(self.Meta.verbose_name)} {self.title}'
