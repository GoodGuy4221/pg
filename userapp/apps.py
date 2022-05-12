from django.apps import AppConfig


class UserappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userapp'
    verbose_name = 'Пользователи'

    def ready(self):
        from .signals import create_user_profile, save_user_profile
