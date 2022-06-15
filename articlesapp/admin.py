from django.contrib import admin

from .models import Articles, Topic


@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Topic)
class TopicsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
