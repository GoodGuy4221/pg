from django.contrib import admin

from .models import Articles, Topic


# prepopulated_fields = {'slug': ('title',)}
@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    pass


@admin.register(Topic)
class TopicsAdmin(admin.ModelAdmin):
    pass
