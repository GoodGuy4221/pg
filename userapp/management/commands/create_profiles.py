"""
Служебный скрипт для заполнения БД таблицы Profile связь один к одному.
Создает профиль пользователям у которых его нет.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from userapp.models import Profile

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in User.objects.filter(profile__isnull=True):
            Profile.objects.create(user=user)
        print('done!')
