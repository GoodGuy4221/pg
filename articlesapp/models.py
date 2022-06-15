from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.template.defaultfilters import slugify

from utils.utils import article_image_directory_path
from utils.mixins import IsActiveFalseMixin


class SaveSlugMixin:
    def save(self, *args, **kwargs):
        if not self.slug:
            string = self.title.translate(str.maketrans(
                'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
                'abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA'
            ))
            self.slug = slugify(string)
        return super().save(*args, **kwargs)


class Topic(IsActiveFalseMixin, SaveSlugMixin, models.Model):
    slug = models.SlugField('URL', max_length=255, unique=True, db_index=True, primary_key=True)
    title = models.CharField(_('название'), unique=True, db_index=True, max_length=64)
    desc = models.TextField(_('описание'), blank=True)
    is_active = models.BooleanField(_('активна'), default=True)

    class Meta:
        ordering = '-title',
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return f'{self.title}'


class Articles(IsActiveFalseMixin, SaveSlugMixin, models.Model):
    slug = models.SlugField('URL', max_length=255, unique=True, db_index=True, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='articles')
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name='articles')
    title = models.CharField(_('заголовок'), max_length=64, db_index=True)
    body = models.TextField(_('текст'))
    is_active = models.BooleanField(_('активна'), default=True)
    created_at = models.DateTimeField(_('создана'), auto_now_add=True)
    updated_at = models.DateTimeField(_('отредактирована'), auto_now=True)

    class Meta:
        ordering = '-created_at',
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'

    def __str__(self):
        return f'{self.Meta.verbose_name} {self.title}'

    def get_absolute_url(self):
        return reverse(viewname='articles:detail_article', kwargs={'pk': self.pk})


class ArticleImages(IsActiveFalseMixin, models.Model):
    article = models.ForeignKey(Articles, on_delete=models.PROTECT, related_name='images')
    image = models.ImageField(_('изображение'), upload_to=article_image_directory_path)
    title = models.CharField(_('заголовок'), max_length=64)
    desc = models.TextField(_('описание'), null=True, blank=True)
    created_at = models.DateTimeField(_('добавлено'), auto_now_add=True)

    class Meta:
        ordering = '-created_at',
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

    def __str__(self):
        return self.title
