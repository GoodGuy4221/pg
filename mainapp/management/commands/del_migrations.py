from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Удаляет все миграции в проекте кроме тех в названии которых есть заглавные буквы'

    def handle(self, *args, **options):
        pass
