from django.core.management.base import BaseCommand
from django.conf import settings

import os


class Command(BaseCommand):
    help = 'Удаляет db.sqlite3 и все миграции в проекте кроме тех в названии которых есть заглавные буквы или не в ' \
           'DO_NOT_DEL'
    DO_NOT_DEL = ('__init__.py',)

    def handle(self, *args, **options):
        os.remove(os.path.join(settings.BASE_DIR, 'db.sqlite3'))
        for root, dirs, files in os.walk(top=settings.BASE_DIR):
            if not root.find('migrations') == -1:
                for name_file in files:
                    if (name_file not in self.DO_NOT_DEL) and (not any(c.isupper() for c in name_file)):
                        os.remove(os.path.join(root, name_file))
