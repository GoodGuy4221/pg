from django.contrib import admin

from .models import ConverterString


@admin.register(ConverterString)
class ConverterStringAdmin(admin.ModelAdmin):
    pass
